import sched, time
import signal
import RPi.GPIO as GPIO


''' Functionality:
Base - updates a random photo every 24 hours

A - update to a new picture - doesn't affect the 24hr loop
B - pause the 24 hr loop
C - play the 24 hr loop
D - display the base image

'''


s = sched.scheduler(time.time, time.sleep)

def update_image():
	print("placeholder: updating image ...")
	print(time.time())
	# get a random image from the usb
	# update the inky with a random image

def update_loop():
	s.enter(5, 1, update_image, ())
	s.run()


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


# Loop through out buttons and attach the "handle_button" function to each
# We're watching the "FALLING" edge (transition from 3.3V to Ground) and
# picking a generous bouncetime of 250ms to smooth out button presses.

GPIO.add_event_detect(BUTTONS[0], GPIO.FALLING, update_image, bouncetime=250)
GPIO.add_event_detect(BUTTONS[1], GPIO.FALLING, handle_button, bouncetime=250)
GPIO.add_event_detect(BUTTONS[2], GPIO.FALLING, handle_button, bouncetime=250)
GPIO.add_event_detect(BUTTONS[3], GPIO.FALLING, handle_button, bouncetime=250)


## would be replaced with a while loop in the final version:
for i in range(5):
	print(i)
	update_loop()