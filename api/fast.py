import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from GenreGuesser.gcp import get_model_from_gcp
import joblib


app = FastAPI()

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
@app.get("/predict")
def predict(lyrics): #input is a string

    #input lyrics are X for prediction
    X_pred = pd.Series([lyrics])

    #get model from GCP
    #pipeline = get_model_from_gcp()

    #get model locally
    pipeline = joblib.load('rob_model.joblib')

    # make prediction
    results = pipeline.predict(X_pred)

    # convert response here?
    pred = results[0]


    return {
        'genre' : pred
    }
