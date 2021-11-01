import os
import requests
import json
from datetime import date, timedelta
import re


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
        
        
def call(page):
    payload = json.dumps({
        "search": "",
        "region": "",
        "regionId": -1,
        "jobTypes": [],
        "coords": None,
        "page": page
    })
    
    headers = {
        'authority': 'pt.jooble.org',
        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        'content-type': 'application/json',
        'trace-id': 'XMWmxyK3vuUtCPTASYtuGLUqtEunghJY',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'accept': '*/*',
        'origin': 'https://pt.jooble.org',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://pt.jooble.org/SearchResult',
        'accept-language': 'en,pt-PT;q=0.9,pt;q=0.8,en-US;q=0.7',
        'cookie': '@key@=1; SessionUtmCookie.pt=; uuid=2150579437689913764; rk_groups=; sever=21; ULang=0; ver=desktop; ts-consent={"date":"2021-09-03T16:56:28.901Z"}; REGION_TOOLTIP_COOKIE=1; SessionUtmCookie.us=; dt_groups=; ssearchstring=; ShouldShowSubscribeTooltip=1; SessionCookie.za=4926216140959339237*-1937988599995428085*637675168568965781; SessionUtmCookie.za=; shistory=%5b%7b%22sid%22%3a-4234727969285232829%2c%22ct%22%3a%222021-09-24T12%3a10%3a21.2366942%22%2c%22qh%22%3a0%2c%22rs%22%3a%22Portugal%22%2c%22ss%22%3a%22%22%7d%5d; .AspNetCore.Session=CfDJ8PKebYMwr05KjAkAOeWcsbjX305MoSzAmNSjh+VvjcklXrXFVGuRIXnvGY8Y3iB/f5VG3V3Q31a+omBQBAToztBR5k0Kd9nBmXWXnwZQPxoxyiNtw9qeuN20cXlXgWpLxNoO4sJGOl1qyheSTx2aQTSWxw1iLWj2jBDvSUAsJSfA; SessionUtmCookie.in=; SessionCookie.in=4351240177793434058*4303635476865319689*637695049712622681; SessionCookie.us=-5018549598333985903*-8093298241897550124*637695053499834966; emailWasAskedBeforeAway=1; datadome=4nbK6w6cWUuMGs-XMj.9c.dSVg0kqL0dBSkJpBjm-cErxZWhAfSVZ7hA.mrOvZrqeJs0YNoerL83pOkP-zVce9TkZhzElmEBPrwNtAGUAE; .AspNetCore.Antiforgery.skJtRLZwyNI=CfDJ8PKebYMwr05KjAkAOeWcsbh75Qx6G1R1VI6Df8MqZ_Uy7T_Y34D9-YahDxwy3Ym5_8f73dDnkt8N5LzQyw8fnmdChlw51ZTvfBgdAYksYb7Ym-nU4Sjl-aXXZaYSYQAi3S7mky89_V0u3G7E_ub1zCE; LastVisit=10/11/2021 1:42:47 AM; AuthId=5095195385154574232; g_state={"i_p":1634003030697,"i_l":2}; SessionCookie.pt=-621295169868825567*1298965443686883331*637695134272370768; SessionCookie.pt=-621295169868825567*-1332793703656602954*637695510493787961; SessionUtmCookie.pt=; LastVisit=10/11/2021 12:06:48 PM; rk_groups=; sever=21'
    }

    response = requests.request("POST", "https://pt.jooble.org/api/serp/jobs", headers=headers, data=payload)
    if response.status_code != 200:
        return 'break'

    results = response.json()
    jobs = results['jobs']
    return jobs

def get_post_date(d):
    # print(d)
    if 'horas' or 'hora' in d:
        post_date = date.today().strftime("%d/%m/%Y")
    elif 'dia atrás' == d:
        post_date = (date.today() - timedelta(days=1)).strftime("%d/%m/%Y")
    else:
        post_date = (date.today() - timedelta(days=int(re.search('\d+', d)[0]))).strftime("%d/%m/%Y")

    return post_date

def handleResults(filename):
    """
    This function handles the json output from the API call.
    :parameter: results -> json response
    :parameter: L -> LandingJobs Class
    """
    job_offers = []
    
    for page in range(1, 1000):
        jobs = call(page)
        # Exit the loop when pages are finished
        if jobs == 'break':
            print(f'Loop exited at page {page}')
            break

        for job in jobs:
            
            try:
                salary = int(re.search('\d+', job['salary'])[0])
            except TypeError:
                salary = ''
            
            job_offers.append(
                {
                'job_title': job['position'],
                'job_description': job['content'], 
                'post_date': get_post_date(job['dateCaption']), 
                'scrape_date': date.today().strftime("%d/%m/%Y"),
                'company': job['company']['name'],
                'job_location': job['location']['name'],
                'job_category': '',
                'job_ref': job['url'],
                'salary': salary,
            })

    save_data_to_json(f"C:/Users/gilnr/OneDrive - NOVASBE/Work Project/Thesis - Code/Data/{filename}", job_offers)


if __name__ == '__main__':
    handleResults('jooble_jobs')
    print('Jobs Retrieved Sucessefuly')
