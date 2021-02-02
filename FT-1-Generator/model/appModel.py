import pyaudio
import numpy as np
import cv2 as cv
from scipy.io import wavfile

from configuration.config import settings
import matplotlib.pyplot as plt


class FtModel:
    def __init__(self):
        self.dtype = settings.DTYPE
        self.channels = settings.CHANNELS
        self.rate = settings.RATE
        self.serialEnabled = True

    def callback(self, in_data, frame_count, time_info, flag):
        audio_data = np.frombuffer(in_data, self.dtype)
        audio_data = cv.ft.FT02D_process(audio_data, self.kernel)
        output = audio_data
        return output, pyaudio.paContinue

    def setKernel(self, maskSize):
        # self.kernel = cv.ft.createKernel(cv.ft.LINEAR, maskSize,  self.channels)
        self.kernel = np.array([
            [0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 1, 0, 1, 0],
            [0, 0, 0, 0, 0]])
        # Gaussian blur
        # self.kernel = np.array([[1, 4, 6, 4, 1],
        #                 [4, 16, 24, 16, 4],
        #                 [6, 24, 36, 24, 6],
        #                 [4, 16, 24, 16, 4],
        #                 [1, 4, 6, 4, 1]])
        # self.kernel = np.array([
        #     [0, 0, 0, 0, 0],
        #     [0, 1, 1, 1, 0],
        #     [1, 1, 1, 1, 1],
        #     [0, 1, 1, 1, 0],
        #     [0, 0, 0, 0, 0]])

    def transform(self, inputFileDir, outputFileDir, maskSize):
        # Set kernel with maskSize
        self.setKernel(maskSize)
        # Retype file to numpy
        self.rate, input_sig = wavfile.read(inputFileDir)
        np_sig = input_sig
        np_sig = np_sig.astype(float)

        transformedInput = cv.ft.FT02D_process(np_sig, self.kernel)
        transformedInput = np.int16(transformedInput)
        wavfile.write(outputFileDir, self.rate, transformedInput)
        return "file was created at " + outputFileDir

    def createImageFromSound(self, fileDir, fileName):
        plt.figure(figsize=(4, 3))
        samplerate, sound = wavfile.read(fileDir)
        partSound = []
        for x in range(settings.NUMBER_OF_DISPLAYED_SAMPLES):
            partSound.append(sound[x])

        plt.plot(partSound)
        plt.savefig(settings.ROOT + "/image/" + fileName + ".png")
