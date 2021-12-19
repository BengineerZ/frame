import time
import threading
import signal
import RPi.GPIO as GPIO
import os
import glob
import random
from inky import Inky7Colour as Inky
from PIL import Image

# inky = Inky()

print("insert usb stick")
time.sleep(10)
print("starting")

# Get the list of all files and directories
path = "/media/pi/*/*"

check_path = "/media/pi/*"

# file_list = []
# for file in glob.iglob(path, recursive=True):
# 	file_list.append(file)

device_list = []
for file in glob.iglob(check_path, recursive=False):
	device_list.append(file)


# print(file_list)
print(device_list)