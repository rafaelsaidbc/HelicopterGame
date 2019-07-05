import pygame
import helicopter
import enemy_heli
import boat
import sprites
import random


pygame.mixer.pre_initi(44100, -16, 1, 512)
pygame.init()

pygame.display.set_icon(sprites.icon)
display_width = 800
display_height = 600
game.display = pygame.display.set_mode((display_width, display_height))

font = '8-Bit-Madness.ttf'

#mensagem da tela
def message_to_screen(message, textfont, size, color):
    my_font = pygame.font.Font(textfont, size)
    my_message = my_font.render(message, 0, color)
    return my_message


# cores de fonte
white = (255,255,255)
black = (0,0,0)
gray = (50,50,50)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)

#converte tudo em
for convert_sprites in sprites.all_sprites:
    convert_sprites.convert_alpha()


clock = pygame.time.Clock()
FPS = 30

player = helicopter.Helicopter = open(100, display_height/2-40)
moving = True
godmode = False

score = 0

highscore_file = open('highscore.dat', 'r')
highscore_int = int(highscore_file.read())

cloud_x = 800
cloud_y = random.randint(0, 400)

enemy_heli = enemy_heli.EnemyHeli(-100, display_height/2-40)
enemy_heli_alive = False

boat = boat.Boat(-100, 430)
boat_alive = False

spaceship_x = 800
spaceship_y = random.randint(0, 400)
spaceship_alive = False
spaceship_hit_player = False
warning_once = True
warning = False
warning_counter = 0
warning_message = message_to_screen('!', font, 200, red)

balloon_x = 800
balloon_y = random.randint(0, 400)

bullets = []

bombs = []

shoot = pygame.mixer.Sound('sounds/shoot.wav')
pop = pygame.mixer.Sound('sounds/pop.wav')
bomb = pygame.mixer.Sound('sounds/bomb.wav')
explosion = pygame.mixer.Sound('sounds/explosion.wav')
explosion2 = pygame.mixer.Sound('sounds/explosion2.wav')
select = pygame.mixer.Sound('sounds/select.wav')
select2 = pygame.mixer.Sound('sounds/select2.wav')
alert = pygame.mixer.Sound('sounds/alert.wav')
whoosh = pygame.mixer.Sound('sounds/whoosh.wav')


def main_menu():
    global cloud_x
    global cloud_y

    menu = True
    selected = 'play'

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_w or event.key == pygame.K_UP:
                    pygame.mixer.Sound.play(select)
                    selected = 'play'

                elif event.type == pygame.K_s or event.key == pygame.K_DOWN:
                    pygame.mixer.Sound.play(select)
                    selected = 'quit'

                elif event.type == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    pygame.mixer.Sound.play(select2)
                    if selected == 'play':
                        menu = False
                    if selected == 'quit':
                        pygame.quit()
                        quit()


        game_display.blit(sprites.background, (0,0))
        game_display.blit(sprites.cloud, (cloud_x, cloud_y))
        if cloud_x <= 800 - 1100:
            cloud_x = 800
            cloud_y = random.randint(0, 400)
        else:
            if not player.wreck_start:
                cloud_x -= 5
            if godmode:
                title = message_to_screen("Helicoptero (GODMODE)", font, 80, yellow)
            else:
                title = message_to_screen("Helicoptero", font, 100, black)

            controls_1 = message_to_screen('Use WASD para mover, SPACE para atirar', font, 30, black)
            controls_2 = message_to_screen('Use SHIFT para jogar bomba, P para pausar', font, 30, black)

            if selected == 'JOGAR':
                play = message_to_screen('Jogar', font, 75, white)
            else:
                play = message_to_screen('Jogar', font, 75, black)

            if selected == 'SAIR':
                game_quit = message_to_screen('Sair', font, 75, black)
            else:
                game_quit = message_to_screen('Sair', font, 75, black)

                title_rect = title.get_rect()
                controls_1_rect = controls_1.get_rect()
                controls_2_rect = controls_2.get_rect()
                play_rect = play.get_rect()
                quit_rect = game_quit.get_rect()

                game_display.blit(title, (display_width/2 - (title_rect[2]/2), 40))
                game_display.blit(controls_1, (display_width / 2 - (controls_1_rect[2] / 2), 120))
                game_display.blit(controls_2, (display_width / 2 - (controls_2_rect[2] / 2), 140))
                game_display.blit(play, (display_width / 2 - (play_rect[2] / 2), 200))
                game_display.blit(game_quit, (display_width / 2 - (game_quit[2] / 2), 260))

                pygame.draw.rect(game_display, blue, (0, 500, 800, 100))
                pygame.display.update()
                pygame.display.set_caption('Velocidade do Helicopter' + str(int(clock.get_fps()))) + 'por segundo'
                clock.tick(FPS)


def pause():
    global hightscore_file
    global hightscore_int

    paused = True

    player.moving_up = False
    player.moving_down = False
    player.moving_left = False
    player.moving_right = False

    paused_text = message_to_screen('Jogo pausado!', font, 100, black)
    paused_text_rect = paused_text.get_rect()
    game_display.blit(paused_text, (display_width / 2 - (paused_text_rect[2] / 2), 40))

    pygame.display.update()
    clock.tick(15)

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if score > highscore_int:
                    highscore_file = open('highscore.dat', 'w')
                    highscore_file.write(str(score))
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pygame.mixer.Sound.play(select)
                        paused = False


def game_loop():
    global spaceship_x
    global spaceship_y
    global spaceship_alive
    global spaceship_hit_player
    global warning
    global warning_counter
    global warning_once

    global bullets
    global moving

    global highscore_file
    global highscore_int
    global score

    global cloud_x
    global cloud_y

    global enemy_heli_alive
    global boat_alive

    game_exit = False
    game_over = False

    game_over_selected = "Jogar novamente"

    while not game_exit:
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if score > highscore_int:
                        highscore_file = open('highscore.dat', 'w')
                        highscore_file.write(str(score))
                        highscore_file.close()
                        pygame.quit()
                        quit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_w or event.key == pygame.K_UP:
                            pygame.mixer.Sound.play(select)
                            game_over_selected = 'Jogar novamente'

                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        pygame.mixer.Sound.play(select)
                        game_over_selected = 'quit'

                        if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                            pygame.mixer.Sound.play(select2)
                            if game_over_selected == 'Jogar novamente':
                                if score > highscore_int:
                                    highscore_file = open('highscore.dat', 'w')
                                    highscore_file.write(str(score))
                                    highscore_file.close()
                                    game_over = False

                                    score = 0

                                    balloon_x = 800

                                    enemy_heli.x = -100
                                    enemy_heli_alive = False
                                    enemy_heli.bullets = []

                                    boat.x = -110
                                    boat_alive = False
                                    boat.bullets = []

                                    spaceship_x = 800
                                    spaceship_alive = False
                                    warning = False
                                    warning_counter = 0
                                    warning_counter = 0

                                    player.wreck_start = False
                                    player.y = display_height / 2 - 40
                                    player.x = 100
                                    player.wrecked = False
                                    player.health = 3
                                    bullets = []

                                    game_loop()
                                if game_over_selected == 'quit':
                                    pygame.quit()
                                    quit()
            game_over_text = message_to_screen('Game over', font, 100, black)
            your_score = message_to_screen('Sua pontuação foi: ' + str(score), font, 50, black)
            if game_over_selected == 'Jogar novamente':
                play_again = message_to_screen('Jogar novamente', font, 75, white)
            else:
                play_again = message_to_screen('Jogar novamente', font, 75, black)
                if game_over_selected == 'quit':
                    game_quit = message_to_screen('Quit', font, 75, white)
                else:
                    game_quit = message_to_screen('Quit', font, 75, black)

            game_over_rect = game_over_text.get_rect()
            your_score_rect = your_score.get_rect()
            play_again_rect = play_again.get_rect()
            game_quit_rect = game_quit.get_rect()

            game_display.blit(game_over_text, (display_width / 2 - game_over_rect[2] / 2, 40))
            game_display.blit(game_over_text, (display_width / 2 - your_score_rect[2] / 2 + 5, 100))
            game_display.blit(game_over_text, (display_width / 2 - play_again_rect[2] / 2, 200))
            game_display.blit(game_over_text, (display_width / 2 - game_quit_rect[2] / 2, 260))

            pygame.display.update()
            pygame.display.set_caption('Velocidade do Helicopter' + str(int(clock.get_fps())) + ' por segundo')
            clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if score > highscore_int:
                    highscore_file = open('highscore.dat', 'w')
                    highscore_file.write(str(score))
                    highscore_file.close()
                    pygame.quit()
                    quit()

                if moving:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_w:
                            player.moving_up = True

                        if event.key == pygame.K_a:
                            player.moving_left = True

                        if event.key == pygame.K_d:
                            player.moving_right = True

                        if event.key == pygame.K_s:
                            player.moving_down = True

                        if event.key == pygame.K_SPACE:
                            if not player.wreck_start:
                                pygame.mixer.Sound.play(shoot)
                                bullets.append(([player.x, player.y]))

                        if event.key == pygame.K_LSHIFT:
                            if not player.wreck_start:
                                pygame.mixer.Sound.play(bomb)
                                bombs.append(([player.x, player.y]))

                        if event.key == pygame.K_p:
                            pygame.mixer.Sound.play(select)
                            pause()

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_w:
                            player.moving_up = False

                        if event.key == pygame.K_a:
                            player.moving_left = False

                        if event.key == pygame.K_s:
                            player.moving_down = False

                        if event.key == pygame.K_d:
                            player.moving_right = False

        if player.health < 1:
            pygame.mixer.Sound.play(explosion)
            player.wreck()

        if player.wrecked:
            game_over = True

        game_display.blit(sprites.background, (0, 0))
        game_display.blit(sprites.cloud, (cloud_x, cloud_y))
        if cloud_x <= 800 - 1100:
            cloud_x = 800
            cloud_y = random.randint(0, 400)
        else:
            if not player.wreck_start:
                cloud_x -= 5

        game_display.blit(player.current, (player.x, player.y))
        game_display.blit(enemy_heli.current, (enemy_heli.x, enemy_heli.y))
        game_display.blit(sprites.spaceship, (spaceship_x, spaceship_y))
        game_display.blit(sprites.boat, (boat.x, boat.y))

        player.player_init()
        enemy_heli.init()
        boat.init()

        if not player.wreck_start and not player.wrecked:
            for draw_bullet in bullets:
                pygame.draw.rect(game_display, black, (draw_bullet[0] + 90, draw_bullet[1] + 40, 10, 10))
            for move_bullet in range(len(bullets)):
                bullets[move_bullet][0] += 40
            for del_bullet in bullets:
                if del_bullet[0] >= 800:
                    bullets.remove(del_bullet)

        if not player.wreck_start and not player.wrecked:
            for draw_bomb in bombs:
                pygame.draw.rect(game_display, black, (draw_bomb[0] + 55, draw_bomb[1] + 70, 20, 20))
            for move_bomb in range(len(bombs)):
                bombs[move_bomb][1] += 20
            for del_bomb in bombs:
                if del_bomb[1] >= 600:
                    bombs.remove(del_bomb)

        if not player.wreck_start and not player.wrecked and not game_over:
            for draw_bullet in enemy_heli.bullets:
                pygame.draw.rect(game_display, gray, (draw_bullet[0], draw_bullet[1] + 40, 40, 10))
                pygame.draw.rect(game_display, red, (draw_bullet[0] + 30, draw_bullet[1] + 40, 10, 10))
            for move_bullet in range(len(enemy_heli.bullets)):
                enemy_heli.bullets[move_bullet][0] -= 15
            for del_bullet in enemy_heli.bullets:
                if del_bullet[0] <= -40:
                    enemy_heli.bullets.remove(del_bullet)