import cv2 as cv
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

if __name__ == '__main__':
    """Main function."""
    # print("fafa")

    input = "E:/School/DP/FT-1-dipl/FT-1-Generator/files/sine.wav"
    # input = "E:/School/DP/latence/KernelUsb44100s.wav"
    rate, input_sig = wavfile.read(input)
    samplerate, sound = wavfile.read(input)
    partSound1 = []
    for x in range(2000):
        partSound1.append(sound[x])

    plt.figure(figsize=(9, 5))
    plt.ylabel('loudness[dB]')
    plt.xlabel('number of samples')
    plt.plot(partSound1, label="latency")
    # plt.legend()
    plt.show()


def FTTutorialPlot():
    print("reading signal")
    input = "E:/WebDevs/Projects/Python/FT-1-dipl/FT-1-Generator/files/sine.wav"
    rate, input_sig = wavfile.read(input)
    np_sig = input_sig
    np_sig = np_sig.astype(float)

    print("creating kernel ")
    maskSize1 = 10
    kernel1 = cv.ft.createKernel(cv.ft.LINEAR, maskSize1, 1)
    direct = cv.ft.FT02D_components(np_sig, kernel1)
    # print(len(direct))
    # print(len(direct))
    transformedInput1 = cv.ft.FT02D_process(np_sig, kernel1)
    transformedInput1 = np.int16(transformedInput1)

    samplerate, sound = wavfile.read(input)
    partSound1 = []
    for x in range(200):
        partSound1.append(sound[x])

    partSound2 = []
    for x in range(20):
        partSound2.append(direct[x])

    # partSound2 = []
    # for x in range(100):
    #     partSound2.append(direct[x]  // maskSize1)

    partSound3 = []
    for x in range(200):
        partSound3.append(transformedInput1[x])

    plt.figure(figsize=(4, 3))
    plt.ylabel('loudness[dB]')
    plt.xlabel('number of samples')
    # plt.plot(partSound1, label="original")
    # plt.plot(partSound2, 'ko', markersize=5, label="FT components")
    # 'orange', label="direct (FT components)",
    plt.plot(partSound3, 'red', label="inverse (Transformed signal, kernel size 10)")
    plt.legend()
    plt.show()


