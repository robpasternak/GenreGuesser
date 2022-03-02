# HERE ARE THE FILLER NAMES I'M USING UNTIL I KNOW WHAT THEY'RE CALLED:
# PIPELINE: from GenreGuesser.ML_PIPELINE import PIPELINE

import pandas as pd
import joblib
from GenreGuesser.data_cleaning import clean_data
from GenreGuesser.model_select import gg_cross_val
from GenreGuesser.model_select import gg_single_split_test
from GenreGuesser.model_select import gg_grid_search
from GenreGuesser.pipeline import pipe

# Dictionary for translating from MusicBrainz genre code to English
GENRE_DICT = {
    '100' : 'rap',
    '73' : 'pop',
    '38' : 'country',
    '114' : 'rock',
    '57' : 'folk',
    '62' : 'jazz'
    }

# Change the following line when we get the full data:
DATA_SOURCE = 'raw_data/data_mini.csv'

if __name__ == '__main__':
    # Read in the data
    data = pd.read_csv(DATA_SOURCE)

    # Remove duplicates, remixes, etc.
    data = clean_data(data)

    # Set the X and y values accordingly.
    # X values are just strings of lyrics (will be vectorized in pipeline),
    # y values are strings indicating a genre.
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
