from .vector import Vector2D
from .body import Body, Polygon, Rectangle, Circle
    
def collide(body_1: Body, body_2: Body, include_rotation = True):
    if body_1.shape_type == "Polygon" and body_2.shape_type == "Polygon":
        normal, depth = polygons_collision(body_1, body_2) #if include_rotation else aabbs_collision(body_1, body_2)
    elif body_1.shape_type == "Circle" and body_2.shape_type == "Circle":
        normal, depth = circles_collision(body_1, body_2)
    elif body_1.shape_type == "Polygon" and body_2.shape_type == "Circle":
        normal, depth = polygon_circle_collision(body_1, body_2)
    elif body_1.shape_type == "Circle" and body_2.shape_type == "Polygon":
        normal, depth = polygon_circle_collision(body_2, body_1)

    if normal is None or depth is None:
        return
    
    if body_1.shape_type == "Polygon" and body_2.shape_type == "Polygon":
        contact_points = polygons_contact_points(body_1, body_2)
    elif body_1.shape_type == "Circle" and body_2.shape_type == "Circle":
        contact_points = circles_contact_points(body_1, body_2)
    elif body_1.shape_type == "Polygon" and body_2.shape_type == "Circle":
        contact_points = polygon_circle_contact_points(body_1, body_2)
    elif body_1.shape_type == "Circle" and body_2.shape_type == "Polygon":
        contact_points = polygon_circle_contact_points(body_2, body_1)
        normal = -normal # Temporal solution
    
    if include_rotation:
        resolution_with_rotation(body_1, body_2, normal, depth, contact_points)
    else:
        resolution(body_1, body_2, normal, depth)

    return contact_points



def aabbs_collision(body_1: Rectangle, body_2: Rectangle):    
    """DEPRECATED: Use polygons_collision instead"""
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
        return None, None

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
    # contact_point = polygons_contact_points(body_1, body_2)
    # resolution(body_1, body_2, normal_vector, penetration_depth)

    return normal_vector, penetration_depth


def circles_collision(body_1: Circle, body_2: Circle):
    assert body_1.shape_type == "Circle" and body_2.shape_type == "Circle", \
        "Both body_1 and body_2 must be of shape_type 'Circle' for Circle collision."
    
    distance = Vector2D.distance(body_1.pos, body_2.pos)

    if distance >= body_1.radius + body_2.radius:
        # If not collision
        return None, None
    
    # If collision

    normal_vector = (body_1.pos - body_2.pos).normalize()

    penetration_depth  = body_1.radius + body_2.radius - distance

    # resolution(body_1, body_2, normal_vector, penetration_depth)

    # contact_point = circles_contact_points(body_1, body_2)
    # resolution_with_rotation(body_1, body_2, normal_vector, penetration_depth, contact_point)

    return normal_vector, penetration_depth
    


def project_circle(center, radius: float, axis: Vector2D):
    direction = axis.normalize()
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

def polygon_circle_collision(polygon: Polygon, circle: Circle):
    assert polygon.shape_type == "Polygon" and circle.shape_type == "Circle", \
        "Shape types of polygon and circle must be 'Polygon' and 'Circle' respectively."
    
    normal = Vector2D(0, 0)
    penetration_depth = float('inf')
    
    for i in range(len(polygon.vertices)):
        va = polygon.vertices[i]
        vb = polygon.vertices[(i + 1) % len(polygon.vertices)]

        edge = vb - va

        axis = Vector2D(-edge.y, edge.x).normalize()
       
        # project circle onto axis
        min_a, max_a = project_vertices(polygon.vertices, axis)
        min_b, max_b = project_circle(circle.pos, circle.radius, axis)
        
        if max_a <= min_b or max_b <= min_a:
            return None, None
        
        axis_depth = min(max_b - min_a, max_a - min_b)

        if axis_depth < penetration_depth:
            penetration_depth = axis_depth
            normal = axis
    
    
    cp_index = find_closest_point_on_polygon(circle.pos, polygon.vertices)
    
    cp = polygon.vertices[cp_index]
    
    axis = (cp - circle.pos).normalize()

    min_a, max_a = project_circle(circle.pos, circle.radius, axis)
    min_b, max_b = project_vertices(polygon.vertices, axis)

    if max_a <= min_b or max_b <= min_a:
        return None, None
    
    axis_depth = min(max_b - min_a, max_a - min_b)

    if axis_depth < penetration_depth:
        penetration_depth = axis_depth
        normal = axis


    direction = (polygon.pos - circle.pos).normalize()
   
    if direction.dot(normal) < 0:
        normal *= -1
        
    # resolution(polygon, circle, normal, penetration_depth)

    # contact_point = polygon_circle_contact_points(polygon, circle)
    # resolution_with_rotation(polygon, circle, normal, penetration_depth, contact_point)

    return normal, penetration_depth

def polygons_collision(polygon_1: Polygon, polygon_2: Polygon):
    normal = Vector2D(0, 0)
    depth = float('inf')

    for i in range(len(polygon_1.vertices)):
        va = polygon_1.vertices[i]
        vb = polygon_1.vertices[(i + 1) % len(polygon_1.vertices)]

        edge = vb - va
        axis = Vector2D(-edge.y, edge.x).normalize()

        min_a, max_a = project_vertices(polygon_1.vertices, axis)
        min_b, max_b = project_vertices(polygon_2.vertices, axis)

        if min_a >= max_b or min_b >= max_a:
            return None, None

        axis_depth = min(max_b - min_a, max_a - min_b)

        if axis_depth < depth:
            depth = axis_depth
            normal = axis

    for i in range(len(polygon_2.vertices)):
        va = polygon_2.vertices[i]
        vb = polygon_2.vertices[(i + 1) % len(polygon_2.vertices)]

        edge = vb - va
        axis = Vector2D(-edge.y, edge.x).normalize()

        min_a, max_a = project_vertices(polygon_1.vertices, axis)
        min_b, max_b = project_vertices(polygon_2.vertices, axis)

        if min_a >= max_b or min_b >= max_a:
            return None, None

        axis_depth = min(max_b - min_a, max_a - min_b)

        if axis_depth < depth:
            depth = axis_depth
            normal = axis

    direction = (polygon_1.pos - polygon_2.pos).normalize()

    if direction.dot(normal) < 0:
        normal *= -1

    # resolution(polygon_1, polygon_2, normal, depth)

    # contact_points = polygons_contact_points(polygon_1, polygon_2)
    # resolution_with_rotation(polygon_1, polygon_2, normal, depth, contact_points)

    return normal, depth


def separate_bodies(body_1: Body, body_2: Body, normal, penetration_depth):
    # Method 1
    # separation_vector = normal * penetration_depth

    # if body_1.is_static:
    #     body_2.pos += separation_vector
    # elif body_2.is_static:
    #     body_1.pos -= separation_vector
    # else:
    #     body_1.pos -= separation_vector / 2
    #     body_2.pos += separation_vector / 2

    # Method 2
    percent = 0.8
    slope = 0.01

    inv_mass1 = 1 / body_1.mass
    inv_mass2 = 1 / body_2.mass
    inv_mass_sum = inv_mass1 + inv_mass2

    if inv_mass_sum == 0: return

    separation_vector = max(penetration_depth - slope, 0) / inv_mass_sum * percent * normal

    if not body_1.is_static:
        body_1.pos -= separation_vector * inv_mass1
    if not body_2.is_static:
        body_2.pos += separation_vector * inv_mass2


def resolution(body_1: Body, body_2: Body, normal_vector: Vector2D, penetration_depth: float):
    normal_vector *= -1

    separate_bodies(body_1, body_2, normal_vector, penetration_depth)
    
    relative_velocity = body_2.velocity - body_1.velocity
    
    penetration_velocity = relative_velocity.dot(normal_vector)

    if penetration_velocity > 0:
        return
    
    r = max(body_1.bounce, body_2.bounce) #MIN?
    j = -(1 + r) * penetration_velocity
    j /= 1 / body_1.mass + 1 / body_2.mass

    impulse =  normal_vector * j

    if body_1.is_static == False:
        body_1.velocity -= impulse / body_1.mass
    if body_2.is_static == False:
        body_2.velocity += impulse / body_2.mass

    # Coulomb friction model
    tangent = relative_velocity - normal_vector * relative_velocity.dot(normal_vector)
    if tangent == Vector2D(0, 0):
        return
    else:
        tangent = tangent.normalize()

    jt = -1 * relative_velocity.dot(tangent)
    jt /= 1 / body_1.mass + 1 / body_2.mass

    static_friction = (body_1.static_friction + body_2.static_friction) / 2

    if abs(jt) <= j * static_friction:
        # friction_impulse = jt * tangent
        friction_impulse = tangent * jt
    else:
        dynamic_friction = (body_1.dynamic_friction + body_2.dynamic_friction) / 2
        # friction_impulse = -j * tangent * dynamic_friction
        friction_impulse = tangent * (-1) * j * dynamic_friction

    if body_1.is_static == False:
        body_1.velocity -= friction_impulse / body_1.mass
    if body_2.is_static == False:
        body_2.velocity += friction_impulse / body_2.mass
    



def resolution_with_rotation(body_1: Body, body_2: Body, normal_vector: Vector2D, penetration_depth: float, contact_point: list[Vector2D]):
    normal_vector *= -1

    separate_bodies(body_1, body_2, normal_vector, penetration_depth)
    
    relative_velocity = body_2.velocity - body_1.velocity

    # Calculate restitution (bounciness)
    r = max(body_1.bounce, body_2.bounce)

    if len(contact_point) == 2: 
        contact_point = (contact_point[0] + contact_point[1]) / 2
    else:
        contact_point = contact_point[0]

    # Calculate impulses for each contact point
    
    r_1 = contact_point - body_1.pos
    r_2 = contact_point - body_2.pos

    r_1_perp = Vector2D(-r_1.y, r_1.x)
    r_2_perp = Vector2D(-r_2.y, r_2.x)

    relative_velocity = (body_2.velocity + r_2_perp * body_2.angular_velocity) - (body_1.velocity + r_1_perp * body_1.angular_velocity)
    penetration_velocity = relative_velocity.dot(normal_vector)

    if penetration_velocity > 0:
        return

    j = -(1 + r) * penetration_velocity
    j /=  1 / body_1.mass + 1 / body_2.mass + (r_1_perp.dot(normal_vector) ** 2)  / body_1.inertia + (r_2_perp.dot(normal_vector) ** 2) / body_2.inertia

    impulse = normal_vector * j

    body_1.velocity -= impulse / body_1.mass 
    body_1.angular_velocity -= r_1.cross(impulse) / body_1.inertia
    body_2.velocity += impulse / body_2.mass 
    body_2.angular_velocity += r_2.cross(impulse) / body_2.inertia


    relative_velocity = (body_2.velocity + r_2_perp * body_2.angular_velocity) - (body_1.velocity + r_1_perp * body_1.angular_velocity)
    tangent = relative_velocity - normal_vector * relative_velocity.dot(normal_vector)
    if tangent == Vector2D(0, 0):
        return
    else:
        tangent = tangent.normalize()

    jt = -1 * relative_velocity.dot(tangent)
    jt /=  1 / body_1.mass + 1 / body_2.mass + (r_1_perp.dot(tangent) ** 2)  / body_1.inertia + (r_2_perp.dot(tangent) ** 2) / body_2.inertia

    static_friction = (body_1.static_friction + body_2.static_friction) / 2

    if abs(jt) <= j * static_friction:
        friction_impulse = jt * tangent
    else:
        dynamic_friction = (body_1.dynamic_friction + body_2.dynamic_friction) / 2
        friction_impulse = -j * tangent * dynamic_friction
 
    body_1.velocity -= friction_impulse / body_1.mass 
    body_1.angular_velocity -= r_1.cross(friction_impulse) / body_1.inertia
    body_2.velocity += friction_impulse / body_2.mass 
    body_2.angular_velocity += r_2.cross(friction_impulse) / body_2.inertia




def circles_contact_points(body_1: Circle, body_2: Circle):
    normal = (body_2.pos - body_1.pos).normalize()

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

def polygon_circle_contact_points(polygon: Polygon, circle: Circle):

    min_distance = float('inf')
    for i in range(len(polygon.vertices)):
        va = polygon.vertices[i]
        vb = polygon.vertices[(i + 1) % len(polygon.vertices)]

        cp, distance = point_to_line_segment_projection(circle.pos, va, vb)

        if distance < min_distance:
            min_distance = distance
            contact_point = cp

        
    return [contact_point]

def polygons_contact_points(polygon_1: Polygon, polygon_2: Polygon):
    epsilon = 0.0005
    min_distance = float('inf')
    contact_point_1 = None
    contact_point_2 = None

    for i in range(len(polygon_1.vertices)):
        vp = polygon_1.vertices[i]
        for j in range(len(polygon_2.vertices)):
            va = polygon_2.vertices[j]
            vb = polygon_2.vertices[(j + 1) % len(polygon_2.vertices)]

            cp, distance = point_to_line_segment_projection(vp, va, vb)

            if contact_point_1 is not None and abs(distance - min_distance) < epsilon and not cp.distance_to(contact_point_1) < epsilon:
                contact_point_2 = cp
            elif distance < min_distance:
                min_distance = distance
                contact_point_2 = None
                contact_point_1 = cp

    for i in range(len(polygon_2.vertices)):
        vp = polygon_2.vertices[i]
        for j in range(len(polygon_1.vertices)):
            va = polygon_1.vertices[j]
            vb = polygon_1.vertices[(j + 1) % len(polygon_1.vertices)]

            cp, distance = point_to_line_segment_projection(vp, va, vb)

            if contact_point_1 is not None and abs(distance - min_distance) < epsilon and not cp.distance_to(contact_point_1) < epsilon:
                contact_point_2 = cp
            elif distance < min_distance:
                min_distance = distance
                contact_point_2 = None
                contact_point_1 = cp

    return [cp for cp in [contact_point_1, contact_point_2] if cp is not None]
                













# Alternative polygon vs polygon contact points detection method BUG

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
    l = l.normalize()
    r = r.normalize()
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
    refv = refv.normalize()
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