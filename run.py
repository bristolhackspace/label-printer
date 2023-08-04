import label_print
import RPi.GPIO as GPIO
import time
import sys

SHORT_STAY_BUTTON = 17
PROJECT_BOX_BUTTON = 27

def print_short_stay_label(channel):
    label_print.print_short_stay_label()

def print_project_box_label(channel):
    label_print.print_project_box_label()

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SHORT_STAY_BUTTON, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(PROJECT_BOX_BUTTON, GPIO.IN, GPIO.PUD_DOWN)

    GPIO.add_event_detect(SHORT_STAY_BUTTON, GPIO.RISING, callback=print_short_stay_label, bouncetime=200)
    GPIO.add_event_detect(PROJECT_BOX_BUTTON, GPIO.RISING, callback=print_project_box_label, bouncetime=200)

    while True:
        time.sleep(0.5)


if __name__ == "__main__":
    main()