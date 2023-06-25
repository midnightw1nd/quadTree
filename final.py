import random
from point import Point
from quadTree import QuadTree

# 生成随机数据
random_points = [Point(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(1000)]

# 创建四叉树
qt = QuadTree(0, 0, 100, 100, 4)

# 插入点到四叉树
for point in random_points:
    qt.insert(qt.root, point)

# 查询某个范围内的点
result = qt.search(qt.root, 20, 20, 30, 30)
for point in result:
    print(f"({point.x}, {point.y})")
