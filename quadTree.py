import pygame
from rectangle import Rectangle
from random import choice

class Quadtree:
    def __init__(self, boundary, capacity):
        # 定义边界
        self.boundary = boundary
        # 定义每个节点分裂的容量，设置为4
        self.capacity = capacity
        # 定义每个节点中包含的实体集合
        self.rectangles = []
        # 此节点是否已经分裂
        self.divided = False



    # 插入节点
    def insert(self, rect):
        # 矩形不在此节点边界内，不插入
        if not self.boundary.intersects(rect):
            return False

        # 如果此节点已经分裂，尝试将矩形插入到相交的子节点中
        if self.divided:
            self.northeast.insert(rect)
            self.northwest.insert(rect)
            self.southeast.insert(rect)
            self.southwest.insert(rect)
        else:
            # 矩形插入此节点
            self.rectangles.append(rect)
            # 如果矩形数量超过容量，分裂
            if len(self.rectangles) > self.capacity:
                self.subdivide()

                rects = self.rectangles.copy()
                self.rectangles = []
                # 将原先在此节点中的矩形重新插入到相应的子节点中
                for r in rects:
                    self.insert(r)  # 这里我们重新使用insert方法
        return True

    # def insert(self, rect):
    #     # 矩形不在此节点边界内，不插入
    #     if not self.boundary.intersects(rect):
    #         return False

    #     # 如果此节点已经分裂，尝试将矩形插入到相交的子节点中
    #     if self.divided:
    #         inserted = False
    #         inserted |= self.northeast.insert(rect)
    #         inserted |= self.northwest.insert(rect)
    #         inserted |= self.southeast.insert(rect)
    #         inserted |= self.southwest.insert(rect)
    #         return inserted

    #     # 矩形插入此节点
    #     self.rectangles.append(rect)
    #     # 如果矩形数量超过容量，分裂
    #     if len(self.rectangles) > self.capacity:
    #         self.subdivide()

    #         rects = self.rectangles.copy()
    #         self.rectangles = []
    #         # 将原先在此节点中的矩形重新插入到相应的子节点中
    #         for r in rects:
    #             self.insert_into_children(r)

    #     return True


    def insert_into_children(self, rect):
        # 将矩形插入到相应的子节点中，并检查是否需要进行分裂
        if self.northeast.boundary.intersects(rect):
            self.northeast.rectangles.append(rect)
            if len(self.northeast.rectangles) > self.northeast.capacity:
                self.northeast.subdivide()
        if self.northwest.boundary.intersects(rect):
            self.northwest.rectangles.append(rect)
            if len(self.northwest.rectangles) > self.northwest.capacity:
                self.northwest.subdivide()
        if self.southeast.boundary.intersects(rect):
            self.southeast.rectangles.append(rect)
            if len(self.southeast.rectangles) > self.southeast.capacity:
                self.southeast.subdivide()
        if self.southwest.boundary.intersects(rect):
            self.southwest.rectangles.append(rect)
            if len(self.southwest.rectangles) > self.southwest.capacity:
                self.southwest.subdivide()
    


    # 分裂函数
    def subdivide(self):
        # 计算四个子节点的边界矩形，并创建子节点
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w / 2
        h = self.boundary.h / 2

        ne = Rectangle(x + w, y, w, h)
        self.northeast = Quadtree(ne, self.capacity)
        nw = Rectangle(x, y, w, h)
        self.northwest = Quadtree(nw, self.capacity)
        se = Rectangle(x + w, y + h, w, h)
        self.southeast = Quadtree(se, self.capacity)
        sw = Rectangle(x, y + h, w, h)
        self.southwest = Quadtree(sw, self.capacity)

        self.divided = True

    # 对于给定的坐标点（鼠标位置），查找该点所在的所有矩形
    def query_point(self, x, y):
        # 如果坐标点不在节点的边界范围内，则返回空列表
        if not self.boundary.contains(x, y):
            return []

        # 如果节点已经分裂，则分别在每个子节点上查询
        if self.divided:
            return (self.northeast.query_point(x, y) +
                    self.northwest.query_point(x, y) +
                    self.southeast.query_point(x, y) +
                    self.southwest.query_point(x, y))

        return self.rectangles


    def draw(self, surface):
        pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(
            self.boundary.x, self.boundary.y, self.boundary.w, self.boundary.h), 1)

        for rect in self.rectangles:
            if rect.moved:
                color_with_alpha = (0, 0, 255) + (100,)  # 高亮显示为蓝色
                pygame.draw.rect(surface, color_with_alpha, pygame.Rect(rect.x, rect.y, rect.w, rect.h))
                # 再绘制一个空心的矩形作为边框
                border_color = (0, 0, 0, 255)  # 黑色，完全不透明
                pygame.draw.rect(surface, border_color, pygame.Rect(rect.x, rect.y, rect.w, rect.h), 1)
            elif rect.selected:
                color_with_alpha = (242, 178, 235) + (100,)  # 粉色表示被选中
                pygame.draw.rect(surface, color_with_alpha, pygame.Rect(rect.x, rect.y, rect.w, rect.h))
                # 再绘制一个空心的矩形作为边框
                border_color = (0, 0, 0, 255)  # 黑色，完全不透明
                pygame.draw.rect(surface, border_color, pygame.Rect(rect.x, rect.y, rect.w, rect.h), 1)
            else:
                color_with_alpha = (0, 255, 0) + (255,)  # 其他矩形为绿色
                pygame.draw.rect(surface, color_with_alpha, pygame.Rect(rect.x, rect.y, rect.w, rect.h), 1)

            

        if self.divided:
            self.northeast.draw(surface)
            self.northwest.draw(surface)
            self.southeast.draw(surface)
            self.southwest.draw(surface)

    # 删除节点中的某一个矩形
    def remove(self, rect):
        if rect in self.rectangles:
            self.rectangles.remove(rect)
            # 判断是否需要合并子节点
            self.merge()
        if self.divided:
            self.northeast.remove(rect)
            self.northwest.remove(rect)
            self.southeast.remove(rect)
            self.southwest.remove(rect)
            self.merge()


    # 移动某一个矩形到随机位置。
    def move(self, old_rect, new_rect):
        self.remove(old_rect)
        new_rect.moved = True
        self.insert(new_rect)

    # 合并子节点。当子节点的父节点的所有子节点都没有数据时，合并这四个子节点。
    def merge(self):
        if self.divided and all([not child.rectangles and not child.divided for child in [self.northeast, self.northwest, self.southeast, self.southwest]]):
            self.divided = False
            self.northeast = None
            self.northwest = None
            self.southeast = None
            self.southwest = None
            return True
        return False
    


    # 清空节点
    def clear(self):
        # 清空当前节点存储的矩形
        self.rectangles = []
        # 如果当前节点已经分裂（即有子节点），则递归地清空子节点
        if self.divided:
            self.northeast.clear()
            self.northwest.clear()
            self.southeast.clear()
            self.southwest.clear()
        # 清空完成后，将当前节点设置为未分裂状态，并删除子节点
        self.divided = False
        self.northeast = None
        self.northwest = None
        self.southeast = None
        self.southwest = None
