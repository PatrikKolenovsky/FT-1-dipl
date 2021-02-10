import pyaudio
import numpy as np
import time
import cv2 as cv

from enum import Enum

class Shape(Enum):
    LINEAR = 1
    SINUS = 2

def set_kernel(mask_type, mask_size):
    if mask_type is Shape.LINEAR:
        return cv.ft.createKernel(cv.ft.LINEAR, mask_size, 1)
    else:
        return cv.ft.createKernel(cv.ft.SINUS, mask_size, 1)


def callback(in_data, frame_count, time_info, flag):
    kernel = set_kernel(Shape.LINEAR, 5)
    audio_data = np.frombuffer(in_data, np.float32)
    audio_data = cv.ft.FT02D_process(audio_data, kernel)
    output = audio_data
    return output, pyaudio.paContinue

if __name__ == '__main__':
    """Main function."""
        
    p = pyaudio.PyAudio()

    CHANNELS = 1
    RATE = 44100
    stream = p.open(format=pyaudio.paFloat32,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    input=True,
                    stream_callback=callback)

    stream.start_stream()

    while stream.is_active():
        time.sleep(5000)
        stream.stop_stream()
        print("Stream is stopped")

    stream.close()

    p.terminate()
