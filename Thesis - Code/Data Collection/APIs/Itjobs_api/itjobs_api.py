import json
import os
from .config import API_KEY
import requests
from datetime import date
from w3lib.html import remove_tags


def save_data_to_json(file_name, data):
    """Save data to a json file creating it if it does not already exist
    :parameter: file_name -> 'example' do not add the '.json' 
    :parameter: data -> json data with the following structure [{},{},...]"""
    # Save Data
    if os.path.exists(file_name+'.json') == False:
        with open(file_name+'.json', 'w', encoding='utf-8') as json_file:
            # json.dump(data, json_file, indent=0, ensure_ascii=False)
            for entry in data:
                json.dump(entry, json_file)
                json_file.write('\n')
        json_file.close()
    else:
        with open(file_name+'.json', 'a+', encoding='utf-8') as json_file:
            # json.dump(data, json_file, indent=0, ensure_ascii=False)
            for entry in data:
                json.dump(entry, json_file, ensure_ascii=False)
                json_file.write('\n')
        json_file.close()
        
def call_api():
    #json query
    params = {
        'api_key': API_KEY,
        'limit': 3890
        }

    response = requests.get(url=f"https://api.itjobs.pt/job/list.json", params=params)
    # print(response)

    # Save results to json
    results = response.json()
    jobs = results['results']
    return jobs

def main(filename):
    jobs = call_api()

    job_offers = []
    for j in jobs:

        title = j['title']
        description = remove_tags(j['body'])
        post_date = j['publishedAt']
        company = j['company']['name']
        try:
            job_location = [i['name'] for i in j['locations']]
            ', '.join(job_location)
        except KeyError:
            job_location = ''

        try:
            salary = j['wage']
        except AttributeError:
            salary = ''

        job_offer = {
            'job_title': title,
            'job_description': description, 
            'post_date': post_date, 
            'scrape_date': date.today().strftime("%d/%m/%Y"),
            'company': company,
            'job_location': job_location,
            'job_category': '',
            'job_ref': f"https://www.itjobs.pt/oferta/{j['id']}/{j['slug']}",
            'salary': salary,
        }

        job_offers.append(job_offer)

    save_data_to_json(f"C:/Users/gilnr/OneDrive - NOVASBE/Work Project/Thesis - Code/Data/{filename}", job_offers)

if __name__ == '__main__':
    main('itjobs_jobs')
    print('Jobs Retrieved successefully')