import os

roaming_folder = os.environ["APPDATA"]
spotify_executable = "Spotify\\Spotify.exe"
spotify_path = os.path.join(roaming_folder, spotify_executable)
print(spotify_path)