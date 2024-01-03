


class Rectangle:
    def __init__(self, x, y, width, height):
        # self.x = x
        # self.y = y
        self.width = width
        self.height = height
        self.pos = [x, y]
        self.velocity = [0, 0]
        self.mass = 1
        self.friction = 0.9
