import math
from .vector import Vector2D


class Body():
    def __init__(self, x, y, mass = 1, static_friction = 0.5, dynamic_friction = 0.5,  bounce = 0.5, name = None, is_static = False):
        self.pos = Vector2D(x, y)
        self.mass = mass if not is_static else float("inf")
        self.static_friction = static_friction
        self.dynamic_friction = dynamic_friction
        self.bounce = bounce
        self.angle = 0
        self.is_static = is_static
        self.name = name
        self.shape_type = None
        self.velocity = Vector2D(0, 0)
        self.angular_velocity = 0
        self.inertia = None

    def rotate(self, angle, in_radians=True):
        if not in_radians:
            angle = math.radians(angle)
        self.angle += angle

class Polygon(Body):
    def __init__(self, x, y, vertices: list[Vector2D, list, tuple], mass=1, static_friction=0.5, dynamic_friction=0.5, bounce=0.5, name=None, is_static=False):
        super().__init__(x, y, mass, static_friction, dynamic_friction, bounce, name, is_static)
        centroid = (
            sum(vertex[0] for vertex in vertices) / len(vertices),
            sum(vertex[1] for vertex in vertices) / len(vertices),
        )

        self._vertices = [Vector2D(vertex[0] - centroid[0], vertex[1] - centroid[1]) for vertex in vertices]
      
        self.shape_type = "Polygon"
        self.inertia = self.calculate_inertia() if not is_static else float("inf")

    @property
    def vertices(self):
        return [vertex.rotate(self.angle).add(self.pos) for vertex in self._vertices]

    @property
    def aabb(self):
        min_x = float('inf')
        max_x = float('-inf')
        min_y = float('inf')
        max_y = float('-inf')

        for v in self.vertices:
            if v.x < min_x: min_x = v.x
            if v.x > max_x: max_x = v.x
            if v.y < min_y: min_y = v.y
            if v.y > max_y: max_y = v.y
            
        return (min_x, min_y, max_x, max_y)

    def calculate_inertia(self):
        area = 0
        center = Vector2D(0, 0)
        mmoi = 0

        prev = len(self._vertices) - 1
        for index in range(len(self._vertices)):
            a = self._vertices[prev]
            b = self._vertices[index]

            area_step = a.cross(b) / 2
            center_step = (a + b) / 3
            mmoi_step = area_step * (a.dot(a) + b.dot(b) + a.dot(b)) / 6

            center = (center * area + center_step * area_step) / (area + area_step)
            area += area_step
            mmoi += mmoi_step

            prev = index

        density = self.mass / area
        mmoi *= density
        mmoi -= self.mass * center.dot(center)

        return mmoi


class Rectangle(Polygon):
    def __init__(self, x, y, width, height, mass = 1, static_friction = 0.5, dynamic_friction = 0.5, bounce = 0.5, name = None, is_static = False):
        Body.__init__(self, x, y, mass, static_friction, dynamic_friction, bounce, name, is_static)
        self.width = width
        self.height = height
        self.shape_type = "Polygon"
        half_width = self.width / 2
        half_height = self.height / 2

        self._vertices = [
            Vector2D(-half_width, -half_height),
            Vector2D(half_width, -half_height),
            Vector2D(half_width, half_height),
            Vector2D(-half_width, half_height)
        ]

        self.inertia = (1 / 12) * mass * (width * width + height * height) if not is_static else float("inf")


class Circle(Body):
    def __init__(self, x, y, radius, mass = 1, static_friction = 0.5, dynamic_friction = 0.5, bounce = 0.5, name = None, is_static = False):
        super().__init__(x, y, mass, static_friction, dynamic_friction, bounce, name, is_static)
        self.radius = radius
        self.shape_type = "Circle"
        self.inertia = (1 / 2) * mass * radius * radius if not is_static else float("inf")

    @property
    def aabb(self):
        return (
            self.pos.x - self.radius,
            self.pos.y - self.radius,
            self.pos.x + self.radius,
            self.pos.y + self.radius
        )
