# HERE ARE THE FILLER NAMES I'M USING UNTIL I KNOW WHAT THEY'RE CALLED:
# PIPELINE: from GenreGuesser.ML_PIPELINE import PIPELINE

import pandas as pd
import joblib
from GenreGuesser.text_preproc import clean_text
from GenreGuesser.data_cleaning import clean_data
from GenreGuesser.ML_PIPELINE import PIPELINE


from sklearn.pipeline import Pipeline
from sklearn.pipeline import make_pipeline
from sklearn.neighbors import KNeighborsClassifier

GENRE_DICT = {
        '100' : 'rap',
        '73' : 'pop',
        '38' : 'country',
        '114' : 'rock',
        '57' : 'folk',
        '62' : 'jazz'
        }

if __name__ == '__main__':
    data = pd.read_csv('raw_data/data.csv')
    data = clean_data(data)
    X = data[['Lyrics']]
    y = data['Genre']
    y_final = y.apply(lambda x : GENRE_DICT(x) if x in GENRE_DICT.keys() else x)
    X_final = X.apply(clean_text)
    PIPELINE = make_pipeline(KNeighborsClassifier())
    PIPELINE.fit(X_final, y_final)
    joblib.dump(PIPELINE, 'model.joblib')
