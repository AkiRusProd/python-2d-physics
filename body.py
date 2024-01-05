from vector import Vector2D


class Body():
    def __init__(self, x, y, mass = 1, friction = 0.3, bounce = 0.5, name = None, body_type = "dynamic"):
        self.pos = Vector2D(x, y)
        self.mass = mass
        self.friction = friction
        self.bounce = bounce
        self.body_type = body_type
        self.name = name
        self.velocity = Vector2D(0, 0)

class Rectangle(Body):
    def __init__(self, x, y, width, height, mass = 1, friction = 0.3, bounce = 0.5, name = None, body_type = "dynamic"):
        super().__init__(x, y, mass, friction, bounce, name, body_type)
        self.pos = Vector2D(x, y)
        self.width = width
        self.height = height
        self.mass = mass
        self.friction = friction
        self.bounce = bounce
        self.name = name
        self.body_type = body_type
        self.velocity = Vector2D(0, 0)

    @property
    def vertices(self):
        x, y = self.pos.x, self.pos.y
        half_width = self.width / 2
        half_height = self.height / 2

        return [
            [x - half_width, y - half_height],
            [x + half_width, y - half_height],
            [x + half_width, y + half_height],
            [x - half_width, y + half_height]
        ]

        # If position is the bottom left edge of the body
        # return [ 
        #     [x, y],
        #     [x + self.width, y],
        #     [x + self.width, y + self.height],
        #     [x, y + self.height]
        # ]
    

    

class Circle(Body):
    def __init__(self, x, y, radius, mass = 1, friction = 0.3, bounce = 0.5, name = None, body_type = "dynamic"):
        super().__init__(x, y, mass, friction, bounce, name, body_type)
        self.pos = Vector2D(x, y)
        self.radius = radius
        self.mass = mass
        self.friction = friction
        self.bounce = bounce
        self.name = name
        self.body_type = body_type
        self.velocity = Vector2D(0, 0)

