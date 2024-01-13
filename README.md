# 2D Physics Engine

This project is a simple 2D physics simulation implemented in Python using the Pygame library for objects visualization. It is designed to simulate basic physical phenomena such as collisions, gravity, and friction for various shapes like rectangles, circles, and convex polygons.

## Features

- **Collision Detection**: Implements Separating Axis Theorem (SAT) for polygon collision detection and handles circle collisions.
- **Collision Response**: Includes impulse-based collision response with support for both linear and rotational kinematics.
- **Friction**: Simulates both static and dynamic friction.
- **Gravity**: Applies gravitational forces to objects.


## Structure

The project is structured into several modules:

- [main.py](src/main.py): The entry point of the application, which sets up the Pygame window and contains the main game loop.
- [body.py](src/body.py): Defines the `Polygon`, `Rectangle`, and `Circle` classes, which represent physical objects in the simulation.
- [space.py](src/space.py): Contains the `Space` class, which manages all bodies and simulates physics steps.
- [vector.py](src/vector.py): Implements the `Vector2D` class for vector operations.
- [collision.py](src/collision.py): Contains functions for collision detection and response.



## Acknowledgments

This project was inspired by various resources on game development and physics simulations, including:

- [2D Engine Collisions](https://2dengine.com/doc/collisions.html)
- [Game Development Tutorials by Tuts+](https://code.tutsplus.com/categories/game-development)
- [Jeffrey Thompson's Collision Detection](https://www.jeffreythompson.org/collision-detection/table_of_contents.php)
- [Dyn4j Physics Engine](https://dyn4j.org/)
- [Chris Hecker's Physics Articles](https://chrishecker.com/images/e/e7/Gdmphys3.pdf)
