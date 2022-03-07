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
SIZE = 20

# Pygame variables
pygame.display.set_caption('Jank Space Invader Clone')
ROOT = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FONT = pygame.font.Font(None, 24)

# Non-constant variables
enemy_list = []
projectiles = []


# This class stores all player data, creates the game object for the player and generally just deals with the player.
class PlayerClass:
    def __init__(self, posx, posy, size, lives):
        self.posx = posx
        self.posy = posy
        self.size = size
        self. lives = lives

    def load_player(self):
        return pygame.Rect(self.posx, self.posy, self.size, self.size)

    def update_pos(self, VEL):
        self.posx -= VEL


# This class handles all the projectiles, both player and enemy
class Projectiles:
    def __init__(self, posx, posy, vel):
        self.posx = posx
        self.posy = posy
        self.vel = vel

    def draw_projectile(self):
        return pygame.Rect(self.posx + SIZE//2.5, self.posy, 4, 8)

    def move_projectile(self):
        self.posy -= self.vel

    def check_hit(self):
        if self.posy < 0:
            return True


# This function is for the chance of an enemy to shoot. Chance should be a float between 1 and 0.1
def enemy_shoot(chance):
    num = randrange(0, 100)
    return num * chance


# Here we check the various events we are looking out for in the program.
def check_events(player_obj):
    # This assigns a list of currents pressed keys to a "keys" variable, we then use this to check for player inputs and execute the relevant code.
    VEL = 4
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_obj.posx > 0:
        player_obj.update_pos(VEL)
    if keys[pygame.K_RIGHT] and player_obj.posx + SIZE < WIDTH:
        player_obj.update_pos(-VEL)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and len(projectiles) < 10:
                projectiles.append(Projectiles(player_obj.posx, player_obj.posy - 4, 8))


# This creates the FPS counter at the top left
def fps_counter():
    count = str(int(clock.get_fps()))
    fps_txt = FONT.render(count, True, WHITE)
    ROOT.blit(fps_txt, (fps_txt.get_width() - fps_txt.get_width()//2, fps_txt.get_height() - fps_txt.get_height()//2))


# This function is used to update the window every frame.
def draw_root(player_obj):
    ROOT.fill(BLACK)
    for item in projectiles:
        if item.check_hit():
            projectiles.pop(projectiles.index(item))
        pygame.draw.rect(ROOT, WHITE, item.draw_projectile())
        item.move_projectile()
    pygame.draw.rect(ROOT, GREEN, player_obj.load_player())
    fps_counter()
    pygame.display.update()


def main():
    screen_center = WIDTH - WIDTH//2 - SIZE//2
    player_object = PlayerClass(screen_center, HEIGHT - SIZE * 2, SIZE, 3)
    while True:
        check_events(player_object)
        draw_root(player_object)
        clock.tick(FPS)


if __name__ == '__main__':
    main()
