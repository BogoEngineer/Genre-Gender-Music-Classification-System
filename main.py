import numpy as np
from scipy import signal
from scipy.io import wavfile
import matplotlib.pyplot as plt
from scipy.fftpack import fft # fourier transform
import os

class Solution:
    def __init__(self, input_path):
        self.input_path = input_path
        self.files = []
        for r,d,f in os.walk(input_path):
            for file in f:
                self.files.append(os.path.join(r, file))

    def plot(self):
        for file in self.files:
            fs, Audiodata = wavfile.read(file)
            title = []
            for c in reversed(file):
                if c == "\\":
                    break
                title.insert(0, c)

            n = len(Audiodata)
            AudioFreq = fft(Audiodata)
            AudioFreq = AudioFreq[0:int(np.ceil((n + 1) / 2.0))]  # Half of the spectrum
            MagFreq = np.abs(AudioFreq)
            MagFreq = MagFreq / float(n)  # Magnitude

            freqAxis = np.arange(0, int(np.ceil((n + 1) / 2.0)), 1.0) * (fs / n)

            # power spectrumc
            MagFreq = MagFreq ** 2
            if n % 2 > 0:  # fft odd
                MagFreq[1:len(MagFreq)] = MagFreq[1:len(MagFreq)] * 2
            else:  # fft even
                MagFreq[1:len(MagFreq) - 1] = MagFreq[1:len(MagFreq) - 1] * 2
            plt.figure(num=''.join(title))
            freqAxis = np.arange(0, int(np.ceil((n + 1) / 2.0)), 1.0) * (fs / n)

            MagFreq1 = []
            for i,mag in enumerate(MagFreq):
                MagFreq1.append(mag[0])

            plt.plot(freqAxis /1000.0, MagFreq1)  # Power spectrum
            plt.xlabel('Frequency (kHz)')
            plt.ylabel('Power spectrum')

        plt.show()

if __name__ == "__main__":
    print("Please enter the absolute path to the folder with multiple .wav files or to the .wav file itself: ")
    input_path = input()
    solution = Solution(input_path)
    solution.plot()

