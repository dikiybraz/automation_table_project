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
        self.motor_x.rotate(ax)
        self.motor_y.rotate(ay)

    def get_coords(self):
        # ???
        pass

    pass


class MockMotor:  # 1
    def __init__(self, angle):
        self.angle = angle
        pass

    def rotate(self, angle):
        # При перемещении пьезоэлемента на 50 ангстрем ротор повернется на некоторый угол, который можно определить следующим образом:
        self.angle += 2 * acos(14 / (sqrt(14 ** 2) + ((angle * (1 * 10 ** (-11)) / 2) ^ 2)))
        # AB -  перемещение пьезолемента в ангстремах (50)
        # rotor_diametr = 14 мм (как пример взял модель 8321). диаметр ротора можно найти на офф сайте (возможно он другой

    pass


class Environment:
    def __init__(self, mocktable, chip):
        self.table = mocktable
        self.chip = chip

    def move(self, dx, dy):
        self.table.move(dx, dy)

    def measure(self):
        return self.chip.value(self.table.x, self.table.y)

    # def rotate(self):
    #   return self.mockmotor.rotate()
    # pass


class Chip:  # 2
    def __init__(self, chip_array):
        self.array = chip_array

    def get_coords(self, array):
        x, y = np.where(self.array == self.get_measure.value)
        return x, y

    # realization
    def value(self, x, y):
        self.x += self.chip.value()
        pass


class PowerMeter:
    def __init__(self, x, y, array):
        self.array = array
        pass

    def get_measure(self, x, y, array):
        l = len(self.array)
        for i in range(l):
            value = np.max(self.array(x, y))

        return value

    pass


arr = np.array([[0, 2, 4, 0, 2],
                [2, 0, 0, 7, 3],
                [0, 4, 6, 9, 0],
                [0, 4, 5, 0, 2],
                [1, 0, 5, 4, 3]])
# массив 5х5 - плоскость с разными оптическими мощностями

ex_setup = Experimental_Setup()
motor_x = MockMotor()
motor_y = MockMotor()
chip = Chip(arr)
table = Table(motor_x, motor_y)
env = Environment(motor_x, motor_y, table, chip)
pwr = PowerMeter()

pwr.get_measure(3, 4, arr)  # вывод максимального значения
chip.get_coords(arr)  # вывод координат
