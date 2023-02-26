import spotipy
import socket
import logging
import pickle
from authorization import sp, programdata_folder
import os
# import win32gui
# import win32api

try:
    with open(programdata_folder+"\playlist_config.txt", "rb") as f:
        dict = pickle.load(f)
except Exception as e:
    logging.info(e)
spotify_path = None
appdata = dict["appdata"]
spotify_executable = "Spotify\\Spotify.exe"
path = os.path.join(appdata, spotify_executable)
logging.info(path)
if os.path.exists(path):
    spotify_path = path
    print(spotify_path)


def previous():

    try:
        sp.previous_track()
        return ('Track skipped')
    except spotipy.client.SpotifyException as e:
        if e.http_status == 404:
            return ('Spotify not opened!')
        else:
            return ('Could not skip track')


def next():

    try:
        sp.next_track()
        return ('Track skipped')
    except spotipy.client.SpotifyException as e:
        if e.http_status == 404:
            return ('Spotify not opened!')
        else:
            return ('Could not skip track')


def pause():
    isPlaying = False
    device_name = socket.gethostname()

    # if win32gui.FindWindow(None, "Spotify"):
    #     print("window exists")
    #     pass

    # elif spotify_path != None:
    #     # The Spotify process is not running, so we start it
    #     try:
    #         win32api.ShellExecute(0, 'open', spotify_path, '', '', 1)
    #     except Exception:
    #         logging.info(Exception)
    try:
        isPlaying = sp.current_user_playing_track()[u'is_playing']
    except TypeError:
        print(Exception)

    if isPlaying:
        try:
            sp.pause_playback()
            return ('Paused')
        except spotipy.client.SpotifyException as e:
            if e.http_status == 404:
                return ('Spotify not opened!')
            else:
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
                    return ('Spotify not opened!')
                sp.transfer_playback(desired_device_id, force_play=True)
                return ('Playing')
            else:
                return ('Could not play')
