import sounddevice as sd
import numpy as np

fs = 48000
duration = 3  # seconds

myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='float64')
sd.wait()

sd.play(myrecording, fs)
sd.wait()