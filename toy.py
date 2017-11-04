import pygame
from pygame import mixer, USEREVENT
import sys
from os import listdir
from os.path import isfile, join

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def print(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


pygame.init()

# Set the width and height of the screen [width,height]
size = [500, 700]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()
joystick_count = pygame.joystick.get_count()

joysticks = []
for i in range(joystick_count):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()
    joysticks.append(joystick)

if len(joysticks) == 0:
    sys.stderr.write('missing joystick')
    pygame.quit()
    sys.exit(1)

# Get ready to print
textPrint = TextPrint()

# set music events
EVENT_MUSIC_STOP = 567

ASSETS_DIR = 'assets/music'
IGNORE_FILES = ['._.DS_Store', '.DS_Store']

mixer.init()
mixer.music.set_endevent(EVENT_MUSIC_STOP)
g_current_track = None

def play_music(n):
    global g_current_track
    
    # read directory sorted by name
    tracks = sorted(
        [f for f in listdir(ASSETS_DIR) if isfile(join(ASSETS_DIR, f)) and f not in IGNORE_FILES]
    )
    n = n % len(tracks)

    # stop playback when trying to play the same track twice
    if mixer.music.get_busy() and g_current_track == n:
        mixer.music.stop()
        g_current_track = None
        return

    try:
        print("Loading track {}: {}".format(n, tracks[n]))
        mixer.music.load(join(ASSETS_DIR, tracks[n]))
        mixer.music.play(1)
        g_current_track = n
    except pygame.error as e:
        mixer.music.stop()
        g_current_track = None
        print("Error: {}".format(e))

#
# physical buttons:
# ------------
# 11 10  9  8
#  7  6  5  4
#-------------
#
BUTTON_MAPPING = {
    0: 11,
    1: 10,
    2: 9,
    3: 8,
    4: 7,
    5: 6,
    6: 5,
    7: 4,
    8: 3,
    9: 2,
    10: 1,
    11: 0
}

# -------- Main Program Loop -----------
while done==False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print(event)
            play_music(BUTTON_MAPPING[event.button])
        elif event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")
        elif event.type == EVENT_MUSIC_STOP:
            print("music stop")
            mixer.music.stop()

    # DRAWING STEP
    screen.fill(WHITE)
    textPrint.reset()

    textPrint.print(screen, "Number of joysticks: {}".format(joystick_count) )
    textPrint.indent()

    # For each joystick:
    for i, joystick in enumerate(joysticks):
        textPrint.print(screen, "Joystick {}".format(i) )
        textPrint.indent()

        # Get the name from the OS for the controller/joystick
        name = joystick.get_name()
        textPrint.print(screen, "Joystick name: {}".format(name) )

        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        textPrint.print(screen, "Number of axes: {}".format(axes) )
        textPrint.indent()

        for i in range( axes ):
            axis = joystick.get_axis( i )
            textPrint.print(screen, "Axis {} value: {:>6.3f}".format(i, axis) )
        textPrint.unindent()

        buttons = joystick.get_numbuttons()
        textPrint.print(screen, "Number of buttons: {}".format(buttons) )
        textPrint.indent()

        for i in range( buttons ):
            button = joystick.get_button( i )
            textPrint.print(screen, "Button {:>2} value: {}".format(i,button) )
        textPrint.unindent()

        # Hat switch. All or nothing for direction, not like joysticks.
        # Value comes back in an array.
        hats = joystick.get_numhats()
        textPrint.print(screen, "Number of hats: {}".format(hats) )
        textPrint.indent()

        for i in range( hats ):
            hat = joystick.get_hat( i )
            textPrint.print(screen, "Hat {} value: {}".format(i, str(hat)) )
        textPrint.unindent()

        textPrint.unindent()

    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second
    clock.tick(20)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit ()

