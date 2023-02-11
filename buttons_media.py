import spotipy
from spotipy.oauth2 import SpotifyOAuth
from client_secrets import client_id, client_secret
# import subprocess
import os
import socket
from pynput.keyboard import Key, Controller
# import time
# import win32gui

# finds path to roaming and sets spotify path
programdata_folder = os.environ["PROGRAMDATA"]+'\Spotify Keyboard'

if not os.path.exists(programdata_folder):
    os.makedirs(programdata_folder)


# spotify_executable = "Spotify\\Spotify.exe"
# path = os.path.join(roaming_folder, spotify_executable)

# if os.path.exists(path):
#     spotify_path = path
#     print(spotify_path)


keyboard = Controller()


def previous():
    # authorization
    redirect_uri = 'https://example.org/callback'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri=redirect_uri,
                                                   scope="playlist-read-collaborative playlist-read-private playlist-modify-public playlist-modify-private user-read-currently-playing playlist-read-private user-modify-playback-state user-library-modify"))\

    try:
        sp.previous_track()
        return ('Track skipped')
    except Exception:
        return ('Could not skip track')


def next():
    # authorization
    redirect_uri = 'https://example.org/callback'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri=redirect_uri,
                                                   scope="playlist-read-collaborative playlist-read-private playlist-modify-public playlist-modify-private user-read-currently-playing playlist-read-private user-modify-playback-state user-library-modify"))\

    try:
        sp.next_track()
        return ('Track skipped')
    except Exception:
        return ('Could not skip track')


def pause():
    # authorization
    redirect_uri = 'https://example.org/callback'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri=redirect_uri,
                                                   scope="playlist-read-collaborative playlist-read-private playlist-modify-public playlist-modify-private user-read-currently-playing playlist-read-private user-modify-playback-state user-library-modify"))\


    isPlaying = False
    device_name = socket.gethostname()

    # def WindowExists(window_name):
    #     try:
    #         win32gui.FindWindow(None, window_name)
    #         return True
    #     except:
    #         return False

    # def IsMinimized(window_name):
    #     hwnd = win32gui.FindWindow(None, window_name)
    #     if hwnd:
    #         return win32gui.IsIconic(hwnd)
    #     return False

    # if WindowExists("Spotify") and not IsMinimized("Spotify"):
    #     pass

    # else:
    #     # The Spotify process is not running, so we start it
    #     subprocess.Popen(spotify_path)
    try:
        isPlaying = sp.current_user_playing_track()[u'is_playing']
    except TypeError:
        print(Exception)

        # subprocess.Popen(spotify_path)
        # print(spotify_path)
        # time.sleep(0.5)
        # keyboard.press(Key.media_play_pause)
        # print("pressed")
        # keyboard.release(Key.media_play_pause)

    if isPlaying:
        try:
            sp.pause_playback()
            return ('Stoped')
        except Exception:
            return ('Could not stop')
    else:
        try:
            sp.start_playback()
            return ('Playing')

        except spotipy.client.SpotifyException as e:
            if e.http_status == 404:
                desired_device_id = None
                devices = sp.devices()
                for device in devices['devices']:
                    if device['name'].lower() == device_name.lower() and device['type'] == 'Computer':
                        desired_device_id = device['id']
                        print(desired_device_id)
                if desired_device_id is None:
                    return ("Could't find device")
                sp.transfer_playback(desired_device_id, force_play=True)
                return ('Playing')
            else:
                return ('Could not play')
