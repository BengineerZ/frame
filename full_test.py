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

### file io

path = "/media/pi/*/*"
device_path = "/media/pi/*"
device_list = []

# Gpio pins for each button (from top to bottom)
BUTTONS = [5, 6, 16, 24]

# These correspond to buttons A, B, C and D respectively
LABELS = ['A', 'B', 'C', 'D']

def check_usb():
	global device_list
	device_list = []
	for file in glob.iglob(device_path, recursive=False):
		device_list.append(file)
	print(f'Num of devices: {len(device_list)}')

def eject_usb(pin):
	label = LABELS[BUTTONS.index(pin)]
    print("Button press detected on pin: {} label: {}".format(pin, label))
	if len(device_list) == 1:
		print(f"Ejecting {device_list[0]}")
		cmd = f"sudo umount {device_list[0]}"
		os.system(cmd)
		global device_list
		device_list = []
	else: 
		print("no device inserted")

def read_files():
	file_list = []
	for file in glob.iglob(path, recursive=True):
		file_list.append(file)

	print(f'Number of files: {len(file_list)}')
	return file_list

### button setup



# Set up RPi.GPIO with the "BCM" numbering scheme
GPIO.setmode(GPIO.BCM)

# Buttons connect to ground when pressed, so we should set them up
# with a "PULL UP", which weakly pulls the input signal to 3.3V.
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Loop through out buttons and attach the "handle_button" function to each
# We're watching the "FALLING" edge (transition from 3.3V to Ground) and
# picking a generous bouncetime of 250ms to smooth out button presses.

GPIO.add_event_detect(BUTTONS[0], GPIO.FALLING, eject_usb, bouncetime=250)


### MAIN:

while True:
	while len(device_list) == 0:
		print("Please insert USB device")
		time.sleep(5)
		check_usb()
	while len(device_list) == 1:
		print(time.time())
		image_list = read_files()
		while len(device_list) == 1:
			print('testing loop')
			print(device_list)
			time.sleep(8)


