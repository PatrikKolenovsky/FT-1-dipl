import wave

import librosa
import mean as mean
import pyaudio
import numpy as np
import cv2 as cv
from scipy.io import wavfile

from configuration.config import settings
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile as wav
from numpy.lib import stride_tricks


class FtModel:
    sampling_rate = 44100
    duration = 2
    hop_length = 347 * duration  # to make time steps 128
    fmin = 20
    fmax = sampling_rate // 2
    n_mels = 128
    n_fft = n_mels * 20
    samples = sampling_rate * duration

    def __init__(self):
        self.dtype = settings.DTYPE
        self.channels = settings.CHANNELS
        self.rate = settings.RATE
        self.kernel = cv.ft.createKernel(cv.ft.LINEAR, 1, 1)
        self.serialEnabled = True

    def callback(self, in_data, frame_count, time_info, flag):
        audio_data = np.frombuffer(in_data, self.dtype)
        audio_data = cv.ft.FT02D_process(audio_data, self.kernel)
        output = audio_data
        return output, pyaudio.paContinue

    def setKernel(self, maskSize, channels):
        self.kernel = cv.ft.createKernel(cv.ft.LINEAR, maskSize, channels)

    def transform(self, inputFileDir, outputFileDir, maskSize):
        # Set kernel with maskSize
        self.setKernel(maskSize, self.channels)
        # Retype file to numpy
        self.rate, input_sig = wavfile.read(inputFileDir)
        np_sig = input_sig
        np_sig = np_sig.astype(float)

        transformedInput = cv.ft.FT02D_process(np_sig, self.kernel)
        transformedInput = np.int16(transformedInput)
        wavfile.write(outputFileDir, self.rate, transformedInput)
        return "file was created at " + outputFileDir

    def createImageFromSound(self, fileDir, fileName):
        # plt.subplot(9, 1, i + 1)
        # Read the wave file to numpy array
        samplerate, sound = wavfile.read(fileDir)
        partSound = []
        i = 1
        for x in range(600):
            partSound.append(sound[x])

        plt.plot(partSound)
        plt.savefig(settings.ROOT + "/image/" + fileName + ".png")
