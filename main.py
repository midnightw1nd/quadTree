import pygame
import random
from rectangle import Rectangle
from quadTree import Quadtree

# 常量定义
CAPACITY = 4
WIDTH, HEIGHT = 800, 600
RECT_MIN_SIZE, RECT_MAX_SIZE = 10, 50
NUM_RECTS = 50

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    boundary = Rectangle(0, 0, WIDTH, HEIGHT)
    qt = Quadtree(boundary, CAPACITY)

    rects = []
    for _ in range(NUM_RECTS):
        w = random.randint(RECT_MIN_SIZE, RECT_MAX_SIZE)
        h = random.randint(RECT_MIN_SIZE, RECT_MAX_SIZE)
        x = random.randint(0, WIDTH - w)
        y = random.randint(0, HEIGHT - h)
        rect = Rectangle(x, y, w, h)
        rects.append(rect)
        qt.insert(rect)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        qt.draw(screen)

        for rect in rects:
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(
                rect.x, rect.y, rect.w, rect.h), 1)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        found = qt.query_point(mouse_x, mouse_y)

        for rect in found:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(
                rect.x, rect.y, rect.w, rect.h))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
