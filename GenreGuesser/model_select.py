from sklearn.model_selection import cross_validate
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score

def gg_cross_val(pipeline, X, y):
    '''
    Performs 5-fold cross-validation, prints the mean accuracy and mean
    fit time, and returns both.
    '''
    cv_result = cross_validate(pipeline, X, y, cv = 5, scoring = 'accuracy')
    mean_test_score = cv_result['test_score'].mean()
    mean_fit_time = cv_result['fit_time'].mean()
    print('5-FOLD CROSS-VALIDATION RESULTS:')
    print(f'Mean Accuracy: {mean_test_score * 100}%')
    print(f'Mean Fit Time: {round(mean_fit_time, 3)}s')
    return mean_test_score, mean_fit_time


def gg_single_split_test(pipeline, X, y):
    '''
    Performs a test with a single 70-30 split and prints the accuracy.
    '''
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .3)
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_pred)
    print('70-30 TRAIN-TEST SPLIT')
    print(f'Accuracy: {test_accuracy * 100}%')
    return test_accuracy


def gg_grid_search(pipeline, X, y):
    '''
    Performs a grid search with every possible number of neighbors from
    3 to 7 (inclusive), and with both uniform and distance-based weighting.
    TAKES A WHILE!
    '''
    n_neighbors_values = list(range(3,8))
    weights_values = ['uniform', 'distance']
    param_grid = {
        'knn__n_neighbors' : n_neighbors_values,
        'knn__weights' : weights_values
    }
    grid = GridSearchCV(estimator = pipeline,
                        scoring = 'accuracy',
                        param_grid = param_grid,
                        n_jobs = -1,
                        cv = 5)
    grid.fit(X,y)
    best_vals = grid.best_params_
    best_n_neighbors = best_vals['knn__n_neighbors']
    best_weights = best_vals['knn__weights']
    best_score = grid.best_score_
    print(f"Best number of neighbors: {best_n_neighbors}")
    print(f"Best weights (uniform or distance): {best_weights}")
    print(f"Best accuracy: {best_score * 100}%")
    return best_n_neighbors, best_weights, best_score
