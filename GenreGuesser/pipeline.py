from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from GenreGuesser.text_preproc import clean_text


def format_func(X_in):
    X_out = X_in.apply(clean_text)
    return X_out

#Create format_transform for data cleaning
format_transform = FunctionTransformer(format_func)

# Create Pipeline
pipe = Pipeline([
    ('format_transform', format_transform),
    ('tfidf', TfidfVectorizer()),
    ('knn', KNeighborsClassifier(weights = 'distance')),
])
