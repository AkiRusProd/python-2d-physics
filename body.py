from utils import ObservableList


class Body():
    def __init__(self, x, y, mass = 1, friction = 0.3, bounce = 0.5, name = None, body_type = "dynamic"):
        self.pos = [x, y]
        self.mass = mass
        self.friction = friction
        self.bounce = bounce
        self.body_type = body_type
        self.name = name

class Rectangle(Body):
    def __init__(self, x, y, width, height, mass = 1, friction = 0.3, bounce = 0.5, name = None, body_type = "dynamic"):
        super().__init__(x, y, mass, friction, bounce, name, body_type)
        self.pos = ObservableList([x, y], callback=self._update_vertices)
        self.width = width
        self.height = height
        self.mass = mass
        self.friction = friction
        self.bounce = bounce
        self.name = name
        self.body_type = body_type
        self.velocity = [0, 0]
        self.vertices = [None, None, None, None]
        self._update_vertices()

    def _update_vertices(self):
        x, y = self.pos
        self.vertices = [[x, y], [x + self.width, y],  [x + self.width, y + self.height], [x, y + self.height]]

class Circle(Body):
    def __init__(self, x, y, radius, mass = 1, friction = 0.3, bounce = 0.5, name = None, body_type = "dynamic"):
        super().__init__(x, y, mass, friction, bounce, name, body_type)
        self.pos = [x, y]
        self.radius = radius
        self.mass = mass
        self.friction = friction
        self.bounce = bounce
        self.name = name
        self.body_type = body_type
        self.velocity = [0, 0]

