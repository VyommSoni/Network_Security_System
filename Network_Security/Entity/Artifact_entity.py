import os
from dataclasses import dataclass
import json


@dataclass
class DataIngestionArtifact:
    train_file_path:str
    test_file_path:str
    feature_storepath:str

@dataclass
class DataValidationArtifact:
    Validation_status:bool
    drift_file_report:str
    valid_train_filepath:str
    invalid_train_filepath:str
    valid_test_filepath:str
    invalid_test_filepath:str
    
@dataclass
class DataTransformationArtifact:
    Preprocessor_Path:str
    transformed_trainfilepath:str
    transformed_testfilepath:str

@dataclass
class ClassificationMetricArtifact:
    f1score:float
    precision_score:float
    recall_score:float
@dataclass
class ModelTrainerArtifact:
    Model_Trained_path:str
    train_metric_artifact:ClassificationMetricArtifact
    test_metric_artifact:ClassificationMetricArtifact

