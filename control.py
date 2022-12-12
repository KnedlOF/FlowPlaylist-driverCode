import serial
from like import *
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from secrets import client_id, client_secret

serialport=serial.Serial('COM3', baudrate=9600, timeout=2)



while 1!=0:
    arduinodata=serialport.readline()
     
    if arduinodata:
       string=arduinodata.decode()
       stripped_data=string.strip()
       values=stripped_data.split(",")
       button1=int(values[0])
       button2=values[1]
       button3=values[2]
       print(button1)
       if button1==1:
            like()
            button1=0
        
    