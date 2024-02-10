import pygame
from sys import exit
import random
import sqlite3

pygame.init()
clock = pygame.time.Clock()

# size window
height = 720
width = 550
screen = pygame.display.set_mode((width, height))

# image load
bird_images = [[pygame.image.load("data/bird_down.png"),
                pygame.image.load("data/bird_mid.png"),
                pygame.image.load("data/bird_up.png")],
               [pygame.image.load("data/bird_down_gold.png"),
                pygame.image.load("data/bird_mid_gold.png"),
                pygame.image.load("data/bird_up_gold.png")]]
count_image = 0
count_bird = 0
sky_change = [pygame.image.load("data/background.png"), pygame.image.load("data/background_night.png")]
bird_change = [[], [pygame.image.load("data/bird_mid.png"), pygame.image.load("data/bird_mid_gold.png")]]
skyline_image = pygame.image.load("data/background.png")
night_image = pygame.image.load("data/background_night.png")
ground_image = pygame.image.load("data/ground.png")
top_pipe_image = pygame.image.load("data/pipe_top.png")
bottom_pipe_image = pygame.image.load("data/pipe_bottom.png")
game_over_image = pygame.image.load("data/game_over.png")
start_image = pygame.image.load("data/start.png")
sky_image = pygame.image.load('data/sky.png')

### sound

pygame.mixer.music.load('sounds/fon.mp3')
jump = pygame.mixer.Sound('sounds/jump.mp3')
loss = pygame.mixer.Sound('sounds/loss.mp3')
volume = 0
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(volume)

# setting
scroll_speed = 1
bird_start_position = (100, 250)
score = 0
max_score = 0
font = pygame.font.SysFont('Segoe', 26)
game_stopped = True
count_fond = 1
option_play = 1


# load base for play
def load_base():
    global max_score, count_image, count_bird, volume
    connect = sqlite3.connect('base.db')
    cursor = connect.cursor()
    all_info = cursor.execute("""SELECT * FROM all_info""").fetchall()[0]
    max_score = all_info[0]
    count_image = all_info[1]
    count_bird = all_info[2]
    volume = all_info[3]
    pygame.mixer.music.set_volume(volume)
    connect.close()


# update base for exit
def update_base():
    global max_score, count_image, count_bird
    connect = sqlite3.connect('base.db')
    cursor = connect.cursor()
    all_info = cursor.execute(
        f"""UPDATE all_info SET record = {max_score}, count_skin = {count_bird}, count_background = {count_image}, volume = {volume}""")
    connect.commit()
    connect.close()


class Start_Menu:
    def __init__(self, screen):
        screen.blit(sky_change[count_image], (0, 0))
        self.font = pygame.font.Font(None, 50)
        self.play_text = self.font.render("Обычный режим", False, (255, 165, 0))
        self.inver_play_text = self.font.render("Сложный режим", False, (255, 165, 0))
        self.skin_text = self.font.render("Настройки", False, (255, 165, 0))
        self.exit_text = self.font.render("Выход", False, (255, 165, 0))

        self.play_x = width // 2 - self.play_text.get_width() // 2
        self.play_y = height // 2 - self.play_text.get_height() // 2 - 75

        self.inver_play_x = width // 2 - self.play_text.get_width() // 2
        self.inver_play_y = height // 2 - self.play_text.get_height() // 2 - 25

        self.skin_x = width // 2 - self.skin_text.get_width() // 2
        self.skin_y = height // 2 - self.skin_text.get_height() // 2 + 25

        self.exit_x = width // 2 - self.exit_text.get_width() // 2
        self.exit_y = height // 2 - self.exit_text.get_height() // 2 + 75

        screen.blit(self.play_text, (self.play_x, self.play_y))
        screen.blit(self.inver_play_text, (self.inver_play_x, self.inver_play_y))
        screen.blit(self.skin_text, (self.skin_x, self.skin_y))
        screen.blit(self.exit_text, (self.exit_x, self.exit_y))

    def check(self, coords):
        if self.play_x - 10 <= coords[0] <= self.play_x - 10 + self.play_text.get_width() + 20 and self.play_y - 10 <= \
                coords[1] <= self.play_y - 10 + self.play_text.get_height() + 20:
            return 1
        elif self.exit_x - 10 <= coords[0] <= self.exit_x - 10 + self.exit_text.get_width() + 20 and self.exit_y - 10 <= \
                coords[1] <= self.exit_y - 10 + self.exit_text.get_height() + 20:
            return 3
        elif self.skin_x - 10 <= coords[0] <= self.skin_x - 10 + self.skin_text.get_width() + 20 and self.skin_y - 10 <= \
                coords[1] <= self.skin_y - 10 + self.skin_text.get_height() + 20:
            return 2
        elif self.inver_play_x - 10 <= coords[
            0] <= self.inver_play_x - 10 + self.inver_play_text.get_width() + 20 and self.inver_play_y - 10 <= \
                coords[1] <= self.inver_play_y - 10 + self.inver_play_text.get_height() + 20:
            return 4


class Setting:
    def __init__(self, screen):
        screen.blit(sky_change[count_image], (0, 0))
        self.font = pygame.font.Font(None, 50)
        self.play_text = self.font.render("Сменить день/ночь", False, (255, 165, 0))
        self.skin_text = self.font.render("Сменить скин", False, (255, 165, 0))
        self.volume_text = self.font.render("Изменить звук", False, (255, 165, 0))
        self.exit_text = self.font.render("Назад", False, (255, 165, 0))

        self.play_x = width // 2 - self.play_text.get_width() // 2
        self.play_y = height // 2 - self.play_text.get_height() // 2 - 75

        self.skin_x = width // 2 - self.skin_text.get_width() // 2
        self.skin_y = height // 2 - self.skin_text.get_height() // 2 - 25

        self.volume_x = width // 2 - self.skin_text.get_width() // 2
        self.volume_y = height // 2 - self.skin_text.get_height() // 2 + 25

        self.exit_x = width // 2 - self.exit_text.get_width() // 2
        self.exit_y = height // 2 - self.exit_text.get_height() // 2 + 75

        screen.blit(self.play_text, (self.play_x, self.play_y))
        screen.blit(self.skin_text, (self.skin_x, self.skin_y))
        screen.blit(self.volume_text, (self.volume_x, self.volume_y))
        screen.blit(self.exit_text, (self.exit_x, self.exit_y))

    def update(self):
        global count_image
        count_image = 0 if count_image == 1 else 1
        screen.blit(sky_change[count_image], (0, 0))
        screen.blit(self.play_text, (self.play_x, self.play_y))
        screen.blit(self.skin_text, (self.skin_x, self.skin_y))
        screen.blit(self.volume_text, (self.volume_x, self.volume_y))
        screen.blit(self.exit_text, (self.exit_x, self.exit_y))

    def check(self, coords):
        if self.play_x - 10 <= coords[0] <= self.play_x - 10 + self.play_text.get_width() + 20 and self.play_y - 10 <= \
                coords[1] <= self.play_y - 10 + self.play_text.get_height() + 20:
            screen.blit(night_image, (0, 0))
            return 1
        elif self.exit_x - 10 <= coords[0] <= self.exit_x - 10 + self.exit_text.get_width() + 20 and self.exit_y - 10 <= \
                coords[1] <= self.exit_y - 10 + self.exit_text.get_height() + 20:
            return 3
        elif self.skin_x - 10 <= coords[0] <= self.skin_x - 10 + self.skin_text.get_width() + 20 and self.skin_y - 10 <= \
                coords[1] <= self.skin_y - 10 + self.skin_text.get_height() + 20:
            return 2
        elif self.volume_x - 10 <= coords[
            0] <= self.volume_x - 10 + self.volume_text.get_width() + 20 and self.volume_y - 10 <= \
                coords[1] <= self.volume_y - 10 + self.volume_text.get_height() + 20:
            return 4


class ChangeBirdSkin:
    def __init__(self, screen):
        screen.blit(sky_change[count_image], (0, 0))
        self.font = pygame.font.Font(None, 50)
        self.play_text = self.font.render("Сменить скин", False, (255, 165, 0))
        self.exit_text = self.font.render("Назад", False, (255, 165, 0))

        self.play_x = width // 2 - self.play_text.get_width() // 2
        self.play_y = height // 2 - self.play_text.get_height() // 2 - 50

        self.exit_x = width // 2 - self.exit_text.get_width() // 2
        self.exit_y = height // 2 - self.exit_text.get_height() // 2
        screen.blit(self.play_text, (self.play_x, self.play_y))
        screen.blit(self.exit_text, (self.exit_x, self.exit_y))

    def change_skin(self, bird, coords):
        global count_bird
        if self.play_x - 10 <= coords[0] <= self.play_x - 10 + self.play_text.get_width() + 20 and self.play_y - 10 <= \
                coords[1] <= self.play_y - 10 + self.play_text.get_height() + 20:
            count_bird = 0 if count_bird == 1 else 1
            bird.image = bird_images[count_bird][1]
        elif self.exit_x - 10 <= coords[0] <= self.exit_x - 10 + self.exit_text.get_width() + 20 and self.exit_y - 10 <= \
                coords[1] <= self.exit_y - 10 + self.exit_text.get_height() + 20:
            return 3


class ChangeVolume:
    def __init__(self, screen):
        screen.blit(sky_change[count_image], (0, 0))
        self.font = pygame.font.Font(None, 50)
        self.plus_text = self.font.render("Прибавить звук", False, (255, 165, 0))
        self.munis_text = self.font.render("Убавить звук", False, (255, 165, 0))
        self.exit_text = self.font.render("Назад", False, (255, 165, 0))

        self.plus_x = width // 2 - self.plus_text.get_width() // 2
        self.plus_y = height // 2 - self.plus_text.get_height() // 2 - 50

        self.minus_x = width // 2 - self.munis_text.get_width() // 2
        self.minus_y = height // 2 - self.munis_text.get_height() // 2

        self.exit_x = width // 2 - self.exit_text.get_width() // 2
        self.exit_y = height // 2 - self.exit_text.get_height() // 2 + 50

        screen.blit(self.plus_text, (self.plus_x, self.plus_y))
        screen.blit(self.munis_text, (self.minus_x, self.minus_y))
        screen.blit(self.exit_text, (self.exit_x, self.exit_y))

    def update(self, coords):
        global volume
        if self.plus_x - 10 <= coords[0] <= self.plus_x - 10 + self.plus_text.get_width() + 20 and self.plus_y - 10 <= \
                coords[1] <= self.plus_y - 10 + self.plus_text.get_height() + 20:
            if volume < 1:
                volume += 0.1
                pygame.mixer.music.set_volume(volume)
        elif self.minus_x - 10 <= coords[
            0] <= self.minus_x - 10 + self.munis_text.get_width() + 20 and self.minus_y - 10 <= \
                coords[1] <= self.minus_y - 10 + self.munis_text.get_height() + 20:
            if volume > 0:
                volume -= 0.1
                pygame.mixer.music.set_volume(volume)
        elif self.exit_x - 10 <= coords[0] <= self.exit_x - 10 + self.exit_text.get_width() + 20 and self.exit_y - 10 <= \
                coords[1] <= self.exit_y - 10 + self.exit_text.get_height() + 20:
            return 3


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = bird_images[count_bird][0]
        self.rect = self.image.get_rect()
        self.rect.center = bird_start_position
        self.image_index = 0
        self.vel = 0
        self.flap = False
        self.alive = True

    def move_for_settings(self):
        self.rect.x = width // 2 - self.image.get_width() // 2
        self.rect.y = height // 2 - self.image.get_height() // 2 - 175

    def update(self, user_input):
        global option_play
        # animate
        if self.alive:
            self.image_index += 1
        if self.image_index >= 30:
            self.image_index = 0
        if option_play == -1:
            self.image = pygame.transform.flip(bird_images[count_bird][self.image_index // 10], False, True)
        else:
            self.image = bird_images[count_bird][self.image_index // 10]

        # move bird
        self.vel += 0.5 * option_play
        if self.vel > 7:
            self.vel = 7
        if self.rect.y < 500:
            self.rect.y += int(self.vel)
        if self.vel == 0:
            self.flap = False

        # change image
        self.image = pygame.transform.rotate(self.image, self.vel * -7)

        # wait space
        if user_input[pygame.K_SPACE] and not self.flap and self.rect.y > 0 and self.alive:
            self.flap = True
            self.vel = -7 * option_play
            jump.play()
        if option_play == -1 and not self.alive:
            self.vel += 5


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, image, pipe_type):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.enter, self.exit, self.passed = False, False, False
        self.pipe_type = pipe_type

    def update(self):
        # move столбов)
        self.rect.x -= scroll_speed
        if self.rect.x <= -width:
            self.kill()

        # Score
        global score
        if self.pipe_type == 'bottom':
            if bird_start_position[0] > self.rect.topleft[0] and not self.passed:
                self.enter = True
            if bird_start_position[0] > self.rect.topright[0] and not self.passed:
                self.exit = True
            if self.enter and self.exit and not self.passed:
                self.passed = True
                score += 1


class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = ground_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self):
        # move ground
        self.rect.x -= scroll_speed
        if self.rect.x <= -width:
            self.kill()


class Sky(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = sky_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self):
        # move ground
        self.rect.x -= scroll_speed
        if self.rect.x <= -width:
            self.kill()


class ButtonExit:
    def __init__(self, screen):
        self.text = font.render("Выйти(Q)", True, (255, 0, 0))
        self.text_x = width - self.text.get_width() - 25
        self.text_y = 25
        screen.blit(self.text, (self.text_x, self.text_y))

    def draw(self, screen):
        screen.blit(self.text, (self.text_x, self.text_y))


def quit_game():
    # exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            update_base()
            pygame.quit()
            exit()


# main function
def main():
    global score, max_score

    # bird
    bird = pygame.sprite.GroupSingle()
    bird.add(Bird())

    # settings
    pipe_timer = 0
    pipes = pygame.sprite.Group()

    # ground
    x_pos_ground, y_pos_ground = 0, 520
    ground = pygame.sprite.Group()
    ground.add(Ground(x_pos_ground, y_pos_ground))
    button = ButtonExit(screen)

    x_pos_sky, y_pos_sky = -1, 0
    sky = pygame.sprite.Group()
    sky.add(Sky(x_pos_sky, y_pos_sky))

    run = True
    while run:
        # exit
        quit_game()

        # reset
        screen.fill((0, 0, 0))

        # wait button
        user_input = pygame.key.get_pressed()

        # draw button
        screen.blit(sky_change[count_image], (0, 0))

        # spawn
        if len(ground) <= 2:
            ground.add(Ground(width, y_pos_ground))
            sky.add(Sky(x_pos_sky, y_pos_sky))

        # draw all
        pipes.draw(screen)
        ground.draw(screen)
        bird.draw(screen)
        button.draw(screen)
        sky.draw(screen)

        # count score
        score_text = font.render('Счет: ' + str(score), True, pygame.Color(255, 255, 255))
        screen.blit(score_text, (20, 20))
        max_score_text = font.render('Рекорд: ' + str(max_score), True, pygame.Color(255, 255, 255))
        screen.blit(max_score_text, (20, 40))
        if score > max_score:
            max_score = score

        # update all
        if bird.sprite.alive:
            pipes.update()
            ground.update()
            sky.update()

        bird.update(user_input)
        if user_input[pygame.K_q]:
            run = False
            entrance()
            break

        # collision
        collision_pipes = pygame.sprite.spritecollide(bird.sprites()[0], pipes, False)
        collision_ground = pygame.sprite.spritecollide(bird.sprites()[0], ground, False)
        collision_sky = pygame.sprite.spritecollide(bird.sprites()[0], sky, False)
        if collision_pipes or collision_ground or collision_sky:
            bird.sprite.alive = False
            loss.play()
            if collision_ground:
                screen.blit(game_over_image, (width // 2 - game_over_image.get_width() // 2,
                                              height // 2 - game_over_image.get_height() // 2))
                if user_input[pygame.K_r]:
                    score = 0
                    break
                if user_input[pygame.K_q]:
                    run = False
                    entrance()
                    break

        # spawn
        if pipe_timer <= 0 and bird.sprite.alive:
            x_top, x_bottom = 550, 550
            y_top = random.randint(-600, -480)
            y_bottom = y_top + random.randint(90, 130) + bottom_pipe_image.get_height()
            pipes.add(Pipe(x_top, y_top, top_pipe_image, 'top'))
            pipes.add(Pipe(x_bottom, y_bottom, bottom_pipe_image, 'bottom'))
            pipe_timer = random.randint(180, 250)
        pipe_timer -= 1

        clock.tick(60)
        pygame.display.update()


# restart and menu
def restart():
    global game_stopped

    while game_stopped:
        quit_game()

        # Draw Menu
        screen.fill((0, 0, 0))
        screen.blit(sky_change[count_image], (0, 0))
        screen.blit(ground_image, Ground(0, 520))
        screen.blit(bird_images[count_bird][0], (100, 250))
        screen.blit(start_image, (width // 2 - start_image.get_width() // 2,
                                  height // 2 - start_image.get_height() // 2))
        # User Input
        user_input = pygame.key.get_pressed()
        button = ButtonExit(screen)
        button.draw(screen)

        if user_input[pygame.K_SPACE]:
            main()
        if user_input[pygame.K_q]:
            entrance()

        pygame.display.update()


# window entrance
def entrance():
    global game_stopped, option_play
    start_window = Start_Menu(screen)
    while game_stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_stopped = False
                update_base()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_window.check(event.pos) == 1:
                    option_play = 1
                    restart()
                elif start_window.check(event.pos) == 3:
                    update_base()
                    game_stopped = False
                elif start_window.check(event.pos) == 2:
                    settings()
                elif start_window.check(event.pos) == 4:
                    option_play = -1
                    restart()
        pygame.display.flip()


# window settings
def settings():
    global game_stopped
    window = Setting(screen)
    while game_stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_stopped = False
                update_base()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if window.check(event.pos) == 1:
                    window.update()
                elif window.check(event.pos) == 3:
                    entrance()
                elif window.check(event.pos) == 2:
                    change_bird()
                elif window.check(event.pos) == 4:
                    change_volume()

        pygame.display.flip()


# change slin window
def change_bird():
    global game_stopped
    window = ChangeBirdSkin(screen)
    bird = pygame.sprite.GroupSingle()
    sprite = Bird()
    sprite.move_for_settings()
    bird.add(sprite)
    while game_stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_stopped = False
                update_base()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if window.change_skin(sprite, event.pos) == 3:
                    settings()

        bird.draw(screen)
        pygame.display.flip()


# change volume window
def change_volume():
    global game_stopped
    window = ChangeVolume(screen)
    while game_stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_stopped = False
                update_base()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if window.update(event.pos) == 3:
                    settings()
        pygame.display.flip()


# main for main
if __name__ == "__main__":
    load_base()
    entrance()
