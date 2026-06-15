from datetime import datetime
import os
from Network_Security.Constants.Training_Constant import *
import json

class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp=timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name=PIPELINE_NAME
        self.artifacts=ARTIFACT_DIR
        self.artifacts_dir=os.path.join(self.artifacts,timestamp)
        self.timestamp=timestamp

class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_ingestion_dir:str=os.path.join(training_pipeline_config.artifacts_dir,DATA_INGESTION_DIR_NAME)
        self.ingested_data_dir:str=os.path.join(self.data_ingestion_dir,DATA_INGESTION_INGESTED_DIR)
        self.feature_store_filepath:str=os.path.join(self.ingested_data_dir,DATA_INGESTION_FEATURE_STORE_PATH)
        self.split_ratio:float=DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.train_file_path:str =os.path.join(self.ingested_data_dir,TRAIN_FILENAME)
        self.test_file_path:str=os.path.join(self.ingested_data_dir,TEST_FILENAME)

class DataValidationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir:str=os.path.join(training_pipeline_config.artifacts_dir,DATA_VALIDATION_DIR)
        self.valid_data_dir:str=os.path.join(self.data_validation_dir,VALID_DIR)
        self.invalid_data_dir:str=os.path.join(self.data_validation_dir,INVALID_DIR)
        self.valid_train_file_path:str=os.path.join(self.valid_data_dir,VALID_TRAIN_FILE_PATH)
        self.invalid_train_file_path:str=os.path.join(self.invalid_data_dir,INVALID_TRAIN_FILE_PATH)
        self.valid_test_file_path:str=os.path.join(self.valid_data_dir,VALID_TEST_FILE_PATH)
        self.invalid_test_file_path:str=os.path.join(self.invalid_data_dir,INVALID_TEST_FILE_PATH)
        self.data_drift_report_file_path:str =os.path.join(self.data_validation_dir,DATA_DRIFT_REPORT_DIR,DATA_DRIFT_REPORT_FILE_NAME)

class DataTransformationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_dir:str=os.path.join(training_pipeline_config.artifacts_dir,DATA_TRANSFORMATION_DIR)
        self.transformed_trainfilepath:str=os.path.join(self.data_transformation_dir,TRANSFORMED_DIR,TRAIN_ARRAY)
        self.transformed_testfilepath:str=os.path.join(self.data_transformation_dir,TRANSFORMED_DIR,TEST_ARRAY)
        self.transformed_object_path:str=os.path.join(self.data_transformation_dir,TRANSFORMED_OBJECT,PREPROCESSOR_PATH)
    
class ModelTrainerConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.model_trainer_dir:str=os.path.join(training_pipeline_config.artifacts_dir,MODEL_TRAINER_DIR)
        self.trained_model_dir:str=os.path.join(self.model_trainer_dir,TRAINED_MODEL_DIR)
        self.model_path:str=os.path.join(self.trained_model_dir,MODEL_FILE_NAME)
        self.expected_accuracy:float=EXPECTED_ACCURACY
        self.threshold:float=THRESHOLD




