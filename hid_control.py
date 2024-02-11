# Install python3 HID package https://pypi.org/project/hid/

from buttons_media import previous, next, pause
from add_to_playlist import playlist
from recommended import recommend, play_playlist
from like import like
from authorization import *

import threading
import struct
import time
import hid
import pickle
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

timeout = 1
prev_song = None
prev_artists = None
prev_playlist_btn = False
prev_play_playlist = False
hotkey = False
hotkey2 = False
recomm_btn = 0
play_playlist_btn = 0 
last_modified = os.path.getmtime(programdata_folder+"\playlist_config.txt")
# default is TinyUSB (0xcafe), Adafruit (0x239a), RaspberryPi (0x2e8a), Espressif (0x303a) VID
USB_VID = [0x2e8a, 0x239a]


# check for device


def device_is_connected(vendor_id, product_id):
    for device in hid.enumerate():
        if device['vendor_id'] == vendor_id and device['product_id'] == product_id:
            return True
    return False


def get_song_info():
    global last_modified
    # gets info about song
    while True:
        song_info_once(delay=2)  
         #checks for changes in settings, for updating LEDs     
        try:   
            current_modified = os.path.getmtime(programdata_folder+"\playlist_config.txt")
        except Exception as e: 
            print("Error:", e)
        if current_modified != last_modified:
            send_color()
            last_modified = current_modified  

# gets info about song, just once, for when you skip songs


def song_info_once(delay=0.1):
    global prev_song
    global prev_artists

    try:
        if delay == 0.1:
            prev_song = None
            prev_artists = None
        track_info = sp.current_user_playing_track()
        if track_info is None:
            prev_song = None
            prev_artists = None
            print('Spotify not playing any tracks.')
            track_artistsblank = ''
            track_nameblank = ''
            clear()
            str_out = b'\x002'
            str_out += track_artistsblank.encode('utf-8')
            dev.write(str_out)
            str_out = b'\x003'
            str_out += track_nameblank.encode('utf-8')
            dev.write(str_out)
        track_name = track_info['item']['name']
        # it cuts track name if it is longer than 46 characters
        if len(track_name) >= 46:
            track_name = track_name[:43]+'...'

        artists = []
        for artist in track_info['item']['artists']:
            artists.append(artist['name'])
        track_artists = ", ".join(artists)

        # it cuts artists name if it is longer than 46 characters
        if len(track_artists) >= 46:
            track_artists = track_artists[:43]+'...'

        if prev_artists != track_artists or prev_song != track_name:
            print(track_name)
            print(track_artists)
            clear()
            str_out = b'\x002'
            str_out += track_artists.encode('utf-8')
            dev.write(str_out)
            str_out = b'\x003'
            str_out += track_name.encode('utf-8')
            dev.write(str_out)
            prev_song = track_name
            prev_artists = track_artists
        time.sleep(delay)
    except:
        time.sleep(delay)


def clear():
    nothing = ' '
    str_out = b'\x002'
    str_out += nothing.encode('utf-8')
    dev.write(str_out)
    str_out = b'\x003'
    str_out += nothing.encode('utf-8')
    dev.write(str_out)


def send_color():
    with open(programdata_folder+"\playlist_config.txt", "rb") as f:
        data = pickle.load(f)
    led_mode=data['led_mode']
    brightness=data['brightness']
    if led_mode=="Static color":
        led_color=data['leds']
    else: 
        led_color=led_mode
    print("Color changed to:", led_color, "Brightness to:", brightness)
    #send color
    str_out=b'\x005'
    str_out +=led_color.encode('utf-8')
    dev.write(str_out)
    #send brightness
    str_out=b'\x006'
    str_out +=brightness.encode('utf-8')
    dev.write(str_out)

# parallel loop
thread = threading.Thread(target=get_song_info)
thread.start()
# loop
while True:

    # get device info

    for device in USB_VID:
        for device_info in hid.enumerate(device):
            print(device_info)
            vendor_id = device_info['vendor_id']
            product_id = device_info['product_id']
            # make device object
            dev = hid.Device(vendor_id, product_id)
            if dev:
                str_out = b'\x001'
                dev.write(str_out)
                new_volume=0
                song_info_once()
                send_color()
                while True:

                    # Get input from console and encode to UTF8 for array of chars.//
                    # hid generic inout is single report therefore by HIDAPI requirement
                    # it must be preceeded with 0x00 as dummy reportID
                    # str_out = b'\x00'
                    # str_out += input("Send text to HID Device : ").encode('utf-8')
                    # dev.write(str_out)
                    # reading input
                    
                    try:
                        
                        str_in = dev.read(8)
                        like_btn = str_in[0]
                        multi_btn = str_in[1]
                        playlist_btn = str_in[2]
                        prev_btn = str_in[3]
                        play_btn = str_in[4]
                        next_btn = str_in[5]
                        volume = str_in[6]
                        #volume_change = str_in[7]
                        print("Received from HID Device:",
                              struct.unpack('<8B', str_in), '\n')
                        


                        if multi_btn == 1:
                            with open(programdata_folder+"\playlist_config.txt", "rb") as f:
                                data = pickle.load(f)
                            multi = data['multi']
                            print(multi)
                            if multi == 'Play playlist':
                                play_playlist_btn = str_in[1]
                                recomm_btn = 0

                            elif multi == 'Recommendations':
                                recomm_btn = str_in[1]
                                play_playlist_btn = 0
                        else:
                            recomm_btn = 0
                            play_playlist_btn = 0

                        if like_btn == 1:
                            like_text = like()
                            str_out = b'\x004'
                            str_out += like_text.encode('utf-8')
                            dev.write(str_out)

                        if recomm_btn == 1:
                            recomm_text = recommend()
                            str_out = b'\x004'
                            str_out += recomm_text.encode('utf-8')
                            dev.write(str_out)

                        # play playlist button
                        if play_playlist_btn == 1:
                            prev_play_playlist = True
                        if play_playlist_btn == 0 and prev_play_playlist == True and hotkey2 == False:
                            play_text = play_playlist()
                            print(play_text)
                            str_out = b'\x004'
                            str_out += play_text.encode(
                                'utf-8')
                            dev.write(str_out)
                            prev_play_playlist = False
                        if play_playlist_btn == 0:
                            prev_play_playlist = False
                            hotkey2 = False
                        elif play_playlist_btn == 1 and prev_play_playlist == True and next_btn:
                            hotkey2 = True
                            with open(programdata_folder+"\playlist_config.txt", "rb") as f:
                                data = pickle.load(f)
                            selected_playlist = data['selected_play']
                            selected_playlists_ids = data['play_playlists_ids']
                            selected_playlists_names = data['play_playlists_names']

                            if selected_playlist in selected_playlists_ids:
                                index = selected_playlists_ids.index(
                                    selected_playlist)
                                number = len(selected_playlists_ids)-1
                                index = index+1
                                if index > number:
                                    index = 0
                                data['selected_play'] = selected_playlists_ids[index]
                                with open(programdata_folder + "\playlist_config.txt", "wb") as file:
                                    pickle.dump(data, file)
                                text_out = selected_playlists_names[index]
                            else:
                                text_out = 'None selected'
                            print(text_out)
                            str_out = b'\x004'
                            str_out += text_out.encode(
                                'utf-8')
                            dev.write(str_out)
                            prev_play_playlist = False

                        # it activates when button goes from 1 to 0
                        if playlist_btn == 1:
                            prev_playlist_btn = True
                        if playlist_btn == 0 and prev_playlist_btn == True and hotkey == False:
                            playlist_text = playlist()
                            str_out = b'\x004'
                            str_out += playlist_text.encode('utf-8')
                            dev.write(str_out)
                            prev_playlist_btn = False
                        if playlist_btn == 0:
                            hotkey = False
                            prev_playlist_btn = False
                        elif playlist_btn == 1 and prev_playlist_btn == True and next_btn:
                            hotkey = True
                            with open(programdata_folder+"\playlist_config.txt", "rb") as f:
                                data = pickle.load(f)
                            playlists_names = data['playlists_names']
                            playlists_ids = data['playlists_ids']
                            current_playlist = data['name']
                            if current_playlist in playlists_names:
                                index = playlists_names.index(current_playlist)
                            num_playlists = len(playlists_names)-1
                            index = index+1
                            if index > num_playlists:
                                index = 0
                            data['id'] = playlists_ids[index]
                            data['name'] = playlists_names[index]
                            print(data['name'])
                            with open(programdata_folder + "\playlist_config.txt", "wb") as file:
                                pickle.dump(data, file)
                            str_out = b'\x004'
                            str_out += playlists_names[index].encode('utf-8')
                            dev.write(str_out)
                            prev_playlist_btn = False

                        if prev_btn == 1 and hotkey == False and hotkey2 == False:
                            prev_text = previous()
                            str_out = b'\x004'
                            str_out += prev_text.encode('utf-8')
                            dev.write(str_out)
                            song_info_once()

                        if next_btn == 1 and hotkey == False and hotkey2 == False:
                            next_text = next()
                            str_out = b'\x004'
                            str_out += next_text.encode('utf-8')
                            dev.write(str_out)
                            song_info_once()

                        if play_btn == 1 and hotkey == False and hotkey2 == False:
                            pause_text = pause()
                            str_out = b'\x004'
                            str_out += pause_text.encode('utf-8')
                            dev.write(str_out)
                            song_info_once()

                        try:
                            with open(programdata_folder+"\playlist_config.txt", "rb") as f:
                                dict = pickle.load(f)

                        except:
                            dict = {}

                        premiumvolume = dict['premium_volume']

                        # non premium volume, changes desktop volume
                        if premiumvolume:
                            set_volume = volume/100
                            devices = AudioUtilities.GetSpeakers()
                            interface = devices.Activate(
                                IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                            volume = cast(interface, POINTER(
                                IAudioEndpointVolume))
                            volume.SetMasterVolumeLevelScalar(set_volume, None)

                        # premium volume, changes volume in spotify
                        else:
                            if (new_volume!=volume):
                                new_volume=volume
                                try:
                                    volume_set = sp.volume(new_volume)
                                    print("Volume changed on: ", new_volume)
                                except spotipy.SpotifyException as e:
                                    if e.http_status == 404:
                                        print('Skipping volume')
                                    if e.http_status == 403:
                                        print("Too many requests!!")
                                        str_out = b'\x004'
                                        str_out += "STOP! wait 30s".encode('utf-8')
                                        dev.write(str_out)
                                        time.sleep(31)

                                except Exception as e:
                                    print(e) 
                        str_out = b'\x007'
                        str_out += "request finnished".encode('utf-8')
                        dev.write(str_out)

                            
                    # if device disconnects, it will try again once a second
                    except hid.HIDException as e:
                        if "The device is not connected" in str(e):
                            if not device_is_connected(vendor_id, product_id):
                                print("Error: Device is not connected")
                                time.sleep(1)
                            else:
                                break
                        else:
                            print(str(e))
                            break
                    except Exception as e:
                        print(e)        