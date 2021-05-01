import math
from random import randrange

import pygame
from pygame import Rect

from config import Color, Screen
from models import Ball, Paddle, Brick

pygame.init()

screen = pygame.display.set_mode((Screen.WIDTH, Screen.HEIGHT))
pygame.display.set_caption('2D Brick Breaker')
pygame.mixer.music.load('resources/music/background.wav')
pygame.mixer.music.play(-1)
fx1 = pygame.mixer.Sound('resources/fx/fx1.wav')
fx2 = pygame.mixer.Sound('resources/fx/fx2.wav')
fx3 = pygame.mixer.Sound('resources/fx/fx3.wav')
fxs = [fx1, fx2, fx3]
clock = pygame.time.Clock()

background_image = pygame.image.load('resources/img/background.jpg')
ball = Ball(Screen.WIDTH / 2 - 100, Screen.HEIGHT - 250, 15, Color.WHITE, [0, 5])
paddle = Paddle(Screen.WIDTH / 2 - 100, Screen.HEIGHT - 30, 200, 20, Color.PINK, None)
bricks = [Brick(i * 160 + 5, j * 40 + 5, 150, 30, Color.BLACK) for i in range(5) for j in range(5)]

running = True


def draw_window():
    screen.blit(background_image, (0, 0))
    ball.draw(screen)
    paddle.draw(screen)
    for brick in bricks:
        brick.draw(screen)

    pygame.display.update()
    pygame.display.flip()
    clock.tick(Screen.FPS)


def check_angle(x1, x2):
    center = [x2 - 10, x2 + 10]
    small_dist = [x2 - 50, x2 + 50]

    if center[0] < x1 < center[1]:
        return 0
    elif small_dist[0] < x1 <= center[0]:
        return 7
    elif small_dist[1] <= x1 < center[1]:
        return -7
    else:
        return 15


while running:

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                paddle.moving_left = True
            elif event.key == pygame.K_d:
                paddle.moving_right = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                paddle.moving_left = False
            elif event.key == pygame.K_d:
                paddle.moving_right = False

    # checking extremes and inverse speed
    if ball.right >= Screen.WIDTH or ball.left <= 0:
        ball.inverse_speed_x()
    elif ball.top >= Screen.HEIGHT or ball.bottom <= 0:
        ball.inverse_speed_y()

    if paddle.right >= Screen.WIDTH:
        paddle.move(-15, 0)
    elif paddle.left <= 0:
        paddle.move(15, 0)

    if ball.rect.colliderect(paddle):
        speed_x = check_angle(ball.center_x, paddle.center_x)
        if speed_x == 0:
            ball.inverse_speed_x()
        else:
            ball.speed[0] = speed_x
        ball.inverse_speed_y()

    for brick in bricks:
        if ball.rect.colliderect(brick):
            ball.inverse_speed_y()
            fxs[randrange(0, len(fxs))].play()
            bricks.remove(brick)

    # updating objects
    ball.update()
    paddle.update()
    for brick in bricks:
        brick.update()

    # render window
    draw_window()
