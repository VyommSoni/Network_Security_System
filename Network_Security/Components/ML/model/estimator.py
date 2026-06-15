import os
import sys
from Network_Security.Exception.NS_exception import NetworkSecurityException
from Network_Security.logging.NS_logging import logging
from pandas import DataFrame
import pandas as pd
from Network_Security.Constants.Training_Constant import *
from sklearn.pipeline import Pipeline
"""
This is basically a wrapper class, we are going to use it as a wrapper """

class NetworkModel:
    def __init__(self,preprocessor:Pipeline,model):
        self.preprocessor=preprocessor
        self.model=model

    def predict(self,X):
        """This function will use for prediction"""
        try:
            transform_x=self.preprocessor.transform(X)
            predict=self.model.predict(transform_x)
            return predict
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    