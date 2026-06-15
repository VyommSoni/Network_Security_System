import pandas as pd
import numpy as np
from Network_Security.Exception.NS_exception import NetworkSecurityException
from Network_Security.logging.NS_logging import logging
import sys
from pandas import DataFrame
import os
from Network_Security.Constants.Training_Constant import *
from Network_Security.Utils.Utils import Commonutils
from Network_Security.Entity.Artifact_entity import (DataTransformationArtifact , DataValidationArtifact)
from Network_Security.Entity.Config_entity import DataTransformationConfig
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline


class DataTransformation:
    def __init__(self,data_transformation_config:DataTransformationConfig,data_validation_artifact:DataValidationArtifact):
        self.utils=Commonutils()
        self.data_transformation_config=data_transformation_config
        self.data_validation_artifact=data_validation_artifact

    
    @staticmethod
    def read_data(filepath:str)->DataFrame:
        try:
            df=pd.read_csv(filepath)
            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def impute(cls)->Pipeline:
        """
        It initilize the KNN imputer object with the parameters present in constant folder"""

        try:
            imputer=KNNImputer(**KNN_IMPUTER_PARAMS)
            logging.info(f'Initilaized the knn imputer with params {KNN_IMPUTER_PARAMS}')

            preprocessor:Pipeline=Pipeline([("imputer",imputer)])

            return preprocessor
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def initiate_data_transformation(self)->DataTransformationArtifact:
        """It will start the process for datatransformation"""

        try:
            logging.info("Starting the DataTransformation Process....")

            train_data=DataTransformation.read_data(self.data_validation_artifact.valid_train_filepath)
            test_data=DataTransformation.read_data(self.data_validation_artifact.valid_test_filepath)


            X_train=train_data.drop(columns=[TARGET_COLUMN],axis=1)
            Y_train=train_data[TARGET_COLUMN]

            X_test=test_data.drop(columns=[TARGET_COLUMN],axis=1)
            Y_test=test_data[TARGET_COLUMN]

            preprocessor=self.impute()
            preprocessor_object=preprocessor.fit(X_train)

            transformed_object_train=preprocessor_object.transform(X_train)
            transformed_object_test=preprocessor_object.transform(X_test)

            train_arr=np.c_[transformed_object_train,np.array(Y_train)]
            test_arr=np.c_[transformed_object_test,np.array(Y_test)]

            os.makedirs(os.path.dirname(self.data_transformation_config.transformed_object_path),exist_ok=True)#[preprocessor dir
            os.makedirs(os.path.dirname(self.data_transformation_config.transformed_trainfilepath),exist_ok=True)# transformed dir


            self.utils.save_numpy_array(array=train_arr,filepath=self.data_transformation_config.transformed_trainfilepath)
            self.utils.save_numpy_array(array=test_arr,filepath=self.data_transformation_config.transformed_testfilepath)
            self.utils.save_object(filepath=self.data_transformation_config.transformed_object_path,obj=preprocessor_object)

            self.utils.save_object(filepath=Final_Model_path,obj=preprocessor_object )
            

            Data_Transformation_artifacts=DataTransformationArtifact(
                Preprocessor_Path=self.data_transformation_config.transformed_object_path,
                transformed_testfilepath=self.data_transformation_config.transformed_testfilepath,
                transformed_trainfilepath=self.data_transformation_config.transformed_trainfilepath
            )
            
            return Data_Transformation_artifacts

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    
