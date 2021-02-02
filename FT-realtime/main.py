import pyaudio
import numpy as np
from .Shape import Shape
import cv2 as cv


def set_kernel(mask_type, mask_size):
    if mask_type is Shape.LINEAR:
        return cv.ft.createKernel(cv.ft.LINEAR, mask_size, 1)
    else:
        return cv.ft.createKernel(cv.ft.SINUS, mask_size, 1)

def callback_ft_transform(in_data, MASK_TYPE, MASK_SIZE):

    kernel = set_kernel(MASK_TYPE, MASK_SIZE)
    audio_data = np.frombuffer(in_data, np.float32)
    audio_data = cv.ft.FT02D_process(audio_data, kernel)
    output = audio_data
    return output, pyaudio.paContinue

if __name__ == '__main__':
    """Main function."""

    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024

    print("App started")
    # TODO add listenner to potentiometer
    # MASK_SIZE = getPotentiometerValue(pin.state, numberOfIntervals)
    MASK_SIZE = 10
    # TODO add shape generator listenner to potentiometer
    # MASK_TYPE = getPotentiometerValue(pin.state, numberOfIntervals)
    MASK_TYPE = Shape.LINEAR
    kernel = set_kernel(MASK_TYPE, MASK_SIZE)
    print("opening the stream")
    callback = callback_ft_transform
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    input=True,
                    stream_callback=callback_ft_transform)
    stream.start_stream()

    while stream.is_active():
        print("listening to pins...")
        # if potentitomer changed
        #    if oldValue !=  getPotentiometerValue
        #       kernel = set_kernel(MASK_TYPE, MASK_SIZE)

