import math
import random
import pygame

class Ball:
    def __init__(self, x, y, size, speed, max_speed=None):
        self.rect = pygame.Rect(x, y, size, size)
        self.base_speed = speed
        self.speed = speed
        # set max speed (configurable)
        self.max_speed = max_speed if max_speed is not None else speed * 1.5

        # random starting direction
        self.dx = random.choice([-1, 1]) * speed
        self.dy = random.choice([-1, 1]) * speed
    
    def move(self):
        # enforce max speed on the actual velocity vector
        current = math.hypot(self.dx, self.dy)
        if current > self.max_speed:
            scale = self.max_speed / current
            self.dx *= scale
            self.dy *= scale
            self.speed = self.max_speed

        self.rect.x += self.dx
        self.rect.y += self.dy
        
    def draw(self, screen):
        pygame.draw.ellipse(screen, (255, 255, 255), self.rect)
        
    def bounce_y(self):
        self.dy *= -1
        
    def bounce_paddle(self, paddle):
        # calculate relative intersection
        ball_center = self.rect.centery
        paddle_center = paddle.rect.centery
        distance = ball_center - paddle_center

        normalized = distance / (paddle.rect.height / 2)

        # max bounce angle (in radians)
        max_angle = math.radians(60)

        bounce_angle = normalized * max_angle

        direction = -1 if self.dx > 0 else 1

        self.speed *= 1.05  # small speed increase

        # cap speed so it never exceeds max_speed
        if self.speed > self.max_speed:
            self.speed = self.max_speed

        self.dx = direction * self.speed * math.cos(bounce_angle)
        self.dy = self.speed * math.sin(bounce_angle)