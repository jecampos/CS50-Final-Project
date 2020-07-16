
import os
import pyaudio
import struct
import numpy as np
import pygame
import tkinter
from tkinter import filedialog
import wave

# Pygame window dimension
DIMENSION = (1200, 600)

# LOAD images from ./resources/
RECORD_IMG = pygame.image.load(os.path.join('resources', 'record-80.png'))
PLAY_IMG = pygame.image.load(os.path.join('resources', 'play-80.png'))
STOP_IMG = pygame.image.load(os.path.join('resources', 'stop-80.png'))
SAVE_IMG = pygame.image.load(os.path.join('resources', 'icons8-save-40.png'))

# images coordinates
R_COORDS = (400, 100)
P_COORDS = (500, 100)
STP_COORDS = (600, 100)
SVE_COORDS = (700, 120)

isRecording = False
record = None
recordData = []
isPlaying = False
playFile = None

# Create recordings folder if it doesn't exist
if not os.path.exists("recordings"):
	os.makedirs("recordings")

# Initialize pygame
pygame.init()

# create pygame window
screen = pygame.display.set_mode(DIMENSION)

# Pygame title
pygame.display.set_caption('Voice App')

# surface for sound visualization
sound = pygame.Surface((1200, 400))

CHUNK = 1024 
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

	"""
	Starts recording audio
	PARAMS: None
	RETURN: None
	"""

	global record, isRecording, recordData

	isRecording = True
	recordData = []


	record = p.open(
		format=FORMAT,
		channels=CHANNELS,
		rate=RATE,
		input=True,
		output=True,
		frames_per_buffer=CHUNK
	)


def stopRecording():
	
	"""
	Stops the recording
	PARAMS: None
	RETURN: None
	"""

	# Stop and close the stream 
	global isRecording

	isRecording = False

	record.stop_stream()
	record.close()

	# Save the recorded data 
	closeR = wave.open("./recordings/.rec", 'wb')
	closeR.setnchannels(CHANNELS)
	closeR.setsampwidth(p.get_sample_size(FORMAT))
	closeR.setframerate(RATE)
	closeR.writeframes(b''.join(recordData))
	closeR.close()



def playRecord():

	""" 
	PLAYS RECORDING
	PARAMS: None
	RETURN: None
	"""

	global playFile, isPlaying

	if os.path.exists("./recordings/.rec"):
		playFile = wave.open("./recordings/.rec", 'rb')
		isPlaying = True
	else:
		print("No recording yet")


def saveRecord():

	"""
	SAVES RECORD TO A .wav FILE
	PARAMS: None
	RETURN: None
	"""

	# Check if there are recordings
	if not os.path.exists("./recordings/.rec"):

		print("No recording")
		return None

	# get save as prompt
	tk = tkinter.Tk()
	filename = filedialog.asksaveasfilename(initialdir="./Final-Project/recordings", title="Save Recording", filetypes = (("wav files", ".wav"), ("all files", ".*")))
	tk.destroy()

	# save file
	os.rename("./recordings/.rec", f"{filename}.wav")


# While the program is running
while True:

	# Listen for events
	for event in pygame.event.get():

		# if exit button is clicked exit the program
		if event.type == pygame.QUIT:

			if os.path.exists('./recordings/.rec'):
				os.remove('./recordings/.rec')
			pygame.quit()
			exit()

		# for mouse button down events
		elif event.type == pygame.MOUSEBUTTONDOWN:

			# get mouse x and y coordinates
			mouseX, mouseY = event.pos
			
			# Check if record surface was pressed
			recordImgPressed = pygame.Rect(R_COORDS[0], R_COORDS[1], RECORD_IMG.get_width(), RECORD_IMG.get_height())
			if recordImgPressed.collidepoint(mouseX, mouseY) and not isRecording:

				startRecording()
				print("clicked record")

			# Check if play surface was pressed
			playImgPressed = pygame.Rect(P_COORDS[0], P_COORDS[1], PLAY_IMG.get_width(), PLAY_IMG.get_height())
			if playImgPressed.collidepoint(mouseX, mouseY):

				playRecord()
				print("clicked play")

			# Check if stop surface was pressed
			stopImgPressed = pygame.Rect(STP_COORDS[0], STP_COORDS[1], STOP_IMG.get_width(), STOP_IMG.get_height())
			if stopImgPressed.collidepoint(mouseX, mouseY) and isRecording:
				
				stopRecording()
				print("clicked stop")


			saveImgPressed = pygame.Rect(SVE_COORDS[0], SVE_COORDS[1], SAVE_IMG.get_width(), SAVE_IMG.get_height())
			if saveImgPressed.collidepoint(mouseX, mouseY):
				
				saveRecord()
				print("clicked save")
			

	# set background color for surfaces
	screen.fill((127, 0, 0))
	sound.fill((0, 0, 0))

	data = struct.unpack(str(CHUNK) + 'h', stream.read(CHUNK))

	# scale the values in data by integer division of 40
	# then store them in a new list
	streamData = []
	for audioData in data:
		if audioData < 0:
			streamData.append(-1 * (abs(audioData // 40)))
		else:
			streamData.append(audioData // 40)

	# x coordinate of the line
	x = 0
	# Random RGB values for the line 
	R = np.random.randint(0, 255)
	G = np.random.randint(0, 255)
	B = np.random.randint(0, 255)

	# Loop through data and draw a line
	for i in range(len(streamData) - 1):

		pygame.draw.line(sound, (R, G, B), (x, streamData[i] + 200), (x + 2, streamData[i + 1] + 200), 3)
		# pygame.draw.rect(sound, (R, G, B), (x, streamData[i] + 200, x + 2, streamData[i + 1]))
		x += 2

	# Check if we are recording
	if isRecording:
		data = record.read(CHUNK)
		recordData.append(data)

	# Check if we are playing a recording
	if isPlaying:
		
		data = playFile.readframes(CHUNK)
		if len(data) > 0:
			stream.write(data)
		else:
			isPlaying = False
			# close file
			playFile.close()


	# Blit to the screen the images and the sound surface
	screen.blit(sound, (0, 200))
	screen.blit(RECORD_IMG, R_COORDS)
	screen.blit(PLAY_IMG, P_COORDS)
	screen.blit(STOP_IMG, STP_COORDS)
	screen.blit(SAVE_IMG, SVE_COORDS)

	# update the window
	pygame.display.update()


