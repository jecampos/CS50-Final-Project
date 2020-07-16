
import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk

plt.style.use("ggplot")

# creating tkinter object
# root = tk.Tk()
# root.geometry("800x700")
# canvas = tk.Canvas(width=600, height=400)
# canvas.pack()

CHUNK = 600
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

stream = p.open(
	format=FORMAT,
	channels=CHANNELS,
	rate=RATE,
	input=True,
	output=True,
	frames_per_buffer=CHUNK
)

plt.ion()
fig, ax = plt.subplots()

x = np.arange(0, 600)
data = stream.read(CHUNK)
data_int16 = struct.unpack(str(CHUNK) + 'h', data)
data_new = []
for i in range(len(data_int16)):
	data_new.append(data_int16[i] % 600)
line, = ax.plot(x, data_new)
ax.set_ylim(-600, 600)


while True:
	data = struct.unpack(str(CHUNK) + 'h', stream.read(CHUNK))

	data_new = []
	for i in range(len(data_int16)):
		if data[i] < 0:
			data_new.append(-1 * (abs(data[i]) % 600))
		else:
			data_new.append(data[i] % 600)

	line.set_ydata(data_new)
	fig.canvas.draw()
	fig.canvas.flush_events()


