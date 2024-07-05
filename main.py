import pygame
import os

pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo do Pinho")
FPS = 60

BORDER = pygame.Rect((WIDTH//2)-5, 0, 10, HEIGHT)

BULLET_VEL = 30
BULLETS_MAX = 1

RED_HIT = pygame.USEREVENT + 1
BLUE_HIT = pygame.USEREVENT + 2

VEL = 4
DASH = VEL * 20
COWBOY_WIDTH, COWBOY_HEIGHT = 55, 60

COWBOY_RED_IMAGE = pygame.image.load(os.path.join('Assets', 'cowboy.png'))
COWBOY_RED = pygame.transform.scale(COWBOY_RED_IMAGE, (COWBOY_WIDTH, COWBOY_HEIGHT))

COWBOY_BLUE = pygame.transform.flip(COWBOY_RED, True, False)    # Import blue cowboy image

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'background.png')),(WIDTH, HEIGHT))

def draw_window(red, blue, bullets):
    WIN.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(WIN, (0, 0, 0), BORDER)
    WIN.blit(COWBOY_RED, (red.x, red.y))
    WIN.blit(COWBOY_BLUE, (blue.x, blue.y))

    for bullet in bullets:
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


def main():

    red = pygame.Rect(200, 200, COWBOY_WIDTH, COWBOY_HEIGHT)
    blue = pygame.Rect(600, 200, COWBOY_WIDTH, COWBOY_HEIGHT)

    bullets_red = []
    bullets_blue = []

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(bullets_red) < BULLETS_MAX:
                     bullet = pygame.Rect((red.x + red.width), (red.y + red.height//2 - 2), 10, 5) 
                     bullets_red.append(bullet)

                if event.key == pygame.K_KP_ENTER and len(bullets_blue) < BULLETS_MAX:
                    bullet = pygame.Rect((blue.x), (blue.y + blue.height//2 - 2), 10, 5) 
                    bullets_blue.append(bullet)

                if event.key == pygame.K_b:
                    red_dash(pygame.key.get_pressed(), red)

                if event.key == pygame.K_KP_3:
                    blue_dash(pygame.key.get_pressed(), blue)

        winner_text= ""
        if event.type == RED_HIT:
            winner_text = "Blue wins!"

        if event.type == BLUE_HIT:
            winner_text = "Red wins!"

        if winner_text:
            pass # Game ends

        keys_pressed = pygame.key.get_pressed()
        red_movement(keys_pressed, red)
        blue_movement(keys_pressed, blue)

        bullet_movement(bullets_red, bullets_blue, red, blue)
        
        draw_window(red, blue, (bullets_red + bullets_blue))

    pygame.quit()


if __name__ == "__main__":
    main()