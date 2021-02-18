import pygame as pg
import numpy as np

zero = 0.000001


def ir(x):
    return int(round(x))


class Vec2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        if isinstance(other, Vec2):
            return self.x * other.x + self.y * other.y
        elif isinstance(other, (int, float)):
            return Vec2(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Vec2(self.x / other, self.y / other)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __imul__(self, other):
        self.x *= other
        self.y *= other
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __neg__(self):
        return Vec2(-self.x, -self.y)

    def __pos__(self):
        return Vec2(self.x, self.y)

    def __str__(self):
        return "V2 " + str(self.x) + " " + str(self.y) + " " + str(self.len())

    def __rmul__(self, other):
        if isinstance(other, Vec2):
            return self.x * other.x + self.y * other.y
        elif isinstance(other, (int, float)):
            return Vec2(self.x * other, self.y * other)

    def get_xy(self):
        return self.x, self.y

    def len(self):
        return np.hypot(self.x, self.y)

    def get_ang(self):
        return np.arctan2(self.y, self.x)

    def set_xy(self, x, y):
        self.x = x
        self.y = y

    def set_len(self, len):
        l = self.len()
        self.x = len * self.x / l
        self.y = len * self.y / l

    def set_ang(self, alpha):
        l = self.len()
        self.x = l * np.cos(alpha)
        self.y = l * np.sin(alpha)

    def e(self):
        l = self.len()
        if l == 0: l = zero
        return Vec2(self.x / l, self.y / l)

    def draw(self, xy0, scale=1, color=(200, 200, 200), arrow=True):
        xy1 = (xy0[0] + self.x * scale, xy0[1] + self.y * scale)
        pg.draw.line(screen, color, (ir(xy0[0]), ir(wh - xy0[1])), (ir(xy1[0]), ir(wh - xy1[1])), 2)
        if arrow:
            betta = np.pi / 4
            alpha = self.get_ang()
            r = np.sqrt(self.x ** 2 + self.y ** 2) / 5
            v1 = Vec2(-self.x, -self.y)
            v1.set_len(r)
            v1.set_ang(np.pi + alpha + betta)
            v1.draw((xy1[0], xy1[1]), 1, color, False)
            v2 = Vec2(-self.x, -self.y)
            v2.set_len(r)
            v2.set_ang(np.pi + alpha - betta)
            v2.draw((xy1[0], xy1[1]), 1, color, False)


class Particle:
    g = 6.67430

    def __init__(self, mass=0.00001, size_r=2, x=0, y=0, vx=0, vy=0):
        self.m = mass
        self.size_r = size_r
        self.r = Vec2(x, y)
        self.v = Vec2(vx, vy)
        self.color = [240, 240, 240]

    def move(self, dt):
        a = self.a()
        self.v += a * dt
        self.r += self.v * dt

    def get_xy(self):
        return self.r.get_xy()

    def a(self):
        f1 = Vec2()
        for particle in particles:
            if particle != self:
                r = particle.r - self.r
                R = r.len() * 1000
                if R < 20000: R = 20000
                f1 += Particle.g * particle.m / R**2 * r.e()
#        f1.draw(self.r.get_xy(), scale=1000)
        return f1

    def vyazcost(self):
        k = 1.5
        self.v = dot_vector_num(self.v, 1 / k)

    def draw(self):
        pg.draw.circle(screen, self.color, (ir(self.r.get_xy()[0]), ir(wh - self.r.get_xy()[1])), self.size_r)


def add(vector_a: Vec2, vector_b: Vec2):
    vector_c = Vec2(vector_a.get_xy()[0] + vector_b.get_xy()[0], vector_a.get_xy()[1] + vector_b.get_xy()[1])
    return vector_c


def dot_vector_num(vector_a: Vec2, num):
    vector_b = Vec2(vector_a.get_xy()[0] * num, vector_a.get_xy()[1] * num)
    return vector_b


pg.init()

ww = 800
wh = int(ww / 9 * 16)
ms = 20
k = 0.005
fps = 60
dt = 20
color_bkg = [0, 0, 0]
"""
particles = [Particle(mass=10000, size_r=6, x=ww//2, y=wh//2 + 50, vx=0.1),
             Particle(mass=10000, size_r=6, x=ww//2, y=wh//2 - 50, vx=-0.1)]
"""
particles = []

n = 20
for i in range(n):
    k = np.random.randint(2000, 10000)
    particles.append(Particle(mass=k, size_r=k//2000, x=np.random.randint(ww//2 - 100, ww//2 + 100), y=np.random.randint(wh//2 - 100, wh//2 + 100), vx=0, vy=0))
particles.append(Particle(mass=20000, size_r=10, x=ww//2, y=wh//2))

screen = pg.display.set_mode((ww, wh))
pg.display.set_caption("the Universe")
clock = pg.time.Clock()
run_x = True

while run_x:
    clock.tick(fps)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run_x = False
    screen.fill(color_bkg)
    for particle in particles:
        particle.move(dt)
        particle.draw()
    pg.display.flip()
pg.quit()
