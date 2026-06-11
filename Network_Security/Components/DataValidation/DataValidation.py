import os 
import sys
from Network_Security.Exception.NS_exception import NetworkSecurityException
from Network_Security.logging.NS_logging import logging
from Network_Security.Constants.Training_Constant import *
from Network_Security.Entity.Config_entity import DataValidationConfig
from Network_Security.Entity.Artifact_entity import DataValidationArtifact,DataIngestionArtifact
from Network_Security.Utils.Utils import Commonutils
from scipy.stats import ks_2samp

import pandas as pd
from pandas import DataFrame
import shutil
from typing import List,Tuple


class DataValidation:
    def __init__(self,datavalidationconfig:DataValidationConfig,dataingestionartifact:DataIngestionArtifact):
        self.data_validation_config=datavalidationconfig
        self.data_ingestion_artifact=dataingestionartifact
        self.utils=Commonutils()

    def validate_schema_cols(self,dataframe:DataFrame)->bool:
        """
        This function will validate the schema of data columns"""

        try:
            NUMBER_OF_COLS= len(self.utils.read_yamlfile(SCHEMA_FILEPATH)['columns'])
            logging.info(f"len of number of cols {NUMBER_OF_COLS}")
            logging.info(f"len of datafranme cols {dataframe.columns}")

            if len(dataframe.columns)==NUMBER_OF_COLS:
                return True
            
            return False
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def check_null_values(self,dataframe:DataFrame)->bool:
        """This function will check the null values in dataset"""

        try:
            if dataframe.isnull().sum().sum()>0:
                logging.info("dataset containing null values inside it")
                return False
            return True
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    #check data drift here
    def detect_dataset_drift(self,base_df,current_df,threshold=0.05):# we are doing hypothesis testing to detect it using ks_2sample because we have numerical columms
        """This functionn will detect data drift """
        try:
            status=True
            report={}
            for column in base_df.columns:
                D1=base_df[column]
                D2=current_df[column]

                is_sample_dist=ks_2samp(D1,D2)

                if threshold==is_sample_dist.pvalue:
                    is_found=False

                is_found=True
                status=False

                report.update(
                    {
                        column:{
                            "P_Value":float(is_sample_dist.pvalue),
                            "Drift_Status":is_found
                        }
                    }
                )
            return status,report 
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    
    @staticmethod
    def read_data(filepath:str)->DataFrame:

        """This function will return dataframe after reading the data
        """,

        try:
            dataframe=pd.read_csv(filepath)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def move_to_invalid_data_dir(self,curr_path:str,dest_path:str):
        """This fucntion will move the data to their correct path"""
        try:
          os.makedirs(dest_path, exist_ok=True)

          destination_file = os.path.join(
            dest_path,
            os.path.basename(curr_path)
          )

          shutil.move(curr_path, destination_file)

          logging.info(
            f"Moved {curr_path} to {destination_file}"
          )
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def initiate_data_validation(self)->DataValidationArtifact:
        """
        This function will initiate the data validation process.."""

        try:
            train_file=self.data_ingestion_artifact.train_file_path
            test_file=self.data_ingestion_artifact.test_file_path

            train_data=DataValidation.read_data(train_file)
            test_data=DataValidation.read_data(test_file)

            validation_status=False

            if self.validate_schema_cols(train_data) and self.validate_schema_cols(test_data) and self.check_null_values(train_data) and self.check_null_values(test_data):
                validation_status=True
                logging.info("validation status is True ,All checks are correct for data")

                #dataset drift
                status,report=self.detect_dataset_drift(base_df=train_data,current_df=test_data)
                if status:
                    logging.info("Dataset Drift Detected...")
                    print('Dataset Drift Detected.!')

                #create folder and write the report inside it
                os.makedirs(os.path.dirname(self.data_validation_config.data_drift_report_file_path),exist_ok=True)
                self.utils.write_yaml_file(file_path=self.data_validation_config.data_drift_report_file_path,content=report,replace=False)#writing the content in filepath

                os.makedirs(os.path.dirname(self.data_validation_config.valid_train_file_path),exist_ok=True)
                train_data.to_csv((self.data_validation_config.valid_train_file_path),index=False)
                test_data.to_csv((self.data_validation_config.valid_test_file_path),index=False)

            else:
                self.move_to_invalid_data_dir(curr_path=train_file , dest_path=(self.data_validation_config.invalid_data_dir))
                self.move_to_invalid_data_dir(curr_path=test_file,dest_path=(self.data_validation_config.invalid_data_dir))

            Data_Validation_Artifact=DataValidationArtifact(
                Validation_status=validation_status,
                drift_file_report=self.data_validation_config.data_drift_report_file_path,
                valid_train_filepath=self.data_validation_config.valid_train_file_path,
                valid_test_filepath=self.data_validation_config.valid_test_file_path,
                invalid_test_filepath=self.data_validation_config.invalid_test_file_path,
                invalid_train_filepath=self.data_validation_config.invalid_train_file_path


            )
            logging.info(f"artifact {Data_Validation_Artifact}")
            print(f"artifact {Data_Validation_Artifact}")
            return Data_Validation_Artifact
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)

