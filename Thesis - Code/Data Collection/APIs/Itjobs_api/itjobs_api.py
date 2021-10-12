from config import API_KEY
import requests
from util import save_data_to_json
from datetime import date
from w3lib.html import remove_tags


def call_api():
    #json query
    params = {
        'api_key': API_KEY,
        'limit': 3890
        }

    response = requests.get(url=f"https://api.itjobs.pt/job/list.json", params=params)
    print(response)

    # Save results to json
    results = response.json()
    jobs = results['results']
    return jobs

def main():
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

    save_data_to_json("C:/Users/gilnr/OneDrive - NOVASBE/Work Project/Thesis - Code/Job Vacancies Data/itjobs_jobs", job_offers)

if __name__ == '__main__':
    main()
    print('Jobs Retrieved successefully')