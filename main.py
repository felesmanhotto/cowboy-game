import pygame
import os
pygame.font.init()

pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo do Pinho")
FPS = 60

BROWN = (128,0,0)

BULLETSCOUNT_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsansa', 100)

BORDER = pygame.Rect((WIDTH//2)-5, 0, 10, HEIGHT)

BULLET_VEL = 30
BULLETS_MAX = 1

RED_HIT = pygame.USEREVENT + 1
BLUE_HIT = pygame.USEREVENT + 2
RED_RELOAD = pygame.USEREVENT + 3
BLUE_RELOAD = pygame.USEREVENT + 4
RED_DASH_RELOAD = pygame.USEREVENT + 5
BLUE_DASH_RELOAD = pygame.USEREVENT + 6

VEL = 4
DASH = VEL * 20
COWBOY_WIDTH, COWBOY_HEIGHT = 55, 60
RELOAD_TIME = 3000

COWBOY_RED_IMAGE = pygame.image.load(os.path.join('Assets', 'cowboy.png'))
COWBOY_RED = pygame.transform.scale(COWBOY_RED_IMAGE, (COWBOY_WIDTH, COWBOY_HEIGHT))

COWBOY_BLUE = pygame.transform.flip(COWBOY_RED, True, False)    # Import blue cowboy image

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'background.png')),(WIDTH, HEIGHT))

def draw_window(red, blue, bullets_red, bullets_blue, bulletscount_red, bulletscount_blue):
    WIN.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(WIN, BROWN, BORDER)
    WIN.blit(COWBOY_RED, (red.x, red.y))
    WIN.blit(COWBOY_BLUE, (blue.x, blue.y))

    bulletscount_red_text = BULLETSCOUNT_FONT.render("Bullets: " + str(bulletscount_blue), 1, (0, 0, 0))
    bulletscount_blue_text = BULLETSCOUNT_FONT.render("Bullets: " + str(bulletscount_red), 1, (0, 0, 0))
    WIN.blit(bulletscount_red_text, (WIDTH - bulletscount_red_text.get_width() - 10, 10))
    WIN.blit(bulletscount_blue_text, (10, 10))

    for bullet in bullets_red:
        pygame.draw.rect(WIN, (25, 25, 25), bullet)

    for bullet in bullets_blue:
            pygame.draw.rect(WIN, (25, 25, 25), bullet)

    pygame.display.update()


def red_movement(keys_pressed, red):
        if keys_pressed[pygame.K_a] and (red.x-VEL) > 0:
            red.x -= VEL
        if keys_pressed[pygame.K_d] and (red.x-VEL) < (BORDER.x - COWBOY_WIDTH):
            red.x += VEL
        if keys_pressed[pygame.K_w] and (red.y-VEL) > 0:
            red.y -= VEL
        if keys_pressed[pygame.K_s] and (red.y-VEL) < (HEIGHT - COWBOY_HEIGHT - 5):
            red.y += VEL                                                        # Not a good fix but works for this game                                  


def blue_movement(keys_pressed, blue):
        if keys_pressed[pygame.K_LEFT] and (blue.x+VEL) > (BORDER.x + BORDER.width):
            blue.x -= VEL
        if keys_pressed[pygame.K_RIGHT] and (blue.x-VEL) < (WIDTH - COWBOY_WIDTH):
            blue.x += VEL
        if keys_pressed[pygame.K_UP] and (blue.y-VEL) > 0:
            blue.y -= VEL
        if keys_pressed[pygame.K_DOWN] and (blue.y-VEL) < (HEIGHT - COWBOY_HEIGHT - 5):
            blue.y += VEL

def red_dash(keys_pressed, red):

    if keys_pressed[pygame.K_w]:
        if (red.y-DASH) > 0:
            red.y -= DASH
        else:
            red.y = 0

    elif keys_pressed[pygame.K_s]:
        if (red.y+DASH) < (HEIGHT - COWBOY_HEIGHT - 5):
            red.y += DASH 
        else:
            red.y = (HEIGHT - COWBOY_HEIGHT - 5)

    elif keys_pressed[pygame.K_a]:
        if (red.x-DASH) > 0:
            red.x -= DASH
        else:
            red.x = 0
    
    elif keys_pressed[pygame.K_d]:
        if (red.x+DASH) < (BORDER.x - COWBOY_WIDTH):
            red.x += DASH
        else:
            red.x = (BORDER.x - COWBOY_WIDTH)


def blue_dash(keys_pressed, blue):

    if keys_pressed[pygame.K_UP]:
        if (blue.y-DASH) > 0:
            blue.y -= DASH
        else:
            blue.y = 0

    elif keys_pressed[pygame.K_DOWN]:
        if (blue.y+DASH) < (HEIGHT - COWBOY_HEIGHT - 5):
            blue.y += DASH 
        else:
            blue.y = (HEIGHT - COWBOY_HEIGHT - 5)

    elif keys_pressed[pygame.K_LEFT]:
        if (blue.x-DASH) > (BORDER.x + BORDER.width):
            blue.x -= DASH
        else:
            blue.x = (BORDER.x + BORDER.width)
    
    elif keys_pressed[pygame.K_RIGHT]:
        if (blue.x+DASH) < (WIDTH - COWBOY_WIDTH):
            blue.x += DASH
        else:
            blue.x = (WIDTH - COWBOY_WIDTH)


def bullet_movement(red_bullets, blue_bullets, red, blue):
    for bullet in red_bullets:
        bullet.x += BULLET_VEL
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            red_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)

    for bullet in blue_bullets:
        bullet.x -= BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            blue_bullets.remove(bullet)
        elif bullet.x < 0:
            blue_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, (0, 0, 0))
    WIN.blit(draw_text, 
             (WIDTH//2 - draw_text.get_width()//2,
             HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():

    red = pygame.Rect(200, 200, COWBOY_WIDTH, COWBOY_HEIGHT)
    blue = pygame.Rect(600, 200, COWBOY_WIDTH, COWBOY_HEIGHT)

    bullets_red = []
    bullets_blue = []
    bulletscount_red = 1
    bulletscount_blue = 1
    dashcount_red = 1
    dashcount_blue = 1

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(bullets_red) < BULLETS_MAX and bulletscount_red > 0:
                     bullet = pygame.Rect((red.x + red.width), (red.y + red.height//2 - 2), 10, 5) 
                     bullets_red.append(bullet)
                     bulletscount_red -= 1
                     pygame.time.set_timer(RED_RELOAD, RELOAD_TIME)


                if event.key == pygame.K_KP_ENTER and len(bullets_blue) < BULLETS_MAX and bulletscount_blue > 0:
                    bullet = pygame.Rect((blue.x), (blue.y + blue.height//2 - 2), 10, 5) 
                    bullets_blue.append(bullet)
                    bulletscount_blue -= 1
                    pygame.time.set_timer(BLUE_RELOAD, RELOAD_TIME)

                if event.key == pygame.K_b and dashcount_red > 0:
                    red_dash(pygame.key.get_pressed(), red)
                    dashcount_red -= 1
                    pygame.time.set_timer(RED_DASH_RELOAD, RELOAD_TIME)

                if event.key == pygame.K_KP_3 and dashcount_blue > 0:
                    blue_dash(pygame.key.get_pressed(), blue)
                    dashcount_blue -= 1
                    pygame.time.set_timer(BLUE_DASH_RELOAD, RELOAD_TIME)
                
            if event.type == RED_RELOAD:
                bulletscount_red += 1
                pygame.time.set_timer(RED_RELOAD, 0)
            
            if event.type == RED_DASH_RELOAD:
                dashcount_red = 1
                pygame.time.set_timer(RED_DASH_RELOAD, 0)

            if event.type == BLUE_RELOAD:
                bulletscount_blue += 1
                pygame.time.set_timer(BLUE_RELOAD, 0)

            if event.type == BLUE_DASH_RELOAD:
                dashcount_blue = 1
                pygame.time.set_timer(BLUE_DASH_RELOAD, 0)

        winner_text= ""
        if event.type == RED_HIT:
            winner_text = "Blue wins!"

        if event.type == BLUE_HIT:
            winner_text = "Red wins!"

        if winner_text:
            pygame.time.set_timer(RED_RELOAD, 0)
            pygame.time.set_timer(BLUE_RELOAD, 0)
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        red_movement(keys_pressed, red)
        blue_movement(keys_pressed, blue)

        bullet_movement(bullets_red, bullets_blue, red, blue)
        
        draw_window(red, blue, bullets_red, bullets_blue, bulletscount_red, bulletscount_blue)

    main()


if __name__ == "__main__":
    main()