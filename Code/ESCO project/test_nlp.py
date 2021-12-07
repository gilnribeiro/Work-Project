from tqdm import tqdm 
import time
import json
import pandas  as pd
from thefuzz import fuzz

FOLDER_PATH = "/Users/gilnr/OneDrive - NOVASBE/Work Project/Code/ESCO project/"

def exactMatchTitle(x:str) -> str:
    if x in esco_dict: # exact match
        return esco_dict[x]['occupation']
    else:
        return "NOT EXACT"
    
def similarityMatchTitle(x:str) -> str:
    job, sim = max([(esco_dict[job]['occupation'], fuzz.token_set_ratio(x, job)) for job in esco_dict], key=lambda x: x[1])
    if sim >= 80:
        return job
    else: # no similarity match
        return f"NOT FOUND - {x} | {job} ({sim})"

# Time
t1 = time.time()

# Load Data
data = pd.read_json(FOLDER_PATH + 'esco_project_data.json')
with open("esco_dictionary.json", 'r', encoding='utf-8') as file:
    esco_dict = json.load(file)
        
data['esco_exact_match'] = data.job_title.apply(lambda x: exactMatchTitle(x))

count = data.loc[data['esco_exact_match'] !='NOT EXACT']['esco_exact_match'].count()
print('There are ', count, ' exact ESCO matches from a total of ', len(data), 
      'jobs. This is approximatly', round(count/len(data),4)*100,'% of jobs')
    
data['esco_similarity_match'] = data.job_title.apply(lambda x: similarityMatchTitle(x))

mask = data['esco_similarity_match'].str.contains('NOT FOUND', case=True, na=False)
print('There are', len(data)-len(data[mask]), 'approximate ESCO matches at 90% match, that is ', 
      round((len(data)-len(data[mask]))/len(data),4)*100,'% of total')

t = time.time() - t1
print('Finish!\n - Time: {t}')