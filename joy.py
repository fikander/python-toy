import pygame
from pygame import mixer, USEREVENT
import sys

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputting the
# information.
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

joy1 = joysticks[0]

# Get ready to print
textPrint = TextPrint()

def get_buttons_on(joy):
    buttons_on = set()
    for i in range(joy.get_numbuttons()):
        if joy.get_button(i):
            buttons_on.add(i)
    return buttons_on

old_buttons_on = get_buttons_on(joy1)

def get_button_pressed(joy):
    global old_buttons_on
    buttons_on = get_buttons_on(joy)
    new_buttons_on = buttons_on.difference(old_buttons_on)
    old_buttons_on = buttons_on
    if len(new_buttons_on):
        return new_buttons_on.pop()
    else:
        return None

# set music events
EVENT_MUSIC_STOP = 567

mixer.init()
mixer.music.set_endevent(EVENT_MUSIC_STOP)

def play_music(n):
    tracks = [
        "assets/music/czerwone_gitary-ciagle_pada.mp3",
        "assets/music/gilberto-desafinado.mp3",
        "assets/music/moby-heaven.mp3",
        "assets/music/native_american-whispering_wind.mp3",
        "assets/music/nat_king_cole-mona_lisa.mp3",
        "assets/music/rem-at_my_most_beautiful.mp3",
        "assets/music/track7.mp3",
        "assets/music/track8.mp3"
     ]
    n = n % len(tracks)
    try:
        mixer.music.load(tracks[n])
        print("Loaded track {}: {}".format(n, tracks[n]))
        mixer.music.play(1)
    except pygame.error as e:
        mixer.music.stop()
        print("Error: {}".format(e))

# -------- Main Program Loop -----------
while done==False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop

        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
            btn = get_button_pressed(joy1)
            if btn:
                play_music(btn)

        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")
            old_buttons_on = get_buttons_on(joy1)
            
        if event.type == EVENT_MUSIC_STOP:
            print("music stop")
            mixer.music.stop()


    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
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

