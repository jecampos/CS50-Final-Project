import sounddevice as sd
import numpy as np
from datetime import datetime
import pygame
import threading

fs = 48000
duration = 1000  # 1 hr limit

pygame.init()

DIMENSION = (600, 400)

SCREEN = pygame.display.set_mode(DIMENSION)

SCREEN.fill((0, 0, 0))

x = 0

def print_sound(indata, frames, time, status):
    global x

    volume_norm = np.linalg.norm(indata)*10
    # print (int(volume_norm))
    pygame.draw.rect(SCREEN, (255,255,255), (x, DIMENSION[1] - int(volume_norm), 1, int(volume_norm)))
    x += 1
    print(x)
    if x > DIMENSION[0]:
        # print("here")
        SCREEN.fill((0,0,0))
        x = 0

    pygame.display.update()


myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='float64')
# start timer of recording
print("[START RECORDING]")
startRecording = datetime.now()
endRecording = 0

def hello():
    with sd.InputStream(callback=print_sound):
        sd.sleep(duration)


thr1 = threading.Thread(target=hello, args=(), kwargs={})

thr1.start()

print(thr1.isAlive())


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

# for i in myrecording:
#     print(" | " * int(i[0]))

# pygame.init()

# DIMENSION = (600, 400)

# SCREEN = pygame.display.set_mode(DIMENSION)

# SCREEN.fill((0, 0, 0))

# while True:

#     for events in pygame.event.get():

#         if  events.type == pygame.QUIT:
#             pygame.quit()
#             break


    
    
