import os
import sys
import numpy as np
import pandas as pd

"""
Defining common constant variable for training pipeline"""


TARGET_COLUMN="Result"
PIPELINE_NAME="NetworkSecurity"
ARTIFACT_DIR="Artifacts"
Final_Model_path="Final_model/model.pkl"
FINAL_MODEL_DIR="FINAL_MODEL"
FILENAME='phising.csv'

TRAINING_BUCKET_NAME="networksecurityvyomm"
TRAIN_FILENAME="train.csv"
TEST_FILENAME="test.csv"
SCHEMA_FILEPATH=os.path.join("Config","Schema.yml")
PARAMS_FILEPATH=os.path.join("Config","params.yml")


"""
Data Ingestion related constant
"""

DATA_INGESTION_COLLECTION_NAME:str ="NewtorkSecurityData"
DATA_INGESTION_DATABASE_NAME:str="NetworkSecurity"
DATA_INGESTION_DIR_NAME:str="DataIngestion"
DATA_INGESTION_FEATURE_STORE_PATH:str="FeatureStore"
DATA_INGESTION_INGESTED_DIR:str="Ingested_Dir"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float=0.2


"""
Data Validation related constant"""
DATA_VALIDATION_DIR:str="DataValidation"
INVALID_DIR:str="INVALID_DATA"
VALID_DIR:str="VALID"
VALID_TRAIN_FILE_PATH:str="Valid_train_file_path"
INVALID_TRAIN_FILE_PATH:str="Invalid_train_file_path"
VALID_TEST_FILE_PATH:str="Valid_test_file_path"
INVALID_TEST_FILE_PATH:str="Invalid_test_file_path"
DATA_DRIFT_REPORT_DIR:str="DRIFT_REPORT"
DATA_DRIFT_REPORT_FILE_NAME:str="Report.yml"


"""
Data Transformation related constant"""

DATA_TRANSFORMATION_DIR:str="DataTransformation"
TRANSFORMED_DIR:str="Transformed_dir"
TRANSFORMED_OBJECT:str="Transformed_Object"
PREPROCESSOR_PATH:str="Preprocessor_Path.pkl"
TRAIN_ARRAY:str="train.npy"
TEST_ARRAY:str="test.npy"

KNN_IMPUTER_PARAMS: dict = {
    "n_neighbors": 3,
    "weights": "uniform",
    "metric": "nan_euclidean"
}

MODEL_TRAINER_DIR:str="Model"
EXPECTED_ACCURACY:float=0.75
TRAINED_MODEL_DIR:str="Trained_model_dir"
THRESHOLD:float=0.05
MODEL_FILE_NAME:str="model.pkl"


