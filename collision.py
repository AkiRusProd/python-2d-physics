from vector import Vector2D
from body import Body, Rectangle, Circle


def aabbs_collision(body_1: Rectangle, body_2: Rectangle):    
    assert body_1.shape_type == "Rectangle" and body_2.shape_type == "Rectangle", \
        "Both body_1 and body_2 must be of shape_type 'Rectangle' for AABB collision."
    
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
    penetration_depth = separation_vector.magnitude()

    # Note: separation vector = normal_vector * penetration_depth

    reaction(body_1, body_2, normal_vector, penetration_depth)



def circles_collision(body_1: Circle, body_2: Circle):
    assert body_1.shape_type == "Circle" and body_2.shape_type == "Circle", \
        "Both body_1 and body_2 must be of shape_type 'Circle' for Circle collision."
    
    distance = Vector2D.distance(body_1.pos, body_2.pos)

    if distance >= body_1.radius + body_2.radius:
        # If not collision
        return
    
    # If collision

    normal_vector = (body_1.pos - body_2.pos).normalize()

    penetration_depth  = body_1.radius + body_2.radius - distance

    reaction(body_1, body_2, normal_vector, penetration_depth)
    



def reaction(body_1: Body, body_2: Body, normal_vector: Vector2D, penetration_depth: float):

    separation_vector = normal_vector * penetration_depth
    
    #   -- find the collision normal
    # relative velocity
    relative_velocity = body_1.velocity - body_2.velocity
    
    
    # penetration speed
    # ps = vx*nx + vy*ny #relative velocity * normal
    penetration_speed = relative_velocity.dot(normal_vector)
    impulse = normal_vector * penetration_speed
   
    if penetration_speed > 0:
        return
    # This check is very important; This ensures that you only resolve collision if the body_1ects are moving towards each othe
        # sx = max(penetration_depth - 0.01, 0) / (1 / body_1.mass + 1 / body_2.mass) * 0.8 * nx * 1/body_1.mass # penetration_depth instead sx?
        # sy = max(penetration_depth - 0.01, 0) / (1 / body_1.mass + 1 / body_2.mass) * 0.8 * ny * 1/body_2.mass # penetration_depth instead sx?
    #  separate the two bodies
    if body_1.is_static == False:
        body_1.pos += separation_vector
    if body_2.is_static == False:
        body_2.pos -= separation_vector
    
    # ts = vx*ny - vy*nx 
    # tx, ty = ny*ts, -nx*ts
    # tx, ty = vx - px, vy - py
    tangent = relative_velocity - impulse
    r = 1 + max(body_1.bounce, body_2.bounce)
    f = min(body_1.friction, body_2.friction)

    # j = (1 + r) * ps
    # j /= 1 / body_1.mass + 1 / body_2.mass
    # p = [j * nx, j * ny]

    impulse /= 1 / body_1.mass + 1 / body_2.mass
    tangent /= 1 / body_1.mass + 1 / body_2.mass

    if body_1.is_static == False:
        body_1.velocity -= (impulse * r + tangent * f) / body_1.mass


    if body_2.is_static == False:
        body_2.velocity += (impulse * r + tangent * f) / body_2.mass



    