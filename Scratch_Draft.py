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
    def __init__(self, motor_x, motor_y):
        self.motor_x = motor_x
        self.motor_y = motor_y

    def move(self, x, y):
        # шаг шарико-винтовой передачи Ph =1 [мм], среднее минимальное линейное перемещение l (х и y) можно
        # определить по формуле

        dx = (0.1 * self.motor_x.rotate(self.motor_x.angle)) / (2 * 3.14)
        dy = (0.1 * self.motor_y.rotate(self.motor_y.angle)) / (2 * 3.14)

        x = x + dx
        y = y + dy

        return [x, y]

    def get_coords(self):
        # ???
        pass

    pass


class MockMotor:
    def __init__(self, angle):
        self.angle = angle

    def rotate(self, angle):
        angle = angle + 0.01
        return angle


class Environment:
    def __init__(self, mocktable, chip):
        self.table = mocktable
        self.chip = chip

    def move(self, dx, dy):
        return self.table.move(dx, dy)

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
motor_x = MockMotor(0)
motor_y = MockMotor(1)
chip = Chip(arr)
table = Table(motor_x, motor_y)
env = Environment(table, chip)
ex_setup = Experimental_Setup(table, env)

# проверка класс environment
# print(ex_setup.measure())  #done
# print(ex_setup.move_table())

# проверка класс environment
# print(env.move(4, 3)) # Done
# print(env.measure())

# проверка класса Table
# print(table.move(2, 1)) # done

# проверка класса чип
# print(chip.value(1, 3)) # done
# print(chip.screen()) # done

# проверка класса мотор
# print(motor_x.rotate(0.11)) # done

