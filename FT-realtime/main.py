from ctypes import *

import RPi.GPIO as GPIO
from time import sleep
import pyaudio
from contextlib import contextmanager
import numpy as np
import math
import time
import cv2 as cv

default_kernel = cv.ft.createKernel(cv.ft.LINEAR, 1, 1)

from enum import Enum

class Shape(Enum):
     LINEAR = 1
     SINUS = 2

CHANNELS = 1
RATE = 44100
KERNEL_TYPE = 1
KERNEL_SIZE = 1


ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)

class KY040:
     def __init__(self, name, clockPin, dataPin, rotaryCallback,
                  streamCallback, counter, number_of_position, controller_type, kernel, p):

         self.name = name
         self.clockPin = clockPin
         self.dataPin = dataPin
         self.rotaryCallback = rotaryCallback
        # Value from rotator (to set type or radius)
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
         GPIO.add_event_detect(self.clockPin, GPIO.FALLING, callback=self._clockCallback, bouncetime=300)

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

             # Parameters settings
             if self.controller_type == "SIZE":
                 global KERNEL_SIZE
                 KERNEL_SIZE = self.counter
                 self.set_kernel()
             if self.controller_type == "TYPE":
                 global KERNEL_TYPE
                 KERNEL_TYPE = self.counter
                 self.set_kernel()
             with noalsaerr():
                self.p = pyaudio.PyAudio()
             self.stream = p.open(format=pyaudio.paFloat32,
                 channels=CHANNELS,
                 rate=RATE,
                 output=True,
                 input=True,
                 stream_callback= self._streamCallback)
             self.stream.start_stream()


     def set_kernel(self):
         print ("'\033[92m'kernel radius: " + str(KERNEL_SIZE) + "'\033[0m'")
         print ("'\033[92m'kernel type: " + str(KERNEL_TYPE) + "'\033[0m'")
         self.kernel = self.CREATE_KERNEL()

     def _streamCallback(self, in_data, frame_count, time_info, flag):
         audio_data = np.frombuffer(in_data, np.float32)
         audio_data = cv.ft.FT02D_process(audio_data, self.kernel)
         sound_level = 3
         output = audio_data * sound_level
         return output, pyaudio.paContinue

     def CREATE_KERNEL(self):
         global KERNEL_TYPE
         # LIN
         # [0, 0.5, 1, 0.5, 0] * [0, 0.5, 1, 0.5, 0]
         # [0, 0.33, 0.66, 1, 0.66, 0.33, 0] * [0, 0.33, 0.66, 1, 0.66, 0.33, 0]
         if KERNEL_TYPE == 1:
             print("Linear")
             V1 = self.GET_LINEAR_VECTOR(KERNEL_SIZE, False)
             V2 = self.GET_LINEAR_VECTOR(KERNEL_SIZE, True)
             KERNEL = np.array(V1) * np.array(V2)
         # SIN
         # [0, 0.707, 1, 0.707, 0] * [0], [0.707], [1], [0.707], [0]]
         elif KERNEL_TYPE == 2:
             print("Sinus")
             V1 = self.GET_SIN_VECTOR(KERNEL_SIZE, False)
             V2 = self.GET_SIN_VECTOR(KERNEL_SIZE, True)
             KERNEL = np.array(V1) * np.array(V2)
         # SIN LIN
         # [0, 0.707, 1, 0.707, 0] * [[0], [0.5], [1], [0.5], [0]]
         elif KERNEL_TYPE == 3:
             print("Sinus/linear")
             V1 = self.GET_SIN_VECTOR(KERNEL_SIZE, False)
             V2 = self.GET_LINEAR_VECTOR(KERNEL_SIZE, True)
             KERNEL = np.array(V1) * np.array(V2)
         # DUAL
         # [1, 0, 1, 0, 1] * [1, 0, 1, 0, 1]
         elif KERNEL_TYPE == 4:
             print("Dual")
             V1 = self.GET_DUAL_VECTOR(KERNEL_SIZE, False)
             V2 = self.GET_DUAL_VECTOR(KERNEL_SIZE, True)
             KERNEL = np.array(V1) * np.array(V2)
         # DUAL LIN
         # [1, 0, 1, 0, 1] * [0, 0.5, 1, 0.5, 0]
         elif KERNEL_TYPE == 5:
             print("Dual/lin")
             V1 = self.GET_DUAL_VECTOR(KERNEL_SIZE, False)
             V2 = self.GET_LINEAR_VECTOR(KERNEL_SIZE, True)
             KERNEL = np.array(V1) * np.array(V2)
         # SQUARE RUSPINNI
         # [0, 0, 1, 1, 1, 0, 0]
         # [[0], [0], [1], [1], [1], [0], [0]]
         elif KERNEL_TYPE == 6:
             print("Square Ruspinni")
             V1 = self.GET_SQUARE_VECTOR(KERNEL_SIZE, False, "RUSPINNI")
             V2 = self.GET_SQUARE_VECTOR(KERNEL_SIZE, True, "RUSPINNI")
             KERNEL = np.array(V1) * np.array(V2)
         # SQUARE
         # [0, 1, 1, 1, 1, 1, 0]
         # [[0], [1], [1], [1], [1], [1], [0]]
         elif KERNEL_TYPE == 7:
             print("Square ++ ")
             V1 = self.GET_SQUARE_VECTOR(KERNEL_SIZE, False, "None")
             V2 = self.GET_SQUARE_VECTOR(KERNEL_SIZE, True, "None")
             KERNEL = np.array(V1) * np.array(V2)

         # SQUARE R+
         # [0, 0, 1, 1, 1, 1, 0]
         # [[0], [0], [1], [1], [1], [1], [0]]
         elif KERNEL_TYPE == 8:
             print("Square/R+")
             V1 = self.GET_SQUARE_VECTOR(KERNEL_SIZE, False, "R+")
             V2 = self.GET_SQUARE_VECTOR(KERNEL_SIZE, True, "R+")
             KERNEL = np.array(V1) * np.array(V2)
         # SQUARE L+
         # [0, 1, 1, 1, 1, 0, 0]
         # [[0], [1], [1], [1], [1], [0], [0]]
         elif KERNEL_TYPE == 9:
             print("Square/L+")
             V1 = self.GET_SQUARE_VECTOR(KERNEL_SIZE, False, "L+")
             V2 = self.GET_SQUARE_VECTOR(KERNEL_SIZE, True, "L+")
             KERNEL = np.array(V1) * np.array(V2)
         # SQUARE  MIX1
         # [0, 1, 1, 1, 1, 0, 0]
         # [[0], [0], [1], [1], [1], [1], [0]]
         elif KERNEL_TYPE == 10:
             print("Square/L+R+")
             V1 = self.GET_SQUARE_VECTOR(KERNEL_SIZE, False, "L+")
             V2 = self.GET_SQUARE_VECTOR(KERNEL_SIZE, True, "R+")
             KERNEL = np.array(V1) * np.array(V2)
         # SQUARE  MIX2
         # [0, 0, 1, 1, 1, 1, 0]
         # [[0], [1], [1], [1], [1], [0], [0]]
         elif KERNEL_TYPE == 11:
             print("Square/R+L+")
             V1 = self.GET_SQUARE_VECTOR(KERNEL_SIZE, False, "R+")
             V2 = self.GET_SQUARE_VECTOR(KERNEL_SIZE, True, "L+")
             KERNEL = np.array(V1) * np.array(V2)
         # SQUARE  MIX2
         # [0, 0, 1, 1, 1, 1, 0]
         # [[0], [1], [1], [1], [1], [0], [0]]
         elif KERNEL_TYPE == 12:
             print("Square Ruspine/Linear")
             V1 = self.GET_SQUARE_VECTOR(KERNEL_SIZE, False, "RUSPINNI")
             LinSize = KERNEL_SIZE + 1
             V2 = self.GET_LINEAR_VECTOR(LinSize, True)
             KERNEL = np.array(V1) * np.array(V2)
             print("V1: " + str(V1))
             print("V2: " + str(V2))
         else:
             print("uknown type")
             KERNEL = []
         return KERNEL

     # size 2 = 0,5
     # size 3 = 0.33 0.66
     # size 4 = 0.25 0.5 0.75
     def GET_LINEAR_VECTOR(self, KERNEL_SIZE, COLUM_FORMAT):
         firstPart = []
         secPart = []

         if (COLUM_FORMAT == True):
             for x in range(KERNEL_SIZE):
                 if (x == 0):
                     firstPart.append([0])
                     continue
                 else:
                     firstPart.append([x / KERNEL_SIZE])
                     secPart.insert(0, [x / KERNEL_SIZE])
             firstPart.append([1])
             ret = firstPart + secPart
             ret.append([0])
         else:
             for x in range(KERNEL_SIZE):
                 if (x == 0):
                     firstPart.append(0)
                     continue
                 else:
                     firstPart.append(x / KERNEL_SIZE)
                     secPart.insert(0, x / KERNEL_SIZE)
             firstPart.append(1)
             ret = firstPart + secPart
             ret.append(0)
         return ret

     # SIN
     # [0, 0.707, 1, 0.707, 0]
     # [0, 0.38, 0.70, 0.92, 1, 0.92, 0.70, 0.38, 0]
     def GET_SIN_VECTOR(self, KERNEL_SIZE, COLUM_FORMAT):
         firstPart = []
         secPart = []
         if (COLUM_FORMAT == True):
             for x in range(KERNEL_SIZE):
                 if (x == 0):
                     firstPart.append([0])
                     continue
                 else:
                     position = (x / KERNEL_SIZE) * 0.5
                     firstPart.append([math.sin(((x / KERNEL_SIZE) * 0.5) * math.pi)])
                     secPart.insert(0, [math.sin(((x / KERNEL_SIZE) * 0.5) * math.pi)])
             firstPart.append([1])
             ret = firstPart + secPart
             ret.append([0])
         else:
             for x in range(KERNEL_SIZE):
                 if (x == 0):
                     firstPart.append(0)
                     continue
                 else:
                     firstPart.append(math.sin(((x / KERNEL_SIZE) * 0.5) * math.pi))
                     secPart.insert(0, math.sin(((x / KERNEL_SIZE) * 0.5) * math.pi))
             firstPart.append(1)
             ret = firstPart + secPart
             ret.append(0)
         return ret

     # DUAL
     # [1, 0, 1, 0, 1]
     def GET_DUAL_VECTOR(self, KERNEL_SIZE, COLUM_FORMAT):
         firstPart = []
         secPart = []
         if (COLUM_FORMAT == True):
             for x in range(KERNEL_SIZE):
                 if x == 0:
                     firstPart.append([1])
                     secPart.append([1])
                     continue
                 else:
                     firstPart.append([0])
                     secPart.insert(0, [0])
             firstPart.append([1])
             ret = firstPart + secPart
         else:
             for x in range(KERNEL_SIZE):
                 if x == 0:
                     firstPart.append(1)
                     secPart.append(1)
                     continue
                 else:
                     firstPart.append(0)
                     secPart.insert(0, 0)
             firstPart.append(1)
             ret = firstPart + secPart
         return ret

     def GET_SQUARE_VECTOR(self, KERNEL_SIZE, COLUM_FORMAT, MODIFICATION):
         firstPart = []
         secPart = []
         if (COLUM_FORMAT == True):
             for x in range(KERNEL_SIZE):
                 if x == 0:
                     firstPart.append([0])
                     secPart.append([0])
                     continue
                 elif x == 1 and MODIFICATION == "RUSPINNI":
                     firstPart.append([0])
                     firstPart.append([1])
                     secPart.insert(0, [1])
                     secPart.append([0])
                     continue
                 elif x == 1 and MODIFICATION == "R+":
                     firstPart.append([0])
                     secPart.insert(0, [1])
                     continue
                 elif x == 1 and MODIFICATION == "L+":
                     firstPart.append([1])
                     secPart.insert(0, [0])
                     continue
                 else:
                     firstPart.append([1])
                     secPart.insert(0, [1])
             firstPart.append([1])
             ret = firstPart + secPart
         else:
             for x in range(KERNEL_SIZE):
                 if x == 0:
                     firstPart.append(0)
                     secPart.append(0)
                     continue
                 elif x == 1 and MODIFICATION == "RUSPINNI":
                     firstPart.append(0)
                     firstPart.append(1)
                     secPart.insert(0, 1)
                     secPart.append(0)
                     continue
                 elif x == 1 and MODIFICATION == "R+":
                     firstPart.append(0)
                     secPart.insert(0, 1)
                     continue
                 elif x == 1 and MODIFICATION == "L+":
                     firstPart.append(1)
                     secPart.insert(0, 0)
                     continue
                 else:
                     firstPart.append(1)
                     secPart.insert(0, 1)
             firstPart.append(1)
             ret = firstPart + secPart

         return ret

if __name__ == "__main__":

     def rotaryChange(direction):
         print ("'\033[92m'turned - " + str(direction) + "'\033[0m'")


     def streamCallback(in_data, frame_count, time_info, flag):
         audio_data = np.frombuffer(in_data, np.float32)
         audio_data = cv.ft.FT02D_process(audio_data, default_kernel)
         output = audio_data * 3
         return output, pyaudio.paContinue


     with noalsaerr():
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
     ky1 = KY040("KY1 ", CLOCKPIN1, DATAPIN1, rotaryChange, stream, 1, 12, "TYPE", default_kernel, p)

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