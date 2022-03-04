#!/usr/src/env python

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.svm import SVC
from GenreGuesser.text_preproc import clean_text
#from gcp import save_model

def format_func(X_in):
    '''
    Transformer function that cleans text,
    integrated as first step of pipeline
    '''
    X_out = X_in.apply(clean_text)
    return X_out

# Create format_transform for data cleaning
format_transform = FunctionTransformer(format_func)

# Create Pipeline, which has the following three steps:
#   - Clean text (remove things like '[VERSE 1]', lemmatize, etc.)
#   - TF-IDF Vectorize
#   - using svm.SVC (with probability = True to allow probabilities,
#       and a linear kernel since that apparently works well for text
svm_pipe = Pipeline([
    ('format_transform', format_transform),
    ('tfidf', TfidfVectorizer()),
    ('svm', svm.SVC(probability = True, kernel = 'linear')),
])

#if __name__ == "__main__":
#    save_model(svm_pipe, "svm")
