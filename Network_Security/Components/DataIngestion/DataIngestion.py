import os
import sys
from Network_Security.Exception.NS_exception import NetworkSecurityException
from Network_Security.logging.NS_logging import logging
from Network_Security.Constants import *
import pandas as pd
from Network_Security.Constants.Training_Constant import *
from Network_Security.Entity.Config_entity import DataIngestionConfig,TrainingPipelineConfig
from Network_Security.Entity.Artifact_entity import DataIngestionArtifact

from sklearn.model_selection import train_test_split
from typing import List,Union,Tuple
from pandas import DataFrame
from MongoDB_Connection.mongo_db_connection import MongoDBClient
from dotenv import load_dotenv

load_dotenv()

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        self.data_ingestion_config=data_ingestion_config

    def Split_into_train_and_test(self,data:DataFrame)->Tuple[DataFrame,DataFrame]:
        """
        This function will  split data into train and test """

        try:
            train,test=train_test_split(data,test_size=self.data_ingestion_config.split_ratio,random_state=42)

            os.makedirs(os.path.dirname(self.data_ingestion_config.train_file_path),exist_ok=True)

            train.to_csv(
                self.data_ingestion_config.train_file_path,header=True,index=False
            )

            test.to_csv(
                self.data_ingestion_config.test_file_path,header=True,index=False
            )
            return train,test
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def export_dataframe(self)->DataFrame:
        '''This function will get data from mongodb database and store it in featurestore filepath..'''

        try:
            MB=MongoDBClient()
            Client=MB.connect(mongo_db_url=os.getenv("MONGO_DB_URL"))#making connection for mongoddatabase

            database=Client[DATA_INGESTION_DATABASE_NAME]
            collection_name=database[DATA_INGESTION_COLLECTION_NAME]

            cursor=collection_name.find()#find all document cursor

            data=list(cursor)

            df=DataFrame(data)

            if "_id" in df.columns:
                df.drop(columns="_id",inplace=True)

            return df

        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def Initiate_Data_Ingestion(self)->DataIngestionArtifact:
        """
        This function will Initiate DataIngestion and store raw files and store train and test files"""

        try:
            logging.info("Initiating the Data_Ingestion processs")
            data=self.export_dataframe()
            logging.info(f"Data shape {data.shape}")

            if not data.empty:
                logging.info("Exported data from mongodb in as a dataframe")

                os.makedirs(os.path.dirname(self.data_ingestion_config.feature_store_filepath),exist_ok=True)#making folder
                data.to_csv(self.data_ingestion_config.feature_store_filepath,index=False,header=True)
                
                #split dataframe
                train,test=self.Split_into_train_and_test(data=data)

                data_ingestion_artifact=DataIngestionArtifact(train_filepath=self.data_ingestion_config.train_file_path,
                                                              test_filepath=self.data_ingestion_config.test_file_path,
                                                              feature_storepath=self.data_ingestion_config.feature_store_filepath
                )

                

                return data_ingestion_artifact

            logging.info("Data exported from mongodb is empty,Please troubleshoot that problem...")



        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
if __name__== "__main__":
    DT=DataIngestion(data_ingestion_config=DataIngestionConfig(training_pipeline_config=TrainingPipelineConfig()))
    DT.Initiate_Data_Ingestion()