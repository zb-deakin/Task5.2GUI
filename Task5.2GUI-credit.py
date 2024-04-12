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

        # gui slider values
        self.brightness: DoubleVar = DoubleVar()
        self.previousBrightness: DoubleVar = DoubleVar()

        # gui widgets
        self.slider = Scale(
            font="Arial 12 bold",
            from_=0,  # minimum slider value
            to=_maxBrightness,  # maximum slider value
            length=200,  # slider width in gui
            label=_name,  # led name for label
            orient=HORIZONTAL,  # make the slider horizontal
            master=_guiWindow,  # add slider to window
            variable=self.brightness,  # adjustable slider value (usually 0-100)
            command=lambda _: self.adjustBrightness(),  # trigger method on value change
        )
        self.slider.set(0)  # by default set slider to zero
        self.slider.pack()  # pack widget into window centered
        Label(guiWindow, text=" ", padx=10, pady=10).pack()  # add a spacer after the widget

    # handle brightness changes to physical LEDs
    def adjustBrightness(self):
        # check if value has changed
        _oldValue = self.previousBrightness.get()
        _newValue = self.brightness.get()

        # do nothing if there was no change
        if _newValue == _oldValue:
            return

        # adjust brightness of LED via PWM
        self.pwmController.ChangeDutyCycle(_newValue)
        self.previousBrightness.set(_newValue)

        # give this a moment
        time.sleep(0.01)

    # tidy up when program is exiting
    def cleanup(self):
        self.pwmController.stop()
        time.sleep(0.01)


# set up data data for GPIO and UI
redPin: int = 17
greenPin: int = 27
bluePin: int = 22
ledNames: dict[int, str] = {
    redPin: "RED LED",
    greenPin: "GREEN LED",
    bluePin: "BLUE LED",
}
allValidPins: list[int] = list(ledNames.keys())
ledWidgets = []

# gui setup
guiWindow: Tk = Tk()
guiWindow.title("LED controller")
Label(
    guiWindow,
    text="Use the sliders to adjust brightness for each LED",
    padx=15,
    pady=10,
    font="Arial 15 italic",
).pack(anchor="w")

for _ledPin in allValidPins:
    ledWidgets.append(PwmLed(guiWindow, _ledPin, ledNames[_ledPin]))


# cleanup when program exits
@atexit.register
def cleanup():
    global ledWidgets

    # pwm cleanup
    for _led in ledWidgets:
        _led.cleanup()

    # board cleanup
    GPIO.cleanup()
    print("\n---> CLEANUP COMPLETE :)\n")


# open ui and run until closed
guiWindow.mainloop()
