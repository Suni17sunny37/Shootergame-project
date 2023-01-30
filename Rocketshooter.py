import pygame
import random
import math

# initilize
pygame.init()
# screen visible
screen = pygame.display.set_mode((800, 600))
title = "SONE7"
# title
pygame.display.set_caption(title)
# logo
logo = pygame.image.load('data\shortcut-script-app.png')
pygame.display.set_icon(logo)
# score
score_font = pygame.font.Font('data/agrha.ttf', 32)
score_x = 10
score_y = 10
# restart game
restart_g = pygame.font.Font('data/agrha.ttf', 32)
restart_x = 60
restart_y = 300
# gamever
gameover_font = pygame.font.Font('data/agrha.ttf', 64)
gameover_x = 150
gameover_y = 200
# score
score = 0
# game status
game_status = 'running'
# game win
gamewin = pygame.font.Font('data/agrha.ttf', 64)
gamewin_x = 200
gamewin_y = 200
# background music
pygame.mixer.music.load('data/Komiku_-_07_-_Battle_of_Pogs.mp3')
pygame.mixer.music.play(-1)
# background image
bg = pygame.image.load('data/background.png')
# bullet sound
bullet_sound = pygame.mixer.Sound('data/heat-vision.mp3')
# explosion sound
explosion_sound = pygame.mixer.Sound('data/Explosion+9.Wav')
# player image
player_img = pygame.image.load('data/rocket.png')
player_x = 375
player_y = 510
player_xchange = 0

# enemy image
enemy_img = []
enemy_x = []
enemy_y = []
enemy_xchange = []
enemy_ychange = []
# Number of enemies
no_of_enemies = 10

for i in range(no_of_enemies):
    enemy_img.append(pygame.image.load('data/spaceship.png'))
    enemy_x.append(random.randint(0, 734))
    enemy_y.append(random.randint(25, 100))
    enemy_xchange.append(2)
    enemy_ychange.append(50)
g = 0
# bullet image
bullet_img = pygame.image.load('data/bullet (1).png')
bullet_x = 0
bullet_y = 510
bullet_ychange = -1
# bullet status
bullet_status = "ready"


# game win
def show_gamewin(x, y):
    gamewin_img = gamewin.render("GAME WIN ", True, (191, 176, 159))
    screen.blit(gamewin_img, (x, y))
    game_status = 'end'


# Method show_player
def show_player(x, y):
    screen.blit(x, y)


# Method show_score
def show_score(x, y):
    score_img = score_font.render("Score :" + str(score), True, (217, 217, 217))
    screen.blit(score_img, (x, y))


# Method show_gameover
def show_gameover(x, y):
    global game_status
    game_over = gameover_font.render("GAME OVER", True, (217, 217, 217))
    screen.blit(game_over, (x, y))
    game_status = 'end'


# Method show_enemy
def show_enemy(x, y, i):
    screen.blit(x, y)


# restart the game
def restart(x, y):
    restart_img = restart_g.render("To Restart The Game Press R", True, (0, 255, 183))
    screen.blit(restart_img, (x, y))


# collosion between player and enemy
def iscollide(x1, y1, x2, y2):
    dis = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
    if dis < 25:
        return True
    else:
        return False


# Method show_bullet
def show_bullet(x, y):
    screen.blit(x, y)


# window visible
game_window = True
while game_window:

    screen.fill((12, 34, 21))
    # screen blits the background image
    screen.blit(bg, (0, 0))
    # events
    for event in pygame.event.get():
        # window quit
        if event.type == pygame.QUIT:
            game_window = False
        # player moves left side
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_xchange = -1
            # player moves right side
            if event.key == pygame.K_RIGHT:
                player_xchange = 1
            # movements of the player
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                player_xchange = 0
            # player choose to restart the game
            if event.key == pygame.K_r:
                if game_status == 'end':
                    game_status = 'running'
                    player_x = 375
                    for i in range(no_of_enemies):
                        enemy_x[i] = random.randint(10, 734)
                        enemy_y[i] = random.randint(20, 100)
                    score = 0
                    pygame.mixer.music.play(-1)
            # bullets release when we are press space bar
            if event.key == pygame.K_SPACE:
                if bullet_status == "ready":
                    bullet_status = "fire"
                    bullet_x = player_x
                    show_bullet(bullet_img, (bullet_x + 10, bullet_y))
                    bullet_sound.play()

    # bullet movements
    if bullet_status == "fire":
        bullet_y += bullet_ychange
        show_bullet(bullet_img, (bullet_x + 10, bullet_y))
    # multiple bullets
    if bullet_y <= 10:
        bullet_y = 510
        bullet_status = "ready"
    # enemy movemnts
    for i in range(no_of_enemies):
        # game over
        if enemy_y[i] > 450:
            if g == 0:
                show_gameover(gameover_x, gameover_y)
            restart(restart_x, restart_y)
            pygame.mixer.music.stop()
            for j in range(no_of_enemies):
                enemy_y[j] = 1200
        enemy_x[i] += enemy_xchange[i]
        if enemy_x[i] <= 0:
            enemy_x[i] = 0
            enemy_xchange[i] = 0.6
            enemy_y[i] += enemy_ychange[i]
        elif enemy_x[i] >= 730:
            enemy_x[i] = 730
            enemy_xchange[i] = -0.6
            enemy_y[i] += enemy_ychange[i]
        show_enemy(enemy_img[i], (enemy_x[i], enemy_y[i]), i)
        collosion = iscollide(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collosion:
            explosion_sound.play()
            bullet_y = 510
            bullet_status = "ready"
            enemy_x[i] = random.randint(0, 734)
            enemy_y[i] = random.randint(10, 100)
            score += 1
        if score == 17:
            show_gamewin(gamewin_x, gamewin_y)
            restart(restart_x, restart_y)
            pygame.mixer.music.stop()
            for i in range(no_of_enemies):
                enemy_y[i] = 1200
            g = 1
    # border of the player
    if player_x <= 0:
        player_x = 0
    if player_x >= 730:
        player_x = 730

    show_score(score_x, score_y)
    show_player(player_img, (player_x, player_y))

    player_x += player_xchange
    pygame.display.update()
