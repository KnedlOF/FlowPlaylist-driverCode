import pickle
from tkinter import messagebox
from authorization import sp


def playlist():

    user_info = sp.current_user()
    username = user_info["id"]
    print(username)
    # checks if it is in playlist
    try:
        with open('playlist_config.txt', "rb") as f:
            dict = pickle.load(f)
    except:
        messagebox.showerror(
            'No playlist, detected. Please select playlist in app.')

    playlist_id = dict['id']

    # checks currently playing song

    cp = sp.current_user_playing_track()

    # if it isnt playing it will not work

    if cp is None:
        print('Spotify not playing any tracks.')

    playlist = sp.user_playlist_tracks(
        username, playlist_id, fields=None, limit=1)
    total = playlist['total']
    offset = total-100
    playlist = sp.user_playlist_tracks(
        username, playlist_id, fields=None, offset=offset, limit=100)
    track_ids = [track['track']['id'] for track in playlist['items']]
    # track_name = cp['item']['name']
    track_id = cp['item']['id']

    # checks if it is in playlist already

    print(track_ids)

    if track_id in track_ids:
        return ('Already in playlist')

    else:
        # adds song to playlist

        try:
            sp.playlist_add_items(playlist_id, [track_id])
            return ("Track added")
        except Exception:
            return ('Could not add track to playlist !!!')
