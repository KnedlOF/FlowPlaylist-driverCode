import spotipy
from spotipy.oauth2 import SpotifyOAuth
from client_secrets import client_id, client_secret
import time
import pickle

redirect_uri = 'https://example.org/callback'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope="playlist-read-collaborative playlist-read-private playlist-modify-public playlist-modify-private user-read-currently-playing"))

MAX_PLAYLISTS = 9
offset = 0
pls = list()
pls_selected = list()


try:
    user_id = sp.current_user()['id']
    user_name = sp.current_user()['display_name']

    while True:
        pl = sp.current_user_playlists(limit=50, offset=offset)
        offset += 50
        pls.extend(pl['items'])
        if pl['total'] <= len(pls):
            break

    pls = [p for p in pls if p['owner']['id'] == user_id]
    pls.sort(key=lambda j: j['name'])

    print('\nHi {},\nHere are your playlists:\n'.format(user_name))
    time.sleep(2)
    for i, p in enumerate(pls):
        print('{}: {}'.format(i + 1, p['name']))

    while len(pls_selected) < MAX_PLAYLISTS:
        _input = input(
            "\nPlease enter playlist no. from the list (Press 'e' to stop):")
        if _input == 'e':
            break
        try:
            i = int(_input)
            if i > len(pls) or i <= 0:
                raise Exception('')
            pls_selected.append(pls[i - 1])
            print('\nCurrent Mappings:')
            for i, p in enumerate(pls_selected):
                print('Alt+{}: {}'.format(i + 1, p['name']))
            print('')
        except Exception:
            print('Invalid Input')

    if len(pls_selected) == 0:
        print('\nNo playlists selected')
        raise Exception('Force Exit')

    with open("playlist_mapping.config", "wb") as f:
        pickle.dump([{'id': p['id'], 'name':p['name']}
                     for p in pls_selected], f)

    print('\nPlaylist Mapping Generated !!!\n\n(⌐■_■)')


except Exception as e:
    if str(e) == 'Force Exit':
        print('\nGoodbye Friend !!!\n\n(⌐■_■)')
    else:
        print('\nOh no !!! Something went wrong\n\n¯\\(°_o)/¯\n\nCheck error.log for more details')
        import logging
        logging.basicConfig(filename="spotify_auto_playlist.log",
                            format="%(asctime)s: %(message)s", level=logging.DEBUG)
        logging.error(e)