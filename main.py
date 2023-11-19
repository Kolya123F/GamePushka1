import math
import random
from random import choice

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
        if ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2) ** 0.5 <= self.r + obj.r:
            return True
        else:
            return False
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        # FIXME
        return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = BLACK

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = BLACK

    def draw(self):
        "Координаты орудия:"
        x = 40
        y = 450
        h = 3
        L = 20 + int(self.f2_power / 4 * 3)
        x1 = x - h * (math.sin(-self.an) + math.cos(-self.an))
        y1 = y + h * (math.sin(-self.an) - math.cos(-self.an))
        x2 = x1 + L * math.cos(-self.an)
        y2 = y1 - L * math.sin(-self.an)
        x3 = x1 + 2 * h * math.sin(-self.an)
        y3 = y1 + 2 * h * math.cos(-self.an)
        x4 = x3 + L * math.cos(-self.an)
        y4 = y3 - L * math.sin(-self.an)

        pygame.draw.polygon(self.screen, self.color,
                     [[x1, y1], [x2, y2],
                      [x4, y4], [x3, y3]])
    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = BLACK


class Target1:
    def __init__(self, screen):
        self.points = 0
        self.live = 1
        self.screen = screen
        self.x = random.randint(500, 730 )
        self.y = random.randint(50, 530)
        self.r = random.randint(20, 50)
        self.color = RED

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = random.randint(500, 600)
        self.y = random.randint(300, 550)
        self.r = random.randint(10, 25)
        self.color = RED
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

class Target2:
    def __init__(self, screen):
        self.points = 0
        self.live = 1
        self.screen = screen
        self.x = random.randint(500, 730)
        self.y = random.randint(50, 530)
        self.r = random.randint(20, 50)
        self.color = RED

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = random.randint(600, 780)
        self.y = random.randint(300, 550)
        self.r = random.randint(35, 40)
        self.color = RED
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

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target1 = Target1(screen)
target2 = Target2(screen)
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    screen.blit(pygame.font.SysFont('Verdana', 40).render(str(score), False, (0, 0, 0)), (30, 20))
    screen.blit(
            pygame.font.SysFont('Verdana', 20).render('Использовано шаров: ' + str(len(balls)), False, (0, 0, 0)),
            (200, 40))
    target1.draw()
    target2.draw()
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move()
        if b.hittest(target1) and target1.live:
            target1.live = 0
            target1.hit()
            target1.new_target()

            balls = []
            score +=1
        if b.hittest(target2) and target2.live:
            target2.live = 0
            target2.hit()
            target2.new_target()

            balls = []
            score += 1
    gun.power_up()

pygame.quit()