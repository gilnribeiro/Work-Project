import json
import jsonlines
import os
import time
from careerjet_api_client import CareerjetAPIClient
import time
from .config import affid
from datetime import date
import csv
# pip install careerjet-api-client
# go to __init__.py careerjet-api-client, correct the Except, e: and the from urlparse -> to -> from urllib.parse
from careerjet_api_client import CareerjetAPIClient


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
        
def main(file_name):
    
    page_size = 99
    # start with arbitrarily large number
    n_pages = 11
    stop = False
    cj  =  CareerjetAPIClient("pt_PT")

    result_json = cj.search({
                            "affid"       :  affid,
                            "user_ip"     : "11.22.33.44",
                            "url"         : "http://www.careerjet.pt/jobsearch?sort=date&l=Portugal",
                            "user_agent"  : "Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0",
                            "location"    : "Portugal",
                            "sort"        : "date", 
                            "pagesize"    : 99,
                            "page"        : 1,
                            "contracttype": None,
                        })

    jobs = result_json["jobs"]
    job_offers = []
    job_offers_csv = []
    for job in jobs:
        try:
            salary = str(job["salary_min"]) + " - " + str(job["salary_max"])
        except:
            salary = job["salary"]

        job_offers.append(
            {
                "job_title": job["title"],
                "job_description": job["description"],
                "post_date": job["date"][:-13],
                "scrape_date": date.today().strftime("%d/%m/%Y"),
                "company": job["company"],
                "job_location": job["locations"],
                "job_category": "",
                "job_href": job["url"],
                "salary": salary
            }
        )
    # Get number of pages
    # n_pages = result_json["pages"]

    for page in range(2, n_pages+1):
        # Wait time 
        time.sleep(0.5)

        # Get json
        result_json = cj.search({
                            "affid"       :  affid,
                            "user_ip"     : "11.22.33.44",
                            "url"         : "http://www.example.com/jobsearch?sort=date&l=Portugal",
                            "user_agent"  : "Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0",
                            "location"    : "Portugal",
                            "sort"        : "date", 
                            "pagesize"    : page_size,
                            "page"        : page,
                            "contracttype": None,
                        })
        # Get jobs
        jobs += result_json["jobs"]
        for job in jobs:
            try:
                salary = str(job["salary_min"]) + " - " + str(job["salary_max"])
            except:
                salary = job["salary"]

            job_offers.append(
                {
                    "job_title": job["title"],
                    "job_description": job["description"],
                    "post_date": job["date"][:-13],
                    "scrape_date": date.today().strftime("%d/%m/%Y"),
                    "company": job["company"],
                    "job_location": job["locations"],
                    "job_category": "",
                    "job_href": job["url"],
                    "salary": salary
                }
            )
            record = (job["title"], job["description"], job["date"][:-13], date.today().strftime("%d/%m/%Y"), job["company"],
                      job["locations"], "", job["url"], salary)
            job_offers_csv.append(record)

    # Save data to csv
    # with open('career_jet_jobs.csv', 'w', newline='', encoding='utf-8') as f:
    #         writer = csv.writer(f)
    #         writer.writerow(['job_title', 'job_description', 'post_date', 'scrape_date', 'company', 'job_location', 'job_category', 'job_href', 'salary'])
    #         writer.writerows(job_offers_csv)
    #         f.close()
    # Save data to json
    save_data_to_json("C:/Users/gilnr/OneDrive - NOVASBE/Work Project/Code/Data/"+file_name, job_offers)
    print("Success")
    # Convert data to csv
    # pandas_json_to_csv("C:/Users/gilnr/OneDrive - NOVASBE/Work Project/Thesis - Code/Job Vacancies Data/"+file_name)     

if __name__ == "__main__":
    main("career_jet_jobs_V1")
    