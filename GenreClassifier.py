import numpy as np
from scipy import signal
from scipy.io import wavfile
import matplotlib.pyplot as plt
from scipy.fftpack import fft  # fourier transform
import os

FRAME = 1000  # 1kHz
MAX_FREQ = 16
MARGIN_OF_ERROR = 0.3 # +-30%

print("Please enter the absolute path to the folder with multiple .wav files or to the .wav file itself: ")
files_to_classify = input()


files = []
for r, d, f in os.walk(files_to_classify):
    for file in f:
        files.append(os.path.join(r, file))

temp = []
for file_to_classify in files:
    counter = 0
    print(file_to_classify)
    fs, Audiodata = wavfile.read(file_to_classify)

    n = len(Audiodata)
    AudioFreq = fft(Audiodata)
    AudioFreq = AudioFreq[0:int(np.ceil((n + 1) / 2.0))]  # Half of the spectrum
    MagFreq = np.abs(AudioFreq)
    MagFreq = MagFreq / float(n)  # Magnitude
    MagFreq = MagFreq ** 2
    if n % 2 > 0:  # fft odd
        MagFreq[1:len(MagFreq)] = MagFreq[1:len(MagFreq)] * 2
    else:  # fft even
        MagFreq[1:len(MagFreq) - 1] = MagFreq[1:len(MagFreq) - 1] * 2

    samples_per_frame = int(int(np.ceil((n + 1) / 2.0)) / 22050)

    MagFreq1 = []
    for mag in MagFreq:
        MagFreq1.append(mag[0])

    total_num_of_samples = len(MagFreq1)
    kHz = 0
    MagFreq1.sort(reverse=True)
    target = MagFreq1[9]
    for mag in MagFreq1:
        if 1-MARGIN_OF_ERROR<mag/target<1+MARGIN_OF_ERROR:
            counter += 1
        else:
            break
    total_score = 100000*counter/total_num_of_samples

    if total_score > 300:
        print("Class: Metal")
    elif total_score>10:
        print("Class: Folk")
    else:
        print("Class: Classical")
