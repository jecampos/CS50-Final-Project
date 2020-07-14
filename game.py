
import pyaudio
import struct
import numpy as np
import pygame
import os

DIMENSION = (1200, 600)

RECORD_IMG = pygame.image.load(os.path.join('resources', 'record-80.png'))
PLAY_IMG = pygame.image.load(os.path.join('resources', 'play-80.png'))

pygame.init()

screen = pygame.display.set_mode(DIMENSION)

sound = pygame.Surface((1200, 400))

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

def startRecording():

	record = p.open(
		format=FORMAT,
		channels=CHANNELS,
		rate=RATE,
		input=True,
		output=True,
		frames_per_buffer=CHUNK
	)

	return record

def stopRecording(record):

	record.stop_stream()
	record.close()


def playRecord(recordData):

	pass


while True:

	R = np.random.randint(0, 255)
	G = np.random.randint(0, 255)
	B = np.random.randint(0, 255)

	for events in pygame.event.get():

		if events.type == pygame.QUIT:

			pygame.quit()
			exit()

	screen.fill((127, 0, 0))
	sound.fill((0, 0, 0))

	data = struct.unpack(str(CHUNK) + 'h', stream.read(CHUNK))

	data_new = []
	for i in range(len(data)):
		if data[i] < 0:
			data_new.append(-1 * (abs(data[i]) // 40))
		else:
			data_new.append(data[i] // 40)

	x = 0
	for i in range(len(data_new) - 1):

		pygame.draw.line(sound, (R, G, B), (x, data_new[i] + 200), (x + 2, data_new[i + 1] + 200), 3)
		x += 2

	screen.blit(sound, (0, 200))
	screen.blit(RECORD_IMG, (525, 100))
	screen.blit(PLAY_IMG, (625, 100))

	

	pygame.display.update()


