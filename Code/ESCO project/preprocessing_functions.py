import re
import pandas as pd
from fold_to_ascii import fold as ascii_fold

"""
Create the Locations dictionary, mapping every City, Municipality and Village to the corresponding City
"""
def locationsDictionary(locations:pd.DataFrame) -> dict:
    """ Create the Locations dictionary, mapping every City, Municipality and Village to the corresponding City.
    
    Args:
        locations (pd.DataFrame): A dataframe with the portuguese entries for city, municipality and village (distrito, concelho, freguesia)

    Returns:
        dict: {city:municipality, city:village, city:city}
    """
    locations_dict = {}
    ambiguos = set()
    for loc in locations.itertuples():
        for campo in [loc.freguesia, loc.concelho, loc.distrito]:
            normalizedLocation = normalizeLocationDict(campo)
            if normalizedLocation in locations_dict and locations_dict[normalizedLocation] != loc.distrito.lower():
                ambiguos.add(normalizedLocation)
            else:
                locations_dict[normalizedLocation] = loc.distrito.lower()
                
    return locations_dict

"""
Create the Locations Dictionary Functions
- Cleaning the Dictionary Locations
"""
def normalizeLocationDict(location: str) -> str:
    lowercased_ascii = ascii_fold(location.lower(), 'REMOVE_ME').replace('REMOVE_ME', '').split(',')[0] # split at , and pick first component
    only_alpha = re.sub(r'[^a-z]', ' ', lowercased_ascii)
    sem_unioes = re.sub(r'uniao d\w+ freguesias d\w+ ', '', only_alpha)
    remove_duplicate_spaces = re.sub(r'\s+', ' ', sem_unioes).strip()
    return remove_duplicate_spaces

"""
JOB LOCATION CLEAN FUNCTIONS
"""
import functools
from typing import Callable
from strsimpy.jaro_winkler import JaroWinkler

# Preprocessing of the Job location
def normalizeLocation(location:str) -> str or list:
    if location is None:
        return ''
    lowercased_ascii = ascii_fold(location.lower(), 'REMOVE_ME').replace('REMOVE_ME', '').split(',')
    if len(lowercased_ascii) == 1:
        only_alpha = re.sub(r'[^a-z]', ' ', lowercased_ascii[0])
        remove_duplicate_spaces = re.sub(r'\s+', ' ', only_alpha).strip()
        return remove_duplicate_spaces
    else:
        return [re.sub(r'\s+', ' ', re.sub(r'[^a-z]', ' ', v)).strip() for v in lowercased_ascii]
    

# Composable function that cleans the job location of Common filler words meaning "Portugal" and replaces other common words with empty spaces to increase the Jaro-winkler metrics accuracy in assigning the most similar string
ComposableFunction = Callable[[str], str]

def compose(*functions: ComposableFunction) -> ComposableFunction:
    return functools.reduce(lambda f, g: lambda x: g(f(x)), functions)


def commonLocationFillers(x:str) -> str:
    portugal_in_other_words = ['todo o pais','todos o pais', 'qualquer zona',
                               'todas as zonas', 'trabalho de casa', 'qualquer']
    for i in portugal_in_other_words: 
        if i in x:
            x = x.replace(i,'portugal') 
    return x.strip()

def replaceWithEmpty(x:str) -> str:
    to_replace = ['ilha de ', 'zona de ', 'e etc']
    for i in to_replace: 
        if i in x:
            x = x.replace(i,'') 
    return x.strip()
        

cleanJobLocation = compose(commonLocationFillers, replaceWithEmpty)


def matchLocation(x:str, locations_dict:dict) -> str:       
    if x in locations_dict: # exact match
        location = locations_dict[x] 
        return location.capitalize()
    elif x in ['portugal', 'remote']:
        return x.capitalize()
    else:
        jarowinkler = JaroWinkler()
        loc, sim = max([(locations_dict[loc], jarowinkler.similarity(x, loc)) for loc in locations_dict], key=lambda x: x[1])
        if sim >= 0.6:
            return loc.capitalize()
        else: # no similarity match
            return f"NOT FOUND"
        
def applyMatchLocation(dataframe, function=matchLocation, columns_list=['job_location'], locations_dict=dict()):
    for i in columns_list:
        dataframe[i] = dataframe[i].apply(lambda x: function(x, locations_dict))
    return dataframe

"""
JOB TITLE CLEAN FUNCTIONS
"""
import functools
from typing import Callable
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

STOPWORDS = stopwords.words('portuguese') + stopwords.words('english')

ComposableFunction = Callable[[str], str]

def compose(*functions: ComposableFunction) -> ComposableFunction:
    return functools.reduce(lambda f, g: lambda x: g(f(x)), functions)

def normalizeTitle(location:str) -> str or list:
    if location is None:
        return ''
    lowercased_ascii = ascii_fold(location.lower(), 'REMOVE_ME').replace('REMOVE_ME', '').split(',')
    if len(lowercased_ascii) == 1:
        only_alpha = re.sub(r'[^a-z]', ' ', lowercased_ascii[0])
        remove_duplicate_spaces = re.sub(r'\s+', ' ', only_alpha).strip()
        return remove_duplicate_spaces
    else:
        return [re.sub(r'\s+', ' ', re.sub(r'[^a-z]', ' ', v)).strip() for v in lowercased_ascii][0] #keep first

def cleanJobChars(x: str) -> str:
    # Capitalize the job title
    x = x.lower()
    stop_chars = ['m f',' para ']
    for stop in stop_chars:
        if stop in x:
            aux = x.split(stop)
            for val in aux:
                if val != stop and val != '':
                    x = val
                    break
    return x.strip()

    
def replaceCommonFillers(x: str) -> str:
    fillers = ['recruta-se para', 'recruta-se', 'oferta de emprego:', 'oferta:', 'oferta de emprego', 'oferta', 'precisa-se', 
               'precisas-se', 'part-time']
    for i in fillers:
        x = x.replace(i, '')
    return x

def removeStopwords(x):
    """Remove stop words from list of tokenized words"""
    new_words = []
    word_tokens = word_tokenize(x)
    for t in word_tokens:
        # print(word)
        if t not in STOPWORDS:
            new_words.append(t)
    return ' '.join(new_words)

cleanJobTitle = compose(normalizeTitle, replaceCommonFillers, cleanJobChars, removeStopwords)