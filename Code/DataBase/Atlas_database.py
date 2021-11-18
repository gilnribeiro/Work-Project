import json 
from pymongo import MongoClient
import ssl
from .config import DEFAULT_CLUSTER, PASSWORD, DEFAULT_DB, USERNAME

class AtlasDatabase():
    def __init__(self, USERNAME=USERNAME, PASSWORD=PASSWORD, DEFAULT_DB=DEFAULT_DB, DEFAULT_CLUSTER=DEFAULT_CLUSTER):
        self.client = MongoClient(f"mongodb+srv://{USERNAME}:{PASSWORD}@{DEFAULT_CLUSTER}.ohzpo.mongodb.net/{DEFAULT_DB}?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE) 

    def pull_data(self, database_name, collection_name):
        """
        Get data from already existing databases and collections
        __ Important __ 
        Make sure to have the config.py set up in the same directory with
        DEFAULT_CLUSTER, PASSWORD, DEFAULT_DB, USERNAME

        :parameter: database_name
        :parameter: collection_name
        """
        # self.client = MongoClient(f'mongodb+srv://{USERNAME}:{PASSWORD}@{DEFAULT_CLUSTER}.ohzpo.mongodb.net/{DEFAULT_DB}?retryWrites=true&w=majority', ssl_cert_reqs=ssl.CERT_NONE) 
        # open the database
        dbname = self.client[database_name]
        # get the collection
        collection = dbname[collection_name]
        # get the data from the collection
        item_details = collection.find()

        return item_details


    def get_database(self, database_name):
        """
        Connect to Mongo.net and create a new database
        __ Important __ 
        Make sure to have the config.py set up in the same directory with
        DEFAULT_CLUSTER, PASSWORD, DEFAULT_DB, USERNAME

        :parameter: database_name
        """

        database = self.client[database_name]
        return database

    def insert_file_data(self, file_location, database_name, collection_name): 
        """
        Insert many (insert files into specified database)
        __ Important __ 
        Make sure to have the config.py set up in the same directory with
        DEFAULT_CLUSTER, PASSWORD, DEFAULT_DB, USERNAME

        :parameter: file_location -> filepath
        :parameter: database_name
        :parameter: collection_name
        """
        # database 
        db = self.client[database_name]
        
        # Created or Switched to collection 
        collection = db[collection_name]
        
        # Loading or Opening the json file
        with open(file_location, encoding='utf-8') as file:
            file_data = json.load(file)
            
        # Inserting the loaded data in the collection if JSON contains data more than one entry insert_many is used else inser_one is used
        if isinstance(file_data, list):
            collection.insert_many(file_data)  
        else:
            collection.insert_one(file_data)

    def delete_many(self, query, database_name, collection_name):
        """
        Delete many (delete a given set of documents that mach a specified query)
        :parameter: query -> mongodb query
        :parameter: database_name
        :parameter: collection_name
        """
        # database 
        db = self.client[database_name]
        
        # Created or Switched to collection 
        collection = db[collection_name]

        # Delete many based on the specified query
        d = collection.delete_many(query)     
    
        print("Deleted Count:", d.deleted_count)