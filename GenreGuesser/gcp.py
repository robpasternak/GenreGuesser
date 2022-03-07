import os
from google.oauth2 import service_account
from google.cloud import storage
from termcolor import colored
import joblib
from GenreGuesser.params import BUCKET_NAME, STORAGE_LOCATION
#from dotenv import load_dotenv, find_dotenv

#load_dotenv(find_dotenv())

#credentials = os.getenv('GCP_APPLICATION_CREDENTIALS')
credentials = service_account.Credentials.from_service_account_file('/credentials.json')
def storage_upload(model_filename, rm=False):
    client = storage.Client(credentials=credentials).bucket(BUCKET_NAME)

    storage_location = f"{STORAGE_LOCATION}{model_filename}"
    blob = client.blob(storage_location)
    blob.upload_from_filename(model_filename)
    print(colored(f"=> {model_filename} uploaded to bucket {BUCKET_NAME} inside {storage_location}",
                  "green"))

def get_model_from_gcp(model_filename):

    client = storage.Client(credentials=credentials).bucket(BUCKET_NAME)
    blob = client.blob(f"{STORAGE_LOCATION}{model_filename}")
    blob.download_to_filename(model_filename)
    pipeline = joblib.load(model_filename)
    return pipeline

def upload_model_to_gcp(model_filename):

    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(STORAGE_LOCATION)
    blob.upload_from_filename(model_filename)


def save_model(model, model_name):
    """method that saves the model into a .joblib file and uploads it on Google Storage /models folder"""

    # saving the trained model to disk is mandatory to then beeing able to upload it to storage
    # Implement here
    joblib.dump(model, f'{model_name}.joblib')
    print(f"saved {model_name}.joblib locally")

    # Implement here
    upload_model_to_gcp(f'{model_name}.joblib')
    print(f"uploaded {model_name}.joblib to gcp cloud storage under \n => {STORAGE_LOCATION}")
