# 定义类表示四叉树节点
class Node:
    def __init__(self, xmin, ymin, xmax, ymax, capacity):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.capacity = capacity
        self.points = []
        self.nodes = []
