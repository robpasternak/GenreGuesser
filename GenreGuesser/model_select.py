from sklearn.model_selection import cross_validate
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score

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
