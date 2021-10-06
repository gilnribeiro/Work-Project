import json
import os
import pandas as pd


def save_data_to_json(file_name, data):
    """Save data to a json file creating it if it does not already exist
    :parameter: file_name -> 'example' do not add the '.json' 
    :parameter: data -> json data with the following structure [{},{},...]"""
    # Save Data
    if os.path.exists(file_name+'.json') == False:
        with open(file_name+'.json', 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=0, ensure_ascii=False)
        json_file.close()
    else:
        with open(file_name+'.json', 'a+', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=0, ensure_ascii=False)
        json_file.close()


def pandas_json_to_csv(file_name):
    """Convert json to csv using pandas, needs to be a structured json [{},{},...]
    :parameter: file_name -> 'example' do not add the '.json' """
    # Json to csv
    df = pd.read_json(file_name+'.json')
    df.to_csv(file_name+'.csv')
