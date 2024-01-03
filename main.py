import pygame
import sys

# https://2dengine.com/doc/collisions.html
# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Falling Squares with Collision and Pushing")

# Set up colors
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Set up square properties
square_size = 50
square1_pos = [width // 4, height // 2 - square_size // 2]
square2_pos = [3 * width // 4 - square_size, height // 2 - square_size // 2]
square_speed = 5

# Set up ground properties
ground_height = 20

# Set up physics variables
jump_force = 2
gravity = 0.5
vertical_velocity1 = 0  # Initial vertical velocity for square 1
vertical_velocity2 = 0  # Initial vertical velocity for square 2

# Initialize movement flags
move_left = False
move_right = False
move_up = False
move_down = False



def check_collision(square1_pos, square2_pos, square_size):
    # return (
    #     square1_pos[0] < square2_pos[0] + square_size
    #     and square1_pos[0] + square_size > square2_pos[0]
    #     and square1_pos[1] < square2_pos[1] + square_size
    #     and square1_pos[1] + square_size > square2_pos[1]
    # )
    # Another solution:
    # -- distance between the rects
    # local dx, dy = a.x - b.x, a.y - b.y
    # local adx = math.abs(dx)
    # local ady = math.abs(dy)
    # -- sum of the extents
    # local shw, shh = a.hw + b.hw, a.hh + b.hh
    # if adx >= shw or ady >= shh then
    #     -- no intersection
    #     return
    # end
    # -- intersection

    dx, dy = square1_pos[0] - square2_pos[0], square1_pos[1] - square2_pos[1]
    adx = abs(dx)
    ady = abs(dy)
    shw, shh = square_size, square_size
    if adx >= shw or ady >= shh:
        # no intersection
        return False
    # intersection
    return True

def separate_collision(square1_pos, square2_pos, square_size):
    #   -- shortest separation
    #   local sx, sy = shw - adx, shh - ady
    #   -- ignore longer axis
    #   if sx < sy then
    #     if sx > 0 then
    #       sy = 0
    #     end
    #   else
    #     if sy > 0 then
    #       sx = 0
    #     end
    #   end
    #   -- correct sign
    #   if dx < 0 then
    #     sx = -sx
    #   end
    #   if dy < 0 then
    #     sy = -sy
    #   end
    #   return sx, sy
    # end
    dx, dy = square1_pos[0] - square2_pos[0], square1_pos[1] - square2_pos[1]
    adx = abs(dx)
    ady = abs(dy)
    shw, shh = square_size, square_size
    sx, sy = shw - adx, shh - ady
    if sx < sy:
        if sx > 0:
            sy = 0
    else:
        if sy > 0:
            sx = 0
    if dx < 0:
        sx = -sx
    if dy < 0:
        sy = -sy
    return sx, sy
    


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
        square1_pos[1] -= square_speed * jump_force
    if move_down:
        square1_pos[1] += square_speed

    # Update square position based on vertical velocity
    square1_pos[1] += vertical_velocity1
    square2_pos[1] += vertical_velocity2

    # Apply gravity to both squares
    vertical_velocity1 += gravity
    vertical_velocity2 += gravity

    # Check for collision with ground
    if square1_pos[1] + square_size >= height - ground_height:
        square1_pos[1] = height - ground_height - square_size  # Set the square just above the ground
        vertical_velocity1 = 0  # Stop the square when it hits the ground

    if square2_pos[1] + square_size >= height - ground_height:
        square2_pos[1] = height - ground_height - square_size  # Set the square just above the ground
        vertical_velocity2 = 0  # Stop the square when it hits the ground

    # Check for collision with screen boundaries
    square1_pos[0] = max(0, min(square1_pos[0], width - square_size))
    square1_pos[1] = max(0, min(square1_pos[1], height - ground_height - square_size))

    square2_pos[0] = max(0, min(square2_pos[0], width - square_size))
    square2_pos[1] = max(0, min(square2_pos[1], height - ground_height - square_size))

    # Check for collision between the two squares 
    # if (
    #     square1_pos[0] < square2_pos[0] + square_size
    #     and square1_pos[0] + square_size > square2_pos[0]
    #     and square1_pos[1] < square2_pos[1] + square_size
    #     and square1_pos[1] + square_size > square2_pos[1]
    # ): #TODO find good solution

    if check_collision(square1_pos, square2_pos, square_size):
        sx, sy = separate_collision(square1_pos, square2_pos, square_size)
        print("Collision detected", sx, sy, vertical_velocity1, vertical_velocity2)
        square1_pos[0] += sx
        square1_pos[1] += sy

        # Collision handling - push the first square away
        # if square1_pos[0] < square2_pos[0]:
        #     square1_pos[0] -= square_speed
        # else:
        #     square1_pos[0] += square_speed

        # if square1_pos[1] < square2_pos[1]:
        #     square1_pos[1] -= square_speed
        # else:
        #     square1_pos[1] += square_speed
        # Collision handling - exchange vertical velocities
        vertical_velocity1, vertical_velocity2 = vertical_velocity2, vertical_velocity1

        # # Push squares away horizontally to prevent overlap

        # if square1_pos[0] < square2_pos[0]:
        #     overlap_x = (square1_pos[0] + square_size) - square2_pos[0]
        #     if overlap_x > 0:
        #         square1_pos[0] -= overlap_x
        #         # square2_pos[0] += overlap_x
        # else:
        #     overlap_x = (square2_pos[0] + square_size) - square1_pos[0]
        #     if overlap_x > 0:
        #         square1_pos[0] += overlap_x
        #         # square2_pos[0] -= overlap_x

        # # Push squares away vertically to prevent overlap
        # if square1_pos[1] < square2_pos[1]:
        #     overlap_y = (square1_pos[1] + square_size) - square2_pos[1]
        #     if overlap_y > 0:
        #         square1_pos[1] += overlap_y
        #         # square2_pos[1] += overlap_y
        # else:
        #     overlap_y = (square2_pos[1] + square_size) - square1_pos[1]
        #     if overlap_y > 0:
        #         square1_pos[1] -= overlap_y
        #         # square2_pos[1] -= overlap_y        



    # Draw background
    screen.fill(white)

    # Draw ground
    pygame.draw.rect(screen, blue, (0, height - ground_height, width, ground_height))

    # Draw squares
    pygame.draw.rect(screen, red, (square1_pos[0], square1_pos[1], square_size, square_size))
    pygame.draw.rect(screen, green, (square2_pos[0], square2_pos[1], square_size, square_size))

    # Update display
    pygame.display.flip()

    # Control frame rate
    pygame.time.Clock().tick(60)
