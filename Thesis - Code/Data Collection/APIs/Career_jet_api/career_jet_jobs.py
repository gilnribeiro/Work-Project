from tqdm import tqdm
import time
from util import save_data_to_json
import config
from careerjet_api_client import CareerjetAPIClient
import time
import config
from datetime import date
# pip install careerjet-api-client
# go to __init__.py careerjet-api-client, correct the Except, e: and the from urlparse -> to -> from urllib.parse
from careerjet_api_client import CareerjetAPIClient


def main(file_name):
    
    page_size = 99
    # start with arbitrarily large number
    n_pages = 10000
    stop = False
    cj  =  CareerjetAPIClient("pt_PT")

    result_json = cj.search({
                            'affid'       :  config.affid,
                            'user_ip'     : '11.22.33.44',
                            'url'         : 'http://www.example.com/jobsearch?sort=date&l=Portugal',
                            'user_agent'  : 'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0',
                            'location'    : 'Portugal',
                            'sort'        : 'date', 
                            'pagesize'    : 99,
                            'page'        : 1,
                            'contracttype': None,
                        })

    jobs = result_json['jobs']
    job_offers = []
    for job in jobs:
        try:
            salary = str(job['salary_min']) + ' - ' + str(job['salary_max'])
        except:
            salary = job['salary']

        job_offers.append(
            {
                'job_title': job['title'],
                'job_description': job['description'],
                'post_date': job['date'][:-13],
                'scrape_date': date.today().strftime("%d/%m/%Y"),
                'company': job['company'],
                'job_location': job['locations'],
                'job_category': '',
                'job_href': job['url'],
                'salary': salary
            }
        )
    # Get number of pages
    n_pages = result_json['pages']

    for page in tqdm(range(2, n_pages+1)):
        # Wait time 
        time.sleep(0.5)

        # Get json
        result_json = cj.search({
                            'affid'       :  config.affid,
                            'user_ip'     : '11.22.33.44',
                            'url'         : 'http://www.example.com/jobsearch?sort=date&l=Portugal',
                            'user_agent'  : 'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0',
                            'location'    : 'Portugal',
                            'sort'        : 'date', 
                            'pagesize'    : page_size,
                            'page'        : page,
                            'contracttype': None,
                        })
        # Get jobs
        jobs += result_json['jobs']
        for job in jobs:
            try:
                salary = str(job['salary_min']) + ' - ' + str(job['salary_max'])
            except:
                salary = job['salary']

            job_offers.append(
                {
                    'job_title': job['title'],
                    'job_description': job['description'],
                    'post_date': job['date'][:-13],
                    'scrape_date': date.today().strftime("%d/%m/%Y"),
                    'company': job['company'],
                    'job_location': job['locations'],
                    'job_category': '',
                    'job_href': job['url'],
                    'salary': salary
                }
            )
    # Save data to json
    save_data_to_json('C:/Users/gilnr/OneDrive - NOVASBE/Work Project/Thesis - Code/Job Vacancies Data/'+file_name, job_offers)
    print('Success')
    # Convert data to csv
    # pandas_json_to_csv('C:/Users/gilnr/OneDrive - NOVASBE/Work Project/Thesis - Code/Job Vacancies Data/'+file_name)     

if __name__ == '__main__':
    main('career_jet_jobs')