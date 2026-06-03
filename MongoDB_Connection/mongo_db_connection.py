import pymongo
import os
import sys
from Network_Security.Exception.NS_exception import NetworkSecurityException
from Network_Security.logging.NS_logging import logging


class MongoDBClient:
    def __init__(self):
        pass

    def connect(self,mongo_db_url):
        '''This function will connect to your database

        '''
        try:

            logging.info("Getting request for Database connection....")
            self.Client=pymongo.MongoClient(mongo_db_url)

            response = self.Client.admin.command('ping')

            if response.get("ok")==1.0:
                logging.info("Successfully build connection...")
                print("Connection built.! to Mongodbdatabase")
                return self.Client
            return "Unable to build connection..."

        except Exception as e:
            raise NetworkSecurityException(e,sys)





            


