


class Rectangle:
    def __init__(self, x, y, width, height):
        # self.x = x
        # self.y = y
        self.width = width
        self.height = height
        self.pos = [x, y]
        self.size = [width, height]
        self.velocity = [0, 0]
        self.mass = 1
        self.friction = 0.3
        self.bounce = 0.5
        self.type = "dynamic"
        self.verticies = [[x, y], [x + width, y],  [x + width, y + height], [x, y + height]]
        self.tag = None

    def move(self, dx, dy):
        self.pos[0] += dx
        self.pos[1] += dy

        x, y = self.pos
        self.verticies = [[x, y], [x + self.width, y],  [x + self.width, y + self.height], [x, y + self.height]]

    def update_verticies(self):
        x, y = self.pos
        self.verticies = [[x, y], [x + self.width, y],  [x + self.width, y + self.height], [x, y + self.height]]


class Circle:
    def __init__(self, x, y, radius):
        self.radius = radius
        self.pos = [x, y]
        self.velocity = [0, 0]
        self.mass = 1
        self.friction = 0.3
        self.bounce = 0.5
        self.type = "dynamic"
        self.tag = None