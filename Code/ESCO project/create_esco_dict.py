import pandas as pd
import json
from preprocessing_functions import removeStopwords
from fold_to_ascii import fold as ascii_fold
import json
import re
import time
from nltk.corpus import stopwords

# Define Global Variables
STOPWORDS = stopwords.words('portuguese') + stopwords.words('english')

def normalizeESCO(occup:str) -> str or list:
    if type(occup) is not str:
        return ''
    first_occupation = occup.split('/')[0]
    lowercased_ascii = ascii_fold(first_occupation.lower(), 'REMOVE_ME').replace('REMOVE_ME', '').split('\n')
    if len(lowercased_ascii) == 1:
        only_alpha = re.sub(r'[^a-z]', ' ', lowercased_ascii[0])
        remove_duplicate_spaces = re.sub(r'\s+', ' ', only_alpha).strip()
        return remove_duplicate_spaces
    else:
        return [re.sub(r'\s+', ' ', re.sub(r'[^a-z]', ' ', v)).strip() for v in lowercased_ascii]

def createEscoRelation():
    # Load the ESCO files
    occupations_en = pd.read_csv("v1.0.8_eng/occupations_en.csv")
    occupations = pd.read_csv("v1.0.8/occupations_pt.csv")
    skills = pd.read_csv("v1.0.8/skills_pt.csv")
    occ_skills_relation = pd.read_csv("v1.0.8/occupationSkillRelations.csv")

    skills.rename(columns={'conceptUri': 'skillUri'}, inplace=True)
    occupations.rename(columns={'conceptUri': 'occupationUri'}, inplace=True)
    occupations_en.rename(columns={'conceptUri': 'occupationUri'}, inplace=True)

    # Split AltLables into lists and then "explode" them into rows in the occupations dataframe
    occupations['altLabels'] = occupations['altLabels'].apply(lambda x: normalizeESCO(x))
    occupations = occupations.explode('altLabels')

    occupations_en['altLabels'] = occupations_en['altLabels'].apply(lambda x: normalizeESCO(x))
    occupations_en = occupations_en.explode('altLabels')

    merged_occupations = pd.merge(occupations, occupations_en[['preferredLabel', 'altLabels','occupationUri']], on=['occupationUri'])
    merged_df = pd.merge(skills, occ_skills_relation, on=['skillUri'])
    esco_relation = pd.merge(merged_occupations, merged_df, on=['occupationUri'])

    merged_occupations.to_csv('esco_merged_occupations.csv')
    merged_df.to_csv('esco_merged_skills.csv')
    esco_relation.to_csv('esco_occupation_skills_relation.csv')
    

def normalizeESCOdict(occup: str) -> str:
    if type(occup) is not str:
        return ''
    first_occupation = occup.split('/')[0]
    lowercased_ascii = ascii_fold(first_occupation.lower(), 'REMOVE_ME').replace('REMOVE_ME', '').split(',')[0] # split at , and pick first component
    only_alpha = re.sub(r'[^a-z]', ' ', lowercased_ascii)
    no_stopwords = removeStopwords(only_alpha)
    remove_duplicate_spaces = re.sub(r'\s+', ' ', no_stopwords).strip()
    return remove_duplicate_spaces


def createEscoDict(merged_occupations, merged_df):
    """Create the ESCO Dictionary with keys as all known occupations in portuguese and english.
    --> Create a dictionary mapping occupations to code, iscoGroup and skills

    Args:
        merged_occupations (pd.DataFrame): merged occupattions (english and portuguese) 
        merged_df (pd.DataFrame): esco merged skills with its relation to occupations through occupationUrr 

    Returns:
        dict: Esco Dictionary with keys as preferred and alt labels from english and portuguese occupations
    """
    esco_dict = {}
    for label in merged_occupations[['preferredLabel_x','altLabels_x', 'preferredLabel_y', 'altLabels_y','occupationUri', 'iscoGroup']].itertuples():
        esco_dict[normalizeESCOdict(label.preferredLabel_x)] = {
            'occupationUri':label.occupationUri, 'iscoGroup':label.iscoGroup, 
            'occupation': normalizeESCOdict(label.preferredLabel_x)
            }
        esco_dict[normalizeESCOdict(label.altLabels_x)] = {
            'occupationUri':label.occupationUri, 'iscoGroup':label.iscoGroup, 
            'occupation': normalizeESCOdict(label.preferredLabel_x)
            }
        esco_dict[normalizeESCOdict(label.preferredLabel_y)] = {
            'occupationUri':label.occupationUri, 'iscoGroup':label.iscoGroup, 
            'occupation': normalizeESCOdict(label.preferredLabel_x)
            }
        esco_dict[normalizeESCOdict(label.altLabels_y)] = {
            'occupationUri':label.occupationUri, 'iscoGroup':label.iscoGroup, 
            'occupation': normalizeESCOdict(label.preferredLabel_x)
            }

    esco_aux_dict = esco_dict.copy() 
    for key in esco_aux_dict:
        esco_dict[key]['skills'] = merged_df.loc[
            merged_df['occupationUri']==esco_dict[key]['occupationUri']
            ]['preferredLabel'].to_list()
    
    return esco_dict

if __name__ == '__main__':
    # To run this file, make sure you are in the ESCO project's directory

    t1 = time.time()
    
    # Create the Esco Relation file
    createEscoRelation()
    print('Esco Relation File Created')
    # Read the created file
    merged_occupations = pd.read_csv('esco_merged_occupations.csv')
    merged_df = pd.read_csv('esco_merged_skills.csv')
    esco_relation = pd.read_csv('esco_occupation_skills_relation.csv')
        
    with open("esco_dictionary.json", 'w', encoding='utf-8') as file:
        json.dump(createEscoDict(merged_occupations, merged_df), file)
        
    t = time.time() - t1
    
    print(f'Finish!\n - Time: {t}')