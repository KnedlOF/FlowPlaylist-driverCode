from tkinter import *
import spotipy
from spotipy.oauth2 import SpotifyOAuth as OriginalSpotifyOAuth
from spotipy.oauth2 import SpotifyStateError
from client_secrets import client_id, client_secret
import pickle
import os
import tkinter as tk
from urllib.parse import urlparse, parse_qs


# modify library


class MyGUI:
    def __init__(self, state=None):
        self.window = tk.Tk()
        self.state = state
        self.photo = PhotoImage(file="pic.png")
        self.window.iconphoto(False, self.photo)
        self.window.title("Authorization URL")
        self.label = tk.Label(
            self.window, text="Enter the URL you were redirected to:")
        self.label.pack()
        self.entry = tk.Entry(self.window, width=50)
        self.entry.pack()
        self.button = tk.Button(
            self.window, text="Submit", command=self.submit)
        self.button.pack()
        self.code = None

    def submit(self):
        url = self.entry.get()
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        state = query_params.get('state', [''])[0]
        self.code = query_params.get('code', [''])[0]
        if self.state is not None and self.state != state:
            raise SpotifyStateError(self.state, state)
        self.window.destroy()

    def show(self):
        self.window.mainloop()

# modify library, so instead of pasting url in console, you need to paste it in tinker


class SpotifyOAuth(OriginalSpotifyOAuth):
    def _get_auth_response_interactive(self, open_browser=False):
        if open_browser:
            self._open_auth_url()
            gui = MyGUI()
            gui.show()
            code = gui.code
        else:
            url = self.get_authorize_url()
            print(f"Go to the following URL: {url}")
            response = input("Enter the URL you were redirected to: ")
            state, code = SpotifyOAuth.parse_auth_response_url(response)
            if self.state is not None and self.state != state:
                raise SpotifyStateError(self.state, state)
        return code


# make folder for cache
programdata_folder = os.environ["PROGRAMDATA"]+'\Spotify Keyboard'
appdata = os.environ["APPDATA"]

if not os.path.exists(programdata_folder):
    os.makedirs(programdata_folder)

cache_path = programdata_folder+'\.cache'

redirect_uri = 'https://example.org/callback'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               cache_path=cache_path,
                                               scope="playlist-read-collaborative playlist-read-private playlist-modify-public playlist-modify-private user-read-currently-playing playlist-read-private user-modify-playback-state user-library-modify user-read-playback-state"))

user_id = sp.current_user()['id']

root = Tk()
# changes logo
photo = PhotoImage(file="pic.png")
root.iconphoto(False, photo)
root.title('Spotify keyboard')
root.geometry('350x200')

part_text = StringVar()
part_label = Label(
    root, text='Select playlist you would like songs to be added to:', font=('bold', 10), pady=10)
part_label.grid(row=0, column=0)


playlists_list = list()
offset = 0


while True:
    playlists = sp.current_user_playlists()
    offset += 50
    playlists_list.extend(playlists['items'])
    if playlists['total'] <= len(playlists_list):
        break

playlists_list = [p for p in playlists_list if p['owner']['id'] == user_id]

playlists_names = [track['name'] for track in playlists_list]
playlists_ids = [track['id'] for track in playlists_list]


def output(options):
    options = menu.get()
    for position, item in enumerate(playlists_names):
        if item == options:
            place = position
            playlist_id = playlists_ids[place]
            print(playlist_id)
            premium_volume = premiumvolume.get()
            file = open(programdata_folder+"\playlist_config.txt", "wb")
            pickle.dump({'id': playlist_id, 'name': options,
                        'appdata': appdata, 'premium_volume': premium_volume}, file)
            file.close()


def outputcheckbox():
    try:
        with open(programdata_folder+"\playlist_config.txt", "rb") as f:
            dict = pickle.load(f)

    except:
        dict = {}
    if 'id' in dict:
        playlist_id = dict['id']
    else:
        playlist_id = playlists_ids[0]
    options = menu.get()
    premium_volume = premiumvolume.get()
    file = open(programdata_folder+"\playlist_config.txt", "wb")
    pickle.dump({'id': playlist_id, 'name': options,
                'appdata': appdata, 'premium_volume': premium_volume}, file)
    file.close()


try:
    with open(programdata_folder+"\playlist_config.txt", "rb") as f:
        dict = pickle.load(f)

except:
    dict = {'name': playlists_names[0],
            'premium_volume': 'false', 'id': playlists_ids[0]}


# app

menu = StringVar()
premiumvolume = IntVar()
menu.set(dict['name'])
premiumvolume.set(dict['premium_volume'])

if playlists_names == None:
    playlists_names = ['No playlists created']
    command = None
else:
    command = output
drop = OptionMenu(root, menu, *playlists_names, command=command)
drop.grid(row=1, column=0)

exit_button = Button(root, text="Exit", command=root.destroy)
exit_button.grid(row=1, column=5)

checkbox = Checkbutton(root, text="Change volume of Spotify (requires Premium)",
                       variable=premiumvolume, command=outputcheckbox)
checkbox.grid(row=2, column=0)

root.mainloop()
