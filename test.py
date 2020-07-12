import sounddevice as sd
import numpy as np
from datetime import datetime

fs = 48000
duration = 360  # 1 hr limit

myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='float64')
# start timer of recording
print("[START RECORDING]")
startRecording = datetime.now()
endRecording = 0

while True:
    command = input("say stop to finish recording: ")
    if command == "stop":
        # end timer of recording
        endRecording = datetime.now()
        sd.stop()
        break

# get the record time by subtracting end with start
recordTime = endRecording - startRecording
print(f"[RECORD TIME] {recordTime}...")

# play recording
print("[PLAYBACK]")
sd.play(myrecording, fs)

# start timer 
playRecord = datetime.now()
endRecord = datetime.now()
# don't end the program while recording is still playing
while endRecord - playRecord <= recordTime:
    endRecord = datetime.now()

print("[END OF PLAYBACK]")
