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

def eject_usb(device_list):
	if len(device_list) == 1:
		print(f"Ejecting {device_list[0]}")
		cmd = f"sudo umount {device_list[0]}"
		os.system(cmd)
		return False
	else: 
		print("no device inserted")

def read_files():
	file_list = []
	for file in glob.iglob(path, recursive=True):
		file_list.append(file)

	print(f'Number of files: {len(file_list)}')
	return file_list

### button setup

# Gpio pins for each button (from top to bottom)
BUTTONS = [5, 6, 16, 24]

# These correspond to buttons A, B, C and D respectively
LABELS = ['A', 'B', 'C', 'D']

# Set up RPi.GPIO with the "BCM" numbering scheme
GPIO.setmode(GPIO.BCM)

# Buttons connect to ground when pressed, so we should set them up
# with a "PULL UP", which weakly pulls the input signal to 3.3V.
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# "handle_button" will be called every time a button is pressed
# It receives one argument: the associated input pin.
def handle_button(pin):
    label = LABELS[BUTTONS.index(pin)]
    print("Button press detected on pin: {} label: {}".format(pin, label))
    if label == 'D':
    	usb_inserted = eject_usb(device_list)

# Loop through out buttons and attach the "handle_button" function to each
# We're watching the "FALLING" edge (transition from 3.3V to Ground) and
# picking a generous bouncetime of 250ms to smooth out button presses.
for pin in BUTTONS:
    GPIO.add_event_detect(pin, GPIO.FALLING, handle_button, bouncetime=250)



### MAIN:

while not usb_inserted:
	print("Please insert USB device")
	time.sleep(5)
	usb_inserted, device_list = check_usb()

print(read_files())

signal.pause()


