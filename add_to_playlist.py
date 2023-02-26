import pickle
from authorization import sp, programdata_folder
import logging
import spotipy


def playlist():

    try:
        user_info = sp.current_user()
    except spotipy.client.SpotifyException as e:
        if e.http_status == 404:
            return ('Spotify not opened!')
        else:
            return ('Could not get user data')

    username = user_info["id"]
    print(username)
    # checks if it is in playlist
    try:
        with open(programdata_folder+"\playlist_config.txt", "rb") as f:
            dict = pickle.load(f)
    except FileNotFoundError as e:
        logging.info(e)
        return ("Choose playlist in app")
    except Exception as e:
        logging.info(e)

    playlist_id = dict['id']

    # checks currently playing song

    try:
        cp = sp.current_user_playing_track()
        if cp is None:
            return ('Spotify not opened!')
    except spotipy.client.SpotifyException as e:
        if e.http_status == 404:
            return ('Spotify not opened!')
        else:
            return ('Something went wrong')

    # if it isnt playing it will not work

    if username != None:
        playlist = sp.user_playlist_tracks(
            username, playlist_id, fields=None, limit=1)
        total = playlist['total']
        if total > 100:
            offset = total-100
        else:
            offset = None
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
