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
	device_list.clear()
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
		device_list.clear()
	else: 
		print("no device inserted")

def read_files():
	file_list = []
	for file in glob.iglob(path, recursive=True):
		file_list.append(file)

	print(f'Number of files: {len(file_list)}')
	return file_list

def check_loop():
	while len(device_list) == 1:
		time.sleep(10)
		print('checking if usb is still in')
		check_usb()
		print(time.time())

	print('usb removed')


### button setup

# Set up RPi.GPIO with the "BCM" numbering scheme
GPIO.setmode(GPIO.BCM)

# Buttons connect to ground when pressed, so we should set them up
# with a "PULL UP", which weakly pulls the input signal to 3.3V.
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Loop through out buttons and attach the "handle_button" function to each
# We're watching the "FALLING" edge (transition from 3.3V to Ground) and
# picking a generous bouncetime of 250ms to smooth out button presses.

GPIO.add_event_detect(BUTTONS[1], GPIO.FALLING, eject_usb, bouncetime=250)


### Image setup:

inky = Inky()

def process_image(f_in, size=(600,448)):
	image = Image.open(f_in)
	image.thumbnail(size, Image.ANTIALIAS)
	image_size = image.size
	
	thumb = image
	
	bg = Image.new('RGB', size, (255, 255, 255))
	
	offset_x = max( (size[0] - image_size[0]) // 2, 0 )
	offset_y = max( (size[1] - image_size[1]) // 2, 0 )
	
	bg.paste(thumb, (offset_x, offset_y))

	return bg

def update_image(file_list):
	print("Updating image ...")
	print(time.time())
	im = process_image(random.choice(file_list))
	inky.set_image(im)
	inky.show()


### MAIN:

def photo_loop(file_list):
	l = threading.currentThread()
	while getattr(l, "do_run", True):
		print('Photo loop')
		t = threading.Thread(target=update_image, args=(file_list,))
		t.start()
		time.sleep(120)
	print("Stopping as you wish.")


mnaul_update_list = []
	
def manual_update(pin):
	update_image(mnaul_update_list)

GPIO.add_event_detect(BUTTONS[0], GPIO.FALLING, manual_update, bouncetime=250)


while True:
	while len(device_list) == 0:
		print("Please insert USB device")
		time.sleep(5)
		check_usb()
	if len(device_list) == 1:
		print(time.time())
		image_list = read_files()
		mnaul_update_list[:] = image_list
		l = threading.Thread(target=photo_loop, args=(image_list,))
		l.start()
		time.sleep(2)
		while len(device_list) == 1:
			time.sleep(10)
			print('checking if usb is still in')
			check_usb()
			print(time.time())

		print('usb removed')
		l.do_run = False
		mnaul_update_list.clear()
			