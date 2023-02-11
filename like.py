from authorization import sp


def like():

    cp = sp.current_user_playing_track()

    # if it isnt playing it will not work

    if cp is None:
        print('Spotify not playing any tracks. Exitting !!!')

    track_id = cp['item']['id']
    print(track_id)
    # checks if it is in playlist already

    try:
        sp.current_user_saved_tracks_add([track_id])
        return ("LIKED")
    except Exception:
        return ("Can't Like")
