from .body import Body
from .collision import collide


def intersect_aabb(body_a, body_b):
    a_min_x, a_min_y, a_max_x, a_max_y = body_a.aabb
    b_min_x, b_min_y, b_max_x, b_max_y = body_b.aabb

    return (
        a_min_x <= b_max_x and
        a_max_x >= b_min_x and
        a_min_y <= b_max_y and
        a_max_y >= b_min_y
    )


class Space:
    def __init__(self, bodies: list[Body], gravity = 9.8, rotation=True):
        self.bodies: list[Body] = bodies
        self.gravity = gravity
        self.rotation = rotation
        self._contact_points = []

    def add(self, body: Body):
        self.bodies.append(body)

    def simulate_gravity(self, dt):
        for body in self.bodies:
            if body.is_static == False:
                body.velocity[1] -= self.gravity * dt

    def update_position(self, dt):
        for body in self.bodies:
            if body.is_static == False:
                body.pos += body.velocity * dt
				
                if self.rotation: body.angle += body.angular_velocity * dt

    def handle_collisions(self):
        self._contact_points = []
        for i in range(len(self.bodies) - 1):
            for j in range(i + 1, len(self.bodies)):
                if self.bodies[i] == self.bodies[j]:
                    continue

                if not intersect_aabb(self.bodies[i], self.bodies[j]):
                    continue
                contact_points = collide(self.bodies[i], self.bodies[j], self.rotation)
                if contact_points is None:
                    continue

                for point in contact_points:
                    if point is None:
                        continue

                    self._contact_points.append(point)

    def step(self, dt):
        self.simulate_gravity(dt)
        self.update_position(dt)
        self.handle_collisions()
