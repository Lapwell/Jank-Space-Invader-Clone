import pygame
from random import randrange
import sys

pygame.init()

# Constant values
BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
WIDTH, HEIGHT = 800, 800
FPS = 60
VEl = 24

# Pygame variables
pygame.display.set_caption('Jank Space Invader Clone')
ROOT = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FONT = pygame.font.Font(None, 24)

# Non-constant values
enemy_list = []
enemy_projectiles = []
player_projectiles = []

# Custom events


# This function is for the chance of an enemy to shoot
def enemy_shoot(chance):
    return randrange(0, chance)


# Here we check the various events we are looking out for in the program. Game events (death, level clears, mplayer input, etc).
def check_events():
    # This assigns a list of currents pressed keys to a "keys" variable, we then use this to check for player inputs and execute the relevant code.
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        pass
    if keys[pygame.K_RIGHT]:
        pass
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
def draw_root():
    ROOT.fill(BLACK)
    fps_counter()
    pygame.display.update()


def main():
    while True:
        check_events()
        draw_root()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
