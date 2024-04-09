import pygame
import time


# Initialize pygame mixer
pygame.mixer.init()

# Define the alarm function
def alarm(germrate, alarm_sound='path/to/alarm/file'):
    alarmlevel = 0.3
    if germrate > alarmlevel:
        # Load the sound
        pygame.mixer.music.load(alarm_sound)
        for _ in range(3):  # Play it 3 times
            pygame.mixer.music.play()
            # Wait for the sound to finish playing
            while pygame.mixer.music.get_busy():
                time.sleep(1)
        # After playing the sound 3 times, stop the mixer
        pygame.mixer.music.stop()