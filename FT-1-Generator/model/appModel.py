import pyaudio
import numpy as np
import cv2 as cv
from PyQt5.QtCore import QMutex

from configuration.config import settings
from scipy.io import wavfile


class FtModel:
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

    # def openStream(self, openingTime, maskSize, channels):
    #     self.setKernel(maskSize, channels)
    #
    #     # opening the stream
    #     p = pyaudio.PyAudio()
    #     stream = p.open(format=pyaudio.paFloat32,
    #                     channels=self.channels,
    #                     rate=self.rate,
    #                     output=True,
    #                     input=True,
    #                     stream_callback=self.callback)
    #     stream.start_stream()
    #
    #     while stream.is_active():
    #         print("Stream started")
    #         time.sleep(openingTime)
    #         stream.stop_stream()
    #         print("Stream stoped")
    #     stream.close()

    # def printConfiguration(self):
    #     print("Data type: ", self.dtype, " Channels: ", self.channels, " Rate: ", self.rate)
    # def printKernel(self):
    #     print(self.kernel)
    # def plotFile(self, inputFileName, color):
    #     samplerate, data = wavfile.read(inputFileName)
    #     times = np.arange(len(data)) / float(samplerate)
    #     plt.figure(figsize=(10, 8))
    #     plt.fill_between(times, data[:, 0], data[:, 1], color=color)
    #     plt.xlim(times[0], times[-1])
    #     plt.xlabel('time (s)')
    #     plt.ylabel('amplitude')
    #     plt.savefig('plot.png', dpi=100)
    #     plt.show()
    #
    # def plotCompareFileData(self, fileName1, fileName2, start, end):
    #     samplerate, data = wavfile.read(fileName1)
    #     index = 1
    #     plotDataX1 = []
    #     plotDataY1 = []
    #     plotDataX2 = []
    #     plotDataY2 = []
    #
    #     print(data)
    #     for sample in data:
    #         if (index > start and index < end):
    #             plotDataX1.append(sample[0])
    #             plotDataY1.append(sample[1])
    #         index = index + 1
    #
    #     index = 1
    #     samplerate, data = wavfile.read(fileName2)
    #     for sample in data:
    #         if (index > start and index < end):
    #             plotDataX2.append(sample[0])
    #             plotDataY2.append(sample[1])
    #         index = index + 1
    #     index = 0
    #     intervalSize = end - start
    #     print(data)
