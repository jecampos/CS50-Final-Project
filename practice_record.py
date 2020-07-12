import sounddevice as sd
import numpy as np

fs = 48000
duration = 3600  # 1 hr limit

myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='float64')

while True:
    command = input("say stop to finish recording: ")
    if command == "stop":
        sd.stop()
        break

sd.play(myrecording, fs)
sd.wait()