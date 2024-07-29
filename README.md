# FlowPlaylist

Whether it is to stay focused during a busy workday, unwind after a long day, or simply enjoy some background tunes while browsing the web, Spotify is a go-to music platform for millions of people. However, collecting music in playlists can disturb our workflow and spend our valuable time. To address this issue, I have developed a Spotify keyboard that simplifies the process of adding tracks to playlists and controlling music playback. The keyboard communicates with a background program on the computer as an HID device. All keyboard requests are sent directly to the Spotify Web API. My primary objective was to design a user friendly and aesthetically pleasing product, which would enhance the listening experience for Spotify users.

![keyboard_smaller_optimized](https://github.com/user-attachments/assets/f13cc91c-5557-4109-a9d2-1ab0796f182c)


# How it works?

A program on a computer gets information from keyboard via HID communication. Based on those it sends requests to Spotify via Web API. 

![shematics](https://github.com/user-attachments/assets/4d966939-096c-4035-8e81-2a61fbe5b9c4)

# About software

You have to upload arduino code to keyboard, which you can get at https://github.com/KnedlOF/Spotify-keyboard-arduino. 
On computer you will have to setup python script, all the code is uploaded here in this repository. But to make your life simpler I have created instalation package, which does everything for you, get it at https://github.com/KnedlOF/FlowPlaylist-Driver. 
Instalation package is created in Advanced Installer. You have the project also included in this repository, it is called [Spotify Keyboard_eng.aip](https://github.com/KnedlOF/FlowPlaylist-driverCode/blob/master/Spotify%20Keyboard_eng.aip). 

# If you have questions join discord: https://discord.gg/FfVAAgvqkJ
