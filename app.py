
import sys
from Network_Security.Constants.Training_Constant import *
from Network_Security.Exception.NS_exception import NetworkSecurityException
from Network_Security.logging.NS_logging import logging
from Network_Security.Components.ML.model.estimator import NetworkModel
from fastapi import FastAPI,File,UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
import pandas as pd
from fastapi.templating import Jinja2Templates
from pandas import DataFrame
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from Network_Security.Utils.Utils import Commonutils
from Network_Security.Entity.Artifact_entity import DataTransformationArtifact
from dotenv import load_dotenv
from Network_Security.Pipeline.TrainingPipeline.training_pipeline import TrainingPipeline

load_dotenv()

templates=Jinja2Templates(directory="./templates")


app=FastAPI()
origins=["*"]

app.add_middleware(
    CORSMiddleware,allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)



@app.get("/",tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


@app.get("/train")
async def train_route():
    try:
        train_pipeline=TrainingPipeline()
        train_pipeline.run_pipeline()

        return Response("Training is Successfull..")
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
@app.get("/predict")
async def predict_route(request:Request,file:UploadFile=File(...)):
    try:
        df=pd.read_csv(file.file)

        preprocessor=Commonutils.load_object(Filepath=DataTransformationArtifact.Preprocessor_Path)
        final_model=Commonutils.load_object(Filepath=Final_Model_path)

        network_model=NetworkModel(preprocessor=preprocessor,model=final_model)

        y_pred=network_model.predict(df)

        df['predicted_column']=y_pred

        table_html=df.to_html(classes='table table-stripped')

        return templates.TemplateResponse("table.html",{"rqeuest":request,"table":table_html})

    except Exception as e:
        raise NetworkSecurityException(e,sys)


    

if __name__=="__main__":
    app_run(app,host="0.0.0.0",port=8000)