import spotipy
from spotipy.oauth2 import SpotifyOAuth
from secrets import client_id, client_secret


redirect_uri = 'https://example.org/callback'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope="playlist-read-collaborative"))\

class SaveSongs:
    def __init__(self):
        self.playlists_ids=""
        

    def find_songs(self):
        playlists=sp.current_user_playlists(limit=50,offset=0)

        for i in playlists['items']:
            self.playlists_ids += (i["name"] +" - "+ i["id"] + "\n" )
        
        print(self.playlists_ids)
   

a=SaveSongs()
a.find_songs()