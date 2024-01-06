from vector import Vector2D
from body import Body, Rectangle, Circle


def aabbs_collision(body_1: Rectangle, body_2: Rectangle):    
    assert body_1.shape_type == "Rectangle" and body_2.shape_type == "Rectangle", \
        "Both body_1 and body_2 must be of shape_type 'Rectangle' for polygon collision."
    
    # If position is the bottom left edge of the body
    # return (
    #     body_1.pos[0] < body_2.pos[0] + body_2.width
    #     and body_1.pos[0] + body_1.width > body_2.pos[0]
    #     and body_1.pos[1] < body_2.pos[1] + body_2.height
    #     and body_1.pos[1] + body_1.height > body_2.pos[1]
    # )

    # Another solution:
    d: Vector2D = body_1.pos - body_2.pos
    ad = abs(d)

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


    normal_vector = separation_vector.normalize
    penetration_depth = separation_vector.magnitude

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

    normal_vector = (body_1.pos - body_2.pos).normalize

    penetration_depth  = body_1.radius + body_2.radius - distance

    reaction(body_1, body_2, normal_vector, penetration_depth)

    contact_point = circles_contact_points(body_1, body_2)

    return contact_point
    


def project_circle(center, radius: float, axis: Vector2D):
    direction = axis.normalize
    # direction_and_radius = Vector2D(*[direction[i] * radius for i in range(len(direction))])
    direction_and_radius = direction * radius

    # p1 = [center[i] + direction_and_radius[i] for i in range(len(center))]
    # p2 = [center[i] - direction_and_radius[i] for i in range(len(center))]

    p1 = center + direction_and_radius
    p2 = center - direction_and_radius

    min_proj = p1.dot(axis)
    max_proj = p2.dot(axis)

    if min_proj > max_proj:
        min_proj, max_proj = max_proj, min_proj

    return min_proj, max_proj


def project_vertices(vertices: list[Vector2D], axis: Vector2D):
    min_proj = float('inf')
    max_proj = float('-inf')

    for v in vertices:
        proj = v.dot(axis)

        if proj < min_proj:
            min_proj = proj
        if proj > max_proj:
            max_proj = proj

    return min_proj, max_proj

def find_closest_point_on_polygon(circle_center: Vector2D, vertices: list[Vector2D]):
    result = -1
    min_distance = float('inf')

    for i, v in enumerate(vertices):
        dist = Vector2D.distance(v, circle_center)

        if dist < min_distance:
            min_distance = dist
            result = i

    return result

def polygon_circle_collision(polygon: Rectangle, circle: Circle):
    assert polygon.shape_type == "Rectangle" and circle.shape_type == "Circle", \
        "Shape types of polygon and circle must be 'Rectangle' and 'Circle' respectively."
    
    normal = Vector2D(0, 0)
    penetration_depth = float('inf')
    
    for i in range(len(polygon.vertices)):
        va = polygon.vertices[i]
        vb = polygon.vertices[(i + 1) % len(polygon.vertices)]

        edge = vb - va

        axis = Vector2D(-edge.y, edge.x).normalize
       
        # project circle onto axis
        min_a, max_a = project_vertices(polygon.vertices, axis)
        min_b, max_b = project_circle(circle.pos, circle.radius, axis)
        
        if max_a <= min_b or max_b <= min_a:
            return False
        
        axis_depth = min(max_b - min_a, max_a - min_b)

        if axis_depth < penetration_depth:
            penetration_depth = axis_depth
            normal = axis
    
    
    cp_index = find_closest_point_on_polygon(circle.pos, polygon.vertices)
    
    cp = polygon.vertices[cp_index]
    
    axis = (cp - circle.pos).normalize

    min_a, max_a = project_circle(circle.pos, circle.radius, axis)
    min_b, max_b = project_vertices(polygon.vertices, axis)

    if max_a <= min_b or max_b <= min_a:
        return False
    
    axis_depth = min(max_b - min_a, max_a - min_b)

    if axis_depth < penetration_depth:
        penetration_depth = axis_depth
        normal = axis


    direction = (polygon.pos - circle.pos).normalize
   
    if direction.dot(normal) < 0:
        normal *= -1
        
    reaction(polygon, circle, normal, penetration_depth)

    contact_point = polygon_circle_contact_points(polygon, circle)

    return contact_point

def polygons_collision(polygon_1: Rectangle, polygon_2: Rectangle):
    normal = Vector2D(0, 0)
    depth = float('inf')

    for i in range(len(polygon_1.vertices)):
        va = polygon_1.vertices[i]
        vb = polygon_1.vertices[(i + 1) % len(polygon_1.vertices)]

        edge = vb - va
        axis = Vector2D(-edge.y, edge.x).normalize

        min_a, max_a = project_vertices(polygon_1.vertices, axis)
        min_b, max_b = project_vertices(polygon_2.vertices, axis)

        if min_a >= max_b or min_b >= max_a:
            return

        axis_depth = min(max_b - min_a, max_a - min_b)

        if axis_depth < depth:
            depth = axis_depth
            normal = axis

    for i in range(len(polygon_2.vertices)):
        va = polygon_2.vertices[i]
        vb = polygon_2.vertices[(i + 1) % len(polygon_2.vertices)]

        edge = vb - va
        axis = Vector2D(-edge.y, edge.x).normalize

        min_a, max_a = project_vertices(polygon_1.vertices, axis)
        min_b, max_b = project_vertices(polygon_2.vertices, axis)

        if min_a >= max_b or min_b >= max_a:
            return

        axis_depth = min(max_b - min_a, max_a - min_b)

        if axis_depth < depth:
            depth = axis_depth
            normal = axis

    direction = (polygon_1.pos - polygon_2.pos).normalize

    if direction.dot(normal) < 0:
        normal *= -1

    reaction(polygon_1, polygon_2, normal, depth)

    contact_points = polygons_contact_points(polygon_1, polygon_2)

    return contact_points

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
        body_1.pos += separation_vector / 2
    if body_2.is_static == False:
        body_2.pos -= separation_vector / 2
    
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



    






def circles_contact_points(body_1: Circle, body_2: Circle):
    normal = (body_2.pos - body_1.pos).normalize

    contact_point = body_1.pos + normal * body_1.radius

    return [contact_point]
    

def point_to_line_segment_projection(point: Vector2D, a: Vector2D, b: Vector2D):
    ab = b - a # line segment vector
    ap = point - a #point vector
    
    proj = ap.dot(ab)
    d = proj / ab.dot(ab) # ad.dot(ab) = len(ab) ** 2, but dot more efficient

    if d <= 0:
        contact_point = a
    elif d >= 1:
        contact_point = b
    else: 
        contact_point = a + ab * d

    distance = Vector2D.distance(contact_point, point)

    return contact_point, distance

def polygon_circle_contact_points(polygon: Rectangle, circle: Circle):

    min_distance = float('inf')
    for i in range(len(polygon.vertices)):
        va = polygon.vertices[i]
        vb = polygon.vertices[(i + 1) % len(polygon.vertices)]

        cp, distance = point_to_line_segment_projection(circle.pos, va, vb)

        if distance < min_distance:
            min_distance = distance
            contact_point = cp

        
    return [contact_point]

def polygons_contact_points(polygon_1: Rectangle, polygon_2: Rectangle):
    epsilon = 0.0005
    min_distance = float('inf')
    contact_point_1 = Vector2D(0, 0)
    contact_point_2 = Vector2D(0, 0)

    for i in range(len(polygon_1.vertices)):
        vp = polygon_1.vertices[i]
        for j in range(len(polygon_2.vertices)):
            va = polygon_2.vertices[j]
            vb = polygon_2.vertices[(j + 1) % len(polygon_2.vertices)]

            cp, distance = point_to_line_segment_projection(vp, va, vb)

            if abs(distance - min_distance) < epsilon and not cp.distance_to(contact_point_1) < epsilon:
                # not cp.dot(contact_point_1) < epsilon ** 2 means cp is not contact_point_1
                contact_point_2 = cp
            elif distance < min_distance:
                min_distance = distance
                contact_point_1 = cp

    for i in range(len(polygon_2.vertices)):
        vp = polygon_2.vertices[i]
        for j in range(len(polygon_1.vertices)):
            va = polygon_1.vertices[j]
            vb = polygon_1.vertices[(j + 1) % len(polygon_1.vertices)]

            cp, distance = point_to_line_segment_projection(vp, va, vb)

            if abs(distance - min_distance) < epsilon and not cp.distance_to(contact_point_1) < epsilon:
                contact_point_2 = cp
            elif distance < min_distance:
                min_distance = distance
                contact_point_1 = cp
                

    return [contact_point_1, contact_point_2]
                













# Alternative polygon vs polygon contact points detection method

def clip(v1, v2, n, o):
    cp = []
    d1 = n.dot(v1) - o
    d2 = n.dot(v2) - o
    if d1 >= 0.0:
        cp.append(v1)
    if d2 >= 0.0:
        cp.append(v2)
    if d1 * d2 < 0.0:
        e = v2 - v1
        u = d1 / (d1 - d2)
        e = e * u + v1
        cp.append(e)
    return cp

def find_farthest_vertex(vertices, n):
    max_projection = -float('inf')
    index = -1
    for i, v in enumerate(vertices):
        projection = n.dot(v)
        if projection > max_projection:
            max_projection = projection
            index = i
    return index

def best_edge(vertices, n):
    index = find_farthest_vertex(vertices, n)
    v = vertices[index]
    v1 = vertices[(index + 1) % len(vertices)]
    v0 = vertices[(index - 1) % len(vertices)]
    l = v - v1
    r = v - v0
    l = l.normalize
    r = r.normalize
    if r.dot(n) <= l.dot(n):
        return (v, v0)
    else:
        return (v, v1)

def polygons_clipping_contact_points(polygon_1, polygon_2, n):
    # Contact Points Using Clipping
    # https://dyn4j.org/2011/11/contact-points-using-clipping/
    n *= -1
    e1 = best_edge(polygon_1.vertices, n)
    e2 = best_edge(polygon_2.vertices, n * -1)
    ref = e1 if abs(e1[0].dot(n)) <= abs(e2[0].dot(n)) else e2
    inc = e2 if ref == e1 else e1
    flip = ref != e1

    refv = ref[1] - ref[0]
    refv = refv.normalize
    o1 = refv.dot(ref[0])
    cp = clip(inc[0], inc[1], refv, o1)
    if len(cp) < 2:
        return []

    o2 = refv.dot(ref[1])
    cp = clip(cp[0], cp[1], refv * -1, o2 * -1)
    if len(cp) < 2:
        return []

    refNorm = Vector2D(-refv.y, refv.x)
    if flip:
        refNorm = refNorm * -1
        
    max_projection = max(refNorm.dot(v) for v in [ref[0], ref[1]])
    
    cp = [point for point in cp if refNorm.dot(point) - max_projection < 0.05]

    return cp