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
WIDTH, HEIGHT = 600, 600  # Dimensions of the window
FPS = 30
SIZE = 20  # This is the size of the player and enemies

# Pygame variables
pygame.display.set_caption('Jank Space Invader Clone')  # Sets the name of the window
ROOT = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FONT = pygame.font.Font(None, 24)  # The font for any text in-game
screen_center = WIDTH - WIDTH // 2 - SIZE // 2

# These lists hold the references(?) for the class objects related to the list.
enemy_list = []
projectiles_list = []


# This class stores all player data, creates the game object for the player and generally just deals with the player.
class PlayerClass:
    def __init__(self, posx, posy, size, lives):
        self.posx = posx
        self.posy = posy
        self.size = size
        self.lives = lives
        self.rect = pygame.Rect(self.posx, self.posy, self.size, self.size)

    def get_player(self):
        return self.rect

    def update_pos(self, VEL):
        self.rect.x -= VEL


class EnemyClass:
    def __init__(self, posx, posy):
        self.posx = posx
        self.posy = posy
        self.rect = pygame.Rect(self.posx, self.posy, 20, 20)

    def get_enemy(self):
        return self.rect

    def update_pos(self, VEL):
        self.rect.x -= VEL

    def enemy_shoot(self, chance):
        num = randrange(0, 100)
        if num > chance:
            projectiles_list.append(Projectiles(self.posx, self.posy, -8))


# This class handles all the projectiles, both player and enemy
class Projectiles:
    def __init__(self, posx, posy, vel):
        self.posx = posx
        self.posy = posy
        self.vel = vel
        self.rect = pygame.Rect(self.posx + SIZE//2.5, self.posy, 4, 8)

    # When called, this method spawns a projectile at a given coords (enemy or player position)
    def draw_projectile(self):
        return self.rect

    # This method moves the projectile object
    def move_projectile(self):
        self.rect.y -= self.vel

    # This checks if the projectile leaves the window or hits something.
    def check_hit(self, player_obj):
        if self.rect.y < 0:
            projectiles_list.pop(projectiles_list.index(self))
        for item in enemy_list:
            if item.rect.colliderect(self.rect):
                enemy_list.pop(enemy_list.index(item))
                projectiles_list.pop(projectiles_list.index(self))
        if player_obj.rect.colliderect(self.rect):
            player_obj.lives -= 1


# Here we check the various events we are looking out for in the program.
def check_events(player_obj):
    # This assigns a list of currents pressed keys to a "keys" variable, we then use this to check for player inputs and execute the relevant code.
    VEL = 8
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
            if event.key == pygame.K_SPACE and len(projectiles_list) < 10:
                projectiles_list.append(Projectiles(player_obj.rect.x, player_obj.rect.y - SIZE / 2, 8))


# This creates the FPS counter at the top left
def fps_counter():
    count = str(int(clock.get_fps()))
    fps_txt = FONT.render(count, True, WHITE)
    ROOT.blit(fps_txt, (fps_txt.get_width() - fps_txt.get_width()//2, fps_txt.get_height() - fps_txt.get_height()//2))


# This function is used to update the window every frame.
def draw_root(player_obj):
    ROOT.fill(BLACK)
    pygame.draw.rect(ROOT, GREEN, player_obj.get_player())
    for item in projectiles_list:
        item.check_hit(player_obj)
        pygame.draw.rect(ROOT, WHITE, item.draw_projectile())
        item.move_projectile()
    for item in enemy_list:
        pygame.draw.rect(ROOT, RED, item.get_enemy())
    fps_counter()
    pygame.display.update()


def main():
    c = 8
    X, Y = 20, 30
    player_object = PlayerClass(screen_center, HEIGHT - SIZE * 2, SIZE, 3)
    while True:
        if c > 0:
            enemy_list.append(EnemyClass(X, Y))
            X += 40
            c -= 1
        else:
            break

    while True:
        check_events(player_object)
        draw_root(player_object)
        clock.tick(FPS)


if __name__ == '__main__':
    main()
