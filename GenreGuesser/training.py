import pandas as pd

from GenreGuesser.julia_text_preproc import clean_text
from GenreGuesser.data_cleaning import clean_data

if __name__ = '__main__':
    data = pd.read_csv('raw_data.csv')
    data = clean_data(data)
    X = data[['Lyrics']]
    y = data[['']]
