import pygame
import sys
import math
from body import Rectangle, Circle

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
    x = 0,
    y = height - ground_height,
    width = width,
    height = ground_height
)
ground.body_type = "static"
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
r1.body_type = "dynamic"
r2.body_type = "dynamic"
c1.body_type = "dynamic"
c2.body_type = "dynamic"

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
    direction_and_radius = [direction[i] * radius for i in range(len(direction))]

    p1 = [center[i] + direction_and_radius[i] for i in range(len(center))]
    p2 = [center[i] - direction_and_radius[i] for i in range(len(center))]

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

    
    # if aabb.body_type == "dynamic":
    #     aabb.pos[0] += normal[0] * depth
    #     aabb.pos[1] += normal[1] * depth
    # if circle.body_type == "dynamic":
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
    
    if aabb.body_type == "dynamic":
        aabb.pos[0] += sx / 2
        aabb.pos[1] += sy / 2
        # aabb.update_vertices()
        # aabb.move(sx, sy)
    if circle.body_type == "dynamic":
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

    if aabb.body_type == "dynamic":
        aabb.velocity[0] -= (px * r + tx * f) / aabb.mass
        aabb.velocity[1] -= (py * r + ty * f) / aabb.mass
    if circle.body_type == "dynamic":
        circle.velocity[0] += (px * r + tx * f) / circle.mass
        circle.velocity[1] += (py * r + ty * f) / circle.mass




def circle_vs_circle_collision(obj1, obj2):
    if not hasattr(obj1, 'radius') or not hasattr(obj2, 'radius'): 
        return False

    # obj1_cpos = (obj1.pos[0] + obj1.radius / 2, obj1.pos[1] + obj1.radius / 2)
    # obj2_cpos = (obj2.pos[0] + obj2.radius / 2, obj2.pos[1] + obj2.radius / 2)
    obj1_cpos = (obj1.pos[0], obj1.pos[1])
    obj2_cpos = (obj2.pos[0], obj2.pos[1])

    # c_dist = ((obj1_cpos[0] - obj2_cpos[0])**2 + (obj1_cpos[1] - obj2_cpos[1])**2)**0.5
    c_dist = distance(obj1_cpos, obj2_cpos)

    if c_dist >= obj1.radius + obj2.radius:
        return False
    
    print("collision!")
     

    # nx, ny = obj1_cpos[0] - obj2_cpos[0], obj1_cpos[1] - obj2_cpos[1]
    nx, ny = normalize([obj1_cpos[0] - obj2_cpos[0], obj1_cpos[1] - obj2_cpos[1]])

    s = obj1.radius + obj2.radius - c_dist
    vx, vy = obj1.velocity[0] - (obj2.velocity[0] or 0), obj1.velocity[1] - (obj2.velocity[1] or 0)
                    
                    
    # penetration speed
    ps = vx*nx + vy*ny #relative velocity * normal

    if ps > 0:
        return
    sx = max(s - 0.01, 0) / (1 / obj1.mass + 1 / obj2.mass) * 0.8 * nx * 1/obj1.mass
    sy = max(s - 0.01, 0) / (1 / obj1.mass + 1 / obj2.mass) * 0.8 * ny * 1/obj2.mass

    # if obj1.body_type == "dynamic":
    #     obj1.pos[0] += s * nx / 2
    #     obj1.pos[1] += s * ny / 2
    # if obj2.body_type == "dynamic":
    #     obj2.pos[0] -= s * nx / 2
    #     obj2.pos[1] -= s * ny / 2

    print(obj1.name, obj1.velocity)
    print(obj2.name, obj2.velocity)

    if obj1.body_type == "dynamic":
        obj1.pos[0] += sx
        obj1.pos[1] += sy
    if obj2.body_type == "dynamic":
        obj2.pos[0] -= sx
        obj2.pos[1] -= sy

    px, py = nx*ps, ny*ps
    tx, ty = vx - px, vy - py
    r = 1 + max(obj1.bounce, obj2.bounce)
    f = min(obj1.friction, obj2.friction)

    px /= 1 / obj1.mass + 1 / obj2.mass
    py /= 1 / obj1.mass + 1 / obj2.mass

    tx /= 1 / obj1.mass + 1 / obj2.mass
    ty /= 1 / obj1.mass + 1 / obj2.mass

    if obj1.body_type == "dynamic":
        obj1.velocity[0] -= (px * r + tx * f) / obj1.mass
        obj1.velocity[1] -= (py * r + ty * f) / obj1.mass
    if obj2.body_type == "dynamic":
        obj2.velocity[0] += (px * r + tx * f) / obj2.mass
        obj2.velocity[1] += (py * r + ty * f) / obj2.mass


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
    if object.body_type == "dynamic": #and object.name != "circle1":
        object.velocity[1] += gravity * object.mass * dt

def update_position(object, dt):
   if object.body_type == "dynamic":
        object.pos[0] += object.velocity[0] * dt
        object.pos[1] += object.velocity[1] * dt
       

def check_screen_collision(obj):
    if obj.body_type == "dynamic":
        if hasattr(obj, 'width'):
            obj.pos[0] = max(0, min(obj.pos[0], width - obj.width))
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
                # print(obj.body_type, obj2.body_type)
                if aabb_vs_aabb_collision(obj, obj2):
                    # print("collision")
                    # print(obj.body_type, obj2.body_type)
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
                        # sx = max(sx - 0.01, 0) / (1 / obj.mass + 1 / obj2.mass) * 0.8 * nx * 1/obj.mass
                        # sy = max(sy - 0.01, 0) / (1 / obj.mass + 1 / obj2.mass) * 0.8 * ny * 1/obj2.mass
                    #     # separate the two objects
                        if obj.body_type == "dynamic":
                            obj.pos[0] += sx
                            obj.pos[1] += sy
                        if obj2.body_type == "dynamic":
                            obj2.pos[0] -= sx
                            obj2.pos[1] -= sy
                    else:
                        continue

                    
                    # ts = vx*ny - vy*nx 
                    # tx, ty = ny*ts, -nx*ts
                    tx, ty = vx - px, vy - py
                    r = 1 + max(obj.bounce, obj2.bounce)
                    f = min(obj.friction, obj2.friction)

                    # if obj.body_type == "dynamic":
                    #     obj.velocity[0] -= (px * r + tx * f)
                    #     obj.velocity[1] -= (py * r + ty * f)
                    # if obj2.body_type == "dynamic":
                    #     obj2.velocity[0] += (px * r - tx * f)
                    #     obj2.velocity[1] += (py * r - ty * f)
                    
                
                    # j = (1 + r) * ps
                    # j /= 1 / obj.mass + 1 / obj2.mass
                    # p = [j * nx, j * ny]

                    # print(obj.mass, obj2.mass, obj.body_type, obj2.body_type)

                    px /= 1 / obj.mass + 1 / obj2.mass
                    py /= 1 / obj.mass + 1 / obj2.mass

                    tx /= 1 / obj.mass + 1 / obj2.mass
                    ty /= 1 / obj.mass + 1 / obj2.mass

                    if obj.body_type == "dynamic":
                        obj.velocity[0] -= (px * r + tx * f) / obj.mass
                        obj.velocity[1] -= (py * r + ty * f) / obj.mass
                    if obj2.body_type == "dynamic":
                        obj2.velocity[0] += (px * r + tx * f) / obj2.mass
                        obj2.velocity[1] += (py * r + ty * f) / obj2.mass

                    # if obj.name == "red":
                    #     print("red", px, py, tx, ty, r, f)
                    
                    # obj.velocity[0] -= (px * (1 + r) + tx * f) * obj.mass / (obj.mass + obj2.mass)
                    # obj.velocity[1] -= (py * (1 + r) + ty * f) * obj2.mass / (obj.mass + obj2.mass)
                    # obj2.velocity[0] += (px * (1 + r) - tx * f) * obj2.mass / (obj.mass + obj2.mass)
                    # obj2.velocity[1] += (py * (1 + r) - ty * f) * obj2.mass / (obj.mass + obj2.mass)

                circle_vs_circle_collision(obj, obj2)
                # aabb_vs_circle_collision(obj, obj2)
                if hasattr(obj, 'radius') and not hasattr(obj2, 'radius'):
                    aabb_vs_circle_collision(obj2, obj)
                if not hasattr(obj, 'radius') and hasattr(obj2, 'radius'):
                    aabb_vs_circle_collision(obj, obj2)

        
        
   



    # Draw background
    screen.fill(white)

    # Draw ground
    pygame.draw.rect(screen, blue, (ground.pos[0], ground.pos[1], width, ground_height))
    # print(ground.pos[0], ground.pos[1], width, ground_height)
    # Draw squares
    pygame.draw.rect(screen, red, (r1.pos[0], r1.pos[1], square_size, square_size))
    pygame.draw.rect(screen, green, (r2.pos[0], r2.pos[1], r2.width, r2.height))
    pygame.draw.circle(screen, blue, (c1.pos[0], c1.pos[1]), c1.radius)
    pygame.draw.circle(screen, blue, (c2.pos[0], c2.pos[1]), c2.radius)
    # pygame.draw.rect(screen, green, (r3.pos[0], r3.pos[1], square_size, square_size))

    # Update display
    pygame.display.flip()

    # Control frame rate
    pygame.time.Clock().tick(fps)
