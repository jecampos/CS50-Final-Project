
import pyaudio
import struct
import numpy as np
import pygame
import os
import wave

DIMENSION = (1200, 600)

RECORD_IMG = pygame.image.load(os.path.join('resources', 'record-80.png'))
PLAY_IMG = pygame.image.load(os.path.join('resources', 'play-80.png'))
STOP_IMG = pygame.image.load(os.path.join('resources', 'stop-80.png'))

R_IMG = (500, 100)
P_IMG = (600, 100)
S_IMG = (700, 100)

isRecording = False
record = None
recordData = []
isPlaying = False
playFile = None

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

	global record, isRecording

	isRecording = True


	record = p.open(
		format=FORMAT,
		channels=CHANNELS,
		rate=44100,
		input=True,
		output=True,
		frames_per_buffer=1024
	)


def stopRecording():

	# Stop and close the stream 
	global isRecording

	isRecording = False

	record.stop_stream()
	record.close()

	# Save the recorded data as a WAV file
	closeR = wave.open("test.wav", 'wb')
	closeR.setnchannels(CHANNELS)
	closeR.setsampwidth(p.get_sample_size(FORMAT))
	closeR.setframerate(RATE)
	closeR.writeframes(b''.join(recordData))
	closeR.close()



def playRecord():

	global playFile, isPlaying

	isPlaying = True

	playFile = wave.open("test.wav", 'rb')



while True:

	R = np.random.randint(0, 255)
	G = np.random.randint(0, 255)
	B = np.random.randint(0, 255)

	for event in pygame.event.get():

		if event.type == pygame.QUIT:

			pygame.quit()
			exit()

		elif event.type == pygame.MOUSEBUTTONDOWN:

			mouseX, mouseY = event.pos
			
			recordImgPressed = pygame.Rect(R_IMG[0], R_IMG[1], RECORD_IMG.get_width(), RECORD_IMG.get_height())
			if recordImgPressed.collidepoint(mouseX, mouseY) and not isRecording:

				startRecording()
				print("clicked record")


			playImgPressed = pygame.Rect(P_IMG[0], P_IMG[1], PLAY_IMG.get_width(), PLAY_IMG.get_height())
			if playImgPressed.collidepoint(mouseX, mouseY):

				playRecord()
				print("clicked play")

			stopImgPressed = pygame.Rect(S_IMG[0], S_IMG[1], STOP_IMG.get_width(), STOP_IMG.get_height())
			if stopImgPressed.collidepoint(mouseX, mouseY):
				
				stopRecording()
				print("clicked stop")

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

	if isRecording:
		data = record.read(1024)
		recordData.append(data)

	if isPlaying:

		data = playFile.readframes(1024)
		if len(data) > 0:
			stream.write(data)
		else:
			isPlaying = False


	screen.blit(sound, (0, 200))
	screen.blit(RECORD_IMG, R_IMG)
	screen.blit(PLAY_IMG, P_IMG)
	screen.blit(STOP_IMG, S_IMG)

	

	pygame.display.update()


