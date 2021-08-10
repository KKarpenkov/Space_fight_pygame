import pygame
import os
pygame.font.init()

#Переменные
WIDTH, HEIGHT = 900,500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space fight')
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
FPS = 60
VEL = 5
BULLET_VEL = 10
HP_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
MAX_BULLETS = 10
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
YELLOW_HIT = pygame.USEREVENT + 1 
RED_HIT = pygame.USEREVENT + 2

#Привязываю файлы дизайна
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

#Отрисовка
def draw_window(red, yellow, red_bullets, yellow_bullets, red_hp, yellow_hp):
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    
    red_hp_text = HP_FONT.render('Health: ' + str(red_hp), 1, WHITE)
    yellow_hp_text = HP_FONT.render('Health: ' + str(yellow_hp), 1, WHITE)
    WIN.blit(red_hp_text, (WIDTH - red_hp_text.get_width() - 10, 10))
    WIN.blit(yellow_hp_text, (10, 10))
    
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet) 
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet) 

    pygame.display.update()

#Движение кораблей
def yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: #left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: #right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: #up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 10: #down
        yellow.y += VEL  

def red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: #left
        red.x -= VEL    
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: #right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: #up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 10: #down
        red.y += VEL 

#Пули
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay (5000)


def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []
    red_hp = 10
    yellow_hp = 10
    
    clock = pygame.time.Clock()
    
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
            
            if event.type == RED_HIT:
                red_hp -= 1
            if event.type == YELLOW_HIT:
                yellow_hp -= 1

        winner_text = ''
        if red_hp <= 0:
            winner_text = 'Yellow wins'
        if yellow_hp <= 0:  
            winner_text = 'Red wins'
                
        if winner_text != '':
            draw_winner(winner_text)         
            break
        
        keys_pressed = pygame.key.get_pressed()
        yellow_movement(keys_pressed, yellow) 
        red_movement(keys_pressed, red)    
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_hp, yellow_hp)
    
    main()

if __name__ == '__main__':
    main()