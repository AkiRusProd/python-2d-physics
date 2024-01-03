import pygame
import sys
import math
from object import Rectangle

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
speed = 50

r1 = Rectangle(
    x=square1_pos[0],
    y=square1_pos[1],
    width = square_size,
    height = square_size
)

r2 = Rectangle(
    x=square2_pos[0],
    y=square2_pos[1],
    width = square_size,
    height = square_size
)


objects = [r1, r2]

# Set up ground properties
ground_height = 20

# Set up physics variables
jump_force = 100
gravity = 9.8
r1.velocity[1] = 0  # Initial vertical velocity for square 1
r2.velocity[1] = 0  # Initial vertical velocity for square 2

r1.velocity[0] = 5  # Initial horizontal velocity for square 1

# Initialize movement flags
move_left = False
move_right = False
move_up = False
move_down = False

r1.mass = 10

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
    

def simulate_gravity(object):
    object.velocity[1] += gravity * object.mass * dt

def simulate_movement(object):
    object.velocity[0] *= object.friction

def update_position(object, dt):
   object.pos[0] += object.velocity[0] * dt
   object.pos[1] += object.velocity[1] * dt

def check_screen_collision(obj):
    obj.pos[0] = max(0, min(obj.pos[0], width - obj.width))
    obj.pos[1] = max(0, min(obj.pos[1], height - ground_height - obj.height))

def check_ground_collision(obj):
    if obj.pos[1] + obj.height >= height - ground_height:
        obj.pos[1] = height - ground_height - obj.height # Set the square just above the ground
        obj.velocity[1] = 0  # Stop the square when it hits the ground
        simulate_movement(obj)

dt = 1/60 # assuming 60 frames per second
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
        # r1.pos[0] -= r1.velocity[0]
        r1.velocity[0] -= speed if r1.velocity[1] == 0 else 0
    if move_right:
        # r1.pos[0] += r1.velocity[0]
        r1.velocity[0] += speed if r1.velocity[1] == 0 else 0
    if move_up:
        # r1.pos[1] -= r1.velocity[0] * jump_force
        r1.velocity[1] = -jump_force if r1.velocity[1] == 0 else r1.velocity[1]
        # r1.velocity[1] = -jump_force
        # r1.velocity[1] -= jump_force
    if move_down:
        # r1.pos[1] += r1.velocity[0]
        r1.velocity[1] = jump_force
    print(r1.velocity)

    # Update square position based on vertical velocity
    # r1.pos[1] += r1.velocity[1]
    # r2.pos[1] += r2.velocity[1]
    for obj in objects:
        update_position(obj, dt)

    # Apply gravity to both squares
    for obj in objects:
        simulate_gravity(obj)


    # update_position(r1, dt)
 

    # Check for collision with ground
    for obj in objects:
        check_ground_collision(obj)

    # Check for collision with screen boundaries
    for obj in objects:
        check_screen_collision(obj)

    if check_collision(r1.pos, r2.pos, square_size):
        sx, sy = separate_collision(r1.pos, r2.pos, square_size)
        print("Collision detected", sx, sy, r1.velocity[1], r2.velocity[1])
        #   -- find the collision normal
        d = math.sqrt(sx**2 + sy**2)
        nx, ny = sx / d, sy / d
        # relative velocity
        vx, vy = r1.velocity[0] - (r2.velocity[0] or 0), r1.velocity[1] - (r2.velocity[1] or 0)
        # penetration speed
        ps = vx*nx + vy*ny
        # if ps <= 0:
        #     #This check is very important; This ensures that you only resolve collision if the objects are moving towards each othe
        #     print("Move the squares away from each other")
        #     print(r1.velocity, r2.velocity)
        #     # separate the two objects
        r1.pos[0] += sx
        r1.pos[1] += sy
    

        # Collision handling - exchange vertical velocities
        r1.velocity[1], r2.velocity[1] = r2.velocity[1], r1.velocity[1]
        
        
   



    # Draw background
    screen.fill(white)

    # Draw ground
    pygame.draw.rect(screen, blue, (0, height - ground_height, width, ground_height))

    # Draw squares
    pygame.draw.rect(screen, red, (r1.pos[0], r1.pos[1], square_size, square_size))
    pygame.draw.rect(screen, green, (r2.pos[0], r2.pos[1], square_size, square_size))

    # Update display
    pygame.display.flip()

    # Control frame rate
    pygame.time.Clock().tick(60)
