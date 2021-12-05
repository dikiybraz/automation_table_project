import sys

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


class Converter:
    def __init__(self, rotate):
        self.rotate = rotate

    def delta_coord(self):
        return self.rotate * 0.01


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
class Search:
    def __init__(self, Experimental_Setup, Chip):
        self.Experimental_Setup = Experimental_Setup
        self.Chip = Chip

    def find(self):
        a = b = c = d = 0
        i = 0  # счетчик
        h = 1  #
        g = 1
        df_x1 = 0
        df_y1 = 0
        df_x2 = 0
        df_y2 = 0

        e = 1
        f = 1
        max = float(self.Experimental_Setup.measure())
        max1  = 0

        while True:
            self.Experimental_Setup.move_table(1, 1)
            # e = f = 1
            current_value = float(self.Experimental_Setup.measure())
            if max != current_value and max < current_value:
                self.Experimental_Setup.move_table(e, 0)
                a = float(self.Experimental_Setup.measure())
                self.Experimental_Setup.move_table(-e, f)
                b = float(self.Experimental_Setup.measure())
                self.Experimental_Setup.move_table(-e, -f)
                c = float(self.Experimental_Setup.measure())
                self.Experimental_Setup.move_table(e, -f)
                d = float(self.Experimental_Setup.measure())
                self.Experimental_Setup.move_table(0, f)

                df_x1 = (current_value - a) / e
                df_y1 = (current_value - b) / f
                df_x2 = (current_value - c) / e
                df_y2 = (current_value - d) / f

                if df_x1 < 0:
                    self.Experimental_Setup.move_table(e, 0)
                    max = float(self.Experimental_Setup.measure())
                elif df_y1 < 0:
                    self.Experimental_Setup.move_table(0, f)
                    max = float(self.Experimental_Setup.measure())
                elif df_x2 < 0:
                    self.Experimental_Setup.move_table(-e, 0)
                    max = float(self.Experimental_Setup.measure())
                elif df_y2 < 0:
                    self.Experimental_Setup.move_table(0, -f)
                    max = float(self.Experimental_Setup.measure())
                elif a > c and b > d:
                    if a > b:
                        self.Experimental_Setup.move_table(e, 0)
                        max = float(self.Experimental_Setup.measure())
                    else:
                        self.Experimental_Setup.move_table(0, f)
                        max = float(self.Experimental_Setup.measure())
                elif a < c and b < d:
                    if c > d:
                        self.Experimental_Setup.move_table(-e, 0)
                        max = float(self.Experimental_Setup.measure())
                    else:
                        self.Experimental_Setup.move_table(0, -f)
                        max = float(self.Experimental_Setup.measure())
                elif a > c and b < d:
                    if a > d:
                        self.Experimental_Setup.move_table(e, 0)
                        max = float(self.Experimental_Setup.measure())
                    else:
                        self.Experimental_Setup.move_table(0, -f)
                        max = float(self.Experimental_Setup.measure())
                elif b > d and a < c:
                    if b > c:
                        self.Experimental_Setup.move_table(0, f)
                        max = float(self.Experimental_Setup.measure())
                    else:
                        self.Experimental_Setup.move_table(-e, 0)
                        max = float(self.Experimental_Setup.measure())

            elif (current_value - max) < -1:

                self.Experimental_Setup.move_table(0, 50)
                current_value = float(self.Experimental_Setup.measure())
                self.Experimental_Setup.move_table(e, 0)
                a = float(self.Experimental_Setup.measure())
                self.Experimental_Setup.move_table(-e, f)
                b = float(self.Experimental_Setup.measure())
                self.Experimental_Setup.move_table(-e, -f)
                c = float(self.Experimental_Setup.measure())
                self.Experimental_Setup.move_table(e, -f)
                d = float(self.Experimental_Setup.measure())
                self.Experimental_Setup.move_table(0, f)

                df_x1 = (current_value - a) / e
                df_y1 = (current_value - b) / f
                df_x2 = (current_value - c) / e
                df_y2 = (current_value - d) / f

                if df_x1 < 0:
                    self.Experimental_Setup.move_table(e, 0)
                    max1 = float(self.Experimental_Setup.measure())
                elif df_y1 < 0:
                    self.Experimental_Setup.move_table(0, f)
                    max1 = float(self.Experimental_Setup.measure())
                elif df_x2 < 0:
                    self.Experimental_Setup.move_table(-e, 0)
                    max1 = float(self.Experimental_Setup.measure())
                elif df_y2 < 0:
                    self.Experimental_Setup.move_table(0, -f)
                    max1 = float(self.Experimental_Setup.measure())
                elif a > c and b > d:
                    if a > b:
                        self.Experimental_Setup.move_table(e, 0)
                        max1 = float(self.Experimental_Setup.measure())
                    else:
                        self.Experimental_Setup.move_table(0, f)
                        max1 = float(self.Experimental_Setup.measure())
                elif a < c and b < d:
                    if c > d:
                        self.Experimental_Setup.move_table(-e, 0)
                        max1 = float(self.Experimental_Setup.measure())
                    else:
                        self.Experimental_Setup.move_table(0, -f)
                        max1 = float(self.Experimental_Setup.measure())
                elif a > c and b < d:
                    if a > d:
                        self.Experimental_Setup.move_table(e, 0)
                        max1 = float(self.Experimental_Setup.measure())
                    else:
                        self.Experimental_Setup.move_table(0, -f)
                        max1 = float(self.Experimental_Setup.measure())
                elif b > d and a < c:
                    if b > c:
                        self.Experimental_Setup.move_table(0, f)
                        max1 = float(self.Experimental_Setup.measure())
                    else:
                        self.Experimental_Setup.move_table(-e, 0)
                        max1 = float(self.Experimental_Setup.measure())

            if max > max1:
                max = max
                print('current =', current_value, 'max =', max, 'df_x1 =', df_x1, 'df_y1 =', df_y1, 'df_x2 =', df_x2,
                      'df_y2 =', df_y2, 'a =', a, 'b = ', b, 'c= ', c, 'd = ', d, 'x = ',
                      self.Experimental_Setup.table.x, 'y = ', self.Experimental_Setup.table.y)
            else:
                max = max1
                print('current =', current_value, 'max =', max1, 'df_x1 =', df_x1, 'df_y1 =', df_y1, 'df_x2 =', df_x2,
                      'df_y2 =', df_y2, 'a =', a, 'b = ', b, 'c= ', c, 'd = ', d, 'x = ',
                      self.Experimental_Setup.table.x, 'y = ', self.Experimental_Setup.table.y)
            # else:
            #     break

            # if current_value > max:
            #
            #     self.Experimental_Setup.move_table(e * 2, 2 * f)
            #     max = current_value
            # elif max > current_value:
            #     self.Experimental_Setup.move_table(e, f)
            #     self.Experimental_Setup.move_table(-1, -1)
            #     if current_value - max < -100:
            #         self.Experimental_Setup.move_table(2*e, -f)
            #         h = e - 2
            #         g = f - 2
            # elif max == current_value:
            #     self.Experimental_Setup.move_table(1, 1)

            # if e <= 0:  # если С или D = 0 ,то мы возращаем предыдущее значение
            #     e = h
            # if f <= 0:
            #     f = g

            # if abs(self.Experimental_Setup.table.x) > 1000:
            #     e = -e
            # if abs(self.Experimental_Setup.table.y) > 2000:
            #     f = -f

            # смена напраления в зависимости от значений df_x и df_y, а также их знаков (+ или -)
            #             if 10 > df_x > 0 and 10 > df_y > 0:
            #                 if abs(df_y) > abs(df_x):
            #                     self.Experimental_Setup.move_table(-50, -50)
            #                     pass
            #                 elif abs(df_y) < abs(df_x):
            #                     self.Experimental_Setup.move_table(50, 50)
            #             elif -5 < df_x < 0 and 5 > df_y > 0:
            #                 self.Experimental_Setup.move_table(20, -20)
            #             elif 5 > df_x > 0 and -5 < df_y < 0:
            #                 self.Experimental_Setup.move_table(-20, 20)
            #             elif -10 < df_x < 0 and -10 < df_y < 0:
            #                 if abs(df_y) > abs(df_x):
            #                     self.Experimental_Setup.move_table(-50, -50)
            #                     pass
            #                 elif abs(df_y) < abs(df_x):
            #                     self.Experimental_Setup.move_table(50, 50)

            if df_y1 == df_x1 == df_y2 == df_x2 == 0:
                e *= 2
                f *= 2



            # print("После\n",current_value, max, df_y, df_x, self.Experimental_Setup.table.x, self.Experimental_Setup.table.y, "\n")


# процедура калибровки
# массив - плоскость с разными оптическими мощностями
motor_x = MockMotor(100)
motor_y = MockMotor(100)
dx = Converter(motor_x.rotate())
dy = Converter(motor_y.rotate())

chip = Chip('Coupler_Simulation_data_2000')
table = Table(motor_x, motor_y, int(dx.delta_coord()), int(dy.delta_coord()))
env = Environment(table, chip)
ex_setup = Experimental_Setup(table, env)
a = Search(ex_setup, chip)

a.find()
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
