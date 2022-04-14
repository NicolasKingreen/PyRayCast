"""
2d ray casting demo made with codingtrain
"""

import pygame
from pygame.locals import *
from pygame.math import Vector2 as Vector

from perlin_noise import PerlinNoise

import random
import sys
from math import radians, cos, sin


SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 400, 400
TARGET_FPS = 30


class Boundary:
    def __init__(self, x1, y1, x2, y2):
        self.a = Vector(x1, y1)
        self.b = Vector(x2, y2)

    def draw(self, surface):
        pygame.draw.line(surface, "white", self.a, self.b, 2)


class Ray:
    def __init__(self, pos, angle):
        self.pos = pos
        self.dir = Vector(cos(angle), sin(angle))

    def draw(self, surface):
        pygame.draw.line(surface, "white", self.pos, self.pos + self.dir * 10)
        pygame.draw.circle(surface, "white", self.pos, 2)

    def look_at(self, x, y):
        self.dir.x = x - self.pos.x
        self.dir.y = y - self.pos.y
        if self.dir:
            self.dir.normalize_ip()

    def cast(self, wall):
        x1 = wall.a.x
        y1 = wall.a.y
        x2 = wall.b.x
        y2 = wall.b.y

        x3 = self.pos.x
        y3 = self.pos.y
        x4 = self.pos.x + self.dir.x
        y4 = self.pos.y + self.dir.y

        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if not den:
            return None

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

        if (0 < t < 1) and (u > 0):
            pt = Vector()
            pt.x = x1 + t * (x2 - x1)
            pt.y = y1 + t * (y2 - y1)
            return pt
        else:
            return None

class Particle:
    def __init__(self):
        self.pos = Vector(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        total_rays = 360
        self.rays = []
        for i in range(0, 360, 10):
            self.rays.append(Ray(self.pos, radians(i)))

    def update(self, pos):
        self.pos = Vector(pos)
        for ray in self.rays:
            ray.pos = Vector(pos)

    def look(self, surface, walls):
        for ray in self.rays:
            closest = None
            record = SCREEN_WIDTH
            for wall in walls:
                pt = ray.cast(wall)
                if pt:
                    d = self.pos.distance_to(pt)
                    if d < record:
                        record = d
                        closest = pt
            if closest:
                pygame.draw.line(surface, "white", self.pos, closest)

    def draw(self, surface):
        pygame.draw.circle(surface, "white", self.pos, 4)
        for ray in self.rays:
            ray.draw(surface)


class Application:
    def __init__(self):
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("2r ray casting")
        self.display_surface = pygame.display.set_mode(SCREEN_SIZE)

        self.setup()

        self.run()

    def setup(self):
        self.particle = Particle()

        self.xoff = 0
        self.yoff = 0.5
        self.noise = PerlinNoise()

        self.walls = []
        for _ in range(5):
            x1 = random.randint(0, SCREEN_WIDTH)
            x2 = random.randint(0, SCREEN_WIDTH)
            y1 = random.randint(0, SCREEN_HEIGHT)
            y2 = random.randint(0, SCREEN_HEIGHT)
            self.walls.append(Boundary(x1, y1, x2, y2))

    def update(self):
        x = abs(self.noise([self.xoff, self.yoff])) * SCREEN_WIDTH * 3
        y = abs(self.noise([self.xoff, self.yoff][:-1])) * SCREEN_HEIGHT * 3
        self.particle.update((x, y))

        self.xoff += 0.01
        self.yoff += 0.01

    def draw(self, surface):
        surface.fill("black")
        for wall in self.walls:
            wall.draw(surface)
        self.particle.draw(surface)
        self.particle.look(surface, self.walls)
        pygame.display.update()

    def run(self):
        self.is_running = True
        while self.is_running:

            frame_time_ms = self.clock.tick(TARGET_FPS)

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.terminate()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.terminate()

            self.update()
            self.draw(self.display_surface)

        pygame.quit()
        sys.exit()

    def terminate(self):
        self.is_running = False


if __name__ == "__main__":
    Application()
