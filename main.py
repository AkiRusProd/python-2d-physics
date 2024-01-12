import pygame
import sys
from body import Rectangle, Circle, Polygon
from space import Space


                                                                                                                      
# References:                                                                                                                                                                                                                                 
# https://2dengine.com/doc/collisions.html                                                                              
# https://habr.com/en/articles/336908/                                                                                  
# https://code.tutsplus.com/how-to-create-a-custom-2d-physics-engine-the-basics-and-impulse-resolution--gamedev-6331t   
# https://habr.com/en/articles/509568/                                                                                  
# https://www.jeffreythompson.org/collision-detection/table_of_contents.php                                             
# https://dyn4j.org/2010/01/sat/                                                                                        
# https://dyn4j.org/2011/11/contact-points-using-clipping/
# https://www.codezealot.org/archives/88/#gjk-support
# https://en.wikipedia.org/wiki/Collision_response#Impulse-based_friction_model
# https://code.tutsplus.com/how-to-create-a-custom-2d-physics-engine-friction-scene-and-jump-table--gamedev-7756t
# https://research.ncl.ac.uk/game/mastersdegree/gametechnologies/physicstutorials/5collisionresponse/Physics%20-%20Collision%20Response.pdf
# https://chrishecker.com/images/e/e7/Gdmphys3.pdf
# https://perso.liris.cnrs.fr/nicolas.pronost/UUCourses/GamePhysics/lectures/lecture%207%20Collision%20Resolution.pdf
# https://code.tutsplus.com/how-to-create-a-custom-2d-physics-engine-oriented-rigid-bodies--gamedev-8032t
# https://stackoverflow.com/questions/31106438/calculate-moment-of-inertia-given-an-arbitrary-convex-2d-polygon


# TODO: 
# Add 2D Rotational Kinematics [OK]
# Add friction to rotational bodies [OK]
# Add SAT for polygons collision instead of AABB [OK]
# Refactor the code
# FIX polygons_clipping_contact_points BUG


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
cyan = (0, 255, 255)



r1 = Rectangle(
    x = 450,
    y = 250,
    width = 25,
    height = 25,
    name = "player",
    mass = 50,
)

r2 = Rectangle(
    x = 200,
    y = 250,
    width = 50,
    height = 50,
    mass=100,
    name="r2",
    # is_static=True
)

c1 = Circle(
    x = 400,
    y = 200,
    radius = 10,
    mass = 30,
    name="circle1"
)


c2 = Circle(
    x =  WIDTH / 2 + 200,
    y =300,
    radius = 25,
    mass = 120,
    is_static=False
)


p = Polygon(
    x = 310,
    y = 250,
    vertices = [(0, 0), (50, 0), (50, 25), (0, 50)],
    mass = 100,
)

p.rotate(90, in_radians=False)

ground = Rectangle(
    x = WIDTH / 2,
    y = 100,
    width = WIDTH / 1.5,
    height = 20,
    is_static = True,
    dynamic_friction=0.5,
    static_friction=0.7,
    mass=float("inf"),
    bounce=0.7,
    name = "ground"
)

platform = Rectangle(
    x = WIDTH / 2 + 200,
    y = 300,
    width = 200,
    height = 20,
    is_static = True,
    mass=float("inf"),
    bounce=0.8,
    static_friction=1,
    name = "platform"
)

platform.rotate(30, in_radians=False)

platform2 = Rectangle(
    x = 70,
    y = 200,
    height = 20,
    width=200,
    is_static = True,
    mass=float("inf"),
    bounce=0.8,
    static_friction=1,
    name = "platform2"
)
platform2.rotate(-60, in_radians=False)

PLAYER_SPEED_X = PLAYER_SPEED_Y = 10
BODIES = [r1, r2, ground, c1, c2, platform, platform2, p]
GRAVITY = 9.8


space = Space(BODIES, GRAVITY)



# Initialize movement flags
move_left = False
move_right = False
move_up = False
move_down = False


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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            new_rect = Rectangle(
                x=mouse_x,
                y=HEIGHT - mouse_y,
                width=20,
                height=20,
                mass=50,
                
            )
            space.add(new_rect)

    # Update player position based on movement flags
    if move_left:
        r1.velocity[0] -= PLAYER_SPEED_X
    if move_right:
        r1.velocity[0] += PLAYER_SPEED_X
    if move_up:
        r1.velocity[1] += PLAYER_SPEED_Y
    if move_down:
        r1.velocity[1] -= PLAYER_SPEED_Y

    space.step(dt)

    screen.fill(white)

    for body in BODIES:
        if body.name == "player":
            color = red
        elif body.is_static:
            color = orange
        else:
            color = black
        
        if body.shape_type == "Polygon":
            pygame.draw.polygon(screen, color, [(vertex.x, HEIGHT -  vertex.y) for vertex in body.vertices])

        elif body.shape_type == "Circle":
            pygame.draw.circle(screen, color, (body.pos[0], HEIGHT -  body.pos[1]), body.radius)

    for point in space._contact_points:
        pygame.draw.circle(screen, green, (point.x,HEIGHT -  point.y), 4)

    # display_surface = pygame.display.get_surface()
    # display_surface.blit(pygame.transform.flip(display_surface, False, True), dest=(0, 0))
    # Update display
    pygame.display.flip()

    pygame.time.Clock().tick(FPS)
