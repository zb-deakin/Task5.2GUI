import atexit
import time
from tkinter import *

import RPi.GPIO as GPIO

# board setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


class PwmLed:

    def __init__(self, _guiWindow: Tk, _ledPin: int, _name: str, _maxBrightness: int = 100) -> None:
        # set up pin on Rpi board
        self.ledPin: int = _ledPin
        GPIO.setup(self.ledPin, GPIO.OUT)

        # pwm setup
        self.pwmController: GPIO.PWM = GPIO.PWM(self.ledPin, _maxBrightness)
        self.pwmController.start(0)

        # gui slider setup
        self.brightness: DoubleVar = DoubleVar()
        self.previousBrightness: DoubleVar = DoubleVar()
        self.slider = Scale(
            master=_guiWindow,
            variable=self.brightness,
            from_=0,
            to=_maxBrightness,
            orient=HORIZONTAL,
            label=_name,
            command=lambda _: self.adjustBrightness(),
            length=200

        )
        self.slider.set(0)
        self.slider.pack()
        Label(guiWindow, text=" ", padx=10, pady=10).pack(anchor="w")

    def adjustBrightness(self):
        _oldValue = self.previousBrightness.get()
        _newValue = self.brightness.get()

        if _newValue == _oldValue:
            return

        self.pwmController.ChangeDutyCycle(_newValue)
        self.previousBrightness.set(_newValue)

        time.sleep(0.01)

    def cleanup(self):
        self.pwmController.stop()
        time.sleep(0.01)


# prepare GPIO pin data
redPin: int = 17
greenPin: int = 27
bluePin: int = 22

ledNames: dict[int, str] = {
    redPin: "RED LED",
    greenPin: "GREEN LED",
    bluePin: "BLUE LED",
}

allValidPins: list[int] = list(ledNames.keys())

leds = []

# gui setup
guiWindow: Tk = Tk()
guiWindow.title("LED controller")
Label(guiWindow, text="Use the sliders to adjust brightness for each LED", padx=10, pady=10).pack(anchor="w")

for _ledPin in allValidPins:
    leds.append(PwmLed(guiWindow, _ledPin, ledNames[_ledPin]))


# cleanup when program exits
@atexit.register
def cleanup():
    global leds

    for _led in leds:
        _led.cleanup()

    GPIO.cleanup()
    print("\n---> CLEANUP COMPLETE :)\n")


guiWindow.mainloop()
