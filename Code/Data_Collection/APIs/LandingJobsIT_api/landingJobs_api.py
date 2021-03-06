import json
import os
import requests
from w3lib.html import remove_tags
from datetime import date


class LandingJobs():
    def __init__(self):
        self.session = requests.Session()
        self.results = 'break'
        self.company = {'name': ''}
    
    def getJobsList(self, limit=50, offset=0):
        response = self.session.get(f'https://landing.jobs/api/v1/jobs?limit={limit}&offset={offset}')
        if response.status_code == 200:
            self.results = response.json()

    def getCompanyInfo(self, id):
        response = self.session.get(f'https://landing.jobs/api/v1/companies/{id}')
        if response.status_code == 200:
            self.company = response.json()        


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


def handleResults(results, L):
    """
    This function handles the json output from the API call.
    :parameter: results -> json response
    :parameter: L -> LandingJobs Class
    """
    job_offer = []

    for job in results:
        if job['country_code'] == 'PT':
            job_description = remove_tags(job['main_requirements']+'\n'+job['nice_to_have']+'\n'+job['perks']+'\n'+job['role_description'])
            L.getCompanyInfo(id=job['company_id'])
            company = L.company['name']

            try:
                salary = str(job['gross_salary_low'])+' - '+str(job['gross_salary_high'])
            except KeyError:
                salary = ''

            job_offer.append({
                'job_title': job['title'],
                'job_description': job_description, 
                'post_date': job['published_at'], 
                'scrape_date': date.today().strftime("%d/%m/%Y"),
                'company': company,
                'job_location': job['city'],
                'job_category': '',
                'job_ref': job['url'],
                'salary': salary,
            })

    return job_offer

def main(filename):
    L = LandingJobs()
    job_offers = []
    for i in range(0, 1000, 50):
        L.getJobsList(limit=50, offset=i)
        if L.results == 'break':
            break
        else:
            job_offers += handleResults(results=L.results, L=L)

    save_data_to_json(f"C:/Users/gilnr/OneDrive - NOVASBE/Work Project/Code/Data/{filename}", job_offers)

if __name__ == '__main__':
    main('LandingJobsIT_jobs')   
    print('Jobs Retrieved successefully')