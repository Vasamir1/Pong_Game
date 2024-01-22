"""Pong by Marcin Kaczorowski
Made with PyGame library.
Sounds and melody come from pixabay.com,
and are used with Pixabay Content License (https://pixabay.com/service/terms/).
Font "Open Sans" used with Open Font License (https://openfontlicense.org/open-font-license-official-text/)"""

import pygame

pygame.init()

# important variables
width = 1440
height = 720
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
screen_color = (21, 21, 30)
player_color = (255, 255, 230)
info_color = (255, 255, 204)
game_font = pygame.font.Font("OpenSans-VariableFont_wdth,wght.ttf", 30)
info_font = pygame.font.Font("OpenSans-VariableFont_wdth,wght.ttf", 20)
clock = pygame.time.Clock()
max_fps = 60
dt = 0
pygame.display.set_caption("Pong by Marcin Kaczorowski")
ESC_INFO = "Press ESC to exit"
P1_CTRL = "Press W and S to move"
P2_CTRL = "Press UP nad DOWN to move"

# game sounds and music
bg_music = pygame.mixer.Sound("sinnesloschen-beam-117362.ogg")
bg_music.set_volume(0.6)
bg_music.play(loops=-1)
hit_snd = pygame.mixer.Sound("menu-selection-102220.ogg")
hit_snd.set_volume(0.6)
lose_snd = pygame.mixer.Sound("videogame-death-sound-43894.ogg")
lose_snd.set_volume(0.6)


class Player:
    # initialing positions, size, velocity and color
    def __init__(self, posx, posy, w, h, vel, col):
        self.posx = posx
        self.posy = posy
        self.w = w
        self.h = h
        self.vel = vel
        self.col = col
        # rect to control position and collision
        self.player_rect = pygame.Rect(posx, posy, w, h)
        # blit
        self.player = pygame.draw.rect(screen, self.col, self.player_rect)

    def draw_player_on_the_screen(self):
        self.player = pygame.draw.rect(screen, self.col, self.player_rect)

    def border_limit(self, y_mov):
        self.posy = self.posy + self.vel * y_mov
        if self.posy <= 0:
            self.posy = 0
        elif self.posy + self.h >= height:
            self.posy = height - self.h

        self.player_rect = (self.posx, self.posy, self.w, self.h)

    def display_score(self, text, score, x, y, col):
        text = game_font.render(text + str(score), True, col)
        text_rect = text.get_rect()
        text_rect.center = (x, y)
        screen.blit(text, text_rect)

    def get_rect_player(self):
        return self.player_rect


class Ball:
    # initialing positions, size, velocity and color
    def __init__(self, posx, posy, r, vel, col):
        self.posx = posx
        self.posy = posy
        self.r = r
        self.vel = vel
        self.col = col
        self.y_mov = -1
        self.x_mov = 1
        # blit
        self.ball = pygame.draw.circle(
            screen, self.col, (self.posx, self.posy), self.r
        )
        # score logic at start
        self.start = 1

    def draw_ball_on_the_screen(self):
        self.ball = pygame.draw.circle(
            screen, self.col, (self.posx, self.posy), self.r
        )

    def ball_movement(self):
        self.posx += self.vel * self.x_mov
        self.posy += self.vel * self.y_mov
        if self.posy <= 0 or self.posy >= height:
            self.y_mov *= -1

        # cleaning score
        if self.posx <= 0 and self.start:
            self.start = 0
            return 1
        elif self.posx >= width and self.start:
            self.start = 0
            return -1
        else:
            return 0

    def reset_pos(self):
        lose_snd.play()
        self.vel = 6
        self.posx = width // 2
        self.posy = height // 2
        self.x_mov *= -1
        self.start = 1

    def collision_with_player(self):
        hit_snd.play()
        self.x_mov *= -1
        self.vel += 1

    def get_rect_ball(self):
        return self.ball


# game blocks
def main():

    # changing ball color based on velocity
    def change_ball_color():
        if ball.vel == 8:
            ball.col = (219, 197, 197)
        elif ball.vel == 10:
            ball.col = (222, 169, 169)
        elif ball.vel == 12:
            ball.col = (217, 89, 89)
        elif ball.vel > 14:
            ball.col = (217, 15, 15)

    # display informations on screen
    def display_information(txt, x, y, col):
        text = info_font.render(txt, True, col)
        text_rect = text.get_rect()
        text_rect.center = (x, y)
        screen.blit(text, text_rect)

    game_run = True
    ball_color = (255, 255, 230)
    ball = Ball(width // 2, height // 2, 9, 6, ball_color)
    player_one = Player(20, 0, 30, 120, 14, player_color)
    player_two = Player(width - 50, 0, 30, 120, 14, player_color)
    players = [player_one, player_two]
    player_one_score = 0
    player_two_score = 0
    player_one_ymov = 0
    player_two_ymov = 0

    while game_run:
        screen.fill(screen_color)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_run = False

        # game render
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player_one_ymov = -1
                if event.key == pygame.K_s:
                    player_one_ymov = 1
                if event.key == pygame.K_UP:
                    player_two_ymov = -1
                if event.key == pygame.K_DOWN:
                    player_two_ymov = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    player_one_ymov = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player_two_ymov = 0

        for player in players:
            if pygame.Rect.colliderect(ball.get_rect_ball(), player.get_rect_player()):
                ball.collision_with_player()

        player_one.border_limit(player_one_ymov)
        player_two.border_limit(player_two_ymov)
        points = ball.ball_movement()

        change_ball_color()

        if points == -1:
            player_one.h -= 10
            player_two.h += 10
            player_one_score += 1
        elif points == 1:
            player_one.h += 10
            player_two.h -= 10
            player_two_score += 1

        if points:
            ball.col = ball_color
            ball.reset_pos()

        player_one.draw_player_on_the_screen()
        player_two.draw_player_on_the_screen()
        ball.draw_ball_on_the_screen()

        player_one.display_score("Player 1:  ", player_one_score, 250, 20, player_color)
        player_two.display_score("Player 2:  ", player_two_score, width-250, 20, player_color)

        display_information(ESC_INFO, (width/2), (height-30), info_color)
        display_information(P1_CTRL, 150, height-50, info_color)
        display_information(P2_CTRL, width-200, height-50, info_color)

        pygame.display.update()
        clock.tick(max_fps)


if __name__ == "__main__":
    main()
    pygame.quit()
