import re
import string
import nltk
nltk.download('stopwords', quiet = True)
nltk.download('punkt', quiet = True)
nltk.download('wordnet', quiet = True)
nltk.download('omw-1.4', quiet = True)
from nltk.corpus import stopwords
from nltk.corpus import words
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

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
