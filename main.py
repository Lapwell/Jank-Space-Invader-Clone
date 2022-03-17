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
WIDTH, HEIGHT = 800, 800  # Dimensions of the window
FPS = 30
SIZE = 20  # This is the size of the player and enemies

# Pygame variables
pygame.display.set_caption('Jank Space Invader Clone')  # Sets the name of the window
ROOT = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FONT = pygame.font.Font(None, 24)  # The font for any text in-game

# These lists hold the references(?) for the class objects related to the list.
enemy_list = []
projectiles = []


# This class stores all player data, creates the game object for the player and generally just deals with the player.
class PlayerClass:
    def __init__(self, posx, posy, size, lives):
        self.posx = posx
        self.posy = posy
        self.size = size
        self. lives = lives
        self.rect = pygame.Rect(self.posx, self.posy, self.size, self.size)

    def spawn_player(self):
        return self.rect

    def update_pos(self, VEL):
        self.rect.x -= VEL


class EnemyClass:
    def __init__(self, posx, posy):
        self.posx = posx
        self.posy = posy
        self.rect = pygame.Rect(self.posx, self.posy, 20, 20)

    def spawn_enemy(self):
        return self.rect

    def update_pos(self, VEL):
        self.rect.x -= VEL

    def enemy_shoot(self, chance):
        num = randrange(0, 100)
        if num > chance:
            projectiles.append(Projectiles(self.posx, self.posy, -8))


# This class handles all the projectiles, both player and enemy
class Projectiles:
    def __init__(self, posx, posy, vel):
        self.posx = posx
        self.posy = posy
        self.vel = vel

    # When called, this method spawns a projectile at a given coords (enemy or player position)
    def draw_projectile(self):
        return pygame.Rect(self.posx + SIZE//2.5, self.posy, 4, 8)

    # This method moves the projectile object
    def move_projectile(self):
        self.posy -= self.vel

    # This checks if the projectile leaves the window or hits something.
    def check_hit(self, player_obj):
        if self.posy < 0:
            return True
        for item in enemy_list:
            if item.collidepoint(self.posx, self.posy):
                return True
        if player_obj.rect.collidepoint(self.posx, self.posy):
            player_obj.lives -= 1
            return True


# Here we check the various events we are looking out for in the program.
def check_events(player_obj):
    # This assigns a list of currents pressed keys to a "keys" variable, we then use this to check for player inputs and execute the relevant code.
    VEL = 4
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_obj.rect.x > 0:
        player_obj.update_pos(VEL)
    if keys[pygame.K_RIGHT] and player_obj.rect.x + SIZE < WIDTH:
        player_obj.update_pos(-VEL)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # This statement check if the spacebar is pressed and spawns on projectile for each press. Holding space doesn't spawn a ton of projectiles all at once.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and len(projectiles) < 10:
                projectiles.append(Projectiles(player_obj.rect.x, player_obj.rect.y - 4, 8))


# This creates the FPS counter at the top left
def fps_counter():
    count = str(int(clock.get_fps()))
    fps_txt = FONT.render(count, True, WHITE)
    ROOT.blit(fps_txt, (fps_txt.get_width() - fps_txt.get_width()//2, fps_txt.get_height() - fps_txt.get_height()//2))


# This function is used to update the window every frame.
def draw_root(player_obj):
    ROOT.fill(BLACK)
    pygame.draw.rect(ROOT, GREEN, player_obj.spawn_player() )
    fps_counter()
    for item in projectiles:
        if item.check_hit(player_obj):
            projectiles.pop(projectiles.index(item))  # This gets the index of the current item and removes it.
        pygame.draw.rect(ROOT, WHITE, item.draw_projectile())
        item.move_projectile()
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
