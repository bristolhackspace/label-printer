import label_print
import RPi.GPIO as GPIO
import time

PROJECT_BOX_BUTTON = 23
SHORT_STAY_BUTTON = 24

DEBOUNCE_TIME = 0.2

def check_channel(channel, callback):
    if GPIO.input(channel):
        start = time.monotonic()
        # Wait long enough for pin to be stable
        while time.monotonic() - start > DEBOUNCE_TIME:
            if not GPIO.input(channel):
                return
        
        callback()

        # Limit maximum button push rate
        time.sleep(0.5)

        # Wait for button to be released before finishing
        while GPIO.input(channel):
            time.sleep(0.1)


def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PROJECT_BOX_BUTTON, GPIO.IN)
    GPIO.setup(SHORT_STAY_BUTTON, GPIO.IN)

    while True:
        time.sleep(0.1)
        check_channel(PROJECT_BOX_BUTTON, label_print.print_project_box_label)
        check_channel(SHORT_STAY_BUTTON, label_print.print_short_stay_label)


if __name__ == "__main__":
    main()