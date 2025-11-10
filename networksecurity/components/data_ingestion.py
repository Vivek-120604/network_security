from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging






##configuration of the data ingestion config

from networksecurity.entity.config_entity import DataIngestionConfig 
from networksecurity.entity.artifact_entity import DataIngestionArtifact
import os, sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import pymongo # Removed the problematic import



from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")


class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
           self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def export_collection_as_dataframe(self):
        try:
            # Read from CSV file instead of MongoDB
            csv_file_path = "Network_data/phisingData.csv"
            df = pd.read_csv(csv_file_path)
            df.replace({"na": np.nan}, inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
        
    
        
    def export_data_into_feature_store(self, dataframe:pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False, header =True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e,sys)    
        
        
        
    def split_data_as_train_test(self, dataframe:pd.DataFrame):
        try:
            train_set, test_set = train_test_split(
                dataframe,
                test_size=self.data_ingestion_config.train_test_split_ratio,
                random_state=42
            )
            train_file_path = self.data_ingestion_config.train_file_path
            test_file_path = self.data_ingestion_config.test_file_path
            
            dir_path = os.path.dirname(train_file_path)
            os.makedirs(dir_path,exist_ok=True)
            
            train_set.to_csv(train_file_path,index=False,header=True)
            test_set.to_csv(test_file_path,index=False,header=True)
            
            return (
                train_file_path,
                test_file_path
            )
        except Exception as e:
            raise NetworkSecurityException(e,sys)
            
    def intiate_data_ingestion(self):
        try: # Fix: Call the method to get the dataframe
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            dataingestionartifact = DataIngestionArtifact(trained_file_path = self.data_ingestion_config.train_file_path,test_file_path=self.data_ingestion_config.test_file_path)  
            return dataingestionartifact
        except Exception as e:
                raise NetworkSecurityException  