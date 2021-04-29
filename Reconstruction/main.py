import math
from scipy.io.wavfile import write
import cv2 as cv
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

# Reading file
input = "sine.wav"
rate, input_sig = wavfile.read(input)
samplerate, sound = wavfile.read(input)

sample = []
mask = []

# Artificialy creating damaged file
for x in range(100):
    if 10 <= x <= 20:
        sample.append(0)
        mask.append(0)
    else:
        sample.append(sound[x])
        mask.append(1)


# Ploting mask
plt.figure(figsize=(4, 3))
plt.ylabel('loudness[dB]')
plt.xlabel('number of samples')
plt.plot(sample, label="original")
plt.legend()
plt.show()

# Ploting mask
plt.figure(figsize=(4, 3))
plt.ylabel('loudness[dB]')
plt.xlabel('number of samples')
plt.plot(mask, label="original")
plt.legend()
plt.show()

# Creating mask
mask = np.array(mask)
data = mask.astype(np.float32)
write("mask.wav", samplerate, data)

# Creating sample
sample = np.array(sample)
data = sample.astype(np.float32)
write("sample.wav", samplerate, data)


output = np.array([])
cv.ft.inpaint(sample, mask, 2, cv.ft.LINEAR, cv.ft.ITERATIVE, output)
# f1 = open("sample.wav", "x")
# f1.write(sample)
# f1.close()

# Creating a mask
# f2 = open("mask.wav", "x")
# f2.write(mask)
# f2.close()
#
# # Creating a mask
# f2 = open("mask.wav", "x")
# samplerate, maskSample = wavfile.read("mask.wav")




