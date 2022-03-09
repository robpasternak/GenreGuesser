# HERE ARE THE FILLER NAMES I'M USING UNTIL I KNOW WHAT THEY'RE CALLED:
# PIPELINE: from GenreGuesser.ML_PIPELINE import PIPELINE

import pandas as pd
import joblib
from GenreGuesser.model_select import gg_cross_val
from GenreGuesser.model_select import gg_single_split_test
from GenreGuesser.model_select import gg_grid_search
from GenreGuesser.model_select import train_test_split
from GenreGuesser.pipeline import get_knn_pipe
from GenreGuesser.svm_pipeline import get_svm_pipe
from sklearn.metrics import accuracy_score
from GenreGuesser.params import GENRE_DICT, DATA_SOURCE
from imblearn.under_sampling import RandomUnderSampler
import sys

# Dictionary for command line reference to models
MODEL_DICT = {
    'knn' : (get_knn_pipe(), 'KNeighbors'),
    'svm' : (get_svm_pipe(), 'SVM'),
}

if __name__ == '__main__':
    sys_args = sys.argv[1:]

    # Read in the data, clean it, and restrict to the right genres
    data = pd.read_csv(DATA_SOURCE)
    data['Genre'] = data['Genre'].apply(lambda x : GENRE_DICT[x] if x in GENRE_DICT.keys() else x)
    data = data.dropna()
    data = data[data['Genre'].isin(['rap', 'country', 'rock', 'pop'])]

    # Set the X and y values accordingly.
    # X values are just strings of lyrics (will be vectorized in pipeline),
    # y values are strings indicating a genre.
    X = data[['Lyrics']]
    y = data['Genre']

    # Uncomment the following lines to undersample pop, rock, and country to 1800
    rus = RandomUnderSampler(sampling_strategy = {'pop' : 1800, 'country' : 1800, 'rock' : 1800})
    X, y = rus.fit_resample(X,y)
    X = X['Lyrics']

    # Split 90-10 into training/validation and test data (reliably with a fixed random state)
    X_tv, X_test, y_tv, y_test = train_test_split(X, y, test_size = .15, random_state = 42)

    # Uncomment the following line to see how many songs from each genre are in the data set
    #print(y.value_counts())

    # Uncomment the following line to see the proportion of songs from each genre in the
    # data set
    #print(y.value_counts(normalize = True))

    if sys_args[0] == 'localfit':
        '''Locally fits the designated model(s)'''
        for sys_arg in sys_args[1:]:
            model_used = MODEL_DICT[sys_arg][0]
            model_used.set_params(verbose = True)
            model_used.fit(X_tv,y_tv)
            joblib.dump(model_used, f"{sys_arg}.joblib")
            print(f"{MODEL_DICT[sys_arg][1]} model fitted and saved as {sys_arg}.joblib")
            test_response = input('Would you like to test the model on the test data? (Y/n)\n')
            if test_response in ['y', 'Y', '']:
                y_pred = model_used.predict(y_test)
                test_accuracy = accuracy_score(y_test, y_pred)
                print(f'Accuracy: {round(test_accuracy * 100, 2)}%')



    if sys_args[0] == 'finalfit':
        '''Locally fits the designated model(s)'''
        final_model = sys_args[1]
        MODEL_DICT[final_model][0].set_params(verbose = True)
        MODEL_DICT[final_model][0].fit(X,y)
        joblib.dump(MODEL_DICT[final_model][0], "model.joblib")
        print(f"Final, {MODEL_DICT[final_model][1]} model fitted and saved as model.joblib")

    if sys_args[0] == 'cross_val':
        '''Performs a local 5-fold cross-validation for the designated model(s)'''
        for sys_arg in sys_args[1:]:
            model_used = MODEL_DICT[sys_arg][0]
            cv_result = gg_cross_val(model_used, X_tv, y_tv, MODEL_DICT[sys_arg][1])

    if sys_args[0] == 'one_split':
        '''Performs a one-shot 70-30 test for the designated model(s)'''
        for sys_arg in sys_args[1:]:
            model_used = MODEL_DICT[sys_arg][0]
            cv_result = gg_single_split_test(model_used, X_tv, y_tv, MODEL_DICT[sys_arg][1])

    if sys_args[0] == 'grid_search':
        '''Performs a grid search for the designated model(s)'''
        for sys_arg in sys_args[1:]:
            model_used = MODEL_DICT[sys_arg][0]
            gg_grid_search(MODEL_DICT[sys_arg][0], X_tv, y_tv, sys_arg, MODEL_DICT[sys_arg][1])
