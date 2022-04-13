#!/usr/src/env python

# For text-cleaning
import re, string
import nltk
nltk.download('stopwords', quiet = True)
nltk.download('punkt', quiet = True)
nltk.download('wordnet', quiet = True)
nltk.download('omw-1.4', quiet = True)
from nltk.corpus import stopwords
from nltk.corpus import words
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# For pipeline
import joblib
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from imblearn.under_sampling import RandomUnderSampler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# Dictionary for translating from MusicBrainz genre code to English
GENRE_DICT = {
    '100' : 'rap',
    100 : 'rap',
    '73' : 'pop',
    73 : 'pop',
    '38' : 'country',
    38 : 'country',
    '114' : 'rock',
    114 : 'rock',
    '57' : 'folk',
    57 : 'folk',
    '62' : 'jazz',
    62 : 'jazz',
    'smooth-jazz': 'jazz',
    }

# Change the following line when we get the full data:
DATA_SOURCE = 'raw_data/full_df.csv'

def clean_text(text):
    #remove 'е'
    text = text.replace('е', 'e')

    #remove headers like [Chorus] etc
    headers = re.findall(r"\[(.*?)\]", text)
    for header in headers:
        text = text.replace(f'[{header}]', ' ')

    #separate lower/upper case words (like 'needHow')
    cap_sep_find = r'([a-z])([A-Z])'
    cap_sep_replace = r'\1 \2'
    text = re.sub(cap_sep_find, cap_sep_replace, text)

    #remove punctuation
    exclude = string.punctuation + "’‘”“"
    for punctuation in exclude:
           text = text.replace(punctuation, ' ')

    #turn text into lowercase
    text = text.lower()

    #remove numericals
    text = ''.join(word for word in text if not word.isdigit())

    #remove stopwords
    stop_words = set(stopwords.words('english'))

    #tokenise
    word_tokens = word_tokenize(text)
    text = [w for w in word_tokens if not w in stop_words]

    #lemmatise
    lemmatizer = WordNetLemmatizer()
    lemmatized = [lemmatizer.lemmatize(word) for word in text]
    text = lemmatized

    #filter out non-ascii words
    words_set = set(words.words())
    safe_set = set(['cliché', 'rosé', 'déjà', 'ménage',  'yoncé', 'beyoncé', 'café', 'crème', 'señor', 'señorita'])
    ascii_list = []
    for word in text:
        if word in words_set or word.isascii() or word in safe_set:
            ascii_list.append(word)
    text = ' '.join(ascii_list)

    text = text.replace('wan na', "wanna")
    text = text.replace('gon na', "gonna")
    text = text.replace('got ta', "gotta")

    return text

# Create Pipeline, which has the following three steps:
#   - Clean text (remove things like '[VERSE 1]', lemmatize, etc.)
#   - TF-IDF Vectorize
#   - using svm.SVC
def get_svm_pipe():
    svm_pipe = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('svm', SVC(probability = True)),
    ])

    return svm_pipe

if __name__ == '__main__':
    print('Getting data')
    data = pd.read_csv(DATA_SOURCE)
    data['Genre'] = data['Genre'].apply(lambda x : GENRE_DICT[x] if x in GENRE_DICT.keys() else x)
    data = data.dropna()
    data = data[data['Genre'].isin(['rap', 'country', 'rock', 'pop'])]
    print(data.head())

    X = data[['Lyrics']]
    y = data['Genre']

    # Undersample for balance
    rus = RandomUnderSampler(random_state = 42)
    X, y = rus.fit_resample(X,y)
    X = X['Lyrics']
    print('Cleaning text...')
    X = X.apply(clean_text)
    print('Text clean.')

    # Split 80-20 into training/validation and test data (reliably with a fixed random state)
    X_tv, X_test, y_tv, y_test = train_test_split(X, y, test_size = .2, random_state = 42)

    heroku_pipe = get_svm_pipe()
    print('Pipe obtained')

    heroku_pipe.set_params(verbose = True)
    print('Pipe verbosity set. Now going to fit')
    heroku_pipe.fit(X_tv,y_tv)
    joblib.dump(heroku_pipe, "heroku.joblib")
    print(f"SVM model fitted and saved as heroku.joblib")
    y_pred = heroku_pipe.predict(y_test)
    test_accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy on test data: {round(test_accuracy * 100, 2)}%')
