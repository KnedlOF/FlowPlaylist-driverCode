import spotipy
from spotipy.oauth2 import SpotifyOAuth
from secrets import client_id, client_secret
import pickle
import sys
import logging
from tkinter import messagebox

_key = 1



#authorization

redirect_uri = 'https://example.org/callback'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope="playlist-read-collaborative playlist-read-private playlist-modify-public playlist-modify-private user-read-currently-playing playlist-read-private user-modify-playback-state user-library-modify"))


#checks if it is in playlist
try:             
    with open('playlist_config.txt', "rb") as f:
        dict=pickle.load(f)
except:
    messagebox.showerror('No playlist, detected. Please select playlist in app.')

playlist_id=dict['id']
username = 	('8sluo6nzp60un03m9xdgp7zsz')

def getTrackIDs(username='8sluo6nzp60un03m9xdgp7zsz', playlist_id='3qt42V60uqPEsvlIl6LvEc'):

    track_ids=[]

    playlist1 = sp.user_playlist_tracks(username, playlist_id, fields=None, offset=0, limit=100)
    playlist2 = sp.user_playlist_tracks(username, playlist_id, fields=None, offset=100, limit=100)
    playlist3 = sp.user_playlist_tracks(username, playlist_id, fields=None, offset=200, limit=100)
    playlist4 = sp.user_playlist_tracks(username, playlist_id, fields=None, offset=300, limit=100)
    playlist5 = sp.user_playlist_tracks(username, playlist_id, fields=None, offset=400, limit=100)
    playlist6 = sp.user_playlist_tracks(username, playlist_id, fields=None, offset=500, limit=100)
    playlist7 = sp.user_playlist_tracks(username, playlist_id, fields=None, offset=600, limit=100)

  
    
   
    for item in playlist1['items']+playlist2['items']+playlist3['items']+playlist4['items']+playlist5['items']+playlist6['items']+playlist7['items']:
        track=item['track']
        track_ids.append(track['id'])
    

    return track_ids


#checks currently playing song

cp = sp.current_user_playing_track()

#if it isnt playing it will not work

if cp is None:
    logging.error('Spotify not playing any tracks. Exitting !!!')

track_name = cp['item']['name']
track_id = cp['item']['id']

#checks if it is in playlist already

track_ids=getTrackIDs()  
print(len(track_ids))
print(track_ids)

if track_id in track_ids:
     logging.error('Track already exists in this playlist.')
     print('Track already exists in this playlist.')



else:
#adds song to playlist
    print('Track added')
    

    try:
        sp.playlist_add_items(playlist_id, [track_id])
    except Exception:
        logging.error('Could not add track to playlist !!!')

