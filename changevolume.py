import spotipy
from spotipy.oauth2 import SpotifyOAuth
from client_secrets import client_id, client_secret
from hid_control import volume

def set_volume():
    #authorization
    redirect_uri = 'https://example.org/callback'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                client_secret=client_secret,
                                                redirect_uri=redirect_uri,
                                                scope="playlist-read-collaborative playlist-read-private playlist-modify-public playlist-modify-private user-read-currently-playing playlist-read-private user-modify-playback-state user-library-modify"))\


    volume_set = sp.volume(volume)

    print(volume_set)
    print("Volume changed on: ".format(volume))
  
