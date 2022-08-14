from inspect import trace
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from secrets import client_id, client_secret
import random

redirect_uri = 'https://example.org/callback'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope='user-read-recently-played'))\




#gets 30 track ids from recently played
recently_played=sp.current_user_recently_played(limit=30, after=None, before=None)

track_ids = [track['track']['id'] for track in recently_played['items']]

   
#get artists
# tracks=sp.tracks(track_ids)
# track_artists = [track['artists'][0]['id'] for track in tracks['tracks']]

#removes duplicates
track_ids=list(dict.fromkeys(track_ids))
# track_artists=list(dict.fromkeys(track_artists))

#randomly selects 5 
sampled_ids=random.sample(track_ids, 5)  
# sampled_artists=random.sample(track_artists, 5) 

recommendations=sp.recommendations(seed_artists=None, seed_genres=None, seed_tracks=sampled_ids ,limit=3, country=None)
recommend_ids=[track['track']['id'] for track in recently_played['items']]

print(recommendations)
