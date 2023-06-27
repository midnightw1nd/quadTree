import datetime
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
ACTION_EVENT = pygame.USEREVENT + 3


def main():

    pygame.init()
    # 定义模拟状态
    simulation_active = False
    selected_rects = []  # 新增，存储需要移动的实体
    round_counter = 0
    next_action = "select"  # 下一个动作：select， move， pause

    # 创建一个稍微大一点的屏幕，这样就有空间来放置按钮
    screen = pygame.display.set_mode((WIDTH + 350, HEIGHT + 150))

    clock = pygame.time.Clock()

    # 调整四叉树边界和按钮位置，让他们在新的屏幕布局中居中
    boundary = Rectangle(50, 100, WIDTH, HEIGHT)
    select_button = Button(50, 35, 100, 50, 'Select')
    move_selected_button = Button(170, 35, 100, 50, 'Move-Sel')
    update_button = Button(290, 35, 100, 50, 'Update-Sel')
    move_button = Button(410,35,100,50, 'Move')
    reset_button = Button(950, 710, 100, 35, 'Reset')
    simulate_button = Button(530,35,100,50, 'simulate')
    stop_button = Button(650,35,100,50, 'stop')
    qt = Quadtree(boundary, CAPACITY)

    # 创建字体对象
    font = pygame.font.Font(None, 24)
    event_font = pygame.font.Font(None, 18)

    # 添加一个列表来存储事件
    events = []

    # 定义清空/存储tag
    clear_tag = False

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

        # history框内已满,将历史操作信息写入文件
        if(clear_tag):
            try:
                with open("log.txt", "a") as log_file:
                    timestamp = datetime.datetime.now()  # 获取当前时间
                    formatted_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                    log_file.write("--------------------------update at" + formatted_timestamp +  "-------------------------------\n")
                    for event in events:
                        log_file.write(event + "\n")
                events.clear()
            except Exception as e:
                print(f"Error writing to log file: {e}")
            finally:
                clear_tag = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # button
            if event.type == pygame.MOUSEBUTTONDOWN:
                # move button
                if move_button.is_over(pygame.mouse.get_pos()):
                    rect = random.choice(rects)
                    new_rect = Rectangle(random.randint(50, WIDTH + 50 - rect.w), random.randint(100, HEIGHT + 100 - rect.h), rect.w, rect.h, moved=True)
                    new_rect.id = rect.id
                    qt.move(rect, new_rect)
                    rect_index = rects.index(rect)  # 找到rect在rects列表中的索引
                    rects[rect_index] = new_rect  # 用new_rect替换原始的Rectangle对象
                    rect.x = new_rect.x
                    rect.y = new_rect.y
                    # 添加事件到事件列表
                    events.append(f"rectangle {rect.id} moved")
                # select button
                elif select_button.is_over(pygame.mouse.get_pos()):
                    # 取消所有矩形的选中状态，然后随机选择一个矩形
                    for rect in rects:
                        rect.selected = False
                    selected_rect = random.choice(rects)
                    selected_rect.selected = True
                    # 添加事件到事件列表
                    events.append(f"rectangle {selected_rect.id} selected")
                # mov-sel button
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
                            events.append(f"selected rectangle {rect.id} moved")
                # update-sel button
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
                        events.append(f"selected rectangle {rect.id} size changed")
                
                # reset button
                elif reset_button.is_over(pygame.mouse.get_pos()):
                    # 删除所有现有矩形
                    rects.clear()
                    # 清空四叉树
                    qt.clear()
                    # 创建新的矩形并添加到四叉树中
                    for i in range(NUM_RECTS):
                        w = random.randint(RECT_MIN_SIZE, RECT_MAX_SIZE)
                        h = random.randint(RECT_MIN_SIZE, RECT_MAX_SIZE)
                        x = random.randint(50, WIDTH + 50 - w)
                        y = random.randint(100, HEIGHT + 100 - h)
                        rect = Rectangle(x, y, w, h)
                        rect.id = i
                        rects.append(rect)
                        qt.insert(rect)
                    # 清空模拟状态
                    simulation_active = False
                    selected_rect = []
                    round_counter = 0
                    next_action = "select"
                    clear_tag = True

                # simulate button
                elif simulate_button.is_over(pygame.mouse.get_pos()):
                    simulation_active = True    #模拟状态为true
                    pygame.time.set_timer(ACTION_EVENT, 1000) 
                    events.append(f"------simulation begins-------")
                    # pygame.time.set_timer(MOVE_EVENT, 3000) 
                    # pygame.time.set_timer(PAUSE_EVENT, 1000) 
                elif stop_button.is_over(pygame.mouse.get_pos()):
                    simulation_active = False   #模拟状态为false
                    events.append(f"------simulation ends-------")
                    clear_tag = True
                    pygame.time.set_timer(ACTION_EVENT, 0)

            elif event.type == ACTION_EVENT:
                if simulation_active:
                    if next_action == "select":
                        num_to_select = random.randint(1, 3)
                        selected_rects = random.sample(rects, num_to_select)  # 随机选择一些矩形
                        for rect in selected_rects:
                            rect.selected = True  # 标记为选中 (粉色)
                            events.append(f"rectangle {rect.id} selected")
                        next_action = "move"  # 设置下一个动作为 'move'
                    elif next_action == "move":
                        if selected_rects:
                            for rect in selected_rects:
                                new_rect = Rectangle(random.randint(50, WIDTH + 50 - rect.w), random.randint(100, HEIGHT + 100 - rect.h), rect.w, rect.h)
                                new_rect.id = rect.id
                                new_rect.moved = True  # 标记为移动 (蓝色)
                                qt.move(rect, new_rect)
                                rect_index = rects.index(rect)
                                rects[rect_index] = new_rect
                                new_rect.selected = False
                                events.append(f"rectangle {rect.id} moved")
                            next_action = "pause"  # 设置下一个动作为 'pause'
                    elif next_action == "pause":
                        round_counter += 1
                        events.append(f"------Simulation round {round_counter} completed------")  # 在历史记录框中添加新的轮数记录
                        next_action = "select"  # 设置下一个动作为 'select'
   

        screen.fill((255, 255, 255))

        # 绘制历史记录文本框
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(WIDTH + 80, 50, 250, 650), 3)
        title_text = font.render("History", True, (0, 0, 0))
        screen.blit(title_text, (WIDTH + 80, 25))  # 在文本框上方显示标题

        
        for i, event in enumerate(events):
            # 渲染每个事件文本并在文本框内显示
            event_text = event_font.render(event, True, (0, 0, 0))
            screen.blit(event_text, (WIDTH + 85, 55 + i * 20))  # 每行文本的高度设为20像素
            # 如果文本内容超出边框，清空文本框。
            if 55 + i * 20 > 650:
                clear_tag = True
        



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
        reset_button.draw(screen)
        simulate_button.draw(screen)
        stop_button.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
