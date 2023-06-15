from tkinter import *
import spotipy
from spotipy.oauth2 import SpotifyOAuth as OriginalSpotifyOAuth
from spotipy.oauth2 import SpotifyStateError
from client_secrets import client_id, client_secret
import pickle
import os
import tkinter as tk
from urllib.parse import urlparse, parse_qs
from functools import partial

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
root.geometry('500x450')

part_text = StringVar()
part_label = Label(
    root, text='Select playlist you would like songs to be added to:', font=('bold', 10), pady=10)
part_label.grid(row=0, column=0)
part_text2 = StringVar()
part_label2 = Label(
    root, text='Select playlists you want to be able to play:', font=('bold', 10), pady=10)
part_label2.grid(row=2, column=0)

part_text3 = StringVar()
part_label3 = Label(
    root, text="Select multifunction button's mode:", font=('bold', 10), pady=10)
part_label3.grid(row=1, column=0)

playlists_list = list()
offset = 0


while True:
    playlists = sp.current_user_playlists()
    offset += 50
    playlists_list.extend(playlists['items'])
    if playlists['total'] <= len(playlists_list):
        break

# get all playlists
all_playlists_names = [track['name'] for track in playlists_list]
all_playlsts_ids = [track['id'] for track in playlists_list]

# get user playlists
playlists_list = [p for p in playlists_list if p['owner']['id'] == user_id]

playlists_names = [track['name'] for track in playlists_list]
playlists_ids = [track['id'] for track in playlists_list]


def output(options):
    try:
        with open(programdata_folder+"\playlist_config.txt", "rb") as f:
            dict = pickle.load(f)
    except:
        dict = {}

    options = menu.get()
    for position, item in enumerate(playlists_names):
        if item == options:
            place = position
            playlist_id = playlists_ids[place]
            print(dict)
            try:
                premium_volume = premiumvolume.get()
            except:
                premium_volume = False
            dict['premium_volume'] = premium_volume
            dict['id'] = playlist_id
            dict['name'] = options
            file = open(programdata_folder+"\playlist_config.txt", "wb")
            pickle.dump(dict, file)
            file.close()


def outputcheckbox():
    try:
        with open(programdata_folder+"\playlist_config.txt", "rb") as f:
            dict = pickle.load(f)
            print(dict)
    except:
        dict = {}
    if 'id' in dict:
        if dict['id'] == None:
            playlist_id = playlists_ids[0]
        else:
            playlist_id = dict['id']
    else:
        playlist_id = playlists_ids[0]
    options = menu.get()
    try:
        premium_volume = premiumvolume.get()
    except:
        premium_volume = False
    dict['premium_volume'] = premium_volume
    dict['id'] = playlist_id
    dict['name'] = options

    file = open(programdata_folder+"\playlist_config.txt", "wb")
    pickle.dump(dict, file)
    file.close()


def multi(selected):
    try:
        with open(programdata_folder+"\playlist_config.txt", "rb") as f:
            dict = pickle.load(f)
    except:
        dict = {}

    dict['multi'] = selected
    file = open(programdata_folder+"\playlist_config.txt", "wb")
    pickle.dump(dict, file)
    file.close()


try:
    with open(programdata_folder+"\playlist_config.txt", "rb") as f:
        dict = pickle.load(f)

except:
    dict = {'id': playlists_ids[0], 'name': playlists_names[0],
            'appdata': appdata, 'premium_volume': False, 'playlists_ids': playlists_ids,
            'playlists_names': playlists_names, 'play_playlists_names': [], 'play_playlists_ids': [], 'selected_play': all_playlsts_ids[0], 'multi': 'Recommendations'}
    file = open(programdata_folder+"\playlist_config.txt", "wb")
    pickle.dump(dict, file)
    file.close()

if 'play_playlists_ids' not in dict:
    file = open(programdata_folder+"\playlist_config.txt", "wb")
    pickle.dump({'id': playlists_ids[0], 'name': playlists_names[0],
                 'appdata': appdata, 'premium_volume': False, 'playlists_ids': playlists_ids,
                'playlists_names': playlists_names, 'play_playlists_names': [], 'play_playlists_ids': [], 'selected_play': all_playlsts_ids[0], 'multi': 'Recommendations'}, file)
    file.close()


def exit_program():
    with open(programdata_folder+"\playlist_config.txt", "rb") as f:
        data = pickle.load(f)
    file = open(programdata_folder+"\playlist_config.txt", "wb")
    data['playlists_ids'] = playlists_ids
    data['playlists_names'] = playlists_names
    pickle.dump(data, file)
    file.close()
    root.destroy()
# app


menu = StringVar()
menu_multi = StringVar()
premiumvolume = IntVar()
menu.set(dict['name'])


premiumvolume.set(dict['premium_volume'])
try:
    selected_playlists_ids = dict['play_playlists_ids']
    selected_playlists_names = dict['play_playlists_names']
    selected_play = dict['selected_play']
except:
    selected_playlists_ids = []
    selected_playlists_names = []
    selected_play = []


print(selected_play)

# menu for add to playlist
if playlists_names == None:
    playlists_names = ['No playlists created']
    command = None
else:
    command = output

drop = OptionMenu(root, menu, *playlists_names, command=command)
drop.grid(row=0, column=3)
drop.config(justify='left', width=15)

# menu for multifunction button
options = list
options = ['Recommendations', 'Play playlist']
try:
    menu_multi.set(dict['multi'])
except:
    menu_multi.set(options[0])

drop = OptionMenu(root, menu_multi, *options, command=multi)
drop.grid(row=1, column=3)
drop.config(justify='left', width=15)


# menu for play playlist

canvas = Canvas(root, width=50, bg='white')
canvas.grid(row=3, column=0, sticky='nsew')


scrollbar = Scrollbar(root, orient=VERTICAL, command=canvas.yview)
scrollbar.grid(row=3, column=2, sticky='ns')
canvas.config(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(
    scrollregion=canvas.bbox('all')))
canvas_frame = Frame(canvas)
canvas.create_window((0, 0), window=canvas_frame, anchor='nw')

frame = Frame(canvas_frame, bg='white')
frame.grid(row=0, column=0)

var_list = []


def choose(index, task):
    with open(programdata_folder+"\playlist_config.txt", "rb") as f:
        data = pickle.load(f)
    if var_list[index].get() == 1:
        selected_playlists_ids.append(all_playlsts_ids[index])
        selected_playlists_names.append(task)
    else:
        selected_playlists_ids.remove(all_playlsts_ids[index])
        selected_playlists_names.remove(task)
    file = open(programdata_folder+"\playlist_config.txt", "wb")
    data['play_playlists_ids'] = selected_playlists_ids
    data['play_playlists_names'] = selected_playlists_names
    pickle.dump(data, file)
    file.close()
    if data['selected_play'] not in selected_playlists_ids:
        with open(programdata_folder+"\playlist_config.txt", "rb") as f:
            dict = pickle.load(f)
        if selected_playlists_ids == []:
            dict['selected_play'] = all_playlsts_ids[0]
        else:
            dict['selected_play'] = selected_playlists_ids[0]
        file = open(programdata_folder+"\playlist_config.txt", "wb")
        pickle.dump(dict, file)
        file.close()


for index, task in enumerate(all_playlists_names):
    var_list.append(IntVar(value=0))
    Checkbutton(frame, variable=var_list[index], text=task, anchor='w', bg='white', command=partial(
        choose, index, task)).pack(anchor='w')
    if task in selected_playlists_names:
        var_list[index].set(1)


frame.bind('<Configure>', lambda e: canvas.configure(
    scrollregion=canvas.bbox('all')))
canvas.create_window((0, 0), window=canvas_frame, anchor='nw')


# exit button
exit_button = Button(root, text="Save & Exit", command=exit_program)
exit_button.grid(row=4, column=3)
exit_button.config(justify='left', width=10)

checkbox = Checkbutton(root, text="Change desktop volume instead of Spotify",
                       variable=premiumvolume, command=outputcheckbox)
checkbox.grid(row=4, column=0)

root.mainloop()
