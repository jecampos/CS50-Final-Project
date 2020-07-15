import tkinter as tk
import numpy as np
import sounddevice as sd
from datetime import datetime
from PIL import Image, ImageTk, ImageDraw


# creating tkinter object
root = tk.Tk()
root.geometry("600x600")
canvas = tk.Canvas(width=600, height=300)
canvas.pack()

# variables for recording
fs = 48000
duration = 360 

# start recording
myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int')

# stopRecording method thats plays back audio when clicked
def stopRecording():
    sd.stop()
    statusLabel['text'] = "Playback"
    sd.play(myrecording, fs)


# status of recording label
statusLabel = tk.Label(root, text="Start Recording")
statusLabel.pack()

# creating stop button (recommended size 80x80 pixels as it looks pretty good)
stopPhoto = ImageTk.PhotoImage(Image.open("resources\\stop-80.png"))

stopButton = tk.Button(root, image=stopPhoto, height=80, width=80, command= lambda: stopRecording())
stopButton["border"] = "0" # making button round
stopButton.pack()

def draw():
    x = 0
    for i in range(len(myrecording) // 1000):
        print(x)
        canvas.create_rectangle(x, 300 - int(myrecording[i] % 300), x, 300, fill="gray")
        canvas.pack()
        x += 1
        if x > 600:
            x = 0

# run tkinter
root.after(0, draw)
root.mainloop()

# Image by OpenClipart-Vectors from Pixabay https://pixabay.com/vectors/sound-button-glossy-set-player-145674/\
# also from https://icons8.com/icon/set/record%20icon/windows