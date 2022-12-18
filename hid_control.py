# Install python3 HID package https://pypi.org/project/hid/
from re import S
import hid
import time
from like import *
from recommended import *
from add_to_playlist import *

# authorization
redirect_uri = 'https://example.org/callback'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                client_secret=client_secret,
                                                redirect_uri=redirect_uri,
                                                scope="playlist-read-collaborative playlist-read-private playlist-modify-public playlist-modify-private user-read-currently-playing playlist-read-private user-modify-playback-state user-library-modify"))


# default is TinyUSB (0xcafe), Adafruit (0x239a), RaspberryPi (0x2e8a), Espressif (0x303a) VID
USB_VID = 0x2e8a

#check for device
def device_is_connected(vendor_id, product_id):
    for device in hid.enumerate():
        if device['vendor_id'] == vendor_id and device['product_id'] == product_id:
            return True
    return False



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
            while True:
                # Get input from console and encode to UTF8 for array of chars.
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
                    volume=int(((str_in[6]+1)*100)/255)
                    print("Received from HID Device:", str_in, '\n')
                    
                    if like_btn==1:
                        like()
                    if recomm_btn==1:
                        recommend()
                    if playlist_btn==1:
                        playlist()
                    if volume:
                            volume_set = sp.volume(volume)
                            print("Volume changed on: ")
                            print(volume)
                            
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
        
                    
