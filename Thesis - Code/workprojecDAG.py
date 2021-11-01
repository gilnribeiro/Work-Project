from Data_Collection.APIs import api_caller
from Data_Collection.Web_Scraping.job_scraping.job_scraping import scrapy_crawler
from Data_Cleaning import pipelines as data_cleaning_pipelines
from DataBase.Atlas_database import AtlasDatabase

import datetime

## GLOBAL VARIABLES
DATA_FOLDER_PATH = "/Users/gilnr/OneDrive - NOVASBE/Work Project/Thesis - Code/Data/"

# Task 1
api_caller

# Task 2
scrapy_crawler

# Task 3
data_cleaning_pipelines

# Task 4
# def LoadToMongoDb():
#     # Initialize Class Object
#     AtlasDb = AtlasDatabase()

#     # Append Data to Historical Database
#     AtlasDb.insert_file_data(file_location=DATA_FOLDER_PATH + 'full_data_clean.json', database_name='jobsdb', collection_name='Full History')

#     # Remove Documents that are older than 60 days counting from Today()
#     today = datetime.today()

#     # Append Data to Last 60 days Database
#     AtlasDb.insert_file_data(file_location=DATA_FOLDER_PATH + 'full_data_clean.json', database_name='jobsdb', collection_name='60 Days')

#     pass
