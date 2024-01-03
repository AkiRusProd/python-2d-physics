import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Moving Squares with Collision and Pushing")

# Set up colors
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Set up square properties
square_size = 50
square1_pos = [width // 4, height // 2 - square_size // 2]
square2_pos = [3 * width // 4 - square_size, height // 2 - square_size // 2]
square_speed = 5

# Initialize movement flags
move_left = False
move_right = False
move_up = False
move_down = False

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left = True
            elif event.key == pygame.K_RIGHT:
                move_right = True
            elif event.key == pygame.K_UP:
                move_up = True
            elif event.key == pygame.K_DOWN:
                move_down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            elif event.key == pygame.K_RIGHT:
                move_right = False
            elif event.key == pygame.K_UP:
                move_up = False
            elif event.key == pygame.K_DOWN:
                move_down = False

    # Update square position based on movement flags
    if move_left:
        square1_pos[0] -= square_speed
    if move_right:
        square1_pos[0] += square_speed
    if move_up:
        square1_pos[1] -= square_speed
    if move_down:
        square1_pos[1] += square_speed

    # Check for collision
    if (
        square1_pos[0] < square2_pos[0] + square_size
        and square1_pos[0] + square_size > square2_pos[0]
        and square1_pos[1] < square2_pos[1] + square_size
        and square1_pos[1] + square_size > square2_pos[1]
    ):
        # Collision handling - push the first square away
        if square1_pos[0] < square2_pos[0]:
            square1_pos[0] -= square_speed
        else:
            square1_pos[0] += square_speed

        if square1_pos[1] < square2_pos[1]:
            square1_pos[1] -= square_speed
        else:
            square1_pos[1] += square_speed

    # Draw background
    screen.fill(white)

    # Draw squares
    pygame.draw.rect(screen, red, (square1_pos[0], square1_pos[1], square_size, square_size))
    pygame.draw.rect(screen, green, (square2_pos[0], square2_pos[1], square_size, square_size))

    # Update display
    pygame.display.flip()

    # Control frame rate
    pygame.time.Clock().tick(60)
