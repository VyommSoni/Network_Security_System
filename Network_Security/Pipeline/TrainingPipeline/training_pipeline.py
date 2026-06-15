import os
import sys
from Network_Security.Components.DataIngestion.DataIngestion import DataIngestion
from Network_Security.Components.DataValidation.DataValidation import DataValidation
from Network_Security.Components.DataTransformation.DataTransformation import DataTransformation
from Network_Security.Components.ModelTrainer.ModelTrainer import ModelTrainer
from Network_Security.Exception.NS_exception import NetworkSecurityException
from Network_Security.logging.NS_logging import logging
from Network_Security.Infrastructure.CLOUD import *
from Network_Security.Constants.Training_Constant import *
from Network_Security.Entity.Config_entity import(
    DataIngestionConfig,DataTransformationConfig,DataValidationConfig,ModelTrainerConfig,TrainingPipelineConfig
)
from Network_Security.Entity.Artifact_entity import (
    DataIngestionArtifact,DataTransformationArtifact,DataValidationArtifact,ModelTrainerArtifact
)

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config=TrainingPipelineConfig()

    def Start_Data_Ingestion(self):
        try:
            self.data_ingestion_config=DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Starting data_ingestion...")
            data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion_config)

            data_ingestion_artifact=data_ingestion.Initiate_Data_Ingestion()

            logging.info(f"Data Ingestion completed and artifact {data_ingestion_artifact}")

            return data_ingestion_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def Start_Data_Validation(self,data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_validation_config=DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Starting the validation process..")

            data_validation=DataValidation(datavalidationconfig=self.data_validation_config,dataingestionartifact=data_ingestion_artifact)

            data_validation_artifact=data_validation.initiate_data_validation()
            logging.info(f"Data Validation completed and artifact {data_validation_artifact}")

            return data_validation_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def Start_Data_Transformation(self,data_validation_artifact:DataValidationArtifact):
        try:
            self.data_transformation_config=DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Starting the transformation process...")

            data_transformation=DataTransformation(data_transformation_config=self.data_transformation_config,data_validation_artifact=data_validation_artifact)

            data_transformation_artifact=data_transformation.initiate_data_transformation()
            logging.info(f"Transformation completed and artfacts {data_transformation_artifact}")

            return data_transformation_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def Start_Model_Trainer(self,Data_Transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Starting model trainer process...")

            Model_Trainer=ModelTrainer(data_transformation_artifact=Data_Transformation_artifact,model_trainer_config=self.model_trainer_config)

            model_trainer_artifact=Model_Trainer.initiate_model_trainer()
            logging.info(f"Model Trained and artifact {model_trainer_artifact}")

            return model_trainer_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)

   #all artifacts folder move to s3 bucket
    def sync_artifact_dir_to_s3(self):
                try:
                    aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
                    S3Sync.sync_folder_to_s3(folder = self.training_pipeline_config.artifacts_dir,aws_bucket_url=aws_bucket_url)
                except Exception as e:
                    raise NetworkSecurityException(e,sys)

    #final model push to s3        
    def sync_saved_model_dir_to_s3(self):
                try:
                    aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/Final_model/{self.training_pipeline_config.timestamp}"
                    S3Sync.sync_folder_to_s3(folder =FINAL_MODEL_DIR,aws_bucket_url=aws_bucket_url)
                except Exception as e:
                    raise NetworkSecurityException(e,sys)  
                      
    def run_pipeline(self):
        try:
            data_ingestion_artifact=self.Start_Data_Ingestion()
            data_validation_artifact=self.Start_Data_Validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact=self.Start_Data_Transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact=self.Start_Model_Trainer(Data_Transformation_artifact=data_transformation_artifact)
            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_dir_to_s3()

            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)


if __name__=="__main__":
    training_pipeline=TrainingPipeline()
    training_pipeline.run_pipeline()
    


    
        
