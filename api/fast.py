from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
    X = lyrics

    # /!\ TODO: get model from GCP

    pipeline = get_model_from_gcp()
    #pipeline = joblib.load('model.joblib')

    # make prediction
    results = pipeline.predict(X)

    # convert response from numpy to python type
    pred = results


    return dict(genre=pred)
