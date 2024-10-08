import pygame
import os
import random
pygame.font.init()
pygame.mixer.init()

pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo do Pinho")
FPS = 60

BROWN = (75,0,0)

BULLETSCOUNT_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsansa', 100)

BORDER = pygame.Rect((WIDTH//2)-5, 0, 10, HEIGHT)


pygame.mixer.music.load(os.path.join('Assets', 'music.mp3'))
pygame.mixer.music.set_volume(0.8)
HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'death-sound.mp3'))
FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'gun-shot.mp3'))
LOAD_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'gun-load.mp3'))
DASH_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'dash-sound.mp3'))
FIRE_SOUND.set_volume(0.3)
LOAD_SOUND.set_volume(0.8)
DASH_SOUND.set_volume(1.5)

BULLET_VEL = 50
MAX_BULLETS = 6

RED_HIT = pygame.USEREVENT + 1
BLUE_HIT = pygame.USEREVENT + 2
RED_RELOAD = pygame.USEREVENT + 3
BLUE_RELOAD = pygame.USEREVENT + 4
RED_DASH_RELOAD = pygame.USEREVENT + 5
BLUE_DASH_RELOAD = pygame.USEREVENT + 6
AMMO_SPAWN = pygame.USEREVENT + 7

VEL = 2     # int pls
DASH = VEL * 20
DASH_RELOAD_TIME = 5000

COWBOY_WIDTH, COWBOY_HEIGHT = 50, 60

COWBOY_RED_IMAGE = pygame.image.load(os.path.join('Assets', 'cowboy.png'))
COWBOY_RED = pygame.transform.scale(COWBOY_RED_IMAGE, (COWBOY_WIDTH, COWBOY_HEIGHT))

COWBOY_BLUE = pygame.transform.flip(COWBOY_RED, True, False)    # Import blue cowboy image

BARREL_WIDTH, BARREL_HEIGHT = 60, 70
TABLE_WIDTH, TABLE_HEIGHT = 80, 60
AMMO_WIDTH, AMMO_HEIGHT = 25, 25
BULLET_WIDTH, BULLET_HEIGHT = 10, 5

BARREL_IMAGE = pygame.image.load(os.path.join('Assets', 'barrel.png'))
BARREL = pygame.transform.scale(BARREL_IMAGE, (BARREL_WIDTH, BARREL_HEIGHT))

TABLE_IMAGE = pygame.image.load(os.path.join('Assets', 'table.png'))
TABLE = pygame.transform.scale(TABLE_IMAGE, (TABLE_WIDTH, TABLE_HEIGHT))

AMMO_IMAGE = pygame.image.load(os.path.join('Assets', 'ammo.png'))
AMMO = pygame.transform.scale(AMMO_IMAGE, (AMMO_WIDTH, AMMO_HEIGHT))

BULLET_IMAGE = pygame.image.load(os.path.join('Assets', 'bullet.png'))
BULLET_RED = pygame.transform.scale(BULLET_IMAGE, (BULLET_WIDTH, BULLET_HEIGHT))
BULLET_BLUE = pygame.transform.flip(BULLET_RED, True, False)

AMMO_VEL = 4
AMMO_SPAWN_TIME = 6000

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'background.png')),(WIDTH, HEIGHT))

def draw_window(red, blue, bullets_red, bullets_blue, bulletscount_red, bulletscount_blue, barrel, table, ammo_list):
    WIN.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(WIN, BROWN, BORDER)
    WIN.blit(COWBOY_RED, (red.x, red.y))
    WIN.blit(COWBOY_BLUE, (blue.x, blue.y))
    WIN.blit(BARREL, (barrel.x, barrel.y))
    WIN.blit(TABLE, (table.x, table.y))

    bulletscount_red_text = BULLETSCOUNT_FONT.render("Bullets: " + str(bulletscount_blue), 1, (25,25,112))
    bulletscount_blue_text = BULLETSCOUNT_FONT.render("Bullets: " + str(bulletscount_red), 1, (178,34,34))
    WIN.blit(bulletscount_red_text, (WIDTH - bulletscount_red_text.get_width() - 10, 10))
    WIN.blit(bulletscount_blue_text, (10, 10))

    for bullet in bullets_red:
        WIN.blit(BULLET_RED, (bullet.x, bullet.y))

    for bullet in bullets_blue:
        WIN.blit(BULLET_BLUE, (bullet.x, bullet.y))

    for ammo in ammo_list:
        WIN.blit(AMMO, (ammo['rect'].x, ammo['rect'].y))

    pygame.display.update()


def collision_test_red(keys_pressed, player, obj):
    if player.colliderect(obj):
        if keys_pressed[pygame.K_a]:
            player.x += VEL
        if keys_pressed[pygame.K_d]:
            player.x -= VEL
        if keys_pressed[pygame.K_w]:
            player.y += VEL
        if keys_pressed[pygame.K_s]:
            player.y -= VEL


def collision_test_blue(keys_pressed, player, obj):
    if player.colliderect(obj):
        if keys_pressed[pygame.K_LEFT]:
            player.x += VEL
        if keys_pressed[pygame.K_RIGHT]:
            player.x -= VEL
        if keys_pressed[pygame.K_UP]:
            player.y += VEL
        if keys_pressed[pygame.K_DOWN]:
            player.y -= VEL


def red_movement(keys_pressed, red, *args):
        if keys_pressed[pygame.K_a] and (red.x-VEL) > 0:
            red.x -= VEL
        if keys_pressed[pygame.K_d] and (red.x-VEL) < (BORDER.x - COWBOY_WIDTH):
            red.x += VEL
        if keys_pressed[pygame.K_w] and (red.y-VEL) > 0:
            red.y -= VEL
        if keys_pressed[pygame.K_s] and (red.y-VEL) < (HEIGHT - COWBOY_HEIGHT - 5):
            red.y += VEL

        for obj in args:
            collision_test_red(keys_pressed, red, obj)  # This collision test feels good but probably isn't really

def blue_movement(keys_pressed, blue, *args):
        if keys_pressed[pygame.K_LEFT] and (blue.x+VEL) > (BORDER.x + BORDER.width):
            blue.x -= VEL
        if keys_pressed[pygame.K_RIGHT] and (blue.x-VEL) < (WIDTH - COWBOY_WIDTH):
            blue.x += VEL
        if keys_pressed[pygame.K_UP] and (blue.y-VEL) > 0:
            blue.y -= VEL
        if keys_pressed[pygame.K_DOWN] and (blue.y-VEL) < (HEIGHT - COWBOY_HEIGHT - 5):
            blue.y += VEL

        for obj in args:
            collision_test_blue(keys_pressed, blue, obj)    

def red_dash(keys_pressed, red, barrel, table):

    if keys_pressed[pygame.K_w]:
        if (red.y-DASH) > 0:
            red.y -= DASH
        else:
            red.y = 0

        if red.colliderect(barrel):
            red.y = barrel.y + BARREL_HEIGHT    # This is terrible
        if red.colliderect(table):
            red.y = table.y + TABLE_HEIGHT

    elif keys_pressed[pygame.K_s]:
        if (red.y+DASH) < (HEIGHT - COWBOY_HEIGHT - 5):
            red.y += BARREL_HEIGHT 
        else:
            red.y = (HEIGHT - COWBOY_HEIGHT - 5)

        if red.colliderect(barrel):
            red.y = barrel.y - COWBOY_HEIGHT
        if red.colliderect(table):
            red.y = table.y - COWBOY_HEIGHT

    elif keys_pressed[pygame.K_a]:
        if (red.x-DASH) > 0:
            red.x -= DASH
        else:
            red.x = 0

        if red.colliderect(barrel):
            red.x = barrel.x + BARREL_WIDTH
        if red.colliderect(table):
            red.x = table.x + TABLE_WIDTH       
    
    elif keys_pressed[pygame.K_d]:
        if (red.x+DASH) < (BORDER.x - COWBOY_WIDTH):
            red.x += DASH
        else:
            red.x = (BORDER.x - COWBOY_WIDTH)

        if red.colliderect(barrel):
            red.x = barrel.x - COWBOY_WIDTH
        if red.colliderect(table):
            red.x = table.x - COWBOY_WIDTH


def blue_dash(keys_pressed, blue, barrel, table):

    if keys_pressed[pygame.K_UP]:
        if (blue.y-DASH) > 0:
            blue.y -= DASH
        else:
            blue.y = 0

        if blue.colliderect(barrel):
            blue.y = barrel.y + BARREL_HEIGHT
        if blue.colliderect(table):
            blue.y = table.y + TABLE_HEIGHT

    elif keys_pressed[pygame.K_DOWN]:
        if (blue.y+DASH) < (HEIGHT - COWBOY_HEIGHT - 5):
            blue.y += DASH 
        else:
            blue.y = (HEIGHT - COWBOY_HEIGHT - 5)

        if blue.colliderect(barrel):
            blue.y = barrel.y - COWBOY_HEIGHT
        if blue.colliderect(table):
            blue.y = table.y - COWBOY_HEIGHT

    elif keys_pressed[pygame.K_LEFT]:
        if (blue.x-DASH) > (BORDER.x + BORDER.width):
            blue.x -= DASH
        else:
            blue.x = (BORDER.x + BORDER.width)

        if blue.colliderect(barrel):
            blue.x = barrel.x + BARREL_WIDTH
        if blue.colliderect(table):
            blue.x = table.x + TABLE_WIDTH
    
    elif keys_pressed[pygame.K_RIGHT]:
        if (blue.x+DASH) < (WIDTH - COWBOY_WIDTH):
            blue.x += DASH
        else:
            blue.x = (WIDTH - COWBOY_WIDTH)

        if blue.colliderect(barrel):
            blue.x = barrel.x - COWBOY_WIDTH
        if blue.colliderect(table):
            blue.x = table.x - COWBOY_WIDTH


def bullet_movement(red_bullets, blue_bullets, red, blue, barrel, table):
    for bullet in red_bullets:
        bullet.x += BULLET_VEL
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            red_bullets.remove(bullet)
        elif barrel.colliderect(bullet) or table.colliderect(bullet) or bullet.x > WIDTH:
            red_bullets.remove(bullet)

    for bullet in blue_bullets:
        bullet.x -= BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            blue_bullets.remove(bullet)
        elif barrel.colliderect(bullet) or table.colliderect(bullet) or bullet.x < 0:
            blue_bullets.remove(bullet)


def ammo_movement(ammo_list, red, blue):

    for ammo in ammo_list:
    
        ammo['rect'].x += ammo['vel_x']
        ammo['rect'].y += ammo['vel_y']

        if ammo['rect'].x <= 0 or ammo['rect'].x >= WIDTH:
            ammo['vel_x'] = -ammo['vel_x']
        if ammo['rect'].y <= 0 or ammo['rect'].y >= HEIGHT:
            ammo['vel_y'] = -ammo['vel_y']

        if red.colliderect(ammo['rect']):
            pygame.event.post(pygame.event.Event(RED_RELOAD))
            ammo_list.remove(ammo)

        if blue.colliderect(ammo['rect']):
            pygame.event.post(pygame.event.Event(BLUE_RELOAD))
            ammo_list.remove(ammo)

def draw_winner(text):
    if text == "Red wins!":
        draw_text = WINNER_FONT.render(text, 1, (178,34,34))
    if text == "Blue wins!":
        draw_text = WINNER_FONT.render(text, 1, (25,25,112))
    WIN.blit(draw_text, 
             (WIDTH//2 - draw_text.get_width()//2,
             HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():

    red = pygame.Rect( 100, 100, COWBOY_WIDTH, COWBOY_HEIGHT)
    blue = pygame.Rect(WIDTH - 100, HEIGHT - 100, COWBOY_WIDTH, COWBOY_HEIGHT)

    barrelx = random.randrange(150 + COWBOY_WIDTH, WIDTH - COWBOY_WIDTH - 150)
    barrely = random.randrange(150 + COWBOY_HEIGHT, HEIGHT - COWBOY_HEIGHT - 150)
    barrel = pygame.Rect(barrelx, barrely, BARREL_WIDTH, BARREL_HEIGHT)

    if barrelx > BORDER.x:
        tablex = random.randrange(150 + COWBOY_WIDTH, BORDER.x - TABLE_WIDTH)
    else:
        tablex = random.randrange(BORDER.x + TABLE_WIDTH, WIDTH - COWBOY_WIDTH - 150)
    tabley = random.randrange(150 + COWBOY_HEIGHT, HEIGHT - COWBOY_HEIGHT - 150)
    table = pygame.Rect(tablex, tabley, TABLE_WIDTH, TABLE_HEIGHT)

    ammo_list = []
    pygame.time.set_timer(AMMO_SPAWN, AMMO_SPAWN_TIME)

    bullets_red = []
    bullets_blue = []
    bulletscount_red = 1
    bulletscount_blue = 1
    dashcount_red = 1
    dashcount_blue = 1

    pygame.mixer.music.play(loops=-1, fade_ms=0)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        winner_text= ""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and bulletscount_red > 0:
                     bullet = pygame.Rect((red.x + red.width), (red.y + red.height//2 - 2), BULLET_WIDTH, BULLET_HEIGHT) 
                     bullets_red.append(bullet)
                     bulletscount_red -= 1
                     FIRE_SOUND.play()

                if event.key == pygame.K_KP_ENTER and bulletscount_blue > 0:
                    bullet = pygame.Rect((blue.x), (blue.y + blue.height//2 - 2), BULLET_WIDTH, BULLET_HEIGHT) 
                    bullets_blue.append(bullet)
                    bulletscount_blue -= 1
                    FIRE_SOUND.play()

                if event.key == pygame.K_b and dashcount_red > 0:
                    red_dash(pygame.key.get_pressed(), red, barrel, table)
                    dashcount_red -= 1
                    pygame.time.set_timer(RED_DASH_RELOAD, DASH_RELOAD_TIME)
                    DASH_SOUND.play()

                if event.key == pygame.K_KP_3 and dashcount_blue > 0:
                    blue_dash(pygame.key.get_pressed(), blue, barrel, table)
                    dashcount_blue -= 1
                    pygame.time.set_timer(BLUE_DASH_RELOAD, DASH_RELOAD_TIME)
                    DASH_SOUND.play()
            
            if event.type == AMMO_SPAWN:
                ammo_x = random.randrange(0, WIDTH)
                ammo_y = random.randrange(0, HEIGHT)
                ammo = {'rect': pygame.Rect(ammo_x, ammo_y, AMMO_WIDTH, AMMO_HEIGHT),
                        'vel_x': AMMO_VEL,
                        'vel_y': AMMO_VEL}
                ammo_list.append(ammo)

            if event.type == RED_RELOAD:
                if bulletscount_red < MAX_BULLETS:
                    bulletscount_red += 1
                    LOAD_SOUND.play()
            
            if event.type == RED_DASH_RELOAD:
                dashcount_red = 1
                pygame.time.set_timer(RED_DASH_RELOAD, 0)

            if event.type == BLUE_RELOAD:
                if bulletscount_blue < MAX_BULLETS:
                    bulletscount_blue += 1
                    LOAD_SOUND.play()

            if event.type == BLUE_DASH_RELOAD:
                dashcount_blue = 1
                pygame.time.set_timer(BLUE_DASH_RELOAD, 0)

            if event.type == RED_HIT:
                HIT_SOUND.play()
                winner_text = "Blue wins!"

            if event.type == BLUE_HIT:
                HIT_SOUND.play()
                winner_text = "Red wins!"

        if winner_text:
            pygame.mixer.music.stop()
            pygame.time.set_timer(RED_RELOAD, 0)
            pygame.time.set_timer(BLUE_RELOAD, 0)
            draw_winner(winner_text)
            break
        
        keys_pressed = pygame.key.get_pressed()
        red_movement(keys_pressed, red, barrel, table)
        blue_movement(keys_pressed, blue, barrel, table)

        bullet_movement(bullets_red, bullets_blue, red, blue, barrel, table)

        ammo_movement(ammo_list, red, blue)
        
        draw_window(red, blue, bullets_red, bullets_blue, bulletscount_red, bulletscount_blue, barrel, table, ammo_list)

    main()


if __name__ == "__main__":
    main()