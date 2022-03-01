# HERE ARE THE FILLER NAMES I'M USING UNTIL I KNOW WHAT THEY'RE CALLED:
# PIPELINE: from GenreGuesser.ML_PIPELINE import PIPELINE

import pandas as pd
import joblib
from GenreGuesser.data_cleaning import clean_data
from GenreGuesser.model_select import gg_cross_val
from GenreGuesser.model_select import gg_single_split_test
from GenreGuesser.model_select import gg_grid_search
from GenreGuesser.pipeline import pipe

GENRE_DICT = {
    '100' : 'rap',
    '73' : 'pop',
    '38' : 'country',
    '114' : 'rock',
    '57' : 'folk',
    '62' : 'jazz'
    }

if __name__ == '__main__':
    data = pd.read_csv('raw_data/data_mini.csv')
    data = clean_data(data)
    X = data['Lyrics']
    y = data['Genre'].apply(lambda x : GENRE_DICT[x] if x in GENRE_DICT.keys() else x)

    # Uncomment the following line to test with a single 70-30 split:
    #gg_single_split_test(pipe, X, y)

    # Uncomment the following line to test with 5-fold cross-validation:
    #cv_result = gg_cross_val(pipe, X, y)

    # Uncomment the following line to perform a grid search (TAKES A WHILE!):
    #gg_grid_search(pipe, X, y)

    pipe.fit(X, y)
    joblib.dump(pipe, 'model.joblib')
    print('Model fitted and saved as model.joblib')
