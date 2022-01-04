import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BULLET_HIT_SOUND = pygame.mixer.Sound('Data/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Data/Gun+Silencer.mp3')

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

HEALTH_FONT = pygame.font.SysFont('comicsans', 20)
ROUND_FONT = pygame.font.SysFont('comicsans', 10)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SHIELD = pygame.USEREVENT + 3
RED_SHIELD = pygame.USEREVENT + 4

FPS = 60

VEL = 3
BULLET_VEL = 11

MAX_BULLETS = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Data', 'space.png')), (WIDTH, HEIGHT))

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Data', 'spaceship_red.png'))

RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Data', 'spaceship_yellow.png'))

YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, red_heal, yellow_heal,
                yellow_won, red_won):
    WIN.blit(SPACE, (0, 0))

    draw_round(yellow_won, red_won)

    pygame.draw.rect(WIN, RED, BORDER)

    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), True, WHITE)

    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), True, WHITE)

    red_heal_text = HEALTH_FONT.render(
        "Heal: " + str(red_heal), True, WHITE)

    yellow_heal_text = HEALTH_FONT.render(
        "Heal: " + str(yellow_heal), True, WHITE)

    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))

    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(yellow_heal_text, (10, 60))

    WIN.blit(red_heal_text, (WIDTH - red_health_text.get_width() - 10, 60))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    pygame.display.update()


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:
        red.x -= VEL

    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:
        red.x += VEL

    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:
        red.y -= VEL

    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:
        red.y += VEL


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:
        yellow.x -= VEL

    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:
        yellow.x += VEL

    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:
        yellow.y -= VEL
        
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:
        yellow.y += VEL


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, True, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def draw_round(yellow_won, red_won):
    red_round_text = ROUND_FONT.render(
        str(red_won), True, WHITE)

    yellow_round_text = ROUND_FONT.render(
        str(yellow_won), True, WHITE)

    WIN.blit(red_round_text, (WIDTH // 2 - 30, 10))

    WIN.blit(yellow_round_text, (WIDTH // 2 + 20, 10))


def yellow_shield(yellow_shield_uses):
    if yellow_shield_uses != 0:
        pygame.event.post(pygame.event.Event(YELLOW_SHIELD))
        pygame.time.set_timer(YELLOW_SHIELD, 1000)


def red_shield(red_shield_uses):
    if red_shield_uses != 0:
        pygame.event.post(pygame.event.Event(RED_SHIELD))
        pygame.time.set_timer(RED_SHIELD, 1000)


def yellow_handle_bullets(yellow_bullets, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)


def red_handle_bullets(red_bullets, yellow):
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def main():
    red_shield_uses = 1

    yellow_shield_uses = 1

    yellow_won = 0
    red_won = 0

    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    yellow_heal = 3
    red_heal = 3

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        draw_round(yellow_won, red_won)
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height // 2 - 2, 10, 5)

                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)

                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_DELETE:
                    if red_heal != 0:
                        if red_health != 10:
                            if red_health < 7:
                                red_health += 3

                                red_heal -= 1
                            else:
                                red_health = 10

                                red_heal -= 1

                if event.key == pygame.K_TAB:
                    if yellow_heal != 0:
                        if yellow_health != 10:
                            if yellow_health < 7:
                                yellow_health += 3

                                yellow_heal -= 1
                            else:
                                yellow_health = 10

                                yellow_heal -= 1

                if event.key == pygame.K_CAPSLOCK:
                    yellow_shield(yellow_shield_uses)

                if event.key == pygame.K_END:
                    red_shield(red_shield_uses)

            if event.type == YELLOW_HIT:
                if event.type != YELLOW_SHIELD:
                    yellow_health -= 1
                    BULLET_HIT_SOUND.play()

            if event.type == RED_HIT:
                if event.type != RED_SHIELD:
                    red_health -= 1
                    BULLET_HIT_SOUND.play()

        winner_text = ''

        if red_health <= 0:
            if red_won >= 2:
                yellow_won += 1
                draw_round(yellow_won + 1, red_won)
                winner_text = 'Yellow Wins!'
            else:
                red_won += 1
                red_health = 10
                red_heal = 3

                draw_round(yellow_won, red_won)

        if yellow_health <= 0:
            if yellow_won >= 2:
                red_won += 1
                draw_round(yellow_won, red_won + 1)
                winner_text = 'Red Wins!'
            else:
                yellow_won += 1
                yellow_health = 10
                yellow_heal = 3

                draw_round(yellow_won, red_won)

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()

        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        red_handle_bullets(red_bullets, yellow)
        yellow_handle_bullets(yellow_bullets, red)

        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health, red_heal, yellow_heal, yellow_won, red_won)
        WIN.fill((0, 0, 0))

    main()


if __name__ == "__main__":
    main()
