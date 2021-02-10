import RPi.GPIO as GPIO
from time import sleep
import time
import cv2 as cv


class KY040:
    
    def __init__(self, name, clockPin, dataPin, rotaryCallback, counter, number_of_position):
        
        self.name = name
        self.clockPin = clockPin
        self.dataPin = dataPin
        self.rotaryCallback = rotaryCallback
        self.counter = counter
        self.number_of_position = number_of_position

        #setup pins
        GPIO.setup(clockPin, GPIO.IN)
        GPIO.setup(dataPin, GPIO.IN)

    def start(self):
        GPIO.add_event_detect(self.clockPin,
                              GPIO.FALLING,
                              callback=self._clockCallback,
                              bouncetime=300)

    def stop(self):
        GPIO.remove_event_detect(self.clockPin)

    def _clockCallback(self, pin):
        if GPIO.input(self.clockPin) == 0:
            data = GPIO.input(self.dataPin)
            if data == 1:
                self.counter += 1
                if self.counter > self.number_of_position:
                    self.counter = 1
                self.rotaryCallback(self.name + " moved ANTICLOCKWISE position " + str(self.counter))
            else:
                self.counter = self.counter - 1 
                if self.counter <= 0:
                    self.counter = self.number_of_position
                self.rotaryCallback(self.name + " moved CLOCKWISE position " + str(self.counter))
    
if __name__ == "__main__":

    def rotaryChange(direction):
        print ("'\033[92m'turned - " + str(direction) + "'\033[0m'")


    GPIO.setmode(GPIO.BCM)
    CLOCKPIN1 = 5
    DATAPIN1 = 6
    SWITCHPIN1 = 13
    ky1 = KY040("KY1 ", CLOCKPIN1, DATAPIN1, rotaryChange, 1, 5)
    
    CLOCKPIN2 = 21
    DATAPIN2 = 16
    SWITCHPIN2 = 12
    ky2 = KY040("KY2 ", CLOCKPIN2, DATAPIN2, rotaryChange, 1, 20)
    
    ky1.start()
    ky2.start()

    try:
        while True:
            sleep(0.1)

    finally:
        GPIO.cleanup()
        print("exit")