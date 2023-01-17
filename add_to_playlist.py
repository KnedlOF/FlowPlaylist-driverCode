import spotipy
from spotipy.oauth2 import SpotifyOAuth
from client_secrets import client_id, client_secret
import pickle
from tkinter import messagebox



def playlist():
    #authorization

    redirect_uri = 'https://example.org/callback'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                client_secret=client_secret,
                                                redirect_uri=redirect_uri,
                                                scope="playlist-read-collaborative playlist-read-private playlist-modify-public playlist-modify-private user-read-currently-playing playlist-read-private user-modify-playback-state user-library-modify"))

    user_info=sp.current_user()
    username=user_info["id"]
    print(username)
    #checks if it is in playlist
    try:             
        with open('playlist_config.txt', "rb") as f:
            dict=pickle.load(f)
    except:
        messagebox.showerror('No playlist, detected. Please select playlist in app.')

    playlist_id=dict['id']

    #checks currently playing song

    cp = sp.current_user_playing_track()

    #if it isnt playing it will not work

    if cp is None:
        print('Spotify not playing any tracks.')

    playlist=sp.user_playlist_tracks(username,playlist_id, fields=None, limit=1)
    total=playlist['total']
    offset=total-100
    playlist=sp.user_playlist_tracks(username,playlist_id, fields=None, offset=offset, limit=100)
    track_ids = [track['track']['id'] for track in playlist['items']]
    # track_name = cp['item']['name']
    track_id = cp['item']['id']

    #checks if it is in playlist already

    print(track_ids)

    if track_id in track_ids:
        return('Already in playlist')



    else:
    #adds song to playlist
        

        try:
            sp.playlist_add_items(playlist_id, [track_id])
            return ("Track added")
        except Exception:
            return('Could not add track to playlist !!!')
