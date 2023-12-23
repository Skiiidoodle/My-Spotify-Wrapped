import spotipy
import requests
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import time
import datetime
import gspread

SPOTIPY_CLIENT_ID ="6780f6cec7ef430494b8782c7407195e"
SPOTIPY_CLIENT_SECRET="31b6031e44f246d0b85cabf2c1eeec5e"
SPOTIPY_REDIRECT_URL="http://127.0.0.1:9090"
SCOPE="user-top-read"

sp=spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                             client_secret=SPOTIPY_CLIENT_SECRET,
                                             redirect_uri=SPOTIPY_REDIRECT_URL,
                                             scope=SCOPE))

#top_tracks_short=sp.current_user_top_tracks(limit=10, offset=0, time_range="short_term")



def get_tracks_id(time_frame):
    track_ids=[]
    for song in time_frame['items']:
        track_ids.append(song['id'])
    return track_ids

#track_ids= get_tracks_id(top_tracks_short)


#track_id='7B3z0ySL9Rr0XvZEAjWZzM'

def get_track_features(id):
    meta=sp.track(id)
    name=meta['name']
    album=meta['album']['name']
    artist=meta['album']['artists'][0]['name']
    spotify_url=meta['external_urls']['spotify']
    album_cover=meta['album']['images'][0]['url']
    track_info=[name, album, artist, spotify_url, album_cover]

    return track_info



#tracks=[]
#for i in range(len(track_ids)):
    #time.sleep(.5)
    #track = get_track_features(track_ids[i])
    #tracks.append(track)
    #print(f"\n{track}")

#df=pd.DataFrame(tracks, columns=['name', 'album', 'artist', 'spotify_url', 'album_cover'])
#print(df.head(5))



#gc=gspread.service_account(filename='spotify-wrapped-408406-9eda9ff82713.json')

#sh= gc.open("Spotify wrapped")
#worksheet = sh.worksheet("short_term")
#val = worksheet.acell('B5').value
#print(val)

def insert_to_gsheet(track_ids):
 
    tracks = []
    for i in range(len(track_ids)):
        time.sleep(.5)
        track = get_track_features(track_ids[i])
        tracks.append(track)

    df = pd.DataFrame(tracks, columns = ['name', 'album', 'artist', 'spotify_url', 'album_cover'])

    gc = gspread.service_account(filename='spotify-wrapped-408406-9eda9ff82713.json')
    sh = gc.open('Yut wrapped')
    worksheet = sh.worksheet(f'{time_period}')
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    print('Done')


time_ranges = ['short_term', 'medium_term', 'long_term']
for time_period in time_ranges:
    top_tracks = sp.current_user_top_tracks(limit=20, offset=0, time_range=time_period)
    track_ids = get_tracks_id(top_tracks)
    insert_to_gsheet(track_ids)

