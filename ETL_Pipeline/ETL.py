import os
import sys
from Network_Security.Exception.NS_exception import NetworkSecurityException
from Network_Security.logging.NS_logging import logging
from MongoDB_Connection.mongo_db_connection import MongoDBClient
import pandas as pd
from pandas import DataFrame
import numpy as np
from dotenv import load_dotenv
from Network_Security.Constants import *
from typing import List,Dict


load_dotenv()


class ETL_Pipeline:
    def __init__(self,File_Path):
        self.File_Path=File_Path

    def Extract_data(self)->DataFrame:
        '''This function will get extract data from  our local system 
        '''

        try:
            logging.info("Extracting data from local Path...")

            Data=pd.read_csv(self.File_Path)

            if not Data.empty:
                logging.info("Succesfully Extracted the data...")
                logging.info(f"Len of Data {len(Data)}")
                return Data
            logging.info("Unable to extract data")
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def Transform_data(self,data:pd.DataFrame)->DataFrame:
        '''This will transform the incoming data'''

        try:
            logging.info("Transforming the data..")

            data=data.drop_duplicates()#removes dupliactes items

            if data.isnull().sum().sum()>0:
                data=data.dropna()
                return data
            return data
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def load_data(self):

        '''This function will store data into mongodb_database'''

        try:
            logging.info(
                "Starting the procedure for storing the data into database.."
                )
            Client=MongoDBClient()
            Connection=Client.connect(mongo_db_url=os.getenv("MONGO_DB_URL"))

            data=pd.read_csv(self.File_Path)

            records=data.to_dict(orient='records')

            Database=Connection['NetworkSecurity']# database name

            Collection=Database['NewtorkSecurityData'] #Collection  name

            Collection.insert_many(records)

            logging.info(
                f"Inserted data of len {len(records)}"
                )

            return records
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        


ETL=ETL_Pipeline(File_Path=FilePath)

Data=ETL.Extract_data()

ETL.Transform_data(Data)

ETL.load_data()





            


        
   
            

            