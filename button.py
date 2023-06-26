
import pygame
# 添加按钮类
class Button:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.rect.x - 2, self.rect.y - 2, self.rect.width + 4, self.rect.height + 4), 0)
        pygame.draw.rect(win, (255, 0, 0), self.rect, 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 15)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.rect.x + (self.rect.w / 2 - text.get_width() / 2), self.rect.y + (self.rect.h / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        return self.rect.collidepoint(pos)
