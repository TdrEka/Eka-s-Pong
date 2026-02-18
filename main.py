import pygame
import sys 
from paddle import Paddle
from ball import Ball

pygame.init()

left_score = 0
right_score = 0

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Eka's Pong")

clock = pygame.time.Clock()
fps = 60

running = True

left_paddle = Paddle(50, HEIGHT//2 - 50, 10, 100)
right_paddle = Paddle(WIDTH - 60, HEIGHT//2 - 50, 10, 100)
ball = Ball(WIDTH//2 - 10, HEIGHT//2 - 10, 20, 5)
font = pygame.font.SysFont(None, 60)

ai_reaction_timer = 0
ai_reaction_delay = 0.5

game_state = "menu"

while running:
    clock.tick(fps)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        left_paddle.move(up=True)
    if keys[pygame.K_s]:
        left_paddle.move(up=False)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_state == "menu":
                game_state = "playing"
    
    if game_state == "playing":
        ball.move()
        if ball.dx > 0:  # only track if ball coming right
            ai_reaction_timer += 1

        if ai_reaction_timer >= ai_reaction_delay:
            if ball.rect.centery < right_paddle.rect.centery:
                right_paddle.move(up=True)
            elif ball.rect.centery > right_paddle.rect.centery:
                right_paddle.move(up=False)
    
            ai_reaction_timer = 0
    
    
    if ball.rect.colliderect(left_paddle.rect):
        ball.rect.left = left_paddle.rect.right
        ball.bounce_paddle(left_paddle)

    if ball.rect.colliderect(right_paddle.rect):
        ball.rect.right = right_paddle.rect.left
        ball.bounce_paddle(right_paddle)

    # top/bottom wall collision
    if ball.rect.top <= 0:
        ball.rect.top = 0
        ball.bounce_y()
    if ball.rect.bottom >= HEIGHT:
        ball.rect.bottom = HEIGHT
        ball.bounce_y()
    
    if ball.rect.left <= 0:
        right_score += 1
        ball.rect.center = (WIDTH//2, HEIGHT//2)
        ball.dx *= -1
    if ball.rect.right >= WIDTH:
        left_score += 1
        ball.rect.center = (WIDTH//2, HEIGHT//2)
        ball.dx *= -1
    
    screen.fill((0, 0, 0))
    left_paddle.draw(screen)
    right_paddle.draw(screen)
    ball.draw(screen)
    left_text = font.render(str(left_score), True, (255, 255, 255))
    right_text = font.render(str(right_score), True, (255, 255, 255))
    screen.blit(left_text, (WIDTH//4, 20))
    screen.blit(right_text, (WIDTH*3//4, 20))
    if game_state == "menu":
        menu_text = font.render("Press SPACE to Start", True, (255, 255, 255))
        screen.blit(menu_text, (WIDTH//2 - menu_text.get_width()//2, HEIGHT//2 - menu_text.get_height()//2))
    pygame.display.flip()
pygame.quit()
sys.exit()