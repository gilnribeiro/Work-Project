from Code.DataBase.Atlas_database import AtlasDatabase
from Code.Data_Collection.APIs.api_caller import main as api_caller
from Code.Data_Collection.Web_Scraping.job_scraping.job_scraping.scrapy_crawler import main as scrapy_crawler
from Code.Data_Cleaning.pipelines import main as data_cleaning_pipelines

import datetime
from datetime import timedelta, timezone


# ## GLOBAL VARIABLES
DATA_FOLDER_PATH = "/Users/gilnr/OneDrive - NOVASBE/Work Project/Code/Data/"

# # LOAD
def LoadToMongoDb():
    """
    Fetches the "full_data_clean.json" from a local folder and loads it to the database in two different collections:
        Collection 1: "Full History" -> Where job vacancies are simply appended to existing ones
        Collection 2: "60 Days" -> Where new job vacancies are appended and documents older than 60 days are dropped from the collection
    """
    # Initialize Class Object
    AtlasDb = AtlasDatabase()

    # Append Data to Historical Database
    AtlasDb.insert_file_data(file_location=DATA_FOLDER_PATH + 'full_data_clean.json', 
                             database_name='jobsdb', collection_name='Full History')

    # Remove Documents that are older than 60 days counting from Today()
    delta = str(datetime.datetime.now(timezone.utc) - timedelta(days=7))
    week_ago = delta.split(' ')[0]+'T00:00:00Z'

    AtlasDb.delete_many(query={
        "post_date": {
            "$lt": week_ago
        }
    }, 
    database_name='jobsdb', 
    collection_name='Last 60 Days')
    

    # Append Data to Last 60 days Database
    AtlasDb.insert_file_data(file_location=DATA_FOLDER_PATH + 'full_data_clean.json', 
                             database_name='jobsdb', collection_name='Last 60 Days')


def extract():
    print('Starting ETL... Extraction from API')
    api_caller()
    print('API Extraction Complete\nInitiating Web Scrapers...')
    scrapy_crawler()
    print('Web Scrapers Complete!\n')


def transform():
    print('Starting Data Transformation...')
    data_cleaning_pipelines()
    print('Data Transformation Complete!')

def load():
    print('Loading data to Mongo DB database')
    LoadToMongoDb()
    print('Loading Complete!')

# # THE ETL PIPELINE
extract()
transform()
load()