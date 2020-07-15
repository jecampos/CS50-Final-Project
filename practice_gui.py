import tkinter as tk
import numpy as np
import pyaudio
from datetime import datetime
from PIL import Image, ImageTk, ImageDraw

CHUNK = 600
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

frames = [] # frames to store audio 

def main():
    # creating tkinter object & setting basic settings
    root = tk.Tk()
    root.geometry("800x700")

    # status of recording 
    statusLabel = tk.Label(root, text="Start Recording")
    statusLabel.place(x=350, y=100)

    # creating record button (recommended size 80x80 pixels icons as it looks pretty good)
    recordPhoto = ImageTk.PhotoImage(Image.open("resources\\record-80.png"))

    recordButton = tk.Button(root, image=recordPhoto, height=40, width=40, command = lambda: startRecording(statusLabel))
    recordButton["border"] = "0"
    recordButton.place(x=200, y=400)

    # creating stop button
    stopPhoto = ImageTk.PhotoImage(Image.open("resources\\stop-80.png"))

    # keep size to 40
    stopButton = tk.Button(root, image=stopPhoto, height=40, width=40, command= lambda: stopRecording(statusLabel))
    stopButton["border"] = "0" # making button round
    stopButton.place(x=275, y=400)

    # run tkinter
    root.mainloop()

def startRecording(statusLabel):

    statusLabel['text'] = "Recording..."
     
    stream = p.open(
	format=FORMAT,
	channels=CHANNELS,
	rate=RATE,
	input=True,
	output=True,
	frames_per_buffer=CHUNK

    while (True):
        data = stream.read(chunk)
        frames.append(data)

)


def stopRecording(statusLabel):
    statusLabel['text'] = "Playback"

main()

def draw():
    x = 0
    for i in range(len(myrecording) // 1000):
        print(x)
        canvas.create_rectangle(x, 300 - int(myrecording[i] % 300), x, 300, fill="gray")
        canvas.pack()
        x += 1
        if x > 600:
            x = 0

# Image by OpenClipart-Vectors from Pixabay https://pixabay.com/vectors/sound-button-glossy-set-player-145674/\
# also from https://icons8.com/icon/set/record%20icon/windows