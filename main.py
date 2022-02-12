import pygame
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

pygame.display.set_caption('Jank Space Invader Clone')
ROOT = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FONT = pygame.font.Font(None, 24)

# Non-constant values


# Custom events


def check_events():
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


def fps_counter():
    count = str(int(clock.get_fps()))
    fps_txt = FONT.render(count, True, WHITE)
    ROOT.blit(fps_txt, (fps_txt.get_width() - fps_txt.get_width()//2, fps_txt.get_height() - fps_txt.get_height()//2))


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
