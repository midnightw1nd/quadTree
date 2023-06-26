
#定义实体的矩形范围
class Rectangle:
    def __init__(self, x, y, w, h, moved=False, selected=False, id=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.moved = moved
        self.selected = selected
        self.id = id

    # 判断一个节点是否包含本实体
    def contains(self, x, y):
        return self.x <= x < self.x + self.w and self.y <= y < self.y + self.h

    # 判断本实体是否被一个矩形完全包含
    def is_contained_in(self, other):
        return (self.x >= other.x and 
                self.y >= other.y and
                self.x + self.w <= other.x + other.w and
                self.y + self.h <= other.y + other.h)
    # 判断两个矩形是否相交
    def intersects(self, other):
        if self.is_contained_in(other) or other.is_contained_in(self):
            return True
        return not (other.x + other.w <= self.x or
                    other.x >= self.x + self.w or
                    other.y + other.h <= self.y or
                    other.y >= self.y + self.h)
    
    

