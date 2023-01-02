import spotipy
from spotipy.oauth2 import SpotifyOAuth
from client_secrets import client_id, client_secret
import subprocess
import os
from pynput.keyboard import Key, Controller
import psutil

# finds path to roaming and sets spotify path
roaming_folder = os.environ["APPDATA"]
spotify_executable = "Spotify\\Spotify.exe"
path = os.path.join(roaming_folder, spotify_executable)

if os.path.exists(path):
    spotify_path=path
    print(spotify_path)


keyboard = Controller()    

def previous():
    #authorization
    redirect_uri = 'https://example.org/callback'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                client_secret=client_secret,
                                                redirect_uri=redirect_uri,
                                                scope="playlist-read-collaborative playlist-read-private playlist-modify-public playlist-modify-private user-read-currently-playing playlist-read-private user-modify-playback-state user-library-modify"))\
    
    try:
        sp.previous_track()
        print('Track skipped')
    except Exception:
        print('Could not skip track')

def next():
    #authorization
    redirect_uri = 'https://example.org/callback'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                client_secret=client_secret,
                                                redirect_uri=redirect_uri,
                                                scope="playlist-read-collaborative playlist-read-private playlist-modify-public playlist-modify-private user-read-currently-playing playlist-read-private user-modify-playback-state user-library-modify"))\
    
    try:
        sp.next_track()
        print('Track skipped')
    except Exception:
        print('Could not skip track')

def pause():
    #authorization
    redirect_uri = 'https://example.org/callback'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                client_secret=client_secret,
                                                redirect_uri=redirect_uri,
                                                scope="playlist-read-collaborative playlist-read-private playlist-modify-public playlist-modify-private user-read-currently-playing playlist-read-private user-modify-playback-state user-library-modify"))\
    
    isPlaying=False
    for proc in psutil.process_iter():
        if proc.name() == "Spotify.exe":
            # The Spotify process is already running, so we don't need to start it
            break
    else:
        # The Spotify process is not running, so we start it
        subprocess.Popen(spotify_path)
    try:
        isPlaying = sp.current_user_playing_track()[u'is_playing']
    except TypeError:
        subprocess.Popen(spotify_path)
        print(spotify_path)
        keyboard.press(Key.media_play_pause)
        print("pressed")
        keyboard.release(Key.media_play_pause)

    if isPlaying:
        try:
            sp.pause_playback()
            print('Stopping')
        except Exception:
            print('Could not stop')
    else:
        try:
            sp.start_playback()
            print('Playing')
        except Exception:
            print('Could not play')
    