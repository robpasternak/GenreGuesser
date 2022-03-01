# HERE ARE THE FILLER NAMES I'M USING UNTIL I KNOW WHAT THEY'RE CALLED:
# PIPELINE: from GenreGuesser.ML_PIPELINE import PIPELINE

import pandas as pd
import re
import joblib
from GenreGuesser.text_preproc import clean_text
from GenreGuesser.data_cleaning import clean_data
#from GenreGuesser.pipeline import pipe


from sklearn.pipeline import make_pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import TfidfVectorizer


def data_prep_combined(X, y):
    GENRE_DICT = {
            '100' : 'rap',
            '73' : 'pop',
            '38' : 'country',
            '114' : 'rock',
            '57' : 'folk',
            '62' : 'jazz'
            }
    y_out = y.apply(lambda x : GENRE_DICT[x] if x in GENRE_DICT.keys() else x)
    X_out = X.apply(clean_text)
    return X_out, y_out

if __name__ == '__main__':
    data = pd.read_csv('raw_data/data_mini.csv')
    print(data['Genre'].unique())
    data = clean_data(data)
    X = data['Lyrics']
    y = data['Genre']
    X_final, y_final = data_prep_combined(X, y)
    pipe = make_pipeline(TfidfVectorizer(), KNeighborsClassifier())
    pipe.fit(X_final, y_final)
    vecto = TfidfVectorizer()
    X_tests = pd.DataFrame(data = vecto.fit_transform(X_final).toarray())
    joblib.dump(pipe, 'model.joblib')
