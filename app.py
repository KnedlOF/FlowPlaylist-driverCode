from tkinter import *
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from client_secrets import client_id, client_secret
import pickle


app=Tk()

#changes logo
photo=PhotoImage(file="pic.png")
app.iconphoto(False,photo) 
app.title('Spotify keyboard')
app.geometry('700x350')

part_text=StringVar()
part_label=Label(app, text='Select playlist you would like songs to be added to:', font=('bold', 10), pady=10)
part_label.grid(row=0, column=0)




redirect_uri = 'https://example.org/callback'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope="playlist-read-collaborative playlist-read-private playlist-modify-public playlist-modify-private user-read-currently-playing playlist-read-private user-modify-playback-state user-library-modify"))



user_id = sp.current_user()['id']
        
playlists_list=list()
offset=0


while True:
    playlists=sp.current_user_playlists()
    offset += 50
    playlists_list.extend(playlists['items'])
    if playlists['total'] <= len(playlists_list):
        break

playlists_list = [p for p in playlists_list if p['owner']['id'] == user_id]

playlists_names = [track['name'] for track in playlists_list]
playlists_ids = [track['id'] for track in playlists_list]


def output(options):
    options=menu.get()
    for position, item in enumerate(playlists_names):
        if item==options:
            place=position
            playlist_id=playlists_ids[place]
            print(playlist_id)
            file=open("playlist_config.txt", "wb")
            pickle.dump({'id':playlist_id,'name':options},file)
            file.close()

           
           

try:             
    with open('playlist_config.txt', "rb") as f:
        dict=pickle.load(f)
        
except:
    dict = {'name': 'Select playlist'}
     
#dropdown menu
menu=StringVar()
menu.set(dict['name'])
drop=OptionMenu(app, menu, *playlists_names, command=output)
drop.grid(row=1, column=0)
exit_button = Button(app, text="Exit", command=app.destroy)
exit_button.grid(row=1, column=5)

app.mainloop()
