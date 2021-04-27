import math

import cv2 as cv
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt


# size 2 = 0,5
# size 3 = 0.33 0.66
# size 4 = 0.25 0.5 0.75
def GET_LINEAR_VECTOR(SIZE, COLUM_FORMAT):
    firstPart = []
    secPart = []

    if (COLUM_FORMAT == True):
        for x in range(SIZE):
            if (x == 0):
                firstPart.append([0])
                continue
            else:
                firstPart.append([x / SIZE])
                secPart.insert(0, [x / SIZE])
        firstPart.append([1])
        ret = firstPart + secPart
        ret.append([0])
    else:
        for x in range(SIZE):
            if (x == 0):
                firstPart.append(0)
                continue
            else:
                firstPart.append(x / SIZE)
                secPart.insert(0, x / SIZE)
        firstPart.append(1)
        ret = firstPart + secPart
        ret.append(0)
    return ret


# SIN
# [0, 0.707, 1, 0.707, 0]
# [0, 0.38, 0.70, 0.92, 1, 0.92, 0.70, 0.38, 0]
def GET_SIN_VECTOR(SIZE, COLUM_FORMAT):
    firstPart = []
    secPart = []
    if (COLUM_FORMAT == True):
        for x in range(SIZE):
            if (x == 0):
                firstPart.append([0])
                continue
            else:
                position = (x / SIZE) * 0.5
                firstPart.append([math.sin(((x / SIZE) * 0.5) * math.pi)])
                secPart.insert(0, [math.sin(((x / SIZE) * 0.5) * math.pi)])
        firstPart.append([1])
        ret = firstPart + secPart
        ret.append([0])
    else:
        for x in range(SIZE):
            if (x == 0):
                firstPart.append(0)
                continue
            else:
                firstPart.append(math.sin(((x / SIZE) * 0.5) * math.pi))
                secPart.insert(0, math.sin(((x / SIZE) * 0.5) * math.pi))
        firstPart.append(1)
        ret = firstPart + secPart
        ret.append(0)
    return ret


# DUAL
# [1, 0, 1, 0, 1]
def GET_DUAL_VECTOR(SIZE, COLUM_FORMAT):
    firstPart = []
    secPart = []
    if (COLUM_FORMAT == True):
        for x in range(SIZE):
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
        for x in range(SIZE):
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


def GET_SQUARE_VECTOR(SIZE, COLUM_FORMAT, MODIFICATION):
    firstPart = []
    secPart = []
    if (COLUM_FORMAT == True):
        for x in range(SIZE):
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
        for x in range(SIZE):
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


def CREATE_KERNEL(KERNEL_TYPE, SIZE):
    # LIN
    # [0, 0.5, 1, 0.5, 0] * [0, 0.5, 1, 0.5, 0]
    # [0, 0.33, 0.66, 1, 0.66, 0.33, 0] * [0, 0.33, 0.66, 1, 0.66, 0.33, 0]
    if KERNEL_TYPE == 1:
        print("Linear")
        V1 = GET_LINEAR_VECTOR(SIZE, False)
        V2 = GET_LINEAR_VECTOR(SIZE, True)
        KERNEL = np.array(V1) * np.array(V2)
    # SIN
    # [0, 0.707, 1, 0.707, 0] * [0], [0.707], [1], [0.707], [0]]
    elif KERNEL_TYPE == 2:
        print("Sinus")
        V1 = GET_SIN_VECTOR(SIZE, False)
        V2 = GET_SIN_VECTOR(SIZE, True)
        KERNEL = np.array(V1) * np.array(V2)
    # SIN LIN
    # [0, 0.707, 1, 0.707, 0] * [[0], [0.5], [1], [0.5], [0]]
    elif KERNEL_TYPE == 3:
        print("Sinus/linear")
        V1 = GET_SIN_VECTOR(SIZE, False)
        V2 = GET_LINEAR_VECTOR(SIZE, True)
        KERNEL = np.array(V1) * np.array(V2)
    # DUAL
    # [1, 0, 1, 0, 1] * [1, 0, 1, 0, 1]
    elif KERNEL_TYPE == 4:
        print("Dual")
        V1 = GET_DUAL_VECTOR(SIZE, False)
        V2 = GET_DUAL_VECTOR(SIZE, True)
        KERNEL = np.array(V1) * np.array(V2)
    # DUAL LIN
    # [1, 0, 1, 0, 1] * [0, 0.5, 1, 0.5, 0]
    elif KERNEL_TYPE == 5:
        print("Dual/lin")
        V1 = GET_DUAL_VECTOR(SIZE, False)
        V2 = GET_LINEAR_VECTOR(SIZE, True)
        KERNEL = np.array(V1) * np.array(V2)
    # SQUARE RUSPINNI
    # [0, 0, 1, 1, 1, 0, 0]
    # [[0], [0], [1], [1], [1], [0], [0]]
    elif KERNEL_TYPE == 6:
        print("Square Ruspinni")
        V1 = GET_SQUARE_VECTOR(SIZE, False, "RUSPINNI")
        V2 = GET_SQUARE_VECTOR(SIZE, True, "RUSPINNI")
        KERNEL = np.array(V1) * np.array(V2)
    # SQUARE
    # [0, 1, 1, 1, 1, 1, 0]
    # [[0], [1], [1], [1], [1], [1], [0]]
    elif KERNEL_TYPE == 7:
        print("Square ++ ")
        V1 = GET_SQUARE_VECTOR(SIZE, False, "None")
        V2 = GET_SQUARE_VECTOR(SIZE, True, "None")
        KERNEL = np.array(V1) * np.array(V2)

    # SQUARE R+
    # [0, 0, 1, 1, 1, 1, 0]
    # [[0], [0], [1], [1], [1], [1], [0]]
    elif KERNEL_TYPE == 8:
        print("Square/R+")
        V1 = GET_SQUARE_VECTOR(SIZE, False, "R+")
        V2 = GET_SQUARE_VECTOR(SIZE, True, "R+")
        KERNEL = np.array(V1) * np.array(V2)
    # SQUARE L+
    # [0, 1, 1, 1, 1, 0, 0]
    # [[0], [1], [1], [1], [1], [0], [0]]
    elif KERNEL_TYPE == 9:
        print("Square/L+")
        V1 = GET_SQUARE_VECTOR(SIZE, False, "L+")
        V2 = GET_SQUARE_VECTOR(SIZE, True, "L+")
        KERNEL = np.array(V1) * np.array(V2)
    # SQUARE  MIX1
    # [0, 1, 1, 1, 1, 0, 0]
    # [[0], [0], [1], [1], [1], [1], [0]]
    elif KERNEL_TYPE == 10:
        print("Square/L+R+")
        V1 = GET_SQUARE_VECTOR(SIZE, False, "L+")
        V2 = GET_SQUARE_VECTOR(SIZE, True, "R+")
        KERNEL = np.array(V1) * np.array(V2)
    # SQUARE  MIX2
    # [0, 0, 1, 1, 1, 1, 0]
    # [[0], [1], [1], [1], [1], [0], [0]]
    elif KERNEL_TYPE == 11:
        print("Square/R+L+")
        V1 = GET_SQUARE_VECTOR(SIZE, False, "R+")
        V2 = GET_SQUARE_VECTOR(SIZE, True, "L+")
        KERNEL = np.array(V1) * np.array(V2)
    # SQUARE  MIX2
    # [0, 0, 1, 1, 1, 1, 0]
    # [[0], [1], [1], [1], [1], [0], [0]]
    elif KERNEL_TYPE == 12:
        print("Square Ruspine/Linear")
        V1 = GET_SQUARE_VECTOR(SIZE, False, "RUSPINNI")
        LinSize = SIZE + 1
        V2 = GET_LINEAR_VECTOR(LinSize, True)
        KERNEL = np.array(V1) * np.array(V2)
        print("V1: " + str(V1))
        print("V2: " + str(V2))
    else:
        print("uknown type")
        KERNEL = []
    return KERNEL


def MULTILE_FT_Plot(TYPE):
    input = "E:/School/DP/FT-1-dipl/FT-1-Generator/files/sine.wav"
    rate, input_sig = wavfile.read(input)
    np_sig = input_sig
    np_sig = np_sig.astype(float)

    SIZE1 = 6
    KERNEL1 = CREATE_KERNEL(TYPE, SIZE1)
    print("------------------- ")
    print("KERNEL with size 2: ")
    print(CREATE_KERNEL(TYPE, 2))
    print("------------------- ")
    TransformedInput1 = cv.ft.FT02D_process(np_sig, KERNEL1)
    TransformedInput1 = np.int16(TransformedInput1)

    SIZE2 = 15
    KERNEL2 = CREATE_KERNEL(TYPE, SIZE2)
    TransformedInput2 = cv.ft.FT02D_process(np_sig, KERNEL2)
    TransformedInput2 = np.int16(TransformedInput2)

    # print("plotting")
    # plt.figure(figsize=(4, 3))
    directory = "E:/School/DP/FT-1-dipl/plot-files/"
    samplerate, sound = wavfile.read(input)
    partSound1 = []
    for x in range(100):
        partSound1.append(sound[x])

    partSound2 = []
    for x in range(100):
        partSound2.append(TransformedInput1[x])

    partSound3 = []
    for x in range(100):
        partSound3.append(TransformedInput2[x])

    fileName1 = "TYPE-" + str(TYPE) + "-SIZE- " + str(SIZE1) + ".wav"
    fileName2 = "TYPE-" + str(TYPE) + "-SIZE- " + str(SIZE2) + ".wav"
    wavfile.write(directory + fileName1,
                  44100, TransformedInput1)
    wavfile.write(directory + fileName2,
                  44100, TransformedInput2)
    # partSound3 = []
    # for x in range(100):
    #     partSound3.append(transformedInput2[x])

    plt.figure(figsize=(9, 5))
    plt.ylabel('loudness[dB]')
    plt.xlabel('number of samples')
    plt.plot(partSound1, label="original")
    plt.plot(partSound2, 'red', label="kernel size " + str(SIZE1))
    plt.plot(partSound3, 'orange', label="kernel size " + str(SIZE2))
    imgName1 = "TYPE-" + str(TYPE) + ".png"
    plt.savefig(imgName1)
    plt.legend()
    plt.show()
    # print("exit")


if __name__ == '__main__':
    """Main function."""
    MULTILE_FT_Plot(12)

    # for x in range(1, 12):
    #     MULTILE_FT_Plot(x)
