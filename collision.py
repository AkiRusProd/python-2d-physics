import math
from vector import Vector2D
from body import Body, Rectangle, Circle


def aabb_collision(body_1: Rectangle, body_2: Rectangle):
    if hasattr(body_1, 'radius') or hasattr(body_2, 'radius'):
        return False
    
    # If position is the bottom left edge of the body
    # return (
    #     body_1.pos[0] < body_2.pos[0] + body_2.width
    #     and body_1.pos[0] + body_1.width > body_2.pos[0]
    #     and body_1.pos[1] < body_2.pos[1] + body_2.height
    #     and body_1.pos[1] + body_1.height > body_2.pos[1]
    # )

    # Another solution:
    d: Vector2D = body_1.pos - body_2.pos
    ad = d.abs()

    sum_half_sizes = Vector2D(body_1.width / 2 + body_2.width /2, body_1.height / 2 + body_2.height / 2)
    
    if ad.x >= sum_half_sizes.x or ad.y >= sum_half_sizes.y:
        # If not collision
        return

    # If collision
    
    separation_vector = sum_half_sizes - ad

    # Ignore longer axis
    if separation_vector.x < separation_vector.y:
        if separation_vector.x > 0:
            separation_vector.y = 0
    else:
        if separation_vector.y > 0:
            separation_vector.x = 0

    # Correct sign
    if d.x < 0:
        separation_vector.x = -separation_vector.x
    if d.y < 0:
        separation_vector.y = -separation_vector.y


    normal_vector = separation_vector.normalize()
    depth = separation_vector.magnitude()

    # Note: separation vector = normal_vector * depth

    reaction(body_1, body_2, normal_vector, depth)
    




def reaction(body_1: Body, body_2: Body, normal_vector: Vector2D, depth: float):

    separation_vector = normal_vector * depth
    
    # print(sx, sy)
    #   -- find the collision normal
    # relative velocity
    # vx, vy = body_1.velocity[0] - (body_2.velocity[0] or 0), body_1.velocity[1] - (body_2.velocity[1] or 0)
    relative_velocity = body_1.velocity - body_2.velocity
    
    
    # penetration speed
    # ps = vx*nx + vy*ny #relative velocity * normal
    penetration_speed = relative_velocity.dot(normal_vector)
    penetration = normal_vector * penetration_speed
   
    if penetration_speed > 0:
        return
    # This check is very important; This ensures that you only resolve collision if the body_1ects are moving towards each othe
        # sx = max(sx - 0.01, 0) / (1 / body_1.mass + 1 / body_2.mass) * 0.8 * nx * 1/body_1.mass
        # sy = max(sy - 0.01, 0) / (1 / body_1.mass + 1 / body_2.mass) * 0.8 * ny * 1/body_2.mass
    #  separate the two bodies
    if body_1.body_type == "dynamic":
        body_1.pos += separation_vector
        # body_1.pos[0] += separation_vector[0]
        # body_1.pos[1] += separation_vector[1]
    if body_2.body_type == "dynamic":
        body_2.pos -= separation_vector
        # body_2.pos[0] -= separation_vector[0]
        # body_2.pos[1] -= separation_vector[1]
    
    # ts = vx*ny - vy*nx 
    # tx, ty = ny*ts, -nx*ts
    # tx, ty = vx - px, vy - py
    tangent = relative_velocity - penetration
    r = 1 + max(body_1.bounce, body_2.bounce)
    f = min(body_1.friction, body_2.friction)

    # j = (1 + r) * ps
    # j /= 1 / body_1.mass + 1 / body_2.mass
    # p = [j * nx, j * ny]

    penetration /= 1 / body_1.mass + 1 / body_2.mass
    tangent /= 1 / body_1.mass + 1 / body_2.mass

    if body_1.body_type == "dynamic":
        # body_1.velocity[0] -= (px * r + tx * f) / body_1.mass
        # body_1.velocity[1] -= (py * r + ty * f) / body_1.mass
        body_1.velocity -= (penetration * r + tangent * f) / body_1.mass


    if body_2.body_type == "dynamic":
        # body_2.velocity[0] += (px * r + tx * f) / body_2.mass
        # body_2.velocity[1] += (py * r + ty * f) / body_2.mass
        body_2.velocity += (penetration * r + tangent * f) / body_2.mass



    