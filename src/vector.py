import math

class Vector2D:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def add(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x + other.x, self.y + other.y)
        elif isinstance(other, tuple) or isinstance(other, list):
            return Vector2D(self.x + other[0], self.y + other[1])
        elif isinstance(other, int) or isinstance(other, float):
            return Vector2D(self.x + other, self.y + other)
        else:
            raise TypeError("Unsupported operand type(s) for +: 'Vector2D' and '{}'".format(type(other).__name__))
        
    def sub(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x - other.x, self.y - other.y)
        elif isinstance(other, tuple) or isinstance(other, list):
            return Vector2D(self.x - other[0], self.y - other[1])
        elif isinstance(other, int) or isinstance(other, float):
            return Vector2D(self.x - other, self.y - other)
        else:
            raise TypeError("Unsupported operand type(s) for -: 'Vector2D' and '{}'".format(type(other).__name__))
        
    def mul(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x * other.x, self.y * other.y)
        elif isinstance(other, tuple) or isinstance(other, list):
            return Vector2D(self.x * other[0], self.y * other[1])
        elif isinstance(other, int) or isinstance(other, float):
            return Vector2D(self.x * other, self.y * other)
        else:
            raise TypeError("Unsupported operand type(s) for *: 'Vector2D' and '{}'".format(type(other).__name__))

    def div(self, other):
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
    def __round__(self, ndigits):
        return Vector2D(round(self.x, ndigits), round(self.y, ndigits))

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
        
    def __add__(self, other):
        return self.add(other)
    
    def __radd__(self, other):
        return self.add(other)
    
    def __sub__(self, other):
        return self.sub(other)
    
    def __rsub__(self, other):
        return Vector2D(0, 0).sub(self).add(other)
    
    def __mul__(self, other):
        return self.mul(other)
    
    def __rmul__(self, other):
        return self.mul(other)
    
    def __truediv__(self, other):
        return self.div(other)
    
    def __rtruediv__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(other.x / self.x, other.y / self.y)
        elif isinstance(other, (tuple, list)):
            return Vector2D(other[0] / self.x, other[1] / self.y)
        elif isinstance(other, (int, float)):
            return Vector2D(other / self.x, other / self.y)
        else:
            raise TypeError("Unsupported operand type(s) for /: '{}' and 'Vector2D'".format(type(other).__name__))
    

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def cross(self, other):
        return self.x * other.y - self.y * other.x

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        magnitude = self.magnitude()
        if magnitude == 0:
            return Vector2D(0, 0)  #
        return Vector2D(self.x / magnitude, self.y / magnitude)
    
    def __abs__(self):
        return Vector2D(abs(self.x), abs(self.y))
    
    def __len__(self):
        return self.magnitude()
    
    def distance_to(self, other):
        return Vector2D.distance(self, other)
    
    @staticmethod
    def distance(v1, v2):
        return ((v1[0] - v2[0])**2 + (v1[1] - v2[1])**2)**0.5
    
    def __str__(self):
        return "Vector2D({}, {})".format(self.x, self.y)

    def __neg__(self):
        return Vector2D(-self.x, -self.y)
        
    def rotate(self, angle, in_radians = True):
        """Rotate the vector by an angle in radians"""
        if not in_radians:
            angle = math.radians(angle)

        cos = math.cos(angle)
        sin = math.sin(angle)
        x = self.x * cos - self.y * sin
        y = self.x * sin + self.y * cos
        return Vector2D(x, y)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __ne__(self, other):
        return not self == other

