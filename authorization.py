import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pickle
import logging
import os

# finds path to roaming and sets spotify path
programdata_folder = os.environ["PROGRAMDATA"]+'\FlowPlaylist'

# starts logging
logging.basicConfig(
    filename=programdata_folder+'\logs.log', level=logging.INFO)
logging.info('Started')

if not os.path.exists(programdata_folder):
    os.makedirs(programdata_folder)


# cache_folder = "A:\\Users\\Mitja\\AppData\\Roaming\\FlowPlaylist\\.cache"
cache_path = programdata_folder+'\.cache'
logging.info(cache_path)
print(cache_path)

x = True
while not os.path.exists(cache_path): 
    if x:
        logging.info('No cache file found')

        x = False
# authorization
redirect_uri = 'https://example.org/callback'

try:
    with open(programdata_folder+"\secrets.txt", "rb") as f:
        secretsdict = pickle.load(f)
except:
    secretsdict = {'client_id': "x", 'client_secret': "x"}
    secretsfile = open(programdata_folder+"\secrets.txt", "wb")
    pickle.dump(secretsdict, secretsfile)
    secretsfile.close()

client_id=secretsdict['client_id']
client_secret=secretsdict['client_secret']
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               cache_path=cache_path,
                                               scope="playlist-read-collaborative playlist-read-private playlist-modify-public playlist-modify-private user-read-currently-playing playlist-read-private user-modify-playback-state user-library-modify user-read-playback-state"))
