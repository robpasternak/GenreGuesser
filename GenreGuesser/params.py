### DATA & MODEL LOCATIONS  - - - - - - - - - - - - - - - - - - -

PATH_TO_LOCAL_MODEL = 'model.joblib'
STORAGE_LOCATION = 'models/models/model.joblib'

### GCP Storage - - - - - - - - - - - - - - - - - - - - - -

BUCKET_NAME = 'lewagon-815-genre-guesser'

##### Data  - - - - - - - - - - - - - - - - - - - - - - - -

# train data file location
# /!\ here you need to decide if you are going to train using the provided and uploaded data/train_1k.csv sample file
# or if you want to use the full dataset (you need need to upload it first of course)
BUCKET_TRAIN_DATA_PATH = 'data/data_mini.csv'

##### Model - - - - - - - - - - - - - - - - - - - - - - - -

# model folder name (will contain the folders for all trained model versions)
MODEL_NAME = 'model'

# model version folder name (where the trained model.joblib file will be stored)
MODEL_VERSION = 'v1'
