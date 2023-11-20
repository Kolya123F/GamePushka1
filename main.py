import math
import random
from random import choice
import numpy as np

import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

score = 0


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # FIXME
        new_x = self.x + self.vx
        new_y = self.y - self.vy

        if 15 < new_x < 786:
            self.x = new_x
        else:
            self.vx = -self.vx * 0.6
            self.vy = -self.vy * 0.8
        if new_y < 550:
            self.y = new_y
        else:
            self.vy = -self.vy * 0.6
            self.vx = self.vx * 0.4

        self.vy -= 2

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2) ** 0.5 <= self.r + obj.r:
            return True
        else:
            return False


class Target1:
    def __init__(self, screen):
        self.R = random.randint(30, 40)
        self.vx = random.randint(3, 5)
        self.points = 0
        self.live = 1
        self.screen = screen
        self.x = random.randint(720, 740)
        self.y = random.randint(350, 450)
        self.dvy = 0.5
        self.r = random.randint(25, 33)
        self.vy = random.randint(2, 5)
        self.color = BLUE

    def new_target(self):
        """ Инициализация новой цели. """
        self.R = random.randint(30, 40)
        self.x = random.randint(720, 740)
        self.y = random.randint(350, 450)
        self.dvy = 0.5
        self.r = random.randint(25, 33)
        self.color = BLUE
        self.live = 1

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.circle(
            screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        pygame.draw.circle(
            screen,
            BLACK,
            (self.x, self.y),
            self.r + 2, 2
        )

    def move(self):
        """
        Переместить уель по прошествии единицы времени.
        Метод описывает перемещение цели за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy
        """

        self.y += self.R * np.sin(self.vy)
        self.vy += self.dvy


class Target2:
    def __init__(self, screen):
        self.omega = random.randint(10, 10)
        self.R = random.randint(4, 6)
        self.points = 0
        self.live = 1
        self.screen = screen
        self.x = random.randint(560, 600)
        self.y = random.randint(50, 530)
        self.r = random.randint(10, 15)
        self.vy = random.randint(2, 5)
        self.color = RED

    def new_target(self):
        """ Инициализация новой цели. """
        self.omega = random.randint(10, 10)
        self.R=random.randint(4, 6)
        self.x=random.randint(560, 600)
        self.y = random.randint(50, 530)
        self.r = random.randint(10, 15)
        self.vy = random.randint(2, 5)
        self.color = RED
        self.live = 1

    def move(self):
        """
        Переместить уель по прошествии единицы времени.
        Метод описывает перемещение цели за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy
        """

        self.y -= self.vy
        if (self.y + self.r >= HEIGHT - 200) and (self.vy < 0):
            self.vy *= -1
        elif (self.y - self.r <= 0) and (self.vy > 0):
            self.vy *= -1
        self.x += self.R*np.cos(self.omega)
        self.omega += 0.4

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.circle(
            screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        pygame.draw.circle(
            screen,
            BLACK,
            (self.x, self.y),
            self.r + 2, 2
        )


class Tank:
    """
    Класс танков. Обладает координатами (изменяемой x и постоянной y), флагом начала выстрела self.f2_on,
    силой выстрела self.f2_power, увеличиваемой при зажатии мыши, типом снаряда self.bullet_type - числом 1 или 2,
    углом наклона орудия self.an, цветом self.color и флагом жизни self.live
    """
    def __init__(self, screen):
        self.screen = screen
        self.x = WIDTH - 700
        self.y = 570
        self.f2_power = 10
        self.f2_on = 0
        self.an = 0
        self.color = GREEN

    def targetting(self, event):
        """Прицеливание. Зависит от положения смещаемой мыши."""
        if event and (event.pos[1] < self.y):
            self.an = math.atan((event.pos[0]-self.x) / (event.pos[1]-self.y))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def fire2_start(self, event):
        """означает начало выстрела и увеличения начальной скорости снарда"""
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел снарядом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, self.x, self.y)
        new_ball.r += 5
        if event.pos[1] < self.y:
            self.an = math.atan((event.pos[0]-self.x) / (event.pos[1]-self.y))
        new_ball.vx = - self.f2_power * math.sin(self.an)
        new_ball.vy = self.f2_power * math.cos(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def power_up(self):
        """Если зажата кнопка мыши, увеличивает начальную скорость снаряда на 1 за 1 кадр перерисовки"""
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY

    def move(self):
        """
        Перемещает танк или влево на 7 пикселей, если в момент вызова зажата кнопка A и не зажата D,
        или вправо на 7 пикселей, если в момент вызова зажата кнопка D и не зажата A,
        в противном случае танк остаётся на месте
        """
        speed = 0
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[97] and (not (pressed_keys[100])) and self.x > 40:
            speed = -7
        elif (not (pressed_keys[97])) and pressed_keys[100] and self.x < WIDTH - 500:
            speed = 7
        self.x += speed

    def draw(self):
        """Рисует гусеничный танк с повернутым в направлении курсора орудием"""
        y11 = self.y + 5 * math.sin(self.an)
        x11 = self.x - 5 * math.cos(self.an)
        y12 = self.y - 5 * math.sin(self.an)
        x12 = self.x + 5 * math.cos(self.an)

        y21 = self.y - (self.f2_power + 20) * math.cos(self.an) - 5 * math.sin(self.an)
        x21 = self.x - (self.f2_power + 20) * math.sin(self.an) + 5 * math.cos(self.an)
        y22 = self.y - (self.f2_power + 20) * math.cos(self.an) + 5 * math.sin(self.an)
        x22 = self.x - (self.f2_power + 20) * math.sin(self.an) - 5 * math.cos(self.an)
        pygame.draw.polygon(self.screen, self.color, [[x11, y11], [x12, y12], [x21, y21], [x22, y22]])
        pygame.draw.circle(self.screen, [29, 150, 20], [self.x, self.y], 20)
        x1 = self.x - 30
        y1 = self.y
        x2 = self.x - 30
        y2 = self.y + 10
        x3 = self.x - 20
        y3 = self.y + 20
        x4 = self.x + 30
        y4 = self.y
        x5 = self.x + 30
        y5 = self.y + 10
        x6 = self.x + 20
        y6 = self.y + 20
        pygame.draw.polygon(self.screen, [29, 100, 20], [[x1, y1], [x2, y2], [x3, y3], [x6, y6], [x5, y5], [x4, y4]])


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
tank = Tank(screen)
target1 = Target1(screen)
target2 = Target2(screen)
finished = False

while not finished:
    screen.fill(WHITE)
    tank.move()
    tank.draw()
    # gun.draw()
    screen.blit(pygame.font.SysFont('Verdana', 40).render(str(score), False, (0, 0, 0)), (30, 20))
    screen.blit(
            pygame.font.SysFont('Verdana', 20).render('Использовано шаров: ' + str(len(balls)), False, (0, 0, 0)),
            (200, 40))
    target1.draw()
    target2.draw()
    target2.move()
    target1.move()
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            tank.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            tank.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            tank.targetting(event)

    for b in balls:
        b.move()
        if b.hittest(target1) and target1.live:
            target1.live = 0
            target1.hit()
            target1.new_target()

            balls = []
            score += 1
        if b.hittest(target2) and target2.live:
            target2.live = 0
            target2.hit()
            target2.new_target()

            balls = []
            score += 1
    tank.power_up()

pygame.quit()
