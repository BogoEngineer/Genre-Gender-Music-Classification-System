# TelecommunicationsHomework

A small data-science project aimed to demonstrate audio classification. There are two classifiers:
- Female/Male voice classifier
- Music genre classifier (Serbian folk, Metal or Classical)

Both of those classifiers are coded/not ML functions that use arbitrarily chosen parameters that were the result of observing power spectrum graphs of audio files in training set.
Those classifiers were later tested on audio files from test set.

FFT ([Fast Fourier transform](https://en.wikipedia.org/wiki/Fast_Fourier_transform)) was used for getting frequency domain from time domain of an audio file.

# USAGE
Every file requires an input that consist of an absolute path to the folder that contains multiple .wav files or a direct absolute path to a single .wav file.
For visual representation of given files' power spectrums use main.py script.
For the gender classifier use MFclassifier.py script.
For the genre classifier use GenreClassifier.py script.
