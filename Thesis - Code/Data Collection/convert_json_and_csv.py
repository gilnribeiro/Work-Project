import json
import os
import csv
import pandas as pd


def save_data_to_json(file_name, data):
    """Save data to a json file creating it if it does not already exist
    :parameter: file_name -> 'example' do not add the '.json'
    :parameter: data -> json data with the following structure [{},{},...]"""
    # Save Data
    if os.path.exists(file_name + '.json') == False:
        with open(file_name + '.json', 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=0, ensure_ascii=False)
        json_file.close()
    else:
        with open(file_name + '.json', 'a+', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=0, ensure_ascii=False)
        json_file.close()


def pandas_json_to_csv(file_name):
    """Convert json to csv using pandas, needs to be a structured json [{},{},...]
    :parameter: file_name -> 'example' do not add the '.json' """
    # Json to csv
    df = pd.read_json(file_name + '.json')
    df.to_csv(file_name + '.csv')


def csv_to_json(file_name):
    """Convert csv to json
    :parameter: file_name -> 'example' do not add the '.csv'
    :returns: file_name.json"""
    json_array = []

    # read csv file
    with open(file_name+'.csv', encoding='utf-8') as csvf:
        # load csv file data using csv library's dictionary reader
        csv_reader = csv.DictReader(csvf)

        # convert each csv row into python dict
        for row in csv_reader:
            # add this python dict to json array
            json_array.append(row)

    # convert python jsonArray to JSON String and write to file
    with open(file_name+'.json', 'w', encoding='utf-8') as jsonf:
        json_string = json.dumps(json_array, indent=4)
        jsonf.write(json_string)


def converter():
    while True:
        file_name = input('Please input the filename to convert: ')
        print('Options:\n 1. Json -> csv\n 2. csv -> Json\n 0. To Exit')
        option = input('Select Option 1, 2 or (0 to exit): ')

        if option == '1':
            pandas_json_to_csv(file_name=file_name)
            print('Conversion Successful')
            break
        elif option == '2':
            csv_to_json(file_name=file_name)
            print('Conversion Successful')
            break
        elif option == '0':
            print('Exit Successfully')
            break
        else:
            print('Please insert a valid option or filename')


if __name__ == '__main__':
    converter()
