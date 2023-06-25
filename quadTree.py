from node import Node

# 定义四叉树
class QuadTree:
    def __init__(self, xmin, ymin, xmax, ymax, capacity):
        self.root = Node(xmin, ymin, xmax, ymax, capacity)

    # 插入点
    def insert(self, node, point):
        if (node.xmin <= point.x < node.xmax) and (node.ymin <= point.y < node.ymax):
            if len(node.points) < node.capacity:
                node.points.append(point)
            else:
                if not node.nodes:
                    self.subdivide(node)
                for child in node.nodes:
                    self.insert(child, point)

    # 分割节点
    def subdivide(self, node):
        dx = (node.xmax - node.xmin) / 2
        dy = (node.ymax - node.ymin) / 2
        node.nodes.append(Node(node.xmin, node.ymin, node.xmin + dx, node.ymin + dy, node.capacity))
        node.nodes.append(Node(node.xmin + dx, node.ymin, node.xmax, node.ymin + dy, node.capacity))
        node.nodes.append(Node(node.xmin, node.ymin + dy, node.xmin + dx, node.ymax, node.capacity))
        node.nodes.append(Node(node.xmin + dx, node.ymin + dy, node.xmax, node.ymax, node.capacity))

    # 搜索函数
    def search(self, node, xmin, ymin, xmax, ymax):
        points = []
        if node.xmin > xmax or node.xmax < xmin or node.ymin > ymax or node.ymax < ymin:
            return points
        for point in node.points:
            if xmin <= point.x < xmax and ymin <= point.y < ymax:
                points.append(point)
        if node.nodes:
            for child in node.nodes:
                points.extend(self.search(child, xmin, ymin, xmax, ymax))
        return points
