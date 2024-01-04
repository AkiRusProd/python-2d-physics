import pygame
import sys
import math
from object import Rectangle, Circle

# https://2dengine.com/doc/collisions.html
# https://habr.com/en/articles/336908/
# https://code.tutsplus.com/how-to-create-a-custom-2d-physics-engine-the-basics-and-impulse-resolution--gamedev-6331t
# https://habr.com/en/articles/509568/

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
speed = 40

r1 = Rectangle(
    x=0,
    y=0,
    width = square_size,
    height = square_size
)

r2 = Rectangle(
    x=square1_pos[0],
    y=square2_pos[1],
    width = square_size * 2,
    height = square_size * 2
)

# c1 = Circle(
#     x=square1_pos[0],
#     y=square1_pos[1],
#     radius = square_size
# )



# r3 = Rectangle(
#     x=square2_pos[0],
#     y=square2_pos[1] + 50,
#     width = square_size,
#     height = square_size
# )



# Set up ground properties
ground_height = 20

ground = Rectangle(
    x = 0,
    y = height - ground_height,
    width = width,
    height = ground_height
)
ground.type = "static"
ground.friction = 0.9
ground.mass = float("inf")
ground.bounce = 0


objects = [r1, r2, ground]
# Set up physics variables
jump_force = 230
gravity = 9.8
r1.velocity[1] = 0  # Initial vertical velocity for square 1
r2.velocity[1] = 0  # Initial vertical velocity for square 2

r1.velocity[0] = 5  # Initial horizontal velocity for square 1

# Initialize movement flags
move_left = False
move_right = False
move_up = False
move_down = False

r1.mass = 30
r2.mass = 300
r1.type = "dynamic"
r2.type = "dynamic"

# r2.velocity[0] = -5



def aabb_vs_aabb_collision(obj1, obj2):
    if hasattr(obj1, 'radius') or hasattr(obj2, 'radius'):
        return False
    # return (
    #     obj1.pos[0] < obj2.pos[0] + obj2.width
    #     and obj1.pos[0] + obj1.width > obj2.pos[0]
    #     and obj1.pos[1] < obj2.pos[1] + obj2.height
    #     and obj1.pos[1] + obj1.height > obj2.pos[1]
    # )
    # Another solution:
    # -- distance between the rects
    
    obj1_cpos = (obj1.pos[0] + obj1.width / 2, obj1.pos[1] + obj1.height / 2)
    obj2_cpos = (obj2.pos[0] + obj2.width / 2, obj2.pos[1] + obj2.height / 2)

    # dx, dy = obj1.pos[0] - obj2.pos[0], obj1.pos[1] - obj2.pos[1]
    dx, dy = obj1_cpos[0] - obj2_cpos[0], obj1_cpos[1] - obj2_cpos[1]
    adx = abs(dx)
    ady = abs(dy)
    # -- sum of the extents
    shw, shh = obj1.width / 2 + obj2.width /2, obj1.height / 2 + obj2.height / 2
    
    if adx >= shw or ady >= shh:
        # no intersection
        return False
    else:
    # intersection
        # print(f"{shw=}, {shh=}, {adx=}, {ady=}, {adx >= shw}, {ady >= shh}")
        return True


def aabb_vs_circle_collision(obj, obj2):
    if hasattr(obj, 'radius') and not hasattr(obj2, 'radius'):
        circle = obj
        aabb = obj2
    elif hasattr(obj2, 'radius') and not hasattr(obj, 'radius'):
        circle = obj2
        aabb = obj
    else:
        return False
      

    # Unpack AABB coordinates
    aabb_x, aabb_y, aabb_width, aabb_height = *aabb.pos, *aabb.size
    
    # Calculate closest point on AABB to the circle center
    closest_x = max(aabb_x, min(circle[0], aabb_x + aabb_width))
    closest_y = max(aabb_y, min(circle[1], aabb_y + aabb_height))
    
    # Calculate distance between the circle center and the closest point on AABB
    distance_x = circle[0] - closest_x
    distance_y = circle[1] - closest_y
    
    # Check if the distance is less than or equal to the circle's radius
    distance_squared = distance_x**2 + distance_y**2
    return distance_squared <= circle[2]**2
    

def separate_collision(obj1, obj2):
    obj1_cpos = (obj1.pos[0] + obj1.width / 2, obj1.pos[1] + obj1.height / 2)
    obj2_cpos = (obj2.pos[0] + obj2.width / 2, obj2.pos[1] + obj2.height / 2)

    # dx, dy = obj1.pos[0] - obj2.pos[0], obj1.pos[1] - obj2.pos[1]
    dx, dy = obj1_cpos[0] - obj2_cpos[0], obj1_cpos[1] - obj2_cpos[1]
    adx = abs(dx)
    ady = abs(dy)
    #   -- shortest separation
    shw, shh = obj1.width / 2 + obj2.width / 2, obj1.height / 2 + obj2.height / 2
    sx, sy = shw - adx, shh - ady
    #   -- ignore longer axis
    if sx < sy:
        if sx > 0:
            sy = 0
    else:
        if sy > 0:
            sx = 0
    #   -- correct sign
    if dx < 0:
        sx = -sx
    if dy < 0:
        sy = -sy
    return sx, sy
    

def simulate_gravity(object):
    if object.type == "dynamic":
        object.velocity[1] += gravity * object.mass * dt

def update_position(object, dt):
   if object.type == "dynamic":
        object.pos[0] += object.velocity[0] * dt
        object.pos[1] += object.velocity[1] * dt

def check_screen_collision(obj):
    if obj.type == "dynamic":
        obj.pos[0] = max(0, min(obj.pos[0], width - obj.width))
        # obj.pos[1] = max(0, min(obj.pos[1], height - ground_height - obj.height))



fps = 360
dt = 1/fps # assuming frames per second
        
# clock = pygame.time.Clock()



# Main game loop
while True:
    # dt = clock.tick(fps) / 1000
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
        r1.velocity[0] -= speed #if r1.velocity[1] == 0 else 0
    if move_right:
        # r1.pos[0] += r1.velocity[0]
        r1.velocity[0] += speed #if r1.velocity[1] == 0 else 0
    if move_up:
        # r1.pos[1] -= r1.velocity[0] * jump_force
        r1.velocity[1] = -jump_force #if r1.velocity[1] == 0 else r1.velocity[1]
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


    # Check for collision with screen boundaries
    for obj in objects:
        check_screen_collision(obj)

    for obj in objects:
        for obj2 in objects:
            if obj != obj2:
                # print(obj.type, obj2.type)
                if aabb_vs_aabb_collision(obj, obj2):
                    # print("collision")
                    # print(obj.type, obj2.type)
                    sx, sy = separate_collision(obj, obj2)
    
                    # print(sx, sy)
                    #   -- find the collision normal
                    d = math.sqrt(sx**2 + sy**2)
                    nx, ny = sx / d, sy / d
                    # relative velocity
                    vx, vy = obj.velocity[0] - (obj2.velocity[0] or 0), obj.velocity[1] - (obj2.velocity[1] or 0)
                    
                    
                    # penetration speed
                    ps = vx*nx + vy*ny #relative velocity * normal
                    px, py = nx*ps, ny*ps
                    if ps <= 0:
                    #     #This check is very important; This ensures that you only resolve collision if the objects are moving towards each othe
                    #     print("Move the squares away from each other")
                    #     print(r1.velocity, r2.velocity)
                        sx = max(sx - 0.01, 0) / (1 / obj.mass + 1 / obj2.mass) * 0.8 * nx * 1/obj.mass
                        sy = max(sy - 0.01, 0) / (1 / obj.mass + 1 / obj2.mass) * 0.8 * ny * 1/obj2.mass
                    #     # separate the two objects
                        if obj.type == "dynamic":
                            obj.pos[0] += sx
                            obj.pos[1] += sy
                        if obj2.type == "dynamic":
                            obj2.pos[0] -= sx
                            obj2.pos[1] -= sy
                    else:
                        continue

                    
                    # ts = vx*ny - vy*nx 
                    # tx, ty = ny*ts, -nx*ts
                    tx, ty = vx - px, vy - py
                    r = 1 + max(obj.bounce, obj2.bounce)
                    f = min(obj.friction, obj2.friction)

                    # if obj.type == "dynamic":
                    #     obj.velocity[0] -= (px * r + tx * f)
                    #     obj.velocity[1] -= (py * r + ty * f)
                    # if obj2.type == "dynamic":
                    #     obj2.velocity[0] += (px * r - tx * f)
                    #     obj2.velocity[1] += (py * r - ty * f)
                    
                
                    # j = (1 + r) * ps
                    # j /= 1 / obj.mass + 1 / obj2.mass
                    # p = [j * nx, j * ny]

                    # print(obj.mass, obj2.mass, obj.type, obj2.type)

                    px /= 1 / obj.mass + 1 / obj2.mass
                    py /= 1 / obj.mass + 1 / obj2.mass

                    tx /= 1 / obj.mass + 1 / obj2.mass
                    ty /= 1 / obj.mass + 1 / obj2.mass

                    if obj.type == "dynamic":
                        obj.velocity[0] -= (px * r + tx * f) / obj.mass
                        obj.velocity[1] -= (py * r + ty * f) / obj.mass
                    if obj2.type == "dynamic":
                        obj2.velocity[0] += (px * r - tx * f) / obj2.mass
                        obj2.velocity[1] += (py * r - ty * f) / obj2.mass

                   
                    
                    # obj.velocity[0] -= (px * (1 + r) + tx * f) * obj.mass / (obj.mass + obj2.mass)
                    # obj.velocity[1] -= (py * (1 + r) + ty * f) * obj2.mass / (obj.mass + obj2.mass)
                    # obj2.velocity[0] += (px * (1 + r) - tx * f) * obj2.mass / (obj.mass + obj2.mass)
                    # obj2.velocity[1] += (py * (1 + r) - ty * f) * obj2.mass / (obj.mass + obj2.mass)

                if aabb_vs_circle_collision(obj, obj2):
                    print("collision!")

        
        
   



    # Draw background
    screen.fill(white)

    # Draw ground
    pygame.draw.rect(screen, blue, (ground.pos[0], ground.pos[1], width, ground_height))
    # print(ground.pos[0], ground.pos[1], width, ground_height)
    # Draw squares
    pygame.draw.rect(screen, red, (r1.pos[0], r1.pos[1], square_size, square_size))
    pygame.draw.rect(screen, green, (r2.pos[0], r2.pos[1], r2.width, r2.height))
    # pygame.draw.circle(screen, blue, (c1.pos[0], c1.pos[1]), square_size) # Here <<<
    # pygame.draw.rect(screen, green, (r3.pos[0], r3.pos[1], square_size, square_size))

    # Update display
    pygame.display.flip()

    # Control frame rate
    pygame.time.Clock().tick(fps)
