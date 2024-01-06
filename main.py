import pygame
import sys
from body import Rectangle, Circle
from collision import aabbs_collision, circles_collision, polygons_collision, polygon_circle_collision


                                                                                                                      
# References:                                                                                                                                                                                                                                 
# https://2dengine.com/doc/collisions.html                                                                              
# https://habr.com/en/articles/336908/                                                                                  
# https://code.tutsplus.com/how-to-create-a-custom-2d-physics-engine-the-basics-and-impulse-resolution--gamedev-6331t   
# https://habr.com/en/articles/509568/                                                                                  
# https://www.jeffreythompson.org/collision-detection/table_of_contents.php                                             
# https://dyn4j.org/2010/01/sat/                                                                                        
# https://dyn4j.org/2011/11/contact-points-using-clipping/
# https://www.codezealot.org/archives/88/#gjk-support



# TODO: 
# Add 2D Rotational Kinematics
# Add SAT for polygons collision instead of AABB [OK]


# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Falling Squares with Collision and Pushing")

# Set up colors
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
orange = (255, 128, 0)

# Set up player properties
PLAYER_SPEED_X = PLAYER_SPEED_Y = 10



r1 = Rectangle(
    x = 0,
    y = 0,
    width = 50,
    height = 50,
    name = "player"
)

r2 = Rectangle(
    x = 250,
    y = 250,
    width = 50 * 2,
    height = 50 * 2,
    # is_static=True
)

c1 = Circle(
    x = 160,
    y = 200,
    radius = 50//2
)


c2 = Circle(
    x = 150 + 100,
    y = 150 - 100,
    radius = 50
)


ground = Rectangle(
    x = 0 + WIDTH / 2,
    y = HEIGHT - 20 / 2,
    width = WIDTH,
    height = 20,
    is_static = True,
    friction=0.9,
    mass=float("inf"),
    bounce=0
)


BODIES = [r1, r2, ground, c1, c2]

# Set up physics variables
GRAVITY = 9.8

r1.mass = 300
r2.mass = 300
c1.mass = 30
c2.mass = 120 #float("inf")





# Initialize movement flags
move_left = False
move_right = False
move_up = False
move_down = False

def simulate_gravity(body):
    if body.is_static == False:
        body.velocity[1] += GRAVITY * body.mass * dt

def update_position(body, dt):
   if body.is_static == False:
        body.pos += body.velocity * dt

def check_screen_collision(body):
    if body.is_static == False:
        if body.shape_type == "Rectangle":
            body.pos[0] = max(0 + body.width / 2, min(body.pos[0], WIDTH - body.width / 2))
        elif body.shape_type == "Circle":
            body.pos[0] = max(0 + body.radius, min(body.pos[0], WIDTH - body.radius))
       



FPS = 360
dt = 1/FPS # assuming frames per second
        
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

    # Update player position based on movement flags
    if move_left:
        r1.velocity[0] -= PLAYER_SPEED_X
    if move_right:
        r1.velocity[0] += PLAYER_SPEED_X
    if move_up:
        r1.velocity[1] -= PLAYER_SPEED_Y
    if move_down:
        r1.velocity[1] += PLAYER_SPEED_Y

    for body in BODIES:
        update_position(body, dt)

    # Apply gravity to all objects
    for body in BODIES:
        simulate_gravity(body)

    # Check for collision with screen boundaries
    for body in BODIES:
        check_screen_collision(body)

    # Draw background
    screen.fill(white)

    for body in BODIES:
        if body.name == "player":
            color = red
        elif body.is_static:
            color = orange
        else:
            color = black
        
        if body.shape_type == "Rectangle":
            pygame.draw.rect(screen, color, (body.pos[0] - body.width / 2, body.pos[1] - body.height / 2, body.width, body.height))
        elif body.shape_type == "Circle":
            pygame.draw.circle(screen, color, (body.pos[0], body.pos[1]), body.radius)

    for i in range(len(BODIES) - 1):
        for j in range(i + 1, len(BODIES)):
            body_1 = BODIES[i]
            body_2 = BODIES[j]

            if body_1 != body_2:
                if body_1.shape_type == "Rectangle" and body_2.shape_type == "Rectangle":
                    # polygons_collision(body_1, body_2)
                    # DEBUG
                    cps = polygons_collision(body_1, body_2)
                    if cps:
                        for cp in cps: 
                            pygame.draw.circle(screen, green, (cp.x, cp.y), 5)

                elif body_1.shape_type == "Circle" and body_2.shape_type == "Circle":
                    # circles_collision(body_1, body_2)
                    # DEBUG
                    cp = circles_collision(body_1, body_2)
                    if cp:
                        cp = cp[0]
                        pygame.draw.circle(screen, green, (cp.x, cp.y), 5)

                elif body_1.shape_type == "Rectangle" and body_2.shape_type == "Circle":
                    # polygon_circle_collision(body_1, body_2)
                    # DEBUG
                    cp = polygon_circle_collision(body_1, body_2)
                    if cp:
                        cp = cp[0]
                        pygame.draw.circle(screen, green, (cp.x, cp.y), 5)

    # Update display
    pygame.display.flip()

    # Control frame rate
    pygame.time.Clock().tick(FPS)
