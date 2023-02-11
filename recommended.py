from authorization import sp


def recommend():
    # gets currently playing song
    currently_played = sp.current_user_playing_track()

    if currently_played is None:
        print('Spotify not playing any tracks. Exitting !!!')

    # only takes id
    track_id = currently_played['item']['id']
    seed_tracks = [track_id]

    # gets recommendations

    try:
        recommendations = sp.recommendations(
            seed_artists=None, seed_genres=None, seed_tracks=seed_tracks, limit=3, country=None)
        recommend_ids = [track['id'] for track in recommendations['tracks']]
        for item in recommendations['tracks']:
            track_id = item['id']
            sp.add_to_queue(track_id)
            print(track_id + " added to queue.")
        return ("Songs added")
    except Exception:
        return ("Can't add")
