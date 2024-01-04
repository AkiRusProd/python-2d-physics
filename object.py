


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
        self.friction = 0.9
        self.bounce = 0.7
        self.type = "dynamic"


class Circle:
    def __init__(self, x, y, radius):
        self.radius = radius
        self.pos = [x, y]
        self.velocity = [0, 0]
        self.mass = 1
        self.friction = 0.9
        self.bounce = 0.3
        self.type = "dynamic"