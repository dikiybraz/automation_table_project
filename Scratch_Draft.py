from numpy.ma import sqrt
from math import acos
from math import radians
import numpy as np


class Experimental_Setup:
    def __init__(self, table, power_meter):
        self.table = table
        self.power_meter = power_meter

    def move_table(self, dx, dy):
        self.table.move(dx, dy)

    def measure(self):
        return self.power_meter.measure()

class Table:
    def __init__(self, motor_x, motor_y):
        self.motor_x = motor_x
        self.motor_y = motor_y

    def move(self, dx, dy):
        # шаг шарико-винтовой передачи Ph =1 [мм], среднее минимальное линейное перемещение l (х и y) можно определить по формуле
        ax = (0.1 * self.rotate(self.MockMotor.angle)) / (2 * 3.14)
        ay = (0.1 * self.rotate(self.MockMotor.angle)) / (2 * 3.14)
        return self.motor_x.rotate(ax), self.motor_y.rotate(ay)

    def get_coords(self):
        # ???
        pass

    pass

class MockMotor:  # 1
    def __init__(self, angle):
        self.angle = angle

    def rotate(self, angle):
        # При перемещении пьезоэлемента на 50 ангстрем ротор повернется на некоторый угол, который можно определить следующим образом:
        self.angle += 2 * ((angle * (1 * 10 ** (-11)) / 2) ^ 2)        # AB -  перемещение пьезолемента в ангстремах (50)
        # rotor_diametr = 14 мм (как пример взял модель 8321). диаметр ротора можно найти на офф сайте (возможно он другой

class Environment:
    def __init__(self, mocktable, chip):
        self.table = mocktable
        self.chip = chip

    def move(self, dx, dy):
        self.table.move(dx, dy)

    def measure(self):
        return self.chip.value(self.table.x, self.table.y)


class Chip:  # 2
    def __init__(self, chip_array):
        self.array = chip_array

    # realization
    def value(self, x, y):
        return self.array[x, y]

arr = np.array([[0, 2, 4, 0, 2],
                [2, 0, 0, 7, 3],
                [0, 4, 6, 9, 0],
                [0, 4, 5, 0, 2],
                [1, 0, 5, 4, 3]])
# массив 5х5 - плоскость с разными оптическими мощностями


motor_x = MockMotor(1)
motor_y = MockMotor(1)
chip = Chip(arr)
table = Table(motor_x, motor_y)
env = Environment(table, chip)
ex_setup = Experimental_Setup(table, env)

print(ex_setup.measure())
