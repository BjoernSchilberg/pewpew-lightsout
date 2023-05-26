import pew  # Import the pew library for controlling LED matrix displays
import random  # Import the random library for generating random numbers

pew.init()  # Initialize the pew library

# Create an 8x8 matrix array with all values set to 0
# This represents the LED display, with each cell in the array corresponding to
# a pixel on the display
screen = pew.Pix()

# Decide how many lights you want to randomly turn on
# Generate a random integer between 0 and 63 (inclusive)
num_lights = random.randint(0, 63)

# Turn on random lights
# For each light to be turned on, generate random x and y coordinates (0-7
# inclusive), and set the pixel at those coordinates to 2 (on)
for i in range(num_lights):
    x = random.randint(0, 7)
    y = random.randint(0, 7)
    screen.pixel(x, y, 2)

# Set initial coordinates for a moving light
x = random.randint(0,7) 
y = random.randint(0,7) 

# Variable to control the blinking of the moving light
blink = True

# Game loop
while True:
    # Set the current pixel to 0 (off) if its current brightness is less than 4, or to 2 (on) otherwise
    screen.pixel(x, y, 0 if screen.pixel(x, y) < 4 else 2)

    # Read the current state of the keys
    keys = pew.keys()

    # Initialize the change in x and y coordinates
    dx = 0
    dy = 0

    # If the up key is pressed and the y coordinate is greater than 0, decrease y
    if keys & pew.K_UP and y > 0:
        dy = -1
    # If the down key is pressed and the y coordinate is less than 7, increase y
    elif keys & pew.K_DOWN and y < 7:
        dy = 1
    # If the left key is pressed and the x coordinate is greater than 0, decrease x
    elif keys & pew.K_LEFT and x > 0:
        dx = -1
    # If the right key is pressed and the x coordinate is less than 7, increase x
    elif keys & pew.K_RIGHT and x < 7:
        dx = 1

    # Get the brightness of the target pixel (the pixel the moving light will
    # move to in the next frame)
    target = screen.pixel(x + dx, y + dy)

    # If the X key is pressed and the target pixel is off or on (but not
    # blinking or bright), turn off or on the pixels in the cross pattern
    # centered at the current pixel
    if target in {0, 2} and (keys & pew.K_X):
        screen.pixel(x, y, 0 if screen.pixel(x, y) in {2} else 2)
        screen.pixel(x + 1, y, 0 if screen.pixel(x + 1, y) in {2} else 2)
        screen.pixel(x - 1, y, 0 if screen.pixel(x - 1, y) in {2} else 2)
        screen.pixel(x, y + 1, 0 if screen.pixel(x, y + 1) in {2} else 2)
        screen.pixel(x, y - 1, 0 if screen.pixel(x, y - 1) in {2} else 2)

    # Update the x and y coordinates
    x += dx
    y += dy

    # Count the number of pixels currently on (not blinking or bright)
    count = 0
    for b in range(8):
        for a in range(8):
            if screen.pixel(a, b) == 2:
                count += 1
    # If there are no pixels on, exit the game loop
    if count == 0:
        break

    # Set the current pixel to blink (if the blink variable is True) or to be on
    # (if the blink variable is False), and to be bright (4) if it is currently
    # on or blinking
    screen.pixel(x, y, (3 if blink else 2) + (4 if screen.pixel(x, y) in {2, 7} else 0))

    # Toggle the blink variable
    blink = not blink

    # Update the display
    pew.show(screen)

    # Wait for 1/6 of a second before the next frame
    pew.tick(1 / 6)
