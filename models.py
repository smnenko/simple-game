import pygame
from pygame.sprite import Sprite
from pygame import Rect


class GameObject(Sprite):
    def __init__(self, x, y, w, h, speed=(0, 0)):
        Sprite.__init__(self)
        self.rect = Rect(x, y, w, h)
        self.speed = speed

    @property
    def left(self):
        return self.rect.left

    @property
    def right(self):
        return self.rect.right

    @property
    def top(self):
        return self.rect.top

    @property
    def bottom(self):
        return self.rect.bottom

    @property
    def height(self):
        return self.rect.height

    @property
    def width(self):
        return self.rect.width

    @property
    def center_x(self):
        return self.rect.centerx

    @property
    def center_y(self):
        return self.rect.centery

    def draw(self, surface):
        pass

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        if self.speed == [0, 0]:
            return

        self.move(*self.speed)


class Brick(GameObject):
    def __init__(self, x, y, w, h, color, special_effect=None):
        GameObject.__init__(self, x, y, w, h)
        self.color = color
        self.special_effect = special_effect

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


class Paddle(GameObject):
    def __init__(self, x, y, w, h, color, offset):
        GameObject.__init__(self, x, y, w, h)
        self.color = color
        self.offset = offset
        self.moving_left = False
        self.moving_right = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def update(self):
        if self.moving_right:
            self.move(15, 0)
        elif self.moving_left:
            self.move(-15, 0)


class Ball(GameObject):
    def __init__(self, x, y, r, color, speed):
        GameObject.__init__(self, x - r, y - r, r * 2, r * 2, speed)
        self.radius = r
        self.diameter = r * 2
        self.color = color

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.center_x, self.center_y), self.radius)

    def inverse_speed_x(self):
        self.speed[0] *= -1

    def inverse_speed_y(self):
        self.speed[1] *= -1
