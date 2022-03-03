import os
from google.cloud import storage
from termcolor import colored
import joblib
from params import BUCKET_NAME, BUCKET_TRAIN_DATA_PATH, MODEL_NAME, MODEL_VERSION, STORAGE_LOCATION

def storage_upload(rm=False):
    client = storage.Client().bucket(BUCKET_NAME)

    local_model_name = 'model.joblib'
    storage_location = f"models/{MODEL_NAME}/{MODEL_VERSION}/{local_model_name}"
    blob = client.blob(storage_location)
    blob.upload_from_filename('model.joblib')
    print(colored(f"=> model.joblib uploaded to bucket {BUCKET_NAME} inside {storage_location}",
                  "green"))
    if rm:
        os.remove('model.joblib')

def get_model_from_gcp(model_name):
    client = storage.Client().bucket(BUCKET_NAME)
    model_name = 'model.joblib'
    blob = client.blob(STORAGE_LOCATION)
    blob.download_to_filename('model.joblib')


def upload_model_to_gcp():

    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(STORAGE_LOCATION)
    blob.upload_from_filename('model.joblib')


def save_model(model, model_name):
    """method that saves the model into a .joblib file and uploads it on Google Storage /models folder"""

    # saving the trained model to disk is mandatory to then beeing able to upload it to storage
    # Implement here
    joblib.dump(model, f'{model_name}.joblib')
    print(f"saved {model_name}.joblib locally")

    # Implement here
    upload_model_to_gcp()
    print(f"uploaded {model_name}.joblib to gcp cloud storage under \n => {STORAGE_LOCATION}")
