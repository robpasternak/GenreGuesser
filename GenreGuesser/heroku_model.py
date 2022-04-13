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
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from imblearn.under_sampling import RandomUnderSampler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate


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

    #rejoin "wan na"/"gon na" to "wanna"/"gonna"
    wannas = re.findall(r"wan na", text)
    gonnas = re.findall(r"gon na", text)
    gottas = re.findall(r"got ta", text)

    for wanna in wannas:
        text = text.replace(wanna, "wanna")

    for gonna in gonnas:
        text = text.replace(gonna, "gonna")

    for gotta in gottas:
        text = text.replace(gotta, "gotta")

    return text

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
#   - using svm.SVC
def get_svm_pipe():
    format_transform = FunctionTransformer(format_func)

    svm_pipe = Pipeline([
        ('format_transform', format_transform),
        ('tfidf', TfidfVectorizer()),
        ('svm', SVC(probability = True)),
    ])

    return svm_pipe

if __name__ == '__main__':
    data = pd.read_csv(DATA_SOURCE)
    data['Genre'] = data['Genre'].apply(lambda x : GENRE_DICT[x] if x in GENRE_DICT.keys() else x)
    data = data.dropna()
    data = data[data['Genre'].isin(['rap', 'country', 'rock', 'pop'])]

    X = data[['Lyrics']]
    y = data['Genre']

    # Undersample for balance
    rus = RandomUnderSampler(random_state = 42)
    X, y = rus.fit_resample(X,y)
    X = X['Lyrics']

    # Split 80-20 into training/validation and test data (reliably with a fixed random state)
    X_tv, X_test, y_tv, y_test = train_test_split(X, y, test_size = .2, random_state = 42)

    heroku_pipe = get_svm_pipe()

    SEP_STRING = f'\n{"=" * 30}\n'
    cv_result = cross_validate(heroku_pipe,
                               X_tv,
                               y_tv,
                               cv = 5,
                               n_jobs = -1,
                               scoring = 'accuracy',
                               verbose = 2)
    mean_test_score = cv_result['test_score'].mean()
    mean_fit_time = cv_result['fit_time'].mean()
    print(SEP_STRING)
    print(f'5-FOLD CROSS-VALIDATION RESULTS, SVM:')
    print(f'Mean Accuracy: {mean_test_score * 100}%')
    print(f'Mean Fit Time: {round(mean_fit_time, 3)}s')
