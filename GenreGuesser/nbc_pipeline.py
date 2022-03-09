from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from GenreGuesser.text_preproc import clean_text


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
#   - Gaussian/MultinomialNB NaiveBayes classifier
def get_nbc_pipe():
    format_transform = FunctionTransformer(format_func)
    nbc_pipe = Pipeline([
        ('format_transform', format_transform),
        ('tfidf', TfidfVectorizer()),
        ('nbc', MultinomialNB()),
    ])

    return nbc_pipe
