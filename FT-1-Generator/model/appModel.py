import pyaudio
import numpy as np
import cv2 as cv
from ..configuration.config import settings
import time
from scipy.io import wavfile

class Model:
    dtype = settings.DTYPE
    channels = settings.CHANNELS
    rate = settings.RATE
    kernel = cv.ft.createKernel(cv.ft.LINEAR, 1, 1)

    def printConfiguration(self):
        print("Data type: ", self.dtype, " Channels: ", self.channels, " Rate: ", self.rate)

    def callback(self, in_data, frame_count, time_info, flag):
        return in_data, pyaudio.paContinue

    def callbackFTransform(self, in_data, frame_count, time_info, flag):
        audio_data = np.frombuffer(in_data, self.dtype)
        audio_data = cv.ft.FT02D_process(audio_data, self.kernel)
        output = audio_data
        return output, pyaudio.paContinue

    def openStream(self, useFTransform, openingTime, maskSize, channels):
        if (useFTransform == True):
            callback = self.callbackFTransform
            self.setKernel(maskSize, channels)
            print("using F-transform")
        else:
            callback = self.callback
            print("basic I/O only")

        print("opening the stream")
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32,
                        channels=self.channels,
                        rate=self.rate,
                        output=True,
                        input=True,
                        stream_callback=self.callbackFTransform)
        stream.start_stream()

        while stream.is_active():
            print("Stream started")
            time.sleep(openingTime)
            stream.stop_stream()
            print("Stream stoped")
        stream.close()

    def setKernel(self, maskSize, channels):
        self.kernel = cv.ft.createKernel(cv.ft.LINEAR, maskSize, channels)
        print("new kernel with mask size ", maskSize, " has been initialized")

    def printKernel(self):
        print(self.kernel)

    def transformFileByFTransform(self, inputFileName, outputFileName, maskSize, channels):
        self.setKernel(maskSize, channels)
        self.rate, input_sig = wavfile.read(inputFileName)
        np_sig = input_sig
        np_sig = np_sig.astype(float)
        transformedInput = cv.ft.FT02D_process(np_sig, self.kernel)
        transformedInput = np.int16(transformedInput)
        wavfile.write(outputFileName, self.rate, transformedInput)
        print("File ", outputFileName, " been created")

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