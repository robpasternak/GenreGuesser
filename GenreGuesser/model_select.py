from sklearn.model_selection import cross_validate

def gg_cross_val(pipeline, X, y):
    cv_result = cross_validate(pipeline, X, y, cv = 5, scoring = 'accuracy')
    mean_test_score = cv_result['test_score'].mean()
    mean_fit_time = cv_result['fit_time'].mean()
    print(f'Mean Accuracy: {mean_test_score * 100}%\nMean Fit Time: {round(mean_fit_time, 3)}s')
    return mean_test_score, mean_fit_time
