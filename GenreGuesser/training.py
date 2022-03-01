# HERE ARE THE FILLER NAMES I'M USING UNTIL I KNOW WHAT THEY'RE CALLED:
# PIPELINE: from GenreGuesser.ML_PIPELINE import PIPELINE

import pandas as pd
import joblib
from GenreGuesser.text_preproc import clean_text
from GenreGuesser.data_cleaning import clean_data
from GenreGuesser.model_select import gg_cross_val
from GenreGuesser.pipeline import pipe



def data_prep_combined(data):
    GENRE_DICT = {
        '100' : 'rap',
        '73' : 'pop',
        '38' : 'country',
        '114' : 'rock',
        '57' : 'folk',
        '62' : 'jazz'
        }
    data_cleaned = clean_data(data)
    X_prelim = data_cleaned['Lyrics']
    y_prelim = data_cleaned['Genre']
    y_out = y_prelim.apply(lambda x : GENRE_DICT[x] if x in GENRE_DICT.keys() else x)
    X_out = X_prelim.apply(clean_text)
    return X_out, y_out

if __name__ == '__main__':
    data = pd.read_csv('raw_data/data_mini.csv')
    X = data['Lyrics']
    y = data['Genre']
    X, y = data_prep_combined(data)
    cv_result = gg_cross_val(pipe, X, y)
    pipe.fit(X, y)
    joblib.dump(pipe, 'model.joblib')
