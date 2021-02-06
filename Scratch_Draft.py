from numpy.ma import sqrt
from math import acos
from math import radians
import numpy as np


class Experimental_Setup:
    def __init__(self, table, env):
        self.table = table
        self.env = env

    def move_table(self, dx, dy):
        self.table.move(dx, dy)

    def measure(self):
        return self.env.measure()


class Table:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        # шаг шарико-винтовой передачи Ph =1 [мм], среднее минимальное линейное перемещение l (х и y) можно определить по формуле
        dx = (0.1 * self.chip.rotate(self.mock_motor)) / (2 * 3.14)
        dy = (0.1 * self.chip.rotate(self.chip)) / (2 * 3.14)
        return dx, dy

    def get_coords(self):
        # ???
        pass

    pass


class MockMotor:
    def __init__(self, angle):
        self.angle = angle

    def rotate(self, angle):
        self.angle += 1
        return self.angle


class Environment:
    def __init__(self, mocktable, chip):
        self.table = mocktable
        self.chip = chip

    def move(self, dx, dy):
        self.table.move(dx, dy)

    def measure(self):
        return self.chip.value(self.table.x, self.table.y)


class Chip:
    def __init__(self, chip_array):
        self.chip_array = chip_array

    def screen(self):
        return self.chip_array

    # realization
    def value(self, x, y):
        return self.chip_array[x, y]


arr = np.array([[0, 3, 4, 0, 2],
                [5, 0, 0, 7, 3],
                [0, 4, 6, 9, 0],
                [0, 4, 5, 0, 2],
                [1, 0, 5, 4, 3]])
# массив 5х5 - плоскость с разными оптическими мощностями


motor_x = 0
motor_y = 1

chip = Chip(arr)
table = Table(motor_x, motor_y)
env = Environment(table, chip)
ex_setup = Experimental_Setup(table, env)

# print(chip.screen())
print(ex_setup.measure())

#print(chip.value(1, 3))
