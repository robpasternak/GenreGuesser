#!/usr/src/env python

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from GenreGuesser.text_preproc import clean_text
import nltk
nltk.download('words')

def format_func(X_in):
    '''
    Transformer function that cleans text,
    integrated as first step of pipeline
    '''
    X_out = X_in.apply(clean_text)
    return X_out

# Create Pipeline, which has the following three steps:
#   - Clean text (remove things like '[VERSE 1]', lemmatize, etc.)
#   - TF-IDF Vectorize
#   - using rfc

def get_rfc_pipe():
    format_transform = FunctionTransformer(format_func)

    rfc_pipe = Pipeline([
        ('format_transform', format_transform),
        ('tfidf', TfidfVectorizer()),
        ('rfc', RandomForestClassifier()),
    ])

    return rfc_pipe
