import pygame
import sys
import math
from body import Rectangle, Circle
from vector import Vector2D
from collision import aabbs_collision, circles_collision

# https://2dengine.com/doc/collisions.html
# https://habr.com/en/articles/336908/
# https://code.tutsplus.com/how-to-create-a-custom-2d-physics-engine-the-basics-and-impulse-resolution--gamedev-6331t
# https://habr.com/en/articles/509568/
# https://www.jeffreythompson.org/collision-detection/table_of_contents.php

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
speed = 20
jump_force = 10


r1 = Rectangle(
    x = 0,
    y = 0,
    width = square_size,
    height = square_size
)

r2 = Rectangle(
    x = 700,
    y = 100,
    width = square_size * 2,
    height = square_size * 2
)

c1 = Circle(
    x=square1_pos[0] + 10,
    y=height - 20,
    radius = square_size//2
)
c1.mass = 50
c1.name = "circle1"

c2 = Circle(
    x=square1_pos[0] + 100,
    y=square1_pos[1] - 100,
    radius = square_size
)
c2.mass = 50
c2.name = "circle2"



# r3 = Rectangle(
#     x=square2_pos[0],
#     y=square2_pos[1] + 50,
#     width = square_size,
#     height = square_size
# )



# Set up ground properties
ground_height = 20

ground = Rectangle(
    x = 0 + width / 2,
    y = height - ground_height / 2,
    width = width,
    height = ground_height
)
ground.is_static = True
ground.friction = 0.9
ground.mass = float("inf")
ground.bounce = 0
ground.name = "ground"

objects = [r1, r2, ground, c1, c2]

# Set up physics variables
gravity = 9.8


# Initialize movement flags
move_left = False
move_right = False
move_up = False
move_down = False

r1.name = "red"
r2.name = "green"
r1.mass = 300
r2.mass = 300
c1.mass = 30
c2.mass = 120 #float("inf")
r1.is_static = False
r2.is_static = False
c1.is_static = False
c2.is_static = False

# r2.velocity[0] = -5



def project_vertices(vertices, axis):
    min_proj = float('inf')
    max_proj = float('-inf')

    for v in vertices:
        proj = dot(v, axis)

        if proj < min_proj:
            min_proj = proj
        if proj > max_proj:
            max_proj = proj

    return min_proj, max_proj


def distance(v1, v2):
    return ((v1[0] - v2[0])**2 + (v1[1] - v2[1])**2)**0.5

def find_closest_point_on_polygon(circle_center, vertices):
    result = -1
    min_distance = float('inf')

    for i, v in enumerate(vertices):
        dist = distance(v, circle_center)

        if dist < min_distance:
            min_distance = dist
            result = i

    return result

def distance(v1, v2):
    return ((v1[0] - v2[0])**2 + (v1[1] - v2[1])**2)**0.5

def project_circle(center, radius, axis):
    direction = normalize(axis)
    direction_and_radius = Vector2D(*[direction[i] * radius for i in range(len(direction))])

    # p1 = [center[i] + direction_and_radius[i] for i in range(len(center))]
    # p2 = [center[i] - direction_and_radius[i] for i in range(len(center))]

    p1 = center + direction_and_radius
    p2 = center - direction_and_radius

    min_proj = dot(p1, axis)
    max_proj = dot(p2, axis)

    if min_proj > max_proj:
        min_proj, max_proj = max_proj, min_proj

    return min_proj, max_proj

def normalize(v):
    norm = math.sqrt(v[0]**2 + v[1]**2)
    return [v[i] / norm for i in range(len(v))]
def dot(v1, v2):
    return v1[0]*v2[0] + v1[1]*v2[1]

def aabb_vs_circle_collision(aabb, circle):
  
    # if hasattr(obj, 'radius') and not hasattr(obj2, 'radius'):
    #     circle = obj
    #     aabb = obj2
    # elif hasattr(obj2, 'radius') and not hasattr(obj, 'radius'):
    #     circle = obj2
    #     aabb = obj
    # else:
    #     return False
    
    # if aabb.name != "red":
    #     return False
    # print(f"{aabb.pos=}")

    # Unpack AABB coordinates
    # aabb_x, aabb_y, aabb_width, aabb_height = *aabb.pos, *aabb.size
    
    # # Calculate closest point on AABB to the circle center
    # closest_x = max(aabb_x, min(circle[0], aabb_x + aabb_width))
    # closest_y = max(aabb_y, min(circle[1], aabb_y + aabb_height))
    
    # # Calculate distance between the circle center and the closest point on AABB
    # distance_x = circle[0] - closest_x
    # distance_y = circle[1] - closest_y
    
    # # Check if the distance is less than or equal to the circle's radius
    # distance_squared = distance_x**2 + distance_y**2
    # return distance_squared <= circle[2]**2
    depth = float('inf')
    
    for i in range(len(aabb.vertices)):
        va = aabb.vertices[i]
        vb = aabb.vertices[(i + 1) % len(aabb.vertices)]

        edge = [vb[0] - va[0], vb[1] - va[1]]

        axis = [-edge[1], edge[0]]
        axis = normalize(axis)

        # project circle onto axis
        min_a, max_a = project_vertices(aabb.vertices, axis)
        min_b, max_b = project_circle(circle.pos, circle.radius, axis)
        # print(min_a, max_a, min_b, max_b)
        if max_a <= min_b or max_b <= min_a:
            
            return False
        
        axis_depth = min(max_b - min_a, max_a - min_b)

        if axis_depth < depth:
            depth = axis_depth
            normal = axis
    
    
    cp_index = find_closest_point_on_polygon(circle.pos, aabb.vertices)
    
    cp = aabb.vertices[cp_index]
    
    axis = [cp[0] - circle.pos[0], cp[1] - circle.pos[1]]
    # print(cp, circle.pos)
    axis = normalize(axis)

    min_a, max_a = project_circle(circle.pos, circle.radius, axis)
    min_b, max_b = project_vertices(aabb.vertices, axis)

    if max_a <= min_b or max_b <= min_a:
        return False
    
    axis_depth = min(max_b - min_a, max_a - min_b)

    if axis_depth < depth:
        depth = axis_depth
        normal = axis

    aabb_center = [aabb.pos[0] + aabb.width / 2, aabb.pos[1] + aabb.height / 2]

    direction = [aabb_center[0] - circle.pos[0], aabb_center[1] - circle.pos[1]]
    direction = normalize(direction)

    if dot(direction, normal) < 0:
        normal = [-normal[0], -normal[1]]

    
    # if aabb.is_static == False:
    #     aabb.pos[0] += normal[0] * depth
    #     aabb.pos[1] += normal[1] * depth
    # if circle.is_static == False:
    #     circle.pos[0] -= normal[0] * depth
    #     circle.pos[1] -= normal[1] * depth
        
    
    sx = normal[0] * depth
    sy = normal[1] * depth
    nx = normal[0]
    ny = normal[1]

    #  #   -- ignore longer axis
    # if sx < sy:
    #     if sx > 0:
    #         sy = 0
    # else:
    #     if sy > 0:
    #         sx = 0

    # aabb_cpos = (aabb.pos[0] + aabb.width / 2, aabb.pos[1] + aabb.height / 2)
    # dx, dy = aabb_cpos[0] - circle.pos[0], aabb_cpos[1] - circle.pos[1]
    # #   -- correct sign
    # if dx < 0:
    #     sx = -sx
    # if dy < 0:
    #     sy = -sy

    # sx = max(sx - 0.01, 0) / (1 / aabb.mass + 1 / circle.mass) * 0.8 * nx * 1/aabb.mass
    # sy = max(sy - 0.01, 0) / (1 / aabb.mass + 1 / circle.mass) * 0.8 * ny * 1/circle.mass
    vx, vy = aabb.velocity[0] - (circle.velocity[0] or 0), aabb.velocity[1] - (circle.velocity[1] or 0) 

    # if circle.name == "circle2" and aabb.name == "red":
    #     print(circle.pos, circle.velocity, f"{depth=} {normal=}")

    ps = vx*nx + vy*ny #relative velocity * normal
    if ps > 0:
        return
    
    if aabb.is_static == False:
        aabb.pos[0] += sx / 2
        aabb.pos[1] += sy / 2
        # aabb.update_vertices()
        # aabb.move(sx, sy)
    if circle.is_static == False:
        circle.pos[0] -= sx / 2
        circle.pos[1] -= sy / 2

    px, py = nx*ps, ny*ps
    tx, ty = vx - px, vy - py
    r = 1 + max(aabb.bounce, circle.bounce)
    f = min(aabb.friction, circle.friction)

    px /= 1 / aabb.mass + 1 / circle.mass
    py /= 1 / aabb.mass + 1 / circle.mass

    tx /= 1 / aabb.mass + 1 / circle.mass
    ty /= 1 / aabb.mass + 1 / circle.mass

    # if aabb.name == "ground":
        # print("ground", px, py, tx, ty, r, f)
    # print( px, py, tx, ty, r, f)

    if aabb.is_static == False:
        aabb.velocity[0] -= (px * r + tx * f) / aabb.mass
        aabb.velocity[1] -= (py * r + ty * f) / aabb.mass
    if circle.is_static == False:
        circle.velocity[0] += (px * r + tx * f) / circle.mass
        circle.velocity[1] += (py * r + ty * f) / circle.mass
    

def simulate_gravity(object):
    if object.is_static == False: #and object.name != "circle1":
        object.velocity[1] += gravity * object.mass * dt

def update_position(object, dt):
   if object.is_static == False:
        object.pos[0] += object.velocity[0] * dt
        object.pos[1] += object.velocity[1] * dt
       

def check_screen_collision(obj):
    if obj.is_static == False:
        if hasattr(obj, 'width'):
            obj.pos[0] = max(0 + obj.width / 2, min(obj.pos[0], width - obj.width / 2))
        elif hasattr(obj, 'radius'):
            obj.pos[0] = max(0 + obj.radius, min(obj.pos[0], width - obj.radius))
        # obj.pos[1] = max(0, min(obj.pos[1], height - ground_height - obj.height))



fps = 360
dt = 1/fps # assuming frames per second
        
# clock = pygame.time.Clock()

epsilon = 0.001 

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
        r1.velocity[0] -= speed
    if move_right:
        r1.velocity[0] += speed
    if move_up:
        r1.velocity[1] -= jump_force
    if move_down:
        r1.velocity[1] += jump_force

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
                if obj.shape_type == "Rectangle" and obj2.shape_type == "Rectangle":
                    aabbs_collision(obj, obj2)
                elif obj.shape_type == "Circle" and obj2.shape_type == "Circle":
                    circles_collision(obj, obj2)
                elif obj.shape_type == "Rectangle" and obj2.shape_type == "Circle":
                    aabb_vs_circle_collision(obj, obj2)
                # if not hasattr(obj, 'radius') and hasattr(obj2, 'radius'):
                #     aabb_vs_circle_collision(obj, obj2)

        
        
   



    # Draw background
    screen.fill(white)

    # Draw ground
    pygame.draw.rect(screen, blue, (ground.pos[0] - ground.width / 2, ground.pos[1] - ground.height / 2, width, ground_height))
    # Draw squares
    pygame.draw.rect(screen, red, (r1.pos[0] - r1.width / 2, r1.pos[1] - r1.height / 2, square_size, square_size))
    pygame.draw.rect(screen, green, (r2.pos[0]- r2.width / 2, r2.pos[1] - r2.height / 2, r2.width, r2.height))
    pygame.draw.circle(screen, blue, (c1.pos[0], c1.pos[1]), c1.radius)
    pygame.draw.circle(screen, blue, (c2.pos[0], c2.pos[1]), c2.radius)

    # Update display
    pygame.display.flip()

    # Control frame rate
    pygame.time.Clock().tick(fps)
