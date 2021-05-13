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


class Max:
    def __init__(self, Experimental_Setup, Chip):
        self.Experimental_Setup = Experimental_Setup
        self.Chip = Chip

    def find(self):
        i = 0  # счетчик
        arr = []
        max = 0

        new_file = open('check_values.txt', 'w+')

        for value in self.Chip.array:
            i = 0
            for i in range(29):
                current_value = float(self.Experimental_Setup.measure())
                self.Experimental_Setup.move_table(1, 0)
                if current_value > max:
                    max = current_value
                    # print(max)

            self.Experimental_Setup.move_table(-29, 1)
            new_file.write('\n')

        print(max)
        new_file.close()

        return new_file

# массив - плоскость с разными оптическими мощностями
motor_x = MockMotor(0)
motor_y = MockMotor(0)
chip = Chip('Coupler_Simulation_data')
table = Table(motor_x, motor_y, 0, 0)
env = Environment(table, chip)
ex_setup = Experimental_Setup(table, env)

# print(chip.value(7,5))
# print(ex_setup.measure())

#print(chip.array)

# ex_setup.move_table(10, 10)
# print(ex_setup.measure())
# print(ex_setup.move_table(6, 4))
# print(ex_setup.measure())
# print(ex_setup.move_table(-6, -4))
# print(ex_setup.measure())

a = Max(ex_setup, chip)
print(a.find())
