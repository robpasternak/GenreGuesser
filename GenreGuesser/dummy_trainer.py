from cgitb import text
from google.cloud import storage
import numpy as np
import joblib
from GenreGuesser.text_preproc import clean_text

import pandas as pd
import string
string.punctuation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

from GenreGuesser.params import BUCKET_NAME, BUCKET_TRAIN_DATA_PATH, MODEL_NAME, MODEL_VERSION, STORAGE_LOCATION


def get_data():
    """method to get the training data (or a portion of it) from google cloud bucket"""
    data = pd.read_csv(f"gs://{BUCKET_NAME}/{BUCKET_TRAIN_DATA_PATH}", nrows=1000, dtype = 'string')
    return data

def preprocess(data):
    text = data['Songs'].apply(clean_text)
    return text

def train_model(text):
    vectorizer = TfidfVectorizer().fit(text)
    data_vectorized = vectorizer.transform(text)

    lda_model = LatentDirichletAllocation(n_components=2).fit(data_vectorized)

    def print_topics(mdl, vct):
        for idx, topic in enumerate(mdl.components_):
            print("Topic %d:" % (idx))
            print([(vct.get_feature_names_out()[i], topic[i])
                        for i in topic.argsort()[:-10 - 1:-1]])


    print_topics(lda_model, vectorizer)
    return lda_model


def upload_model_to_gcp():


    client = storage.Client()

    bucket = client.bucket(BUCKET_NAME)

    blob = bucket.blob(STORAGE_LOCATION)

    blob.upload_from_filename('model.joblib')


def save_model(lda_model):
    """method that saves the model into a .joblib file and uploads it on Google Storage /models folder
    HINTS : use joblib library and google-cloud-storage"""

    # saving the trained model to disk is mandatory to then beeing able to upload it to storage
    # Implement here
    joblib.dump(lda_model, 'model.joblib')
    print("saved model.joblib locally")

    # Implement here
    upload_model_to_gcp()
    print(f"uploaded model.joblib to gcp cloud storage under \n => {STORAGE_LOCATION}")


# if __name__ == '__main__':
#     # get training data from GCP bucket
#     data = get_data()

#     # preprocess data
#     text = preprocess(data)

#     # train model (locally if this file was called through the run_locally command
#     # or on GCP if it was called through the gcp_submit_training, in which case
#     # this package is uploaded to GCP before being executed)
#     lda_model = train_model(text)

#     # save trained model to GCP bucket (whether the training occured locally or on GCP)
#     save_model(lda_model)
