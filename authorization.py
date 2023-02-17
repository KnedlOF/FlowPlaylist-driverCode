import spotipy
from spotipy.oauth2 import SpotifyOAuth
from client_secrets import client_id, client_secret
import logging
import os

# finds path to roaming and sets spotify path
programdata_folder = os.environ["PROGRAMDATA"]+'\Spotify Keyboard'

# starts logging
logging.basicConfig(
    filename=programdata_folder+'\logs.log', level=logging.INFO)
logging.info('Started')

if not os.path.exists(programdata_folder):
    os.makedirs(programdata_folder)


# cache_folder = "A:\\Users\\Mitja\\AppData\\Roaming\\Spotify Keyboard\\.cache"
cache_path = programdata_folder+'\.cache'
logging.info(cache_path)
print(cache_path)

x = True
while not os.path.exists(cache_path):
    if x:
        logging.info('No cache')
        x = False

# authorization
redirect_uri = 'https://example.org/callback'


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               cache_path=cache_path,
                                               scope="playlist-read-collaborative playlist-read-private playlist-modify-public playlist-modify-private user-read-currently-playing playlist-read-private user-modify-playback-state user-library-modify user-read-playback-state"))
