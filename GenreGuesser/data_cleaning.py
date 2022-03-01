import pandas as pd

def clean_data(input):
    '''genre data cleaning function'''
    
    #dropping duplicates
    input = input.drop_duplicates(subset = ['Artists', 'Songs'],keep = 'first').reset_index(drop = True)
    
    #dropping np Nans
    input = input.dropna()
    
    #deleting songs with mix / remix in title
    input = input[input["Songs"].str.contains("Mix|Remix")==False]
    
    #spliting Artists column into a Main Artist
    input['Main Artist'] = input['Artists'].str.split('Featuring|&')
    input['Main Artist'] = input['Main Artist'].apply(lambda x: x[0])

    #selecting relevant columns
    input = input[['Main Artist','Artists', 'Songs', 'Year']]
    
    # return input
    return input