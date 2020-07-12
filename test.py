import sounddevice as sd
import numpy as np
from datetime import datetime

fs = 48000
duration = 360  # 1 hr limit

myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='float64')
# start timer of recording
start = datetime.now()
end = 0

while True:
    command = input("say stop to finish recording: ")
    if command == "stop":
        # end timer of recording
        end = datetime.now()
        sd.stop()
        break

# get the record time by subtracting end with start
recordTime = end - start
print(recordTime)

# play recording
sd.play(myrecording, fs)

# start timer 
playStart = datetime.now()
playEnd = datetime.now()
# don't end the program while recording is still playing
while playEnd - playStart <= recordTime:
    print(playEnd - playStart)
    playEnd = datetime.now()
