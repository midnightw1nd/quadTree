import math
import random
import time

import matplotlib.pyplot as plt

from button import Button
from main import WIDTH, HEIGHT, NUM_RECTS, RECT_MIN_SIZE, RECT_MAX_SIZE
from quadTree import Quadtree
from rectangle import Rectangle

from memory_profiler import profile
import pandas as pd
import matplotlib
from rtreelib import RTree, Rect

matplotlib.use('TkAgg')


def generate_random_rect_one():
    w = random.randint(RECT_MIN_SIZE, RECT_MAX_SIZE)
    h = random.randint(RECT_MIN_SIZE, RECT_MAX_SIZE)
    x = random.randint(50, WIDTH + 50 - w)
    y = random.randint(100, HEIGHT + 100 - h)
    rect = Rectangle(x, y, w, h)
    return rect


class PerformanceTest:
    def __init__(self, cap):
        self.boundary = Rectangle(50, 100, WIDTH, HEIGHT)
        self.qt = Quadtree(self.boundary, cap)

    def test_insert_one(self):
        new_rect = generate_random_rect_one()
        self.qt.insert(new_rect)

    # @profile
    def test_insert_many_times(self, quantity=500):
        hundreds = quantity
        time_start = time.time()
        for i in range(hundreds):
            self.test_insert_one()
        time_end = time.time()
        return hundreds, time_end - time_start

    def test_query_one(self):
        x = random.uniform(self.boundary.x, self.boundary.x + self.boundary.w)
        y = random.uniform(self.boundary.y, self.boundary.y + self.boundary.h)
        self.qt.query_point(x, y)

    def test_query_many_times(self, quantity=500):
        times = quantity
        time_start = time.time()
        for i in range(times):
            self.test_query_one()
        time_end = time.time()
        return times, time_end - time_start


def generate_rect_one():
    w = random.randint(RECT_MIN_SIZE, RECT_MAX_SIZE)
    h = random.randint(RECT_MIN_SIZE, RECT_MAX_SIZE)
    x = random.randint(50, WIDTH + 50 - w)
    y = random.randint(100, HEIGHT + 100 - h)
    rect = Rect(x, y, w, h)
    return rect


class MyRTree:
    def __init__(self):
        self.rt = RTree()

    def test_insert_one(self, dat):
        self.rt.insert(dat, generate_rect_one())

    def test_insert_many_times(self, quantity=500):
        hundreds = quantity
        time_start = time.time()
        for i in range(hundreds):
            self.test_insert_one(i)
        time_end = time.time()
        return hundreds, time_end - time_start

    def test_query_one(self):
        self.rt.query(generate_rect_one())

    def test_query_many_times(self, quantity=500):
        times = quantity
        time_start = time.time()
        for i in range(times):
            self.test_query_one()
        time_end = time.time()
        return times, time_end - time_start


caps = []
inserts = []
queries = []
quantities = []
for capacity in range(7, 31):
    mt = PerformanceTest(capacity)
    hundreds_times, time_insert = mt.test_insert_many_times(500)
    _, time_query = mt.test_query_many_times(500)
    caps.append(capacity)
    inserts.append(time_insert)
    queries.append(time_query)

t = RTree()
t = MyRTree()
_, time_insert = t.test_query_many_times()
_, time_query = t.test_query_many_times()

data = {"capacity": caps, "insert time": inserts, "query time": queries}
table = pd.DataFrame(data, index=range(1, 31 - 7 + 1), columns=["capacity", "insert time", "query time"])
print(table)
print(f"RTree insert time is {time_insert}, query time is{time_query}.")
line_data = pd.DataFrame({"insert time": inserts, "query time": queries}, index=caps)
line_data.plot(kind='line')

# caps.clear()
# inserts.clear()
# queries.clear()
# quantities.clear()
# for quantity in range(100, 1000, 100):
#     real_cap = max(4, math.ceil(NUM_RECTS / pow(4, 6)))
#     real_cap = math.ceil((real_cap + math.ceil(NUM_RECTS / 19)) / 2)
#     mt = PerformanceTest(real_cap)
#     hundreds_times, time_insert = mt.test_insert_many_times(quantity)
#     _, time_query = mt.test_query_many_times(quantity)
#     quantities.append(quantity)
#     caps.append(real_cap)
#     inserts.append(time_insert)
#     queries.append(time_query)
#
# data = {"capacity": caps, "nodes": quantities, "insert time": inserts, "query time": queries}
# table = pd.DataFrame(data, index=range(1, 10), columns=["capacity", "nodes", "insert time", "query time"])
# print(table)
# line_data = pd.DataFrame({"insert time": inserts, "query time": queries}, index=quantities)
# line_data.plot(kind="line")
plt.show()
