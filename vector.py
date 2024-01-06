import math

class Vector2D:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x + other.x, self.y + other.y)
        elif isinstance(other, tuple) or isinstance(other, list):
            return Vector2D(self.x + other[0], self.y + other[1])
        elif isinstance(other, int) or isinstance(other, float):
            return Vector2D(self.x + other, self.y + other)
        else:
            raise TypeError("Unsupported operand type(s) for +: 'Vector2D' and '{}'".format(type(other).__name__))
        

    def __sub__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x - other.x, self.y - other.y)
        elif isinstance(other, tuple) or isinstance(other, list):
            return Vector2D(self.x - other[0], self.y - other[1])
        elif isinstance(other, int) or isinstance(other, float):
            return Vector2D(self.x - other, self.y - other)
        else:
            raise TypeError("Unsupported operand type(s) for -: 'Vector2D' and '{}'".format(type(other).__name__))
        
    def __mul__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x * other.x, self.y * other.y)
        elif isinstance(other, tuple) or isinstance(other, list):
            return Vector2D(self.x * other[0], self.y * other[1])
        elif isinstance(other, int) or isinstance(other, float):
            return Vector2D(self.x * other, self.y * other)
        else:
            raise TypeError("Unsupported operand type(s) for *: 'Vector2D' and '{}'".format(type(other).__name__))

    def __truediv__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x / other.x, self.y / other.y)
        elif isinstance(other, tuple) or isinstance(other, list):
            return Vector2D(self.x / other[0], self.y / other[1])
        elif isinstance(other, int) or isinstance(other, float):
            return Vector2D(self.x / other, self.y / other)
        else:
            raise TypeError("Unsupported operand type(s) for /: 'Vector2D' and '{}'".format(type(other).__name__))

    def __iter__(self):
        yield self.x
        yield self.y

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Index out of range")

    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError("Index out of range")

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def cross(self, other):
        return self.x * other.y - self.y * other.x

    @property
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    @property
    def normalize(self):
        magnitude = self.magnitude
        return Vector2D(self.x / magnitude, self.y / magnitude)
    
    def __abs__(self):
        return Vector2D(abs(self.x), abs(self.y))
    
    def __len__(self):
        return self.magnitude
    
    def distance_to(self, other):
        return Vector2D.distance(self, other)
    
    @staticmethod
    def distance(v1, v2):
        return ((v1[0] - v2[0])**2 + (v1[1] - v2[1])**2)**0.5
    
    def __repr__(self):
        return "Vector2D({}, {})".format(self.x, self.y)


