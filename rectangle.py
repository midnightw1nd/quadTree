
#定义实体的矩形范围
class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    # 判断一个节点是否包含本实体
    def contains(self, x, y):
        return self.x <= x < self.x + self.w and self.y <= y < self.y + self.h

    # 判断两个矩形是否相交
    def intersects(self, other):
        return not (other.x + other.w <= self.x or
                    other.x >= self.x + self.w or
                    other.y + other.h <= self.y or
                    other.y >= self.y + self.h)
