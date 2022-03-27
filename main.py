import pygame
import random
import sys

pygame.init()

# Constant variables
BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
WIDTH, HEIGHT = 800, 800  # Dimensions of the window
FPS = 60
SIZE = 20  # This is the size of the player and enemies
CHANCE = 4

# Pygame variables
pygame.display.set_caption('Jank Space Invader Clone')  # Sets the name of the window
ROOT = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FONT = pygame.font.Font(None, 24)  # The font for any text in-game
screen_center = WIDTH - WIDTH // 2 - SIZE // 2

# Other variables.
game_over = False
win = False
direction = 1
move_count = 0
# Game over text
game_over_text = FONT.render('GAME OVER', False, RED)
game_over_screen = game_over_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
# Win text
win_text = FONT.render('YOU WIN', False, GREEN)
win_screen = win_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))

# Custom pygame events.
ENEMY_MOVE_EVENT = 25  # This is an event to move the enemies
ENEMY_MOVE_TIMER = 1200
pygame.time.set_timer(ENEMY_MOVE_EVENT, ENEMY_MOVE_TIMER)
ENEMY_SHOOT_EVENT = 26
ENEMY_SHOOT_TIMER = 2000
pygame.time.set_timer(ENEMY_SHOOT_EVENT, ENEMY_SHOOT_TIMER)

# These lists hold the references(?) for the class objects related to the list.
enemy_list = []
projectiles_list = []
enemy_projectiles_list = []


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

    def check_health(self):
        if self.lives <= 0:
            global game_over
            game_over = True


class EnemyClass:
    def __init__(self, posx, posy):
        self.posx = posx
        self.posy = posy
        self.rect = pygame.Rect(self.posx, self.posy, SIZE, SIZE)

    def get_enemy(self):
        return self.rect

    def update_pos(self, VEL):
        self.rect.x -= VEL


# This class handles all the projectiles, both player and enemy
class Projectiles:
    def __init__(self, posx, posy, vel, from_enemy):
        self.posx = posx
        self.posy = posy
        self.vel = vel
        self.from_enemy = from_enemy
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
        if self.rect.y > HEIGHT:
            enemy_projectiles_list.pop(enemy_projectiles_list.index(self))
        for item in enemy_list:
            if item.rect.colliderect(self.rect) and not self.from_enemy:
                enemy_list.pop(enemy_list.index(item))
                projectiles_list.pop(projectiles_list.index(self))
                return True
        if player_obj.rect.colliderect(self.rect):
            enemy_projectiles_list.pop(enemy_projectiles_list.index(self))
            player_obj.lives -= 1


# Here we check the various events we are looking out for in the program.
def check_events(player_obj):
    # This assigns a list of currents pressed keys to a "keys" variable, we then use this to check for player inputs and execute the relevant code.
    global direction
    global move_count
    global game_over
    VEL = 4
    skip = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_obj.rect.x > 0:
        player_obj.update_pos(VEL)
    if keys[pygame.K_RIGHT] and player_obj.rect.x + SIZE < WIDTH:
        player_obj.update_pos(-VEL)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # This event is to allow the enemies to shoot. Every time the event flag is raised, all enemies have a chance to shoot.
        if event.type == ENEMY_SHOOT_EVENT:
            for item in enemy_list:
                num = random.randrange(0, len(enemy_list), 2)
                if num < CHANCE:
                    enemy_projectiles_list.append(Projectiles(item.rect.x, item.rect.y, -4, True))
        #  This event is about letting enemies move in steps, instead of a smooth slide across the screen.
        if event.type == ENEMY_MOVE_EVENT:
            if move_count >= 8:
                direction = direction * -1
                move_count = 0
                skip = True
                for item in enemy_list:
                    item.rect.y += SIZE * 2
            for item in enemy_list:
                if not skip:  # This skip is so that the enemies don't move down and right/left in one movement. The enmies move down then left/right in two movements.
                    item.rect.x += VEL * 4 * direction
            move_count += 1
        # This statement check if the spacebar is pressed and spawns on projectile for each press. Holding space doesn't spawn a ton of projectiles all at once.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and len(projectiles_list) < 10:
                projectiles_list.append(Projectiles(player_obj.rect.x, player_obj.rect.y - SIZE / 2, 4, False))


# This creates the FPS counter at the top left.
def fps_counter():
    count = str(int(clock.get_fps()))
    fps_txt = FONT.render(count, True, WHITE)
    ROOT.blit(fps_txt, (fps_txt.get_width() - fps_txt.get_width()//2, fps_txt.get_height() - fps_txt.get_height()//2))


# This function is used to update the window every frame.
def draw_root(player_obj):
    ROOT.fill(BLACK)
    pygame.draw.rect(ROOT, GREEN, player_obj.get_player())
    # pygame.draw.rect(ROOT, WHITE, (0, 0, 10, 10))
    # pygame.draw.rect(ROOT, WHITE, (WIDTH - 10, 0, 10, 10))
    for item in projectiles_list:
        item.check_hit(player_obj)
        pygame.draw.rect(ROOT, WHITE, item.draw_projectile())
        item.move_projectile()
    if len(enemy_list) == 0:
        global win
        win = True
    for item in enemy_projectiles_list:
        pygame.draw.rect(ROOT, WHITE, item.draw_projectile())
        item.check_hit(player_obj)
        item.move_projectile()
    for item in enemy_list:
        pygame.draw.rect(ROOT, RED, item.get_enemy())
    fps_counter()
    pygame.display.update()


def main():
    num = 24
    c = num
    x, y = 20, 30
    z = 4
    player_object = PlayerClass(screen_center, HEIGHT - SIZE * 2, SIZE, 3)
    while c > 0:
        enemy_list.append(EnemyClass(x, y))
        x += SIZE * 2
        c -= 1
        if z == 0 and c < 9:
            break
        if c < 9:
            y += SIZE * 2
            c = num
            x = 20
            z -= 1

    while True:
        if game_over:
            while True:
                ROOT.fill(BLACK)
                ROOT.blit(game_over_text, game_over_screen)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                clock.tick(FPS)
        if win:
            while True:
                ROOT.fill(BLACK)
                ROOT.blit(win_text, win_screen)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                clock.tick(FPS)
        check_events(player_object)
        player_object.check_health()
        draw_root(player_object)
        clock.tick(FPS)


if __name__ == '__main__':
    main()
