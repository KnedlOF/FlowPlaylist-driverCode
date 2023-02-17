# Install python3 HID package https://pypi.org/project/hid/

from buttons_media import previous, next, pause
from add_to_playlist import playlist
from recommended import recommend
from like import like
from authorization import *

import threading
import struct
import time
import hid

timeout = 1


# default is TinyUSB (0xcafe), Adafruit (0x239a), RaspberryPi (0x2e8a), Espressif (0x303a) VID
USB_VID = 0x2e8a


# check for device
def device_is_connected(vendor_id, product_id):
    for device in hid.enumerate():
        if device['vendor_id'] == vendor_id and device['product_id'] == product_id:
            return True
    return False


def get_song_info():
    # gets info about song
    while True:
        song_info_once(delay=2)

# gets info about song, just once, for when you skip songs


def song_info_once(delay=0.1):
    try:
        track_info = sp.current_user_playing_track()
        if track_info is None:
            print('Spotify not playing any tracks.')
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

        print(track_name)
        print(track_artists)
        str_out = b'\x002'
        str_out += track_artists.encode('utf-8')
        dev.write(str_out)
        str_out = b'\x003'
        str_out += track_name.encode('utf-8')
        dev.write(str_out)
        time.sleep(delay)
    except:
        time.sleep(delay)


# parallel loop
thread = threading.Thread(target=get_song_info)
thread.start()
# loop
while True:

    # get device info
    for device_info in hid.enumerate(USB_VID):
        print(device_info)
        vendor_id = device_info['vendor_id']
        product_id = device_info['product_id']

        # make device object
        dev = hid.Device(vendor_id, product_id)
        if dev:
            new_volume = 0
            request_in_progress = False
            previous_volume = 0
            str_out = b'\x001'
            dev.write(str_out)

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
                    recomm_btn = str_in[1]
                    playlist_btn = str_in[2]
                    prev_btn = str_in[3]
                    play_btn = str_in[4]
                    next_btn = str_in[5]
                    volume = str_in[6]
                    volume_change = str_in[7]
                    print("Received from HID Device:",
                          struct.unpack('<8B', str_in), '\n')

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
                    if playlist_btn == 1:
                        playlist_text = playlist()
                        str_out = b'\x004'
                        str_out += playlist_text.encode('utf-8')
                        dev.write(str_out)
                    if prev_btn == 1:
                        prev_text = previous()
                        str_out = b'\x004'
                        str_out += prev_text.encode('utf-8')
                        dev.write(str_out)
                        song_info_once()
                    if next_btn == 1:
                        next_text = next()
                        str_out = b'\x004'
                        str_out += next_text.encode('utf-8')
                        dev.write(str_out)
                        song_info_once()
                    if play_btn == 1:
                        pause_text = pause()
                        str_out = b'\x004'
                        str_out += pause_text.encode('utf-8')
                        dev.write(str_out)

                    # for big volume changes it sends volume by at least 5
                    if volume_change == 1 and abs(volume-new_volume) >= 5:
                        new_volume = volume
                        if not request_in_progress:
                            request_in_progress = True
                            try:
                                volume_set = sp.volume(new_volume)
                            except (spotipy.SpotifyException, TimeoutError) as e:
                                print(str(e))
                                time.sleep(3)
                            print("Volume changed on: ", new_volume)
                            previous_volume = volume
                            request_in_progress = False
                    # for small changes it sends volume by 1
                    elif volume_change == 0 and new_volume != volume:
                        new_volume = volume
                        if not request_in_progress:
                            request_in_progress = True
                            try:
                                volume_set = sp.volume(new_volume)
                            except (spotipy.SpotifyException, TimeoutError) as e:
                                print(str(e))
                                time.sleep(3)
                            print("Volume changed on: ", new_volume)
                            previous_volume = volume
                            request_in_progress = False

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
