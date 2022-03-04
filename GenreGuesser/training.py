# HERE ARE THE FILLER NAMES I'M USING UNTIL I KNOW WHAT THEY'RE CALLED:
# PIPELINE: from GenreGuesser.ML_PIPELINE import PIPELINE

import pandas as pd
import joblib
from GenreGuesser.data_cleaning import clean_data
from GenreGuesser.model_select import gg_cross_val
from GenreGuesser.model_select import gg_single_split_test
from GenreGuesser.model_select import gg_grid_search
from GenreGuesser.pipeline import pipe
from GenreGuesser.svm_pipeline import svm_pipe
from GenreGuesser.params import GENRE_DICT, MODEL_DICT, DATA_SOURCE
import sys

if __name__ == '__main__':
    sys_args = sys.argv[1:]

    # Read in the data
    data = pd.read_csv(DATA_SOURCE)

    # Set the X and y values accordingly.
    # X values are just strings of lyrics (will be vectorized in pipeline),
    # y values are strings indicating a genre.
    X = data['Lyrics']
    y = data['Genre'].apply(lambda x : GENRE_DICT[x] if x in GENRE_DICT.keys() else x)

    # Uncomment the following line to see how many songs from each genre in the data set
    #print(y.value_counts())

    if sys_args[0] == 'localfit':
        for sys_arg in sys_args[1:]:
            MODEL_DICT[sys_arg][0].set_params(verbose = True)
            MODEL_DICT[sys_arg][0].fit(X,y)
            joblib.dump(MODEL_DICT[sys_arg][0], f"{sys_arg}_model.joblib")
            print(f"{MODEL_DICT[sys_arg][1]} model fitted and saved as {sys_arg}_model.joblib")

    if sys_args[0] == 'cross_val':
        for sys_arg in sys_args[1:]:
            cv_result = gg_cross_val(MODEL_DICT[sys_arg][0], X, y, MODEL_DICT[sys_arg][1])

    if sys_args[0] == 'one_split':
        for sys_arg in sys_args[1:]:
            cv_result = gg_single_split_test(MODEL_DICT[sys_arg][0], X, y, MODEL_DICT[sys_arg][1])

    if sys_args[0] == 'grid_search':
        for sys_arg in sys_args[1:]:
            gg_grid_search(MODEL_DICT[sys_arg][0], X, y, sys_arg, MODEL_DICT[sys_arg][1])
