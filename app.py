import streamlit as st
import requests


url = 'https://genre-guesser-2cfzxdapea-ew.a.run.app'
predict = '/predict?lyrics='
lyrics = st.text_input('INSERT LYRICS BELOW')
if lyrics != '' :
    lyrics = lyrics.replace(' ', '%20')
    prediction_url = url+predict+lyrics
    data = requests.get(prediction_url).json()
    genre = data.get('genre')
    if genre == 'rock':
        st.markdown(f"Baby you're a fan of Rock n Rolllll")
    if genre =='rap':
        st.markdown('R.I.P. Eazy E, he defined the Rap Genre')
    if genre =='pop':
        st.markdown('Your tastebuds have a problem, Bud. Grow up and stop listening to Pop')

    st.markdown(f'The genre of the given lyrics is...{genre}')
