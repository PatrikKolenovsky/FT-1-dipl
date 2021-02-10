import RPi.GPIO as GPIO
from time import sleep
import pyaudio
import numpy as np
import time
import cv2 as cv

default_kernel = cv.ft.createKernel(cv.ft.LINEAR, 1, 1)
from enum import Enum

class Shape(Enum):
    LINEAR = 1
    SINUS = 2
    
CHANNELS = 1
RATE = 44100

class KY040:
    
    def __init__(self, name, clockPin, dataPin, rotaryCallback,
                 streamCallback, counter, number_of_position, controller_type, kernel, p):
        
        self.name = name
        self.clockPin = clockPin
        self.dataPin = dataPin
        self.rotaryCallback = rotaryCallback
        self.counter = counter
        self.number_of_position = number_of_position
        self.controller_type = controller_type
        self.stream = streamCallback
        self.kernel = kernel
        self.p = p
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

            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()
            if self.controller_type == "SIZE":
                self.set_kernel(Shape.LINEAR, self.counter)
            self.p = pyaudio.PyAudio()    
            self.stream = p.open(format=pyaudio.paFloat32,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                input=True,
                stream_callback= self._streamCallback)
            self.stream.start_stream()
            

    def set_kernel(self, mask_type, mask_size):
        print ("'\033[92m'mask size: " + str(mask_size) + "'\033[0m'")
        if mask_type is Shape.LINEAR:
            self.kernel = cv.ft.createKernel(cv.ft.LINEAR, mask_size, 1)
        else:
            self.kernel = cv.ft.createKernel(cv.ft.SINUS, mask_size, 1)
        
    def _streamCallback(self, in_data, frame_count, time_info, flag):
        audio_data = np.frombuffer(in_data, np.float32)
        audio_data = cv.ft.FT02D_process(audio_data, self.kernel)
        output = audio_data
        return output, pyaudio.paContinue
    
if __name__ == "__main__":

    def rotaryChange(direction):
        print ("'\033[92m'turned - " + str(direction) + "'\033[0m'")


    def streamCallback(in_data, frame_count, time_info, flag):
        audio_data = np.frombuffer(in_data, np.float32)
        audio_data = cv.ft.FT02D_process(audio_data, default_kernel)
        output = audio_data
        return output, pyaudio.paContinue

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    input=True,
                    stream_callback=streamCallback)
    
    
    GPIO.setmode(GPIO.BCM)
    CLOCKPIN1 = 5
    DATAPIN1 = 6
    SWITCHPIN1 = 13
    ky1 = KY040("KY1 ", CLOCKPIN1, DATAPIN1, rotaryChange, stream, 1, 5, "TYPE", default_kernel, p)
    
    CLOCKPIN2 = 21
    DATAPIN2 = 16
    SWITCHPIN2 = 12
    ky2 = KY040("KY2 ", CLOCKPIN2, DATAPIN2, rotaryChange, stream, 1, 20, "SIZE", default_kernel, p)
    
    ky1.start()
    ky2.start()

    try:
        while True:
            sleep(0.1)

    finally:
        GPIO.cleanup()
        print("exit")
