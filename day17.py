
from dataclasses import dataclass
from collections import namedtuple
from functools import lru_cache


def x_position(initial_position, initial_velocity, time):
    pos = initial_position
    vel = initial_velocity
    acc = 1 if initial_velocity < 0 else -1
    for _ in range(time, 0, -1):
        if vel == 0:
            return pos
        pos += vel
        vel += acc
    return pos


def y_position(initial_position, initial_velocity, time, acc=-1):
    pos = initial_position
    vel = initial_velocity
    for _ in range(time, 0, -1):
        pos += vel
        vel += acc
    return pos

def position_after(initial_position, velocity_x, velocity_y, time):
    return {
        "x": x_position(initial_position, velocity_x, time),
        "y": y_position(initial_position, velocity_y, time),
    }


@dataclass
class Target:
    x1: int
    x2: int
    y1: int
    y2: int

    @property
    def y_range(self):
        return range(self.y1, self.y2)

    @property
    def max_y(self):
        return max(self.y1, self.y2)

    @property
    def x_range(self):
        return range(self.x1, self.x2)

    @property
    def max_x(self):
        return max(self.x1, self.x2)

    def hit_by_after(self, iv, xv, yv, t):
        pos = position_after(iv, xv, yv, t)
        return self.in_side_x(pos["x"]) and self.in_side_y(pos["y"])

    def in_side_x(self, x):
        if self.x1 < self.x2:
            return x >= self.x1 and x <= self.x2
        else:
            return x <= self.x1 and x >= self.x2

    def in_side_y(self, y):
        if self.y1 < self.y2:
            return y >= self.y1 and y <= self.y2
        else:
            return y <= self.y1 and y >= self.y2


def solve(target: Target):

    print(target)

    heights = []

    vmax = 100
    for iv in range(0, vmax):
        for iy in range(0, vmax):
            ttih = times_target_is_hit(target, 0, iv, iy)
            if ttih:
                max_height = max_height_after(ttih, 0, iv, iy)
                heights.append(max_height)

    return max(heights)


def process_instructions(test_data):

    x_data, y_data = test_data.split(", ")
    x_data = x_data[2:].split("..")
    y_data = y_data[2:].split("..")

    x1, x2 = int(x_data[0]), int(x_data[1])
    y1, y2 = int(y_data[0]), int(y_data[1])

    t = Target(x1, x2, y1, y2)

    return solve(t)


def max_height_after(times, i, iv, iy):
    heights = []
    for hit_time in times:
        for t in range(0, hit_time):
            pos = position_after(i, iv, iy, t)
            heights.append(pos["y"])
    return max(heights)


def times_target_is_hit(target, iv, vx, vy, tmax=250):
    times = []
    has_been_hit = None
    for t in range(0, tmax):
        hit = target.hit_by_after(iv, vx, vy, t)
        if hit:
            times.append(t)
            has_been_hit = True
        else:
            if has_been_hit is True:
                return times
    return times


def test_day_short_input1():

    assert y_position(0, 2, 0) == 0
    assert y_position(0, 2, 1) == 2
    assert y_position(0, 2, 2) == 3
    assert y_position(0, 2, 3) == 3
    assert y_position(0, 2, 4) == 2
    assert y_position(0, 2, 5) == 0
    assert y_position(0, 2, 6) == -3
    assert y_position(0, 2, 7) == -7

    assert x_position(0, 7, 0) == 0
    assert x_position(0, 7, 1) == 7
    assert x_position(0, 7, 2) == 13
    assert x_position(0, 7, 3) == 18
    assert x_position(0, 7, 4) == 22
    assert x_position(0, 7, 5) == 25
    assert x_position(0, 7, 6) == 27
    assert x_position(0, 7, 7) == 28
    assert x_position(0, 7, 8) == 28
    assert x_position(0, 7, 9) == 28
    assert x_position(0, 7, 10) == 28


def test_day_short_input11():

    assert position_after(0, 2, 2, 0) == {"x": 0, "y": 0}
    assert position_after(0, 7, 2, 7) == {"x": 28, "y": -7}
    assert position_after(0, 6, 3, 9) == {"x": 21, "y": -9}
    assert position_after(0, 9, 0, 4) == {"x": 30, "y": -6}


def test_day_short_input12():

    assert position_after(0, -2, 2, 0) == {"x": 0, "y": 0}
    assert position_after(0, -7, 2, 7) == {"x": -28, "y": -7}
    assert position_after(0, -6, 3, 9) == {"x": -21, "y": -9}
    assert position_after(0, -9, 0, 4) == {"x": -30, "y": -6}


def test_day_short_input2():
    target = Target(x1=20, x2=30, y1=-10, y2=-5)
    assert target.hit_by_after(0, 7, 2, 7)
    assert target.hit_by_after(0, 6, 3, 9)
    assert target.hit_by_after(0, 9, 0, 4)
    
    assert not target.hit_by_after(0, 2, 2, 0)
    for t in range(1, 11):
        assert not target.hit_by_after(0, -7, -14, t)


def test_day_short_input3():
    target = Target(x1=20, x2=30, y1=-10, y2=-5)
    times = times_target_is_hit(target, 0, 6, 9) 
    assert times == [20]
    assert max_height_after(times, 0, 6, 9) == 45


def test_day_short_input4():
    target = Target(x1=-30, x2=-20, y1=-10, y2=-5)
    times = times_target_is_hit(target, 0, -6, 9) 
    assert times == [20]
    assert max_height_after(times, 0, -6, 9) == 45


def test_day_short_input():
    test_instructions = "x=20..30, y=-10..-5"
    result = process_instructions(test_instructions)
    assert result == 45


def test_day_real_input_viper():
    test_instructions = "x=209..238, y=-86..-59"
    result = process_instructions(test_instructions)
    assert result == 3655


def test_day_real_input():
    test_instructions = "x=81..129, y=-150..-108"
    result = process_instructions(test_instructions)
    assert result == 11175


if __name__ == "__main__":
    test_day_short_input()
    test_day_real_input()
    #test_day_real_input_viper()