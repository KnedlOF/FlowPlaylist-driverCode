from authorization import sp
import spotipy


def like():
    track_id = None

    try:
        cp = sp.current_user_playing_track()

        if cp is None:
            return ('No tracks playing')

        track_id = cp['item']['id']
        print(track_id)

    except spotipy.client.SpotifyException as e:
        if e.http_status == 404:
            return ('Spotify not opened!')
        else:
            return ('Something went wrong')

    if track_id != None:
        try:
            sp.current_user_saved_tracks_add([track_id])
            return ("LIKED")
        except spotipy.client.SpotifyException as e:
            if e.http_status == 404:
                return ('Spotify not opened!')
            else:
                return ('Could not like')
