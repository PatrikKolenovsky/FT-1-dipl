import cv2 as cv
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt


def FTTutorialPlot():
    print("reading signal")
    input = "D:/Python/FT-1-dipl/FT-1-Generator/files/sine.wav"
    rate, input_sig = wavfile.read(input)
    np_sig = input_sig
    np_sig = np_sig.astype(float)

    print("creating kernel ")
    maskSize1 = 3
    kernel1 = cv.ft.createKernel(cv.ft.LINEAR, maskSize1, 1)
    print("transforming")
    direct = cv.ft.FT02D_components(np_sig, kernel1)
    print(len(direct))
    print(len(direct[0]))
    transformedInput1 = cv.ft.FT02D_process(np_sig, kernel1)
    transformedInput1 = np.int16(transformedInput1)

    samplerate, sound = wavfile.read(input)
    partSound1 = []
    for x in range(100):
        partSound1.append(sound[x])

    # partSound2 = []
    # for x in range(600):
    #     partSound2.append(direct[x])

    partSound2 = []
    for x in range(100):
        partSound2.append(direct[x]  // maskSize1)
    partSound3 = []
    for x in range(100):
        partSound3.append(transformedInput1[x])

    plt.figure(figsize=(9, 5))
    plt.ylabel('loudness[dB]')
    plt.xlabel('number of samples')
    plt.plot(partSound1, label="original")
    plt.plot(partSound2, 'ko', markersize=2, label="FT components")
    # 'orange', label="direct (FT components)",
    plt.plot(partSound3, 'red', label="inverse (Transformed signal, kernel size 9)")
    plt.legend()
    plt.show()


def MultiLineFTPlot():
    print("reading signal")
    # Create an instance of `QApplication`
    input = "D:/Python/FT-1-dipl/FT-1-Generator/files/sine.wav"
    rate, input_sig = wavfile.read(input)
    np_sig = input_sig
    np_sig = np_sig.astype(float)

    print("creating kernel ")
    maskSize1 = 11
    kernel1 = cv.ft.createKernel(cv.ft.LINEAR, maskSize1, 1)
    print("transforming")
    transformedInput1 = cv.ft.FT02D_process(np_sig, kernel1)
    transformedInput1 = np.int16(transformedInput1)

    print("creating kernel ")
    maskSize2 = 30
    kernel2 = cv.ft.createKernel(cv.ft.LINEAR, maskSize2, 1)
    print("transforming")
    transformedInput2 = cv.ft.FT02D_process(np_sig, kernel2)
    transformedInput2 = np.int16(transformedInput2)

    print("plotting")
    # plt.figure(figsize=(4, 3))
    samplerate, sound = wavfile.read(input)
    partSound1 = []
    for x in range(100):
        partSound1.append(sound[x])

    partSound2 = []
    for x in range(100):
        partSound2.append(transformedInput1[x])

    partSound3 = []
    for x in range(100):
        partSound3.append(transformedInput2[x])

    plt.figure(figsize=(9, 5))
    plt.ylabel('loudness[dB]')
    plt.xlabel('number of samples')
    plt.plot(partSound1, label="original")
    plt.plot(partSound2, 'orange', label="kernel size 11")
    plt.plot(partSound3, 'red', label="kernel size 30")
    plt.legend()
    plt.show()
    print("exit")

    maskSize2 = 20
    kernel2 = cv.ft.createKernel(cv.ft.LINEAR, maskSize2, 1)


if __name__ == '__main__':
    """Main function."""
    FTTutorialPlot()
