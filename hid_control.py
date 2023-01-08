# Install python3 HID package https://pypi.org/project/hid/
from re import S
import hid
import time
import struct
import threading

from like import *
from recommended import recommend
from add_to_playlist import playlist
from buttons_media import previous, next, pause


# authorization
redirect_uri = 'https://example.org/callback'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                client_secret=client_secret,
                                                redirect_uri=redirect_uri,
                                                scope="playlist-read-collaborative playlist-read-private playlist-modify-public playlist-modify-private user-read-currently-playing playlist-read-private user-modify-playback-state user-library-modify"))


timeout=1


# default is TinyUSB (0xcafe), Adafruit (0x239a), RaspberryPi (0x2e8a), Espressif (0x303a) VID
USB_VID = 0x2e8a


#check for device
def device_is_connected(vendor_id, product_id):
    for device in hid.enumerate():
        if device['vendor_id'] == vendor_id and device['product_id'] == product_id:
            return True
    return False

def get_song_info():
#gets info about song
    while True:
            try:
                track_info=sp.current_user_playing_track()
                if track_info is None:
                    print('Spotify not playing any tracks.')

                track_name=track_info['item']['name']
                if len(track_name)>=46:
                    track_name=track_name[:43]+'...'
                artists=[]
                for artist in track_info['item']['artists']:
                    artists.append(artist['name'])
                track_artists=", ".join(artists)
                if len(track_artists)>=46:
                    track_artists=track_artists[:43]+'...'
                print(track_name)
                print(track_artists)
                str_out=b'\x002'
                str_out+=track_artists.encode('utf-8')
                time.sleep(0.1)
                dev.write(str_out)
                str_out=b'\x003'
                str_out+=track_name.encode('utf-8')
                dev.write(str_out)    
                time.sleep(2) 
            except:
                time.sleep(2)
#gets info about song, just once, for when you skip songs

def song_info_once():
    try:
        track_info=sp.current_user_playing_track()
        if track_info is None:
            print('Spotify not playing any tracks.')
        track_name=track_info['item']['name']
        if len(track_name)>=46:
            track_name=track_name[:43]+'...'
        artists=[]
        for artist in track_info['item']['artists']:
            artists.append(artist['name'])
        track_artists=", ".join(artists)
        if len(track_artists)>=46:
            track_artists=track_artists[:43]+'...'
        print(track_name)
        print(track_artists)
        str_out=b'\x002'
        str_out+=track_artists.encode('utf-8')
        time.sleep(0.01)
        dev.write(str_out)
        str_out=b'\x003'
        str_out+=track_name.encode('utf-8')
        dev.write(str_out)    
    except:
        time.sleep(0.1)    
#parallel loop
thread = threading.Thread(target=get_song_info)
thread.start()
#loop  
while True:

    #get device info
    for device_info in hid.enumerate(USB_VID):
        print(device_info)
        vendor_id=device_info['vendor_id']
        product_id=device_info['product_id']

        #make device object
        dev = hid.Device(vendor_id, product_id)
        if dev:
            new_volume=0
            request_in_progress=False
            previous_volume=0
            str_out=b'\x001'
            dev.write(str_out)
            
            while True:
                
                
                # Get input from console and encode to UTF8 for array of chars.//
                # hid generic inout is single report therefore by HIDAPI requirement
                # it must be preceeded with 0x00 as dummy reportID
                # str_out = b'\x00'
                # str_out += input("Send text to HID Device : ").encode('utf-8')
                # dev.write(str_out)
                
                #reading input
                try:
                    str_in = dev.read(8)
                    like_btn=str_in[0]
                    recomm_btn=str_in[1]
                    playlist_btn=str_in[2]
                    prev_btn=str_in[3]
                    play_btn=str_in[4]
                    next_btn=str_in[5]
                    volume=str_in[6]
                    volume_change=str_in[7]
                    print("Received from HID Device:", struct.unpack('<8B', str_in), '\n')
                    
                    if like_btn==1:
                        like()
                        str_out=b'\x004'
                        dev.write(like)
                    if recomm_btn==1:
                        recommend()
                    if playlist_btn==1:
                        playlist()
                    if prev_btn==1:
                        previous()
                        song_info_once()
                    if next_btn==1:
                        next()
                        song_info_once()
                    if play_btn==1:
                        pause()
                    
                    #for big volume changes it sends volume by 5
                    if volume_change==1 and volume%5==0:
                        new_volume=volume
                        if not request_in_progress:
                            request_in_progress=True
                            try:
                                volume_set = sp.volume(new_volume)
                            except (spotipy.SpotifyException,TimeoutError) as e:
                                print (str(e))
                                time.sleep(3)
                            print("Volume changed on: ", new_volume)
                            previous_volume=volume
                            request_in_progress=False
                    #for small changes it sends volume by 1        
                    elif volume_change==0 and new_volume!=volume:
                        new_volume=volume
                        if not request_in_progress:
                            request_in_progress=True
                            try:
                                volume_set = sp.volume(new_volume)
                            except (spotipy.SpotifyException,TimeoutError) as e:
                                print (str(e))
                                time.sleep(3)
                            print("Volume changed on: ", new_volume)
                            previous_volume=volume
                            request_in_progress=False

                #if device disconnects, it will try again once a second    
                except hid.HIDException as e:
                    if "The device is not connected" in str(e):
                        if not device_is_connected(vendor_id, product_id):
                            print("Error: Device is not connected")
                            time.sleep(1)
                        else:
                            break
                    else:
                        print (str(e))
                        break

                    
