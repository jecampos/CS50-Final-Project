import tkinter as tk
import numpy as np
import pyaudio
from datetime import datetime
from PIL import Image, ImageTk, ImageDraw
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
filename = "test.wav"

p = pyaudio.PyAudio()

filename = "test.wav"

frames = [] # frames to store audio 

stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    frames_per_buffer=CHUNK,
    input=True,
    output=True
)

record = p.open(
	format=FORMAT,
	channels=CHANNELS,
	rate=44100,
	input=True,
	output=True,
	frames_per_buffer=1024
)


isRecording = False
isStopped = False
isPlaying = False

def main():
    # creating tkinter object & setting basic settings
    root = tk.Tk()
    root.geometry("800x700")

    # status of recording 
    statusLabel = tk.Label(root, text="Start Recording")
    statusLabel.place(x=350, y=100)

    # creating record button (recommended size 80x80 pixels icons as it looks pretty good)
    recordPhoto = ImageTk.PhotoImage(Image.open("resources\\record-80.png"))

    recordButton = tk.Button(root, image=recordPhoto, height=40, width=40, command = lambda: startRecording())
    recordButton["border"] = "0"
    recordButton.place(x=200, y=400)

    # creating stop button
    stopPhoto = ImageTk.PhotoImage(Image.open("resources\\stop-80.png"))

    # keep size to 40
    stopButton = tk.Button(root, image=stopPhoto, height=40, width=40, command= lambda: stopRecording())
    stopButton["border"] = "0" # making button round
    stopButton.place(x=275, y=400)

    # creating play button
    playPhoto = ImageTk.PhotoImage(Image.open("resources\\play-80.png"))

    # keep size to 40
    playButton = tk.Button(root, image=playPhoto, height=40, width=40, command= lambda: playRecording())
    playButton["border"] = "0" # making button round
    playButton.place(x=350, y=400)

    # records 
    if isRecording:

        data = record.read(CHUNK)
        frames.append(data)

    # stops
    elif isStopped:

        record.stop_stream()
        record.close()

        savewf = wave.open(filename, 'wb')
        savewf.setnchannels(CHANNELS)
        savewf.setsampwidth(p.get_sample_size(FORMAT))
        savewf.setframerate(RATE)
        savewf.writeframes(b''.join(frames))
        savewf.close()

    # plays
    elif isPlaying:

        playwf = wave.open(filename, 'rb')
        playdata = playwf.readframes(CHUNK)

        while len(data) > 0:
            stream.write(playdata)
            playdata = playwf.readframes(CHUNK)



    # run tkinter
    root.mainloop()

def startRecording():

    global isRecording, isStopped, isPlaying

    isRecording = True
    isStopped = False
    isPlaying = False

    while isRecording == True:
        data = record.read(CHUNK)
        frames.append(data)

def stopRecording():

    global isRecording, isStopped, isPlaying

    isRecording = False
    isStopped = True
    isPlaying = False

    record.stop_stream()
    record.close()

    savewf = wave.open(filename, 'wb')
    savewf.setnchannels(CHANNELS)
    savewf.setsampwidth(p.get_sample_size(FORMAT))
    savewf.setframerate(RATE)
    savewf.writeframes(b''.join(frames))
    savewf.close()


def playRecording():

    global isRecording, isStopped, isPlaying

    isRecording = False
    isStopped = False
    isPlaying = True

    playwf = wave.open(filename, 'rb')
    playdata = playwf.readframes(CHUNK)

    while len(playdata) > 0:
        stream.write(playdata)
        playdata = playwf.readframes(CHUNK)

main()


# Image by OpenClipart-Vectors from Pixabay https://pixabay.com/vectors/sound-button-glossy-set-player-145674/\
# also from https://icons8.com/icon/set/record%20icon/windows