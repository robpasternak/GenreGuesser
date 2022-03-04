from calendar import c
from distutils.command.clean import clean
from json.tool import main
from selenium import webdriver
'''from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains'''
from selenium.common.exceptions import NoSuchElementException,WebDriverException
'''from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC'''
from selenium.webdriver.common.by import By
import pandas as pd
from bs4 import BeautifulSoup
import time
import regex as re
import progressbar
import string

PATH = "/Users/julespastor/Desktop/chromedriver"




if True:
    #all the lists we need to instantiate
    full_lyrics = []
    Arists = []
    WArtists = []
    BArtists = []
    WSongs = []
    BSongs = []
    Songs = []
    Year = []
    Lyrics = []
    Bill_link = []
    Wat_link = []
    Bmain_artist = []
    Wmain_artist = []
    BGenre = []
    WGenre = []
    WLink = []
    BLi = []

    #genre we need, using keys for Bill and values for dict
    genres = {
        'rap' : 100,
        'pop' : 73,
        'country' : 38,
        'rock' : 114,
        'folk' : 57,
        'smooth-jazz' : 62
        }


def scrolly(main_driver, ScrollNumber):
    '''Scrolls a given number (ScrollNumber) of times'''
    for i in range(0,ScrollNumber):
         #results = driver.find_elements_by_xpath('//div[@class="feed-item"]')
        #Results=Results+results
        main_driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(2)

def clean_song(song):
    s = song.translate(str.maketrans('', '', string.punctuation))
    s = s.replace(' ','-').lower()
    return s

def clean_data(df):
    '''genre data cleaning function'''

    #dropping duplicates
    input = df.drop_duplicates(subset = ['Artists', 'Song'],keep = 'first').reset_index(drop = True)

    #dropping np Nans
    input = df.dropna()

    #deleting songs with mix / remix in title
    input = df[df["Song"].str.contains("Mix|Remix")==False]

    #spliting Artists column into a new Solo Artist
    input['Main_Artist'] = df['Artists'].str.split('Featuring|&')
    input['Main_Artist'] = input['Main_Artist'].apply(lambda x: x[0])

    #selecting relevant columns
    input = input[['Main_Artist','Artists', 'Song']]

    # return df
    return input

def scrappy(main_driver, url):
    '''Scrappes the lyrics of a song on genius based on the url it is provided'''
    main_driver.get(url)

    time.sleep(.1)

    try:
        main_driver.find_element(By.XPATH,'//*[@id="onetrust-accept-btn-handler"]').click()
        html = main_driver.page_source
    except NoSuchElementException:
        html = main_driver.page_source

    soup = BeautifulSoup(html, "html.parser")
    try:
        goup = soup.find('main', class_='SongPage__Container-sc-19xhmoi-0 buKnHw').find('div', class_='SongPage__Section-sc-19xhmoi-3 cXvCRB')
        baby_goup = goup.find('div', class_='SongPage__LyricsWrapper-sc-19xhmoi-5 UKjRP').find('div', id='lyrics-root-pin-spacer').find('div', class_='SongPageGriddesktop__TwoColumn-sc-1px5b71-1 hfRKjb Lyrics__Root-sc-1ynbvzw-1 kZmmHP')
        lyrics = baby_goup.find_all('div', class_='Lyrics__Container-sc-1ynbvzw-6 jYfhrf')
        tmp = []
        for lyric in lyrics:
            content = lyric.text
            tmp.append(content)
        joined = ' '.join(tmp)
    except AttributeError:
        joined = None

    return joined

#returns the url => url is for Genius
def get_url(artist, song):
    '''Generates the Geniys Lyrics url based on the artist and song provided'''
    base_url = 'https://genius.com/'
    clean_artist = artist.translate(str.maketrans('', '', string.punctuation))
    clean_artist= artist.lower().replace(' ','-')

    if type(song) == 'str':
        c_song = clean_song(song)
    else:
        c_song = clean_song(str(song))
    url = base_url+clean_artist+'-'+c_song+'-lyrics'
    return url

#uses link which is for the song website
#returns a list of songs and artists to be used by scrappy
def wat(link,driver,gr):
    '''Returns a dataframe containing the artist and song name from the Waterloo Source '''

    driver.get(link)
    scrolly(driver, 10)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    goup = soup.find('table', class_='music').find('tbody').find_all('tr')
    for gew in goup:
        data = gew.find_all('td')
        artist = data[1].text
        WArtists.append(artist)
        song = data[2].text
        WSongs.append(song)
        year = data[5].text
        Year.append(year)
        ma = artist.split('&')[0].split('Featuring')[0].rstrip()
        Wmain_artist.append(ma)
        WGenre.append(gr)


    data = {
        'Artists' : WArtists,
        'Song' : WSongs,
        'Main_Artist' : Wmain_artist,
        'Genre' : WGenre
    }
    df = pd.DataFrame.from_dict(data)
    return df

def bill(link,driver,gr):
    '''Returns a dataframe containing the artist and song name from the Billboard Source '''

    driver.get(link)
    time.sleep(1)
    try :
        driver.find_element(By. XPATH, '//*[@id="onetrust-accept-btn-handler"]')
    except NoSuchElementException :
        pass
    scrolly(driver, 10)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    time.sleep(.1)

    try :
        goup = soup.find('main').find('div' ,{'class' : re.compile(r"^lrv-u-background-color-brand-accent-blue post-")})
        baby_goup = goup.find('div', class_='pmc-paywall').find('div', class_='chart-results // lrv-a-wrapper lrv-u-padding-lr-00@mobile-max').find('div', class_='u-max-width-960 lrv-u-margin-lr-auto')
        tiny_goup = baby_goup.find('div', class_='chart-results-list // u-padding-b-250')
        kevin = tiny_goup.find_all('div', class_='o-chart-results-list-row-container')
        for t in kevin:
            tin = t.find('ul')
            nano_goup = tin.find('li', class_='lrv-u-width-100p').find('ul', class_='lrv-a-unstyle-list lrv-u-flex lrv-u-height-100p').find('li', class_='o-chart-results-list__item // lrv-u-flex-grow-1 lrv-u-flex lrv-u-flex-direction-column lrv-u-justify-content-center lrv-u-border-b-1 lrv-u-border-color-grey-light lrv-u-padding-l-2 lrv-u-padding-l-1@mobile-max')
            song = nano_goup.find('h3').text.strip('\n')
            BSongs.append(song)
            artist = nano_goup.find('span').text.strip('\n')
            BArtists.append(artist)
            ma = artist.split('&')[0].split('Featuring')[0].rstrip()
            Bmain_artist.append(ma)
            BGenre.append(gr)

    except AttributeError:
        pass


    data = {
        'Artists' : BArtists,
        'Song' : BSongs,
        'Main_Artist' : Bmain_artist,
        'Genre' : BGenre
    }
    df = pd.DataFrame.from_dict(data)
    return df

def get_bill_link(genre):
    '''Returns the URL from which to scrape artist name, songs and date of publication for BillBoard source'''
    base_url = 'https://www.billboard.com/charts/year-end/'
    end = '-songs/'
    year = 2022
    c_genre = genre.lower()
    BLink = []
    for i in range(1,15):
        y = year - i
        if genre == ('pop' or 'rock'):
            link = (f'{base_url}{y}/{c_genre}{end}')
        else:
            link = (f'{base_url}{y}/hot-{c_genre}{end}')
        BLink.append(link)

    return BLink, genre

def get_wat_link(genre):
    '''Returns the URL from which to scrape artist name, songs and date of publication for Waterloo source'''
    base_url = 'https://cs.uwaterloo.ca/~dtompkin/music/genre/mbgenre'
    end = '.html'
    link = (f'{base_url}{genre}{end}')
    return link, genre


def overlord():
    '''Returns the lyrics of all songs based on the genre of the link provided for both sources'''
    driver = webdriver.Chrome(executable_path = PATH)
    Wat_genres = list(genres.values())
    Bill_genres = list(genres.keys())

    bar = progressbar.ProgressBar(maxval=len(Wat_genres), \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    for genre in Wat_genres:
        wl = get_wat_link(genre)[0]
        WLink.append(wl)
    for link in WLink:
        i = WLink.index(link)
        gr = Wat_genres[i]
        Wdf = wat(link,driver,gr)
        bar.update((WLink.index(link))+1)
    bar.finish()

    bar1 = progressbar.ProgressBar(maxval=len(Bill_genres), \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar1.start()
    for genre in Bill_genres:
        BLink = get_bill_link(genre)[0]
        for link in BLink:
            i = Bill_genres.index(genre)
            gr = Bill_genres[i]
            Bdf = bill(link,driver,gr)
        bar1.update((Bill_genres.index(genre))+1)
    bar1.finish()

    frames = [Wdf, Bdf]
    #incorporate the cleaning function
    #the df is now cleaned and we will look at series
    df = pd.concat(frames).reset_index(drop=True)
    driver.close()
    return df

def scrapstar(df):
    main_driver = webdriver.Chrome(executable_path = PATH)
    art = df['Main_Artist'].tolist()
    songz = df['Song'].tolist()

    bar = progressbar.ProgressBar(maxval=len(art), \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()

    for i in range (0, len(art)):
        try :
            artist = art[i]
            song = songz[i]
            url = get_url(artist, song)
            full_lyrics = scrappy(main_driver, url)
            Lyrics.append(full_lyrics)
            bar.update(i)
        except WebDriverException:
            print('\n\n WebDriverException \n\n')
            Lyrics.append(None)
    bar.finish()

    main_driver.close()
    genre = list(df['Genre'])

    dict_df = {
        'Lyrics' : Lyrics,
        'Genre' : genre
    }
    result = pd.DataFrame(data=dict_df)
    return  result



'''!!!!!FOR TESTING PURPOSES ONLY!!!!!'''
#song_info = overlord()
#full_df.to_csv(f'../raw_data/data.csv')
if __name__ == '__main__':
    song_info = pd.read_csv(f'../raw_data/song_data.csv')
    s_info = song_info[8000:12000]
    sample_df = scrapstar(s_info)
    sample_df.to_csv(f'../raw_data/woo1.csv')
'''

    data1 = pd.read_csv('../raw_data/rap_pop_country_alpha.csv')
    data2 = pd.read_csv('../raw_data/woo.csv')
    frames = [data1, data2]
    full_df = pd.concat(frames)
    full_df.drop_duplicates()
    full_df.reset_index(inplace = True)
    full_df = full_df[['Lyrics', 'Genre']]
    full_df.to_csv('../raw_data/updated_data.csv')'''
