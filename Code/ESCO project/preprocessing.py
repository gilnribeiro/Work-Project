import pandas as pd
from preprocessing_functions import *
from Code.Data_Cleaning.data_cleaning_functions import applyFuncToColumn, listToRows, removeDupes
import json

    
def main():
    DATAFOLDER_PATH = "/Users/gilnr/OneDrive - NOVASBE/Work Project/Code/Data/"
    ESCO_FOLDER = '/Users/gilnr/OneDrive - NOVASBE/Work Project/Code/ESCO project/'
    
    # Load Data
    data = pd.read_json(DATAFOLDER_PATH + 'full_data_clean.json')
    
    # Load Locations Data
    try:
        with open(ESCO_FOLDER + "locations_dictionary.json", 'r', encoding='utf-8') as file:
            locations_dict = json.load(file)
    except FileNotFoundError:
        # Read excel file with cities, municipalities, villages
        locations = pd.read_excel(ESCO_FOLDER + 'freguesias-metadata.xlsx')
        locations_dict = locationsDictionary(locations)
        with open("locations_dictionary.json", 'w', encoding='utf-8') as file:
            json.dump(locations_dict, file, ensure_ascii=False)

    data_clean = (data.
                pipe(applyFuncToColumn, function=normalizeLocation, columns_list=["job_location"]).
                pipe(listToRows, column="job_location").
                pipe(applyFuncToColumn, function=cleanJobLocation, columns_list=["job_location"]).
                pipe(applyMatchLocation, function=matchLocation, columns_list=['job_location'], locations_dict=locations_dict).
                pipe(applyFuncToColumn, function=cleanJobTitle, columns_list=['job_title']).
                pipe(removeDupes, ['job_title', 'job_description','company', 'job_location']))

    print(f'Previous shape: {data.shape}\nCurrent shape:{data_clean.shape}')
    print(f"""
      Initial number of unique job titles
      - Before applying text normalization -> {data['job_title'].nunique()} 
      - After applying text normalization  -> {data_clean['job_title'].nunique()}""")
    
    mask = data_clean['job_location'].str.contains('NOT FOUND', case=True, na=False)
    print('There are', len(data_clean) - len(data_clean[mask]), 'location matches at a 60% match, that is ', round((len(data_clean) - len(data_clean[mask]))/len(data_clean),2)*100,'% of total')

    with open(ESCO_FOLDER + 'esco_project_data.json', 'w', encoding='utf-8') as file:
        data_clean.to_json(file, force_ascii=False, orient='records', date_format='iso', date_unit='s')
        
if __name__ == '__main__':
    main()