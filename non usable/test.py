
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from client_secrets import client_id, client_secret
import pickle
import sys
import logging
import argparse
import sys
import pprint
parser = argparse.ArgumentParser()
parser.add_argument("key", type=int)
_key = 1

logging.basicConfig(filename="spotify_auto_playlist.log",
                    format="%(asctime)s: %(message)s", level=logging.INFO)
logging.info('Alt+{} key pressed'.format(_key))

try:
    with open("playlist_mapping.config", "rb") as f:
        pls = pickle.load(f)
except Exception:
    sys.exit(1)
    logging.error(
        'Could not load playlist mappings. Please run "list_playlists.py" first to generate playlist mappings')

if _key > len(pls):
    logging.error('No mapping associated with Alt+{} key'.format(_key))
    sys.exit(1)

redirect_uri = 'https://example.org/callback'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope="playlist-read-collaborative playlist-read-private playlist-modify-public playlist-modify-private user-read-currently-playing"))



playlist_id=('3qt42V60uqPEsvlIl6LvEc')
username = 	('8sluo6nzp60un03m9xdgp7zsz')

def getTrackIDs(username='8sluo6nzp60un03m9xdgp7zsz', playlist_id='3qt42V60uqPEsvlIl6LvEc'):

    track_ids=[]

    playlist = sp.user_playlist(username, playlist_id)
    
    for item in playlist['tracks']['items']:
        track=item['track']
        track_ids.append(track['id'])

    return track_ids



track_ids=getTrackIDs()  

if '56Ydhy30ogSmTKTyDxcirY' in track_ids:
    print("fuck yea it is in")
print(len(track_ids))
print(track_ids)

