from numpy.ma import sqrt
from math import acos
from math import radians
import numpy as np
class Experimental_Setup:
    def __init__(self, table, env):
        self.table = table
        self.env = env

    def move_table(self, dx, dy):
        self.env.move(dx, dy)

    def measure(self):
        return self.env.measure()

class Environment:
    def __init__(self, table, chip):
        self.table = table
        self.chip = chip

    def move(self, dx, dy):
        self.table.move(dx, dy)

    def measure(self):
        return self.chip.value(self.table.x, self.table.y)


class Table:
    def __init__(self, motor_x, motor_y , x , y):
        self.motor_x = motor_x
        self.motor_y = motor_y
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy



class MockMotor:
    def __init__(self, angle):
        self.angle = angle

    def rotate(self):
        return self.angle + 1

class Chip:
    def __init__(self, chip_array):
        self.chip_array = chip_array

    def screen(self):
        return self.chip_array

    # realization
    def value(self, x, y):
        return self.chip_array[x, y]


arr = np.array([])
# массив 5х5 - плоскость с разными оптическими мощностями

motor_x = MockMotor(3)
motor_y = MockMotor(4)
chip = Chip(arr)
table = Table(motor_x, motor_y, 1, 1)
env = Environment(table, chip)
ex_setup = Experimental_Setup(table, env)

print(ex_setup.measure())
print(ex_setup.move_table(1, 1))
print(ex_setup.measure())