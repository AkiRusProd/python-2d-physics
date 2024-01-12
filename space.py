from body import Body
from collision import collide


class Space():
    def __init__(self, bodies: list[Body], gravity = 9.8):
        self.bodies: list[Body] = bodies
        self.gravity = gravity

        self._contact_points = []

    def add(self, body: Body):
        self.bodies.append(body)

    def simulate_gravity(self, dt):
        for body in self.bodies:
            if body.is_static == False:
                body.velocity[1] += self.gravity * body.mass * dt

    def update_position(self, dt):
        for body in self.bodies:
            if body.is_static == False:
                body.pos += body.velocity * dt
                body.angle += body.angular_velocity * dt

    def handle_collisions(self):
        self._contact_points = []
        for i in range(len(self.bodies) - 1):
            for j in range(i + 1, len(self.bodies)):
                if self.bodies[i] == self.bodies[j]:
                    continue

                contact_points = collide(self.bodies[i], self.bodies[j])
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