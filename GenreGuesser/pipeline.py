from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer

#Create rounder for data cleaning
rounder = FunctionTransformer()

# Create Pipeline
pipe = Pipeline([
    ('rounder', rounder)
    ('tfidf', TfidfVectorizer()),
    ('knn', KNeighborsClassifier(weights = 'distance')),
])

# Set parameters to search
parameters = {
    'count__ngram_range': ((1,1), (2,2)),
    'nb__alpha': (0.1,1)}

# Perform grid search
grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1,
                           verbose=1, scoring = "accuracy",
                           refit=True, cv=5)

grid_search.fit(data.text,y)

grid_search.model
