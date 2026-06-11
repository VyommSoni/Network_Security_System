import os
import sys
import yaml
import numpy as np
import pickle
from Network_Security.Exception.NS_exception import NetworkSecurityException
from Network_Security.logging.NS_logging import logging


class Commonutils:

    def __init__(self):
        pass
    
    @staticmethod
    def read_yamlfile(Filepath:str)->dict:
        """
        This function will read the yml file """

        try:
            with open(Filepath,"r") as file:
                content=yaml.safe_load(file)
                return content
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def save_object(filepath:str,obj:object):
        """
        This will save the model in the filepath location"""

        try:
            with open(filepath,'wb') as file:
                content=pickle.dump(obj,file)
                return content
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    @staticmethod
    def load_object(Filepath:str):
        """This fucntion will load the model"""

        try:
            with open(Filepath,"rb") as file:
               content= pickle.load(file)
               return content
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def write_yaml_file(file_path: str, content: dict, replace: bool = False) -> None:
       """
      Write dictionary content to a YAML file.
       """
       try:
         mode = "w" if replace else "a"

         with open(file_path,mode) as file:
             content=yaml.dump(content,file,default_flow_style=False)
             return content
         
       except Exception as e:
         raise NetworkSecurityException(e,sys)
       
    def save_numpy_array(array:np.array,filepath:str):
        """
        This function will save the array into the filepath location"""
        try:
            with open(filepath,"w") as file:
                return np.save(file,array)
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def load_numpy_array(self,filepath:str):
        """This function will load the numpy array from the given file location"""
        try:
            with open(filepath,"r") as file:
                return np.load(file)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
