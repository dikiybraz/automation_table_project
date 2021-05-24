import self as self
from numpy.ma import sqrt
from math import acos
from math import radians
import os
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
    def __init__(self, motor_x, motor_y, x, y):
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
    def __init__(self, filename):
        self.array = self.read_from_file(filename)

    def read_from_file(self, filename):
        file = open(str(filename) + '.txt', 'r')
        lines = file.readlines()
        rows = []

        for line in lines:
            columns = []
            for value in line.split():
                columns.append(float(value))
            rows.append(columns)

        file.close()
        return rows

    def value(self, x, y):
        return self.array[y][x]


# class check_plato:
#     def __init__(self, Experimental_Setup, a, b):
#         self.Experimental_Setup = Experimental_Setup
#         self.a = a
#         self.b = b
#         pass
#
#     def check(self, a, b):
#         if self.a == self.b:
#             self.Experimental_Setup.table.move_table(3, 4)
#         else:
#             pass


class Max:
    def __init__(self, Experimental_Setup, Chip):
        self.Experimental_Setup = Experimental_Setup
        self.Chip = Chip

    # def f(self, x, y):
    #     return self.Experimental_Setup.table.x * self.Experimental_Setup.table.x + self.Experimental_Setup.table.y * self.Experimental_Setup.table.y
    #
    # def df_x(self, x):
    #     return round(0.05 * self.Experimental_Setup.table.x)
    #
    # def df_y(self, y):
    #     return round(0.01 * self.Experimental_Setup.table.y)

    def find(self):
        i = 0  # счетчик

        # new_file = open('check_values.txt', 'w+')
        c = 1
        d = 1
        max = float(self.Experimental_Setup.measure())

        while True:

            current_value = float(self.Experimental_Setup.measure())

            if current_value > max:
                max = current_value
            elif max > current_value:
                i += 1
                if i == 5:
                    break

            self.Experimental_Setup.move_table(c, 0)
            a = float(self.Experimental_Setup.measure())
            self.Experimental_Setup.move_table(-c, c)
            b = float(self.Experimental_Setup.measure())

            df_x = (max - a) / c
            df_y = (max - b) / d

            print(current_value, max, self.Experimental_Setup.table.x, self.Experimental_Setup.table.y)

            # self.Experimental_Setup.move_table(self.df_x(self.Experimental_Setup.table.x), self.df_y(self.Experimental_Setup.table.y))
            # current_value = float(self.Experimental_Setup.measure())

            if abs(df_y) > abs(df_x):
                pass
            else:
                i = 0
                self.Experimental_Setup.move_table(c, -d)

            if df_y == 0 and df_x == 0:
                c *= 2
                d += 2






# процедура калибровки

# массив - плоскость с разными оптическими мощностями
motor_x = MockMotor(0)
motor_y = MockMotor(0)
chip = Chip('Coupler_Simulation_data_1000')
table = Table(motor_x, motor_y, 1, 1)
env = Environment(table, chip)
ex_setup = Experimental_Setup(table, env)

# print(chip.value(7,5))
# print(ex_setup.measure())

# print(chip.array)
#
#
#
#
#
#
#
# ex_setup.move_table(10, 10)
# print(ex_setup.measure())
# print(ex_setup.move_table(6, 4))
# print(ex_setup.measure())
# print(ex_setup.move_table(-6, -4))
# print(ex_setup.measure())

a = Max(ex_setup, chip)
a.find()

