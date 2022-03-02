import os

from google.cloud import storage
from termcolor import colored

from GenreGuesser.params import BUCKET_NAME, BUCKET_TRAIN_DATA_PATH, MODEL_NAME, MODEL_VERSION, STORAGE_LOCATION

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

def get_model_from_gcp():
    client = storage.Client().bucket(BUCKET_NAME)
    model_name = 'model.joblib'
    blob = client.blob(STORAGE_LOCATION)
    blob.download_to_filename('model.joblib')
