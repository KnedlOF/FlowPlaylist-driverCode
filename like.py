import spotipy
from spotipy.oauth2 import SpotifyOAuth
from secrets import client_id, client_secret
import logging


redirect_uri = 'https://example.org/callback'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope="playlist-read-collaborative playlist-read-private playlist-modify-public playlist-modify-private user-read-currently-playing playlist-read-private user-modify-playback-state user-library-modify"))\


cp = sp.current_user_playing_track()

#if it isnt playing it will not work

if cp is None:
    print('Spotify not playing any tracks. Exitting !!!')

track_id = cp['item']['id']
print(track_id)
#checks if it is in playlist already


#adds song to playlist

    

try:
    sp.current_user_saved_tracks_add([track_id])
    print('Track added')
except Exception:
    logging.error('Could not add track to playlist !!!')
    print('Could not add track to playlist !!!')

  