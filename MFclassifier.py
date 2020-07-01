import numpy as np
from scipy import signal
from scipy.io import wavfile
import matplotlib.pyplot as plt
from scipy.fftpack import fft  # fourier transform
import os

FRAME = 1000  # 1kHz
MAX_FREQ = 16

print("Please enter the absolute path to the folder with multiple .wav files or to the .wav file itself: ")
files_to_classify = input()


files = []
for r, d, f in os.walk(files_to_classify):
    for file in f:
        files.append(os.path.join(r, file))

temp = []
for file_to_classify in files:
    scores = []
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

    samples_per_frame = int(int(np.ceil((n + 1) / 2.0))/22050)

    MagFreq1 = []
    for mag in MagFreq:
        MagFreq1.append(mag[0])

    total_power = 0
    for i in range(FRAME*MAX_FREQ*samples_per_frame):
        total_power+=MagFreq1[i]

    for i in range(MAX_FREQ):
        curr_score = 0
        for j in range(FRAME*samples_per_frame):
            index = i*1000*samples_per_frame + j
            curr_score += MagFreq1[index]

        scores.append(curr_score/total_power)

    for i, score in enumerate(scores):
        scores[i] = [score, i]
    scores.sort(reverse=True)
    print(file_to_classify)

    top5 = []
    for score in scores:
        score[0] *=100
        score[1] += 1
        if score[1]<18:
            top5.append(score)
        if len(top5) == 5:
            break

    w_score = 0
    w_total = 0
    for top in top5:
        w_score += top[0]*top[1]
        w_total += top[0]

    weighted_score = w_score/w_total

    for i, mag in enumerate(MagFreq1):
        if i > 18*1000*samples_per_frame:
            MagFreq1[i] = [0, i/(1000*samples_per_frame)]
            continue
        MagFreq1[i] = [mag, i/(1000*samples_per_frame)]


    MagFreq1.sort(reverse=True)

    maxs = []

    max_positions = 0
    total_weight = 0
    for i in range(10):
        max_positions += MagFreq1[i][0]*MagFreq1[i][1]
        total_weight += MagFreq1[i][0]

    approx_position = max_positions/total_weight
    final_score = (max_positions/total_weight+w_score/w_total)/2

    if final_score > 9:
        print("Class: Female")
        print("Status: Almost sure")
    elif final_score<8:
        print("Class: Male")
        print("Status: Almost sure")
    else:
        if weighted_score >8.5 or approx_position > 8.5:
            print("Class: Female")
            print("Status: Not so sure")
        else:
            print("Class: Male")
            print("Status: Not so sure")
    temp.append((max_positions/total_weight+w_score/w_total)/2)