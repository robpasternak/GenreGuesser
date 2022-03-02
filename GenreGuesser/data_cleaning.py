import pandas as pd

def clean_data(input):
    '''genre data cleaning function'''

    #dropping duplicates
    input = input.drop_duplicates(subset = ['Artists', 'Song'],keep = 'first').reset_index(drop = True)

    #dropping np Nans
    input = input.dropna()

    #deleting songs with mix / remix in title
    input = input[input["Song"].str.contains("Mix|Remix")==False].reset_index(drop=True)

    #spliting Artists column into a Main Artist
    input['Main_Artist'] = input['Artists'].str.split('Featuring|&')
    input['Main_Artist'] = input['Main_Artist'].apply(lambda x: x[0])

    #selecting relevant columns
    input = input[['Lyrics', 'Genre']]

    # return input
    return input
