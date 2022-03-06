import pygame
from random import randrange
import sys

pygame.init()

# Constant variables
BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
WIDTH, HEIGHT = 800, 800
FPS = 30
SIZE = 32

# Pygame variables
pygame.display.set_caption('Jank Space Invader Clone')
ROOT = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FONT = pygame.font.Font(None, 24)

# Non-constant variables
enemy_list = []
enemy_projectiles = []
player_projectiles = []


# This class stores all player data, creates the game object for the player and generally just deals with the player.
class PlayerClass:
    def __init__(self, posx, size, lives):
        self.posx = posx
        self.size = size
        self. lives = lives

    def load_player(self):
        return pygame.Rect(self.posx, (HEIGHT - SIZE * 2), self.size, self.size)

    def update_pos(self, new_pos):
        self.posx = self.posx - new_pos


# This function is for the chance of an enemy to shoot. Chance should be a float between 1 and 0.1
def enemy_shoot(chance):
    num = randrange(0, 100)
    return num * chance


# Here we check the various events we are looking out for in the program.
def check_events(player_obj):
    # This assigns a list of currents pressed keys to a "keys" variable, we then use this to check for player inputs and execute the relevant code.
    VEL = 10
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_obj.update_pos(VEL)
    if keys[pygame.K_RIGHT]:
        player_obj.update_pos(-VEL)
    if keys[pygame.K_SPACE]:
        pass
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


# This function uses the assigned function on line 18 (clock = pygame.time.Clock()) to get the current frame.
# Once we get the framce "count" we then draw the number on the top left of the window.
def fps_counter():
    count = str(int(clock.get_fps()))
    fps_txt = FONT.render(count, True, WHITE)
    ROOT.blit(fps_txt, (fps_txt.get_width() - fps_txt.get_width()//2, fps_txt.get_height() - fps_txt.get_height()//2))


# This function is used to update the window every frame.
def draw_root(player_obj):
    ROOT.fill(BLACK)
    pygame.draw.rect(ROOT, GREEN, player_obj.load_player())
    fps_counter()
    pygame.display.update()


def main():
    screen_center = WIDTH - WIDTH//2 - SIZE//2
    player_object = PlayerClass(screen_center, 20, 3)
    while True:
        check_events(player_object)
        draw_root(player_object)
        clock.tick(FPS)


if __name__ == '__main__':
    main()
