from sklearn.model_selection import cross_validate
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
import numpy as np

SEP_STRING = f'\n{"=" * 30}\n'

def gg_cross_val(pipeline, X, y, name):
    '''
    Performs 5-fold cross-validation, prints the mean accuracy and mean
    fit time, and returns both.
    '''
    cv_result = cross_validate(pipeline,
                               X,
                               y,
                               cv = 5,
                               n_jobs = -1,
                               scoring = 'accuracy',
                               verbose = 2)
    mean_test_score = cv_result['test_score'].mean()
    mean_fit_time = cv_result['fit_time'].mean()
    print(SEP_STRING)
    print(f'5-FOLD CROSS-VALIDATION RESULTS, {name}:')
    print(f'Mean Accuracy: {mean_test_score * 100}%')
    print(f'Mean Fit Time: {round(mean_fit_time, 3)}s')
    return mean_test_score, mean_fit_time


def gg_single_split_test(pipeline, X, y, name):
    '''
    Performs a test with a single 70-30 split and prints the accuracy.
    '''
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .3)
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_pred)
    print(f'70-30 TRAIN-TEST SPLIT, {name}:')
    print(f'Accuracy: {test_accuracy * 100}%')
    return test_accuracy


def gg_grid_search(pipeline, X, y, short_name, long_name):
    '''
    grid search knn:
    Performs a grid search with every possible number of neighbors from
    3 to 7 (inclusive), and with both uniform and distance-based weighting.
    TAKES A WHILE!
    '''
    if short_name == 'knn':
        n_neighbors_values = list(range(3,8))
        weights_values = ['uniform', 'distance']

        param_grid = {
            'knn__n_neighbors' : n_neighbors_values,
            'knn__weights' : weights_values
        }

    '''
    grid search gb:
    Performs a grid search with....
    '''

    if short_name == 'gb':
        n_estimators = [200, 800]
        max_features = ['auto', 'sqrt']
        max_depth = [10, 40]
        max_depth.append(None)
        min_samples_split = [10, 30, 50]
        min_samples_leaf = [1, 2, 4]
        learning_rate = [.1, .5]
        subsample = [.5, 1.]

        param_grid = {
            'n_estimators': n_estimators,
            'max_features': max_features,
            'max_depth': max_depth,
            'min_samples_split': min_samples_split,
            'min_samples_leaf': min_samples_leaf,
            'learning_rate': learning_rate,
            'subsample': subsample
             }

    '''
    grid search svm:
    Performs a grid search with the penalty parameter C, gamma (kernel coefficient), degree (polynomial kernel function), kernel (kernel type in algorithm) with the
    the probability true.
    '''

    if short_name == 'svm':
        C = [.0001, .001, .01]
        gamma = [.0001, .001, .01, .1, 1, 10, 100]
        degree = [1, 2, 3, 4, 5]
        kernel = ['linear', 'rbf', 'poly']
        probability = [True]

        param_grid = {
            'svm_C': C,
            'svm_kernel': kernel,
            'svm_gamma': gamma,
            'svm_degree': degree,
            'svm_probability': probability
             }
    '''
    grid search rfc:
    Performs a grid search with the n_estimators (number of trees), max_features (max number of features considered for splitting a node),
    max_depth (max number of levels in each decision tree), min_samples_split (min number of data points placed in a node before the node is split),
    min_samples_leaf (min number of data points allowed in a leaf node), bootstrap (method for sampling data points)
    '''
    if short_name == 'rfc':
        n_estimators = [int(x) for x in np.linspace(start = 200, stop = 1000, num = 5)]
        max_features = ['auto', 'sqrt']
        max_depth = [int(x) for x in np.linspace(20, 100, num = 5)]
        max_depth.append(None)
        min_samples_split = [2, 5, 10]
        min_samples_leaf = [1, 2, 4]
        bootstrap = [True, False]
        probability = [True]

        param_grid = {
            'n_estimators': n_estimators,
            'max_features': max_features,
            'max_depth': max_depth,
            'min_samples_split': min_samples_split,
            'min_samples_leaf': min_samples_leaf,
            'bootstrap': bootstrap}

    grid = GridSearchCV(estimator = pipeline,
                        scoring = 'accuracy',
                        param_grid = param_grid,
                        n_jobs = -1,
                        cv = 5,
                        verbose = 2)
    grid.fit(X,y)
    best_vals = grid.best_params_

    if short_name == 'knn':
        best_n_neighbors = best_vals['knn__n_neighbors']
        best_weights = best_vals['knn__weights']
        best_score = grid.best_score_
        print(SEP_STRING)
        print(f'GRID SEARCH RESULTS, {long_name}:')
        print(f"Best number of neighbors: {best_n_neighbors}")
        print(f"Best weights (uniform or distance): {best_weights}")
        print(f"Best accuracy: {best_score * 100}%")
        return best_n_neighbors, best_weights, best_score

    if short_name == 'gb':
        best_n_estimators = best_vals['n_estimators']
        best_max_features = best_vals['max_features']
        best_max_depth = best_vals['max_depth']
        best_min_samples_split = best_vals['min_samples_split']
        best_min_samples_leaf = best_vals['min_samples_leaf']
        best_min_learning_rate = best_vals['learning_rate']
        best_min_learning_subsample = best_vals['subsample']
        best_score = grid.best_score_
        print(SEP_STRING)
        print(f'GRID SEARCH RESULTS, {long_name}:')
        print(f"Best n_estimators: {best_n_estimators}")
        print(f"Best max_features: {best_max_features}")
        print(f"Best max_depth: {best_max_depth}")
        print(f"Best min_samples_split: {best_min_samples_split}")
        print(f"Best min_samples_leaf: {best_min_samples_leaf}")
        print(f"Best min_learning_rate: {best_min_learning_rate}")
        print(f"Best min_learning_subsample: {best_min_learning_subsample}")
        print(f"Best accuracy: {best_score * 100}%")
        return best_n_estimators, best_max_features, best_max_depth, best_min_samples_split, best_min_samples_leaf, best_min_learning_rate, best_min_learning_subsample, best_score

    if short_name == 'svm':
        best_C = best_vals['svm_C']
        best_kernel = best_vals['svm_kernel']
        best_gamma = best_vals['svm_gamma']
        best_degree = best_vals['svm_degree']
        best_probability = best_vals['svm_probability']
        best_score = grid.best_score_
        print(SEP_STRING)
        print(f'GRID SEARCH RESULTS, {long_name}:')
        print(f"Best penalty parameter C: {best_C}")
        print(f"Best kernel: {best_kernel}")
        print(f"Best gamma: {best_gamma}")
        print(f"Best degree: {best_degree}")
        print(f"Best probability: {best_probability}")
        print(f"Best accuracy: {best_score * 100}%")
        return best_C, best_kernel, best_gamma, best_degree, best_probability, best_score

    if short_name == 'rfc':
        best_n_estimators = best_vals['n_estimators']
        best_max_features = best_vals['max_features']
        best_max_depth = best_vals['max_depth']
        best_min_samples_split = best_vals['min_samples_split']
        best_min_samples_leaf = best_vals['min_samples_leaf']
        best_bootstrap = best_vals['bootstrap']
        best_score = grid.best_score_
        print(SEP_STRING)
        print(f'GRID SEARCH RESULTS, {long_name}:')
        print(f"Best n_estimators: {best_n_estimators}")
        print(f"Best max_features: {best_max_features}")
        print(f"Best max_depth: {best_max_depth}")
        print(f"Best min_samples_split: {best_min_samples_split}")
        print(f"Best min_samples_leaf: {best_min_samples_leaf}")
        print(f"Best bootstrap: {best_bootstrap}")
        print(f"Best accuracy: {best_score * 100}%")
        return best_n_estimators, best_max_features, best_max_depth, best_min_samples_split, best_min_samples_leaf, best_bootstrap, best_score
