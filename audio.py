
import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt
import time

plt.style.use("ggplot")

CHUNK = 1024 * 4
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

x = np.arange(0, CHUNK)
data = stream.read(CHUNK)
data_int16 = struct.unpack(str(CHUNK) + 'h', data)
line, = ax.plot(x, data_int16)
ax.set_ylim([-2**15,(2**15)-1])


while True:
	data = struct.unpack(str(CHUNK) + 'h', stream.read(CHUNK))
	line.set_ydata(data)
	fig.canvas.draw()
	fig.canvas.flush_events()


