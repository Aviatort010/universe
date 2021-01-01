import pygame as pg
import numpy as np


class Vec2:
    def __init__(self, x_cor=0, y_cor=0):
        self.x = x_cor
        self.y = y_cor

    def get_xy(self):
        return [self.x, self.y]

    def get_len(self):
        return np.hypot(self.x, self.y)

    def get_angle(self):
        return np.arctan2(self.y, self.x)

    def set_xy(self, x, y):
        self.x = x
        self.y = y

    def set_len(self, len):
        l = self.len()
        self.x = len * self.x / l
        self.y = len * self.y / l

    def set_angle(self, alpha):
        l = self.len()
        self.x = l * np.cos(alpha)
        self.y = l * np.sin(alpha)

    def draw(self, xy0, scale, color, arrow=True):
        xy1 = (xy0[0] + self.x * scale, xy0[1] + self.y * scale)
        pg.draw.line(screen, color, (int(round(xy0[0])), int(round(wh - xy0[1]))),
                     (int(round(xy1[0])), int(round(wh - xy1[1]))), 2)
        if arrow:
            betta = np.pi / 4
            alpha = self.angle()
            r = np.sqrt(self.x ** 2 + self.y ** 2) / 5
            v1 = Vec2(-self.x, -self.y)
            v1.set_len(r)
            v1.set_angle(np.pi + alpha + betta)
            v1.draw((xy1[0], xy1[1]), 1, color, False)
            v2 = Vec2(-self.x, -self.y)
            v2.set_len(r)
            v2.set_angle(np.pi + alpha - betta)
            v2.draw((xy1[0], xy1[1]), 1, color, False)


"""""
class Universe:
    def __init__(self, gravity_constant=2.81):
        self.g = gravity_constant
"""""


class Particle:
    def __init__(self, mass=1, radius=2, x_cor=0, y_cor=0, vel_x=0, vel_y=0):
        self.m = mass
        self.r_s = radius
        self.r_v = Vec2(x_cor, y_cor)
        self.v_v = Vec2(vel_x, vel_y)
        self.color = [240, 240, 240]
        self.g = 6.67430

    def move(self, dt):
        dv = dot_vector_num(self.react(), dt)
        self.v_v = add(self.v_v, dv)
        dr = dot_vector_num(self.v_v, dt)
        self.r_v = add(self.r_v, dr)

    def get_xy(self):
        return [self.r_v.get_xy()[0], self.r_v.get_xy()[1]]

    def get_mass(self):
        return self.m

    def react(self):
        f_end = Vec2()
        for particle in particles:
            rad = np.hypot(self.v_v.get_xy()[0] - particle.get_xy()[0], self.v_v.get_xy()[1] - particle.get_xy()[1])
            i_0 = Vec2(self.v_v.get_xy()[0] - particle.get_xy()[0], self.v_v.get_xy()[1] - particle.get_xy()[1])
            i_0 = dot_vector_num(i_0, 1 / rad)
            f = Vec2(dot_vector_num(i_0, self.g * particle.get_mass() * self.m / rad))
            f_end = add(f_end, f)
        a = Vec2(dot_vector_num(f_end, 1 / self.m))
        return a

    def draw(self):
        pg.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.r)


def add(vector_a: Vec2, vector_b: Vec2):
    vector_c = Vec2(vector_a.get_xy()[0] + vector_b.get_xy()[0], vector_a.get_xy()[1] + vector_b.get_xy()[1])
    return vector_c


def dot_vector_num(vector_a: Vec2, num):
    vector_b = Vec2(vector_a.get_xy()[0] * num, vector_a.get_xy()[1] * num)
    return vector_b


pg.init()

ww = 1000
wh = int(ww / 16 * 9)
ms = 100
k = 0.00005
fps1 = 1 / 30 * 1000
color_bkg = [0, 0, 0]

particles = []
n = 1000
for i in range(n):
    particles.append(Particle(1, 2, np.random.randint(10, ww - 10), np.random.randint(10, wh - 10),
                            k * (np.random.randint(-100, 100)), k * (np.random.randint(-100, 100))))

screen = pg.display.set_mode((ww, wh))
pg.display.set_caption("the Universe")

TICK = pg.USEREVENT + 1
pg.time.set_timer(TICK, ms)
fps = pg.time.Clock()

run_x = True

while run_x:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run_x = False
        if TICK:
            dt = ms
    screen.fill(color_bkg)
    for particle in particles:
        particle.move(dt)
        particle.draw()
    pg.display.flip()
pg.quit()
