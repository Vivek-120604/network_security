import os
import sys
import json
import pandas as pd
import pymongo
import certifi
from networksecurity.logging.logger import logging
ca = certifi.where()
from networksecurity.exception.exception import NetworkSecurityException

from dotenv import load_dotenv
load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

# This log is good, check your terminal to ensure this URL is not 'None'
logging.info(f"MongoDB URL: {MONGO_DB_URL}") 



class NetworkDATAExtract():

    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def cv_to_json(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)

            # convert DataFrame to a list of dictionaries (one dict per row)
            records = data.to_dict('records')
            return records
        except Exception as e:
            raise  NetworkSecurityException(e, sys)
        
    
    # --- THIS IS THE MODIFIED FUNCTION ---
    # It now inserts in batches to prevent timeouts
    def insert_data_mongodb(self, records, database, collection, batch_size=1000):
        try:
            if not records:
                logging.info("No records to insert.")
                return 0
            
            # Use 'self.' for database/collection names passed as arguments
            self.database_name = database
            self.collection_name = collection

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            # Use the provided database and collection names
            self.database = self.mongo_client[self.database_name]
            self.collection = self.database[self.collection_name]
            
            total_inserted = 0
            logging.info(f"Starting batch insert of {len(records)} records in batches of {batch_size}...")

            # Loop through the records in chunks (batches)
            for i in range(0, len(records), batch_size):
                batch = records[i:i + batch_size]
                if batch:
                    self.collection.insert_many(batch)
                    total_inserted += len(batch)
                    logging.info(f"Inserted batch {i // batch_size + 1}, total records: {total_inserted}")

            self.mongo_client.close() # Close connection
            logging.info("Batch insert completed successfully.")
            return total_inserted
        
        except Exception as e:
            # This will catch the 'connection closed' error and report it
            raise NetworkSecurityException(e,sys)  
    

if __name__ == "__main__":
    FILE_PATH = "Network_data/phissing_data.csv"
    DATABASE = "VIVEK_AI"
    COLLECTION = "NETWORK_SECURITY"
    
    try:
        networkobj = NetworkDATAExtract()
        
        logging.info("Extracting records from CSV...")
        records = networkobj.cv_to_json(file_path = FILE_PATH)
        
        # --- THIS LOGGING LINE IS MODIFIED ---
        # We log the *length* of records, not the records themselves
        logging.info(f"Total records extracted from CSV: {len(records)}") 
        
        no_of_records = networkobj.insert_data_mongodb(records=records, database=DATABASE, collection=COLLECTION)
        
        logging.info(f"Total number of records inserted in MongoDB: {no_of_records}")

    except Exception as e:
        # This will catch the NetworkSecurityException and log it
        logging.error(f"Script failed: {e}")
        sys.exit(1)