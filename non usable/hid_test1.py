# Install python3 HID package https://pypi.org/project/hid/
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
    for device_info in hid.enumerate(USB_VID):
        print(device_info)
        vendor_id = device_info['vendor_id']
        product_id = device_info['product_id']
        try:
            device = hid.Device(vendor_id, product_id)
        except hid.HIDException as e:
            if "The device is not connected" in str(e):
                if not device_is_connected(vendor_id, product_id):
                    print("Error: Device is not connected")
                    time.sleep(1)
                else:
                    break
            else:
                print(str(e))
                break
        else:
            while True:
                # Get input from console and encode to UTF8 for array of chars.
                # hid generic inout is single report therefore by HIDAPI requirement
                # it must be preceeded with 0x00 as dummy reportID
                # str_out = b'\x00'
                # str_out += input("Send text to HID Device : ").encode('utf-8')
                # device.write(str_out)
                try:
                    data = device.read_nonblocking(8)
                    print("Received from HID Device:", data, '\n')
                except hid.HIDException as e:
                    if "The device is not connected" in str(e):
                        if not device_is_connected(vendor_id, product_id):
                            print("Error: Device is not connected")
                            time.sleep(1)
                        else:
                            break
                    else:
                        print(str(e))
                        break
