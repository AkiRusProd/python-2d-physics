import math
from vector import Vector2D


class Body():
    def __init__(self, x, y, mass = 1, friction = 0.3, bounce = 0.5, name = None, is_static = False):
        self.pos = Vector2D(x, y)
        self.mass = mass
        self.friction = friction
        self.bounce = bounce
        self._angle = 0
        self.is_static = is_static
        self.name = name
        self.shape_type = None
        self.velocity = Vector2D(0, 0)

class Rectangle(Body):
    def __init__(self, x, y, width, height, mass = 1, friction = 0.3, bounce = 0.5, name = None, is_static = False):
        super().__init__(x, y, mass, friction, bounce, name, is_static)
        self.pos = Vector2D(x, y)
        self.width = width
        self.height = height
        self.mass = mass
        self.friction = friction
        self.bounce = bounce
        self._angle = 0
        self.name = name
        self.shape_type = "Rectangle"
        self.velocity = Vector2D(0, 0)

    @property
    def vertices(self):
        # x, y = self.pos.x, self.pos.y
        half_width = self.width / 2
        half_height = self.height / 2

        # return [
        #     Vector2D(x - half_width, y - half_height),
        #     Vector2D(x + half_width, y - half_height),
        #     Vector2D(x + half_width, y + half_height),
        #     Vector2D(x - half_width, y + half_height)
        # ]

        # If position is the bottom left edge of the body
        # return [ 
        #     [x, y],
        #     [x + self.width, y],
        #     [x + self.width, y + self.height],
        #     [x, y + self.height]
        # ]

        vertices = [
            Vector2D(-half_width, -half_height),
            Vector2D(half_width, -half_height),
            Vector2D(half_width, half_height),
            Vector2D(-half_width, half_height)
        ]

        return [vertex.rotate(self._angle).add(self.pos) for vertex in vertices]

    
    def rotate(self, angle, in_radians=True):
        if not in_radians:
            angle = math.radians(angle)
        self._angle += angle

class Circle(Body):
    def __init__(self, x, y, radius, mass = 1, friction = 0.3, bounce = 0.5, name = None, is_static = False):
        super().__init__(x, y, mass, friction, bounce, name, is_static)
        self.pos = Vector2D(x, y)
        self.radius = radius
        self.mass = mass
        self.friction = friction
        self.bounce = bounce
        self._angle = 0
        self.name = name
        self.shape_type = "Circle"
        self.is_static = is_static
        self.velocity = Vector2D(0, 0)

