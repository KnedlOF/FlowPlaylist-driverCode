
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from secrets import client_id, client_secret
import pickle
import sys
import logging
import argparse
import sys

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

#authorization

redirect_uri = 'https://example.org/callback'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope="playlist-read-collaborative playlist-read-private playlist-modify-public playlist-modify-private user-read-currently-playing playlist-read-private"))


#checks if it is in playlist
playlist_id=('3qt42V60uqPEsvlIl6LvEc')
username = 	('8sluo6nzp60un03m9xdgp7zsz')

def getTrackIDs(username='8sluo6nzp60un03m9xdgp7zsz', playlist_id='3qt42V60uqPEsvlIl6LvEc'):
    results = sp.user_playlist(sp.current_user()['id'],playlist_id)
    song_list = []
    dup_list = []

    for i, item in enumerate(results['tracks']['items']):
        if item['track']['id'] in song_list:
            dup_list.append({"uri":item['track']['id'], "positions":[i]})
        song_list.append(item['track']['id'])

    sp.user_playlist_remove_specific_occurrences_of_tracks(sp.current_user()['id'], playlist_id, dup_list)

    print("Duplicate Songs removed from Playlist!")


#checks currently playing song

cp = sp.current_user_playing_track()

#if it isnt playing it will not work

if cp is None:
    logging.error('Spotify not playing any tracks. Exitting !!!')

track_name = cp['item']['name']
track_id = cp['item']['id']

#checks if it is in playlist already

# track_ids=getTrackIDs()  

# if track_id in track_ids:
#     logging.error('Track already exists in this playlist.')


# print(len(track_ids))
# print(track_ids)


#adds song to playlist
# logging.info('Adding track "{}"" to playlist "{}"'.format(
#     track_name, pls[_key - 1]['name']))


# try:
#     sp.playlist_add_items(pls[_key - 1]['id'], [track_id])
# except Exception:
#     logging.error('Could not add track to playlist !!!')