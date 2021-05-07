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

sample_dir = "sample.wav"
mask_dir = "mask.wav"

# Creating sample
sample = np.array(sample)
data = sample.astype(np.float32)
write(sample_dir, samplerate, data)

# Creating mask
mask = np.array(mask)
data = mask.astype(np.uint8)
write(mask_dir, samplerate, data)


# Reading files for reconstruction
samplerate, sample_file = wavfile.read(sample_dir)
samplerate, mask_file = wavfile.read(mask_dir)

# Ploting sample
# plt.ylabel('loudness[dB]')
# plt.xlabel('number of samples')
# plt.plot(sample_file, label="sample wave")
# plt.legend()
# plt.show()

# Ploting mask
# plt.ylabel('loudness[dB]')
# plt.xlabel('number of samples')
# plt.plot(mask_file, label="mask")
# plt.legend()
# plt.show()

# Reconstruction
output = np.array([])
output = cv.ft.inpaint(sample_file, mask_file, 3, cv.ft.LINEAR, cv.ft.ITERATIVE, output)


# Ploting reconstruction
plt.ylabel('loudness[dB]')
plt.xlabel('number of samples')
plt.plot(output, label="reconstructed")
plt.legend()
plt.show()