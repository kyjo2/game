import random
import numpy as np
from django.utils.translation import gettext_lazy as _
from numpy.linalg import norm



class Bar:
    width: float
    height: float
    map_width: float
    map_height: float
    x: float
    y: float

    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def _up(self):
        self.y = self.y - self.height / 10
        if self.y < 0:
            self.y = 0

    def _down(self):
        self.y = self.y + self.height / 10
        if self.y > 3 * self.height:
            self.y = 3 * self.height

    def _left(self):
        self.x = self.x - self.width / 10
        if self.x < 0:
            self.x = 0

    def _right(self):
        self.x = self.x + self.width / 10
        if self.x > 3 * self.width:
            self.x = 3 * self.width

class Player:
    score: int
    bar: Bar

    def __init__(self, bar: Bar):
        self.score = 0
        self.bar = bar


class Map:
    width: float
    height: float

    def __init__(self, width, height):
        self.width = width
        self.height = height


class Ball:
    radius: float
    x: float
    y: float
    speed: float
    direction: tuple

    def __init__(self, x, y):
        self.radius = 10
        self.x = x
        self.y = y
        self.speed = 30
        self.direction = (self.random_dir(), random.uniform(-1, 1))

    def move(self):
        self.x += self.speed * self.direction[0]
        self.y += self.speed * self.direction[1]

    def hit_wall(self, map: Map):
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.bounce([1, -1])
        elif self.y + self.radius >= map.height:
            self.y = map.height - self.radius
            self.bounce([1, -1])
            
    def bounce(self, bounce_direction=tuple):
        self.direction = (self.direction[0] * bounce_direction[0], self.direction[1] * bounce_direction[1])
        correction = random.uniform(0.9, 1.1)
        self.direction = (self.direction[0] * correction, self.direction[1] * correction)
        self.adjust_ball_speed()

    def adjust_ball_speed(self):
        dir = np.array(self.direction)
        self.direction = tuple(dir / norm(dir))

    def reset(self, map: Map):

        self.x = map.width / 2
        self.y = map.height / 2
        self.direction = (self.random_dir(), self.random_dir())
        self.adjust_ball_speed()

    def random_dir(self):
        if random.choice([True, False]):
            return random.uniform(0.5, 0.9)
        else:
            return random.uniform(-0.9, -0.5)


class PingPongGame:
    left: Player
    right: Player
    up: Player
    down: Player
    map: Map
    ball: Ball
    finished: None

    def __init__(self, map_width, map_height):
 
        bar_long = map_height / 4
        bar_short = map_width / 80
        self.left = Player(Bar(bar_short, bar_long, 0, (map_height - bar_long) / 2))
        self.right = Player(Bar(bar_short, bar_long, map_width - bar_short, (map_height - bar_long) / 2))
        self.up = Player(Bar(bar_long, bar_short, (map_width - bar_long) / 2, 0))
        self.down = Player(Bar(bar_long, bar_short, (map_width - bar_long) / 2, map_height - bar_short))
        self.map = Map(map_width, map_height)
        self.ball = Ball(map_width / 2, map_height / 2)
        self.finished = False
        self.started_at = None

    def plus_score(self, str):

        if str == 'left_win':
            self.left.score += 1
        elif str == 'right_win':
            self.right.score += 1
        elif str == 'up_win':
            self.up.score += 1
        elif str == 'down_win':
            self.down.score += 1

    def is_right_win(self):
        left_point = self.ball.x - self.ball.radius

        if left_point <= self.left.bar.x + self.left.bar.width:
            if self.ball.y <= self.left.bar.y + self.left.bar.height and self.ball.y >= self.left.bar.y:
                self.ball.bounce([-1, 1])
                return False
            else:
                return True
            
    def is_left_win(self):
        right_point = self.ball.x + self.ball.radius

        if right_point >= self.right.bar.x:
            if self.ball.y <= self.right.bar.y + self.right.bar.height and self.ball.y >= self.right.bar.y:
                self.ball.bounce([-1, 1])
                return False
            else:
                return True
            
    def is_down_win(self):
        up_point = self.ball.y - self.ball.radius

        if up_point <= self.up.bar.y + self.up.bar.height:
            if self.ball.x <= self.left.bar.x + self.left.bar.width and self.ball.x >= self.left.bar.x:
                self.ball.bounce([1, -1])
                return False
            else:
                return True
            
    def is_up_win(self):
        down_point = self.ball.y + self.ball.radius

        if down_point >= self.down.bar.y:
            if self.ball.x <= self.down.bar.x + self.down.bar.width and self.ball.x >= self.right.bar.x:
                self.ball.bounce([1, -1])
                return False
            else:
                return True