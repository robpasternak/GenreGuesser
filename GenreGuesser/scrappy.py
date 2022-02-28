from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
from bs4 import BeautifulSoup
import time

PATH = "/Users/julespastor/Desktop/chromedriver"


url = 'https://genius.com/Kid-cudi-heart-of-a-lion-kid-cudi-theme-music-lyrics'

if True:
    full_lyrics = []
    Artists = []
    Songs = []
    Year = []
    Lyrics = []

def scrolly(main_driver, ScrollNumber):
    for i in range(0,ScrollNumber):
         #results = driver.find_elements_by_xpath('//div[@class="feed-item"]')
        #Results=Results+results
        main_driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(2)


def scrappy(url):

    main_driver = webdriver.Chrome(executable_path = PATH)
    main_driver.get(url)

    time.sleep(.1)

    main_driver.find_element(By.XPATH,'//*[@id="onetrust-accept-btn-handler"]').click()

    html = main_driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    goup = soup.find('main', class_='SongPage__Container-sc-19xhmoi-0 buKnHw').find('div', class_='SongPage__Section-sc-19xhmoi-3 cXvCRB')
    baby_goup = goup.find('div', class_='SongPage__LyricsWrapper-sc-19xhmoi-5 UKjRP').find('div', id='lyrics-root-pin-spacer').find('div', class_='SongPageGriddesktop__TwoColumn-sc-1px5b71-1 hfRKjb Lyrics__Root-sc-1ynbvzw-1 kZmmHP')
    lyrics = baby_goup.find_all('div', class_='Lyrics__Container-sc-1ynbvzw-6 jYfhrf')
    for lyric in lyrics:
        content = lyric.text
        full_lyrics.append(content)
    return full_lyrics

#returns the url => url is for Genius
def get_url(artist, song):
    base_url = 'https://genius.com/'
    clean_artist = artist.lower().replace(' ','-')
    clean_song = song.lower().replace(' ','-')
    url = base_url+clean_artist+'-'+clean_song+'-lyrics'
    return url

#uses link which is for the song website
#returns a list of songs and artists to be used by scrappy
def a_and_s(link):
    driver = webdriver.Chrome(executable_path=PATH)
    driver.get(link)
    scrolly(driver, 10)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    goup = soup.find('table', class_='music').find('tbody').find_all('tr')
    for gew in goup:
        data = gew.find_all('td')
        artist = data[1].text
        Artists.append(artist)
        song = data[2].text
        Songs.append(song)
        year = data[5].text
        Year.append(year)
    driver.close()
    data = {
        'Artists' : Artists,
        'Songs' : Songs,
        'Year' : Year
    }
    df = pd.DataFrame.from_dict(data)
    return df

def overlord(link):

    df = a_and_s(link)
    #incorporate the cleaning function
    #the df is now cleaned and we will look at series

    Art = df['Artists'].tolist()
    Songz = df['Songs'].tolist()
    for i in range (1, len(Art)):
        artist = Art[i]
        song = Songz[i]
        url = get_url(artist, song)
        full_lyrics = scrappy(url)
        Lyrics.append(full_lyrics)
        break
    #df['Lyrics'] = pd.Series(Lyrics)
    print(Lyrics)
    #return df




link = 'https://cs.uwaterloo.ca/~dtompkin/music/genre/mbgenre100.html'
df = overlord(link)
df.to_csv('../raw_data/rap_data.csv')
