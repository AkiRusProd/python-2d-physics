import pygame
import sys
import math
from object import Rectangle

# https://2dengine.com/doc/collisions.html
# https://habr.com/en/articles/336908/
# https://code.tutsplus.com/how-to-create-a-custom-2d-physics-engine-the-basics-and-impulse-resolution--gamedev-6331t

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
    x=square1_pos[0],
    y=square2_pos[1],
    width = square_size,
    height = square_size
)

# r3 = Rectangle(
#     x=square2_pos[0],
#     y=square2_pos[1] + 50,
#     width = square_size,
#     height = square_size
# )

objects = [r1, r2]

# Set up ground properties
ground_height = 20

# Set up physics variables
jump_force = 200
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
r2.mass = 5

# r2.velocity[0] = -5

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

    for obj in objects:
        for obj2 in objects:
            if obj != obj2:
                # print(obj, obj2)
                if check_collision(obj.pos, obj2.pos, obj.width):
                    sx, sy = separate_collision(obj.pos, obj2.pos, square_size)
                    # print("Collision detected", sx, sy, obj.velocity[1], obj2.velocity[1])
                    #   -- find the collision normal
                    d = math.sqrt(sx**2 + sy**2)
                    nx, ny = sx / d, sy / d
                    # relative velocity
                    vx, vy = obj.velocity[0] - (obj2.velocity[0] or 0), obj.velocity[1] - (obj2.velocity[1] or 0)
                    
                    # penetration speed
                    ps = vx*nx + vy*ny
                    if ps <= 0:
                    #     #This check is very important; This ensures that you only resolve collision if the objects are moving towards each othe
                    #     print("Move the squares away from each other")
                    #     print(r1.velocity, r2.velocity)
                    #     # separate the two objects
                        obj.pos[0] += sx
                        obj.pos[1] += sy

                        obj2.pos[0] -= sx
                        obj2.pos[1] -= sy
                    else:
                        continue

                    px, py = nx*ps, ny*ps
                    # ts = vx*ny - vy*nx 
                    # tx, ty = ny*ts, -nx*ts
                    tx, ty = vx - px, vy - py
                    r = 1 + max(obj.bounce, obj2.bounce)
                    f = 1 + max(obj.friction, obj2.friction)

                    # obj.velocity[0] -= (px * r + tx * f)
                    # obj.velocity[1] -= (py * r + ty * f)
                    # obj2.velocity[0] += (px * r - tx * f)
                    # obj2.velocity[1] += (py * r - ty * f)
                    
                
                    # j = (1 + r) * ps
                    # j /= 1 / obj.mass + 1 / obj2.mass
                    # p = [j * nx, j * ny]

                    px /= 1 / obj.mass + 1 / obj2.mass
                    py /= 1 / obj.mass + 1 / obj2.mass
                    obj.velocity[0] -= (px * (1 + r) + tx * f) / obj.mass
                    obj.velocity[1] -= (py * (1 + r) + ty * f) / obj.mass
                    obj2.velocity[0] += (px * (1 + r) - tx * f) / obj2.mass
                    obj2.velocity[1] += (py * (1 + r) - ty * f) / obj2.mass

                   
                    
                    # obj.velocity[0] -= (px * (1 + r) + tx * f) * obj.mass / (obj.mass + obj2.mass)
                    # obj.velocity[1] -= (py * (1 + r) + ty * f) * obj2.mass / (obj.mass + obj2.mass)
                    # obj2.velocity[0] += (px * (1 + r) - tx * f) * obj2.mass / (obj.mass + obj2.mass)
                    # obj2.velocity[1] += (py * (1 + r) - ty * f) * obj2.mass / (obj.mass + obj2.mass)

        
        
   



    # Draw background
    screen.fill(white)

    # Draw ground
    pygame.draw.rect(screen, blue, (0, height - ground_height, width, ground_height))

    # Draw squares
    pygame.draw.rect(screen, red, (r1.pos[0], r1.pos[1], square_size, square_size))
    pygame.draw.rect(screen, green, (r2.pos[0], r2.pos[1], square_size, square_size))
    # pygame.draw.rect(screen, green, (r3.pos[0], r3.pos[1], square_size, square_size))

    # Update display
    pygame.display.flip()

    # Control frame rate
    pygame.time.Clock().tick(60)
