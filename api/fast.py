import os
from posixpath import dirname
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from GenreGuesser.gcp import get_model_from_gcp
from google.oauth2 import service_account
import os
from os.path import join
from google.cloud import storage
#from dotenv import load_dotenv, find_dotenv


app = FastAPI()

#env_path = join(dirname(dirname(__file__)),'.env') # ../.env
#env_path = find_dotenv()

#load_dotenv(find_dotenv())

credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

#client = storage.Client(credentials=GOOGLE_APPLICATION_CREDENTIALS)


#add middleware for frontend (Java) to communicate with backend (Python)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


#add endpoint at root
@app.get("/")
def index():
    return {"greeting": "Hello world"}

#add endpoint at /predict
@app.get("/predict_knn")
def predict_knn(lyrics): #input is a string
    #input lyrics are X for prediction
    X_pred = pd.Series([lyrics])
    #get model from GCP
    pipeline = get_model_from_gcp("knn.joblib")
    # make prediction
    results = pipeline.predict(X_pred)
    pred = results[0]

    return {
        'genre' : pred
    }

#add endpoint at /predict
@app.get("/predict_svm")
def predict_svm(lyrics): #input is a string
    #input lyrics are X for prediction
    X_pred = pd.Series([lyrics])
    #get model from GCP
    pipeline = get_model_from_gcp("svm.joblib")
    # make prediction
    results = pipeline.predict(X_pred)
    pred = results[0]

    return {
        'genre' : pred
    }

#add endpoint at /predict
@app.get("/predict_rfc")
def predict_rfc(lyrics): #input is a string
    #input lyrics are X for prediction
    X_pred = pd.Series([lyrics])
    #get model from GCP
    pipeline = get_model_from_gcp("rfc.joblib")
    # make prediction
    results = pipeline.predict(X_pred)
    pred = results[0]

    return {
        'genre' : pred
    }

@app.get("/testing")
def testing():
    return credentials
