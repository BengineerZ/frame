import time
import threading
import signal
import RPi.GPIO as GPIO
import os
import glob
import random
from inky import Inky7Colour as Inky
from PIL import Image

print("starting")

path = "/media/pi/*/*"
device_path = "/media/pi/*"
usb_inserted = False
device_list = []

def check_usb():
	device_list = []
	for file in glob.iglob(device_path, recursive=False):
		device_list.append(file)

	
	print(len(device_list))
	if len(device_list) == 1:
		return True, device_list
	return False, device_list

while not usb_inserted:
	print("Please insert USB device")
	time.sleep(5)
	usb_inserted, device_list = check_usb()

print("Device inserted, ejecting")
print(device_list[0])

cmd = f"sudo umount {device_list[0]}"
os.system(cmd)

time.sleep(4)

check_usb()


