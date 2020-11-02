#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math
import time

SCREEN_DIM = (800, 600)


# =======================================================================================
# Функции для работы с векторами
# =======================================================================================

def sub(x, y):
    """"+ возвращает разность двух векторов"""
    return x[0] - y[0], x[1] - y[1]


def add(x, y):
    """+ возвращает сумму двух векторов"""
    return x[0] + y[0], x[1] + y[1]


def length(x):
    """+ возвращает длину вектора"""
    return math.sqrt(x[0] * x[0] + x[1] * x[1])


def mul(v, k):
    """+ возвращает произведение вектора на число"""
    return v[0] * k, v[1] * k


def vec(x, y):
    """возвращает пару координат, определяющих вектор (координаты точки конца вектора),
    координаты начальной точки вектора совпадают с началом системы координат (0, 0)"""
    return sub(y, x)


# =======================================================================================
# Основные классы
# =======================================================================================
class Vec2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        """возвращает сумму двух векторов"""
        return Vec2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """"возвращает разность двух векторов"""
        return Vec2d(self.x - other.x, self.y - other.y)

    def __mul__(self, k):
        """возвращает произведение вектора на число"""
        return Vec2d(self.x * k, self.y * k)

    def __len__(self):
        """возвращает длину вектора"""
        return int(math.sqrt(self.x ** 2 + self.y ** 2))

    def int_pair(self):
        """Возвращает текущие координаты вектора"""
        return int(self.x), int(self.y)

    def __str__(self):
        """Печать"""
        return str(self.int_pair())

    def __repr__(self):
        """Печать"""
        return str((self.x, self.y))


class Polyline:
    def __init__(self):
        self.points = []
        self.speeds = []

    def add_point(self, vec):
        self.points.append(vec)

    def add_speed(self, speed):
        self.speeds.append(speed)

    def set_points(self):
        for i, (point, speed) in enumerate(zip(self.points, self.speeds)):
            self.points[i] = point + speed
            if point.x > SCREEN_DIM[0] or point.x < 0:
                self.speeds[i] = Vec2d(speed.x * (-1), speed.y)
            if point.y > SCREEN_DIM[1] or point.y < 0:
                self.speeds[i] = Vec2d(speed.x, speed.y * (-1))
        print('!\t', self.points,'\t', self.speeds)

    def draw_points(self, gameDisplay, width=3, color=(255, 255, 255)):
        for p in self.points:
            pygame.draw.circle(gameDisplay, color,
                               (p.int_pair()), width)

    def draw_lines(self, gameDisplay, width=3, color=(255, 255, 255)):
        for first, last in zip(self.points[-1:] + self.points[:-1], self.points):
            pygame.draw.line(gameDisplay, color,
                             (first.int_pair()), (last.int_pair()), width)


class Knot(Polyline):
    pass


# =======================================================================================
# Функции отрисовки
# =======================================================================================
def draw_points(points, style="points", width=3, color=(255, 255, 255)):
    """функция отрисовки точек на экране"""
    if style == "line":
        for p_n in range(-1, len(points) - 1):
            pygame.draw.line(gameDisplay, color,
                             (int(points[p_n][0]), int(points[p_n][1])),
                             (int(points[p_n + 1][0]), int(points[p_n + 1][1])), width)

    elif style == "points":
        for p in points:
            pygame.draw.circle(gameDisplay, color,
                               (int(p[0]), int(p[1])), width)


def draw_help():
    """функция отрисовки экрана справки программы"""
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["", ""])
    data.append([str(steps), "Current points"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


# =======================================================================================
# Функции, отвечающие за расчет сглаживания ломаной
# =======================================================================================
def get_point(points, alpha, deg=None):
    if deg is None:
        deg = len(points) - 1
    if deg == 0:
        return Vec2d(*points[0])
    a = Vec2d(*points[deg])
    b = get_point(points, alpha, deg - 1)
    return a * alpha + b * (1 - alpha)


def get_points(base_points, count):
    alpha = 1 / count
    res = []
    for i in range(count):
        res.append(get_point(base_points, i * alpha).int_pair())
    return res


def get_knot(points, count):
    if len(points) < 3:
        return []
    res = []
    for i in range(-2, len(points) - 2):
        ptn = []
        ptn.append(mul(add(points[i], points[i + 1]), 0.5))
        ptn.append(points[i + 1])
        ptn.append(mul(add(points[i + 1], points[i + 2]), 0.5))

        res.extend(get_points(ptn, count))
    return res


def set_points(points, speeds):
    """функция перерасчета координат опорных точек"""
    for p in range(len(points)):
        points[p] = add(points[p], speeds[p])
        if points[p][0] > SCREEN_DIM[0] or points[p][0] < 0:
            speeds[p] = (- speeds[p][0], speeds[p][1])
        if points[p][1] > SCREEN_DIM[1] or points[p][1] < 0:
            speeds[p] = (speeds[p][0], -speeds[p][1])


# =======================================================================================
# Основная программа
# =======================================================================================
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    points = []
    speeds = []
    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)
    line = Polyline()

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    line.points = []
                    points = []
                    speeds = []
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                line.add_point(Vec2d(*event.pos))
                a, b = random.random() * 2, random.random() * 2
                line.add_speed(Vec2d(a, b))
                points.append(event.pos)
                speeds.append((a, b))

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        line.draw_points(gameDisplay)
        line.draw_lines(gameDisplay, 5, color)

        draw_points(points)
        draw_points(get_knot(points, steps), "line", 3, color)
        if not pause:
            set_points(points, speeds)
            line.set_points()
            print('~\t', points, '\t', speeds)
            time.sleep(0.1)
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
