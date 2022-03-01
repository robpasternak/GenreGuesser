import re
import string
string.punctuation
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

def clean_text(text):

    #remove headers like [Chorus] etc
    headers = re.findall(r"\[(.*?)\]", text)
    for header in headers:
        text = text.replace(header, ' ')

    #separate lower/upper case words (like 'needHow')
    text = re.findall('[A-Z][^A-Z]*', text)
    text = " ".join(text)

    #remove punctuation
    exclude = string.punctuation + "’‘”“"
    for punctuation in exclude:
           text = text.replace(punctuation, '')

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

    text = ' '.join(text)

    #rejoin "wan na"/"gon na" to "wanna"/"gonna"
    wannas = re.findall(r"wan na", text)
    gonnas = re.findall(r"gon na", text)
    for wanna in wannas:
        text = text.replace(wanna, "wanna")

    for gonna in gonnas:
        text = text.replace(gonna, "gonna")

    return text
