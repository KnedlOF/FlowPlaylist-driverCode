from hid_control import volume
from authorization import sp


def set_volume():
    volume_set = sp.volume(volume)

    print(volume_set)
    print("Volume changed on: ".format(volume))
