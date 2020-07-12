import matplotlib 
import sounddevice as sd
import numpy as np
import pygame

WIDTH, HEIGHT = 600, 400
x = 0

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

def print_sound(indata, frames, time, status):
    global x

    volume_norm = np.linalg.norm(indata)*10
    # print (int(volume_norm))
    pygame.draw.rect(screen, (255,255,255), (x, HEIGHT - int(volume_norm), 1, int(volume_norm)))
    x += 1

    if x > WIDTH:
        print("here")
        screen.fill((0,0,0))
        x = 0

    pygame.display.update()


while True:

    # screen.fill((0, 0, 0))

    with sd.InputStream(callback=print_sound):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        sd.sleep(100000)


#  From https://stackoverflow.com/questions/40138031/how-to-read-realtime-microphone-audio-volume-in-python-and-ffmpeg-or-similar
