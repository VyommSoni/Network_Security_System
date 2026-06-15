import os
import sys
from Network_Security.Exception.NS_exception import NetworkSecurityException
from Network_Security.logging.NS_logging import logging
from pandas import DataFrame
import pandas as pd
from sklearn.metrics import f1_score,precision_score,recall_score

from Network_Security.Entity.Artifact_entity import ClassificationMetricArtifact


class Metric:

    def get_classification_metric(y_true,y_pred)->ClassificationMetricArtifact:
        """This will calculate Classification metric and return it"""
        try:
            f1_score_=f1_score(y_true,y_pred)
            precision_score_=precision_score(y_true,y_pred)
            recall_score_=recall_score(y_true,y_pred)

            classification_metric=ClassificationMetricArtifact(
                f1score=f1_score_,
                recall_score=recall_score_,
                precision_score=precision_score_
            )

            return classification_metric
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)