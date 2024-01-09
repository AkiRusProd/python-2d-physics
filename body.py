import math
from vector import Vector2D


class Body():
    def __init__(self, x, y, mass = 1, static_friction = 0.5, dynamic_friction = 0.5,  bounce = 0.5, name = None, is_static = False):
        self.pos = Vector2D(x, y)
        self.mass = mass
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

class Rectangle(Body):
    def __init__(self, x, y, width, height, mass = 1, static_friction = 0.5, dynamic_friction = 0.5, bounce = 0.5, name = None, is_static = False):
        super().__init__(x, y, mass, static_friction, dynamic_friction, bounce, name, is_static)
        self.pos = Vector2D(x, y)
        self.width = width
        self.height = height
        self.mass = mass if not is_static else float("inf")
        self.static_friction = static_friction
        self.dynamic_friction = dynamic_friction
        self.bounce = bounce
        self.angle = 0
        self.name = name
        self.shape_type = "Rectangle"
        self.velocity = Vector2D(0, 0)
        self.angular_velocity = 0
        self.inertia = (1 / 12) * mass * (width * width + height * height) if not is_static else float("inf")

    @property
    def vertices(self):
        half_width = self.width / 2
        half_height = self.height / 2

        vertices = [
            Vector2D(-half_width, -half_height),
            Vector2D(half_width, -half_height),
            Vector2D(half_width, half_height),
            Vector2D(-half_width, half_height)
        ]

        return [vertex.rotate(self.angle).add(self.pos) for vertex in vertices]

    
    def rotate(self, angle, in_radians=True):
        if not in_radians:
            angle = math.radians(angle)
        self.angle += angle

class Circle(Body):
    def __init__(self, x, y, radius, mass = 1, static_friction = 0.5, dynamic_friction = 0.5, bounce = 0.5, name = None, is_static = False):
        super().__init__(x, y, mass, static_friction, dynamic_friction, bounce, name, is_static)
        self.pos = Vector2D(x, y)
        self.radius = radius
        self.mass = mass if not is_static else float("inf")
        self.static_friction = static_friction
        self.dynamic_friction = dynamic_friction
        self.bounce = bounce
        self.angle = 0
        self.name = name
        self.shape_type = "Circle"
        self.is_static = is_static
        self.velocity = Vector2D(0, 0)
        self.angular_velocity = 0
        self.inertia = (1 / 2) * mass * radius * radius if not is_static else float("inf")

    def rotate(self, angle, in_radians=True):
        if not in_radians:
            angle = math.radians(angle)
        self.angle += angle
