# Install python3 HID package https://pypi.org/project/hid/
from re import S
import hid
import time

# default is TinyUSB (0xcafe), Adafruit (0x239a), RaspberryPi (0x2e8a), Espressif (0x303a) VID
USB_VID = 0x2e8a
def device_is_connected(vendor_id, product_id):
    for device in hid.enumerate():
        if device['vendor_id'] == vendor_id and device['product_id'] == product_id:
            return True
    return False
while True:
    for dict in hid.enumerate(USB_VID):
        print(dict)
        vendor_id=dict['vendor_id']
        product_id=dict['product_id']
        dev = hid.Device(vendor_id, product_id)
        if dev:
            while True:
                # Get input from console and encode to UTF8 for array of chars.
                # hid generic inout is single report therefore by HIDAPI requirement
                # it must be preceeded with 0x00 as dummy reportID
                # str_out = b'\x00'
                # str_out += input("Send text to HID Device : ").encode('utf-8')
                # dev.write(str_out)
                try:
                    str_in = dev.read(8)
                    print("Received from HID Device:", str_in, '\n')
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
        
                    