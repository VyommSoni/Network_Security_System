import os
import sys
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
import mlflow
from sklearn.tree import DecisionTreeClassifier
from Network_Security.Exception.NS_exception import NetworkSecurityException
from Network_Security.logging.NS_logging import logging
from Network_Security.Entity.Artifact_entity import ModelTrainerArtifact,DataTransformationArtifact,ClassificationMetricArtifact
from Network_Security.Entity.Config_entity import ModelTrainerConfig
from Network_Security.Utils.Utils import Commonutils
from sklearn.metrics import accuracy_score
from Network_Security.Components.ML.model.estimator import NetworkModel
from Network_Security.Components.ML.Metric.classification_metric import Metric
import pandas as pd
import numpy as np
from Network_Security.Constants.Training_Constant import *
from sklearn.model_selection import GridSearchCV
from pandas import DataFrame
import dagshub



dagshub.init(repo_owner='svyom21', repo_name='Network_Security_System', mlflow=True)


class ModelTrainer:
    def __init__(self,data_transformation_artifact:DataTransformationArtifact,model_trainer_config:ModelTrainerConfig):
        self.data_transformation_artifact=data_transformation_artifact
        self.model_trainer_config=model_trainer_config
        self.utils=Commonutils()
        self.models={
         "RandomForest": RandomForestClassifier(),
          "knn": KNeighborsClassifier(),
          "decision_tree": DecisionTreeClassifier(),
          "logistic_regression": LogisticRegression()
             }

    def evaluate_models(self,
                        X_train,
                        X_test,
                        y_train,
                        y_test,
                        models):
        try:
             report = {}

             for i in range(len(list(models))):
                model = list(models.values())[i]

                model.fit(X_train, y_train)  # Train model

                y_test_pred = model.predict(X_test)
                y_train_pred=model.predict(X_train)

                test_model_score = accuracy_score(y_test, y_test_pred)

                report[list(models.keys())[i]] = test_model_score

             return report,y_test_pred,y_train_pred

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def get_best_model(self,
                       x_train: np.array,
                       y_train: np.array,
                       x_test: np.array,
                       y_test: np.array):
        try:

            model_report,y_test_pred,y_train_pred= self.evaluate_models(
                X_train=x_train,
                y_train=y_train,
                X_test=x_test,
                y_test=y_test,
                models=self.models
            )

            print(model_report)

            best_model_score = max(sorted(model_report.values()))

            ## To get best model name from dict

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model_object = self.models[best_model_name]

            return best_model_name, best_model_object, best_model_score,y_test_pred,y_train_pred
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def Track_Mlflow(self,best_model,classification_metric:ClassificationMetricArtifact):
        """This function will be use for the tracking of  multiple experiment that we will perform.."""

        try:
            with mlflow.start_run():
                f1_score=classification_metric.f1score
                precision_score=classification_metric.precision_score
                recall_score=classification_metric.recall_score

                mlflow.log_metric("f1_score",f1_score)
                mlflow.log_metric("precision_score",precision_score)
                mlflow.log_metric("recall_score",recall_score)

                mlflow.sklearn.log_model(best_model,"Model")

        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def finetune_best_model(self,
                            best_model_object: object,
                            best_model_name,
                            X_train,
                            y_train,
                            ) -> object:

        try:

            model_param_grid = self.utils.read_yamlfile(Filepath=PARAMS_FILEPATH)["model_selection"]["model"][
                    best_model_name]["search_param_grid"]


            grid_search = GridSearchCV(
                best_model_object, param_grid=model_param_grid, cv=5, n_jobs=1, verbose=1)

            grid_search.fit(X_train, y_train)

            best_params = grid_search.best_params_

            print("best params are:", best_params)

            finetuned_model = best_model_object.set_params(**best_params)

            return finetuned_model
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_model_trainer(self)->ModelTrainerArtifact:
        """This function will start the model training process"""

        try:
           logging.info("Starting the model training process...")
           train_arr=self.utils.load_numpy_array(filepath=self.data_transformation_artifact.transformed_trainfilepath)
           test_arr=self.utils.load_numpy_array(filepath=self.data_transformation_artifact.transformed_testfilepath)

           X_train,Y_train,X_test,Y_test=train_arr[:,:-1],train_arr[:,-1],test_arr[:,:-1],test_arr[:,-1]

           #train model

           best_modelname,best_modelobject, bestmodel_score,y_test_pred,y_train_pred=self.get_best_model(x_train=X_train,y_train=Y_train,x_test=X_test,y_test=Y_test)
           logging.info(
               "Got best_model_name,best_model_object and best_model_score"
           )

           if bestmodel_score>EXPECTED_ACCURACY:
                #finetune the best model
                finedtuned_model=self.finetune_best_model(best_model_object=best_modelobject,best_model_name=best_modelname,X_train=X_train,y_train=Y_train)

                logging.info(" Sucessfully Finetunned best model")

                train_metric_artifact=Metric.get_classification_metric(y_pred=Y_train,y_true=y_train_pred)

                logging.info("Train metric artifact , Experiment Tracking with Mlflow..")
                self.Track_Mlflow(best_model=best_modelname,classification_metric=train_metric_artifact)


                #load the preprocessor
                Preprocessor=self.utils.load_object(Filepath=self.data_transformation_artifact.Preprocessor_Path)

                #wrap up the model
                best_model=NetworkModel(preprocessor=Preprocessor,model=finedtuned_model)

                os.makedirs(os.path.dirname(self.model_trainer_config.model_path),exist_ok=True)

                self.utils.save_object(filepath=self.model_trainer_config.model_path,obj=best_model)

                self.utils.save_object(filepath=Final_Model_path,obj=best_model)

                model_trainer_artifact=ModelTrainerArtifact(
                    Model_Trained_path=self.model_trainer_config.model_path,
                    test_metric_artifact=Metric.get_classification_metric(y_pred=Y_test,y_true=y_test_pred),
                    train_metric_artifact=Metric.get_classification_metric(y_pred=Y_train,y_true=y_train_pred)
                )

                return model_trainer_artifact
           
           logging.info(
               f"Model Accuracy is less than expected accuracy , best_model_score {bestmodel_score}"
               )
           
        except Exception as e:
            raise NetworkSecurityException(e,sys)

