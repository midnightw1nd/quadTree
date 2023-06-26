import pygame
import random
from random import choice
from rectangle import Rectangle
from quadTree import Quadtree
from button import Button
# 常量定义
CAPACITY = 4
WIDTH, HEIGHT = 800, 600
RECT_MIN_SIZE, RECT_MAX_SIZE = 10, 50
NUM_RECTS = 50
COLOR_CHANGE_EVENT = pygame.USEREVENT + 1
MOVE_EVENT = pygame.USEREVENT + 2

def main():

    pygame.init()
    # 定义模拟状态
    simulate = False
    stop = False
    # 创建一个稍微大一点的屏幕，这样就有空间来放置按钮
    screen = pygame.display.set_mode((WIDTH + 100, HEIGHT + 150))

    clock = pygame.time.Clock()

    # 调整四叉树边界和按钮位置，让他们在新的屏幕布局中居中
    boundary = Rectangle(50, 100, WIDTH, HEIGHT)
    select_button = Button(50, 35, 100, 50, 'Select')
    move_selected_button = Button(170, 35, 100, 50, 'Move-Sel')
    update_button = Button(290, 35, 100, 50, 'Update-Sel')
    move_button = Button(410,35,100,50, 'Move')
    simulate_button = Button(530,35,100,50, 'simulate')
    stop_button = Button(650,35,100,50, 'stop')
    qt = Quadtree(boundary, CAPACITY)
    font = pygame.font.Font(None, 24)
    rects = []
    for i in range(NUM_RECTS):
        w = random.randint(RECT_MIN_SIZE, RECT_MAX_SIZE)
        h = random.randint(RECT_MIN_SIZE, RECT_MAX_SIZE)
        x = random.randint(50, WIDTH + 50 - w)
        y = random.randint(100, HEIGHT + 100 - h)
        rect = Rectangle(x, y, w, h)
        rect.id = i
        rects.append(rect)
        qt.insert(rect)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # move button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if move_button.is_over(pygame.mouse.get_pos()):
                    rect = random.choice(rects)
                    new_rect = Rectangle(random.randint(50, WIDTH + 50 - rect.w), random.randint(100, HEIGHT + 100 - rect.h), rect.w, rect.h, moved=True)
                    new_rect.id = rect.id
                    qt.move(rect, new_rect)
                    rect_index = rects.index(rect)  # 找到rect在rects列表中的索引
                    rects[rect_index] = new_rect  # 用new_rect替换原始的Rectangle对象
                    rect.x = new_rect.x
                    rect.y = new_rect.y
                elif select_button.is_over(pygame.mouse.get_pos()):
                    # 取消所有矩形的选中状态，然后随机选择一个矩形
                    for rect in rects:
                        rect.selected = False
                    selected_rect = random.choice(rects)
                    selected_rect.selected = True

                elif move_selected_button.is_over(pygame.mouse.get_pos()):
                    # 找到选中的矩形，然后移动它
                    for rect in rects:
                        if rect.selected:
                            new_rect = Rectangle(random.randint(50, WIDTH + 50 - rect.w), 
                                                random.randint(100, HEIGHT + 100 - rect.h), 
                                                rect.w, 
                                                rect.h, 
                                                moved=True)
                            new_rect.id = rect.id
                            qt.move(rect, new_rect)
                            rect_index = rects.index(rect)
                            rects[rect_index] = new_rect

                            rect.x = new_rect.x
                            rect.y = new_rect.y
                elif update_button.is_over(pygame.mouse.get_pos()):
                    # 首先，找出被选中的矩形
                    selected_rect = None
                    for rect in rects:
                        if rect.selected:
                            selected_rect = rect
                            break
                    # 如果找到了被选中的矩形，随机更新其形状，并从四叉树中移除，然后再重新插入
                    if selected_rect is not None:
                        qt.remove(selected_rect)
                        new_w = random.randint(RECT_MIN_SIZE, RECT_MAX_SIZE)
                        new_h = random.randint(RECT_MIN_SIZE, RECT_MAX_SIZE)
                        selected_rect.w = new_w
                        selected_rect.h = new_h
                        qt.insert(selected_rect)
            #     elif simulate_button.is_over(pygame.mouse.get_pos()):
            #         pygame.time.set_timer(MOVE_EVENT, 3000)
            #     elif stop_button.is_over(pygame.mouse.get_pos()):
            #         pygame.time.set_timer(MOVE_EVENT, 0)
            # elif event.type == MOVE_EVENT:
            #     num_to_move = random.randint(1, 5)  # number of rectangles to move
            #     for _ in range(num_to_move):
            #         rect = random.choice(rects)
            #         new_rect = Rectangle(random.randint(50, WIDTH + 50 - rect.w), random.randint(100, HEIGHT + 100 - rect.h), rect.w, rect.h, moved=True)
            #         new_rect.id = rect.id
            #         qt.move(rect, new_rect)
            #         rect_index = rects.index(rect)  # find the index of rect in the rects list
            #         rects[rect_index] = new_rect  # replace the original Rectangle object with new_rect
            #         rect.x = new_rect.x
            #         rect.y = new_rect.y

                
                # simulate
        # if simulate and not stop:
        #     num_to_move = random.randint(1, 5)  # number of rectangles to move
        #     for _ in range(num_to_move):
        #         rect = random.choice(rects)
        #         new_rect = Rectangle(random.randint(50, WIDTH + 50 - rect.w), random.randint(100, HEIGHT + 100 - rect.h), rect.w, rect.h, moved=True)
        #         new_rect.id = rect.id
        #         qt.move(rect, new_rect)
        #         rect_index = rects.index(rect)  # find the index of rect in the rects list
        #         rects[rect_index] = new_rect  # replace the original Rectangle object with new_rect
        #         rect.x = new_rect.x
        #         rect.y = new_rect.y


        screen.fill((255, 255, 255))
        qt.draw(screen)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        found = qt.query_point(mouse_x, mouse_y)

        for rect in found:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(
                rect.x, rect.y, rect.w, rect.h))
            id_text = font.render(str(rect.id), True, (0, 0, 0))
            screen.blit(id_text, (rect.x, rect.y - 20))  # 在矩形的上方显示编号


        select_button.draw(screen)
        move_selected_button.draw(screen)
        move_button.draw(screen)
        update_button.draw(screen)
        # simulate_button.draw(screen)
        # stop_button.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
