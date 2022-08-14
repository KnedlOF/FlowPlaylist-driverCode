from inspect import trace
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from secrets import client_id, client_secret
import logging

redirect_uri = 'https://example.org/callback'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope='playlist-read-collaborative playlist-read-private playlist-modify-public playlist-modify-private user-read-currently-playing playlist-read-private user-modify-playback-state user-library-modify'))\




#gets currently playing song
currently_played=sp.current_user_playing_track()

if currently_played is None:
    logging.error('Spotify not playing any tracks. Exitting !!!')

#only takes id
track_id = currently_played['item']['id']
seed_tracks=[track_id]

#gets recommendations
recommendations=sp.recommendations(seed_artists=None, seed_genres=None, seed_tracks=seed_tracks ,limit=3, country=None)
recommend_ids = [track['id'] for track in recommendations['tracks']]

for item in recommendations['tracks']:
        track_id=item['id']
        queue=sp.add_to_queue(track_id)
        print(track_id +" added to queue.")
