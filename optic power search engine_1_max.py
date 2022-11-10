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


class Search:
    def __init__(self, Experimental_Setup, Chip):
        self.Experimental_Setup = Experimental_Setup
        self.Chip = Chip

    def calculation(self):

        self.Experimental_Setup.move(1, 1)
        # e = f = 1
        current_value = float(self.Experimental_Setup.measure())

        self.Experimental_Setup.move(e, 0)
        a = float(self.Experimental_Setup.measure())
        self.Experimental_Setup.move(-e, f)
        b = float(self.Experimental_Setup.measure())
        self.Experimental_Setup.move(-e, -f)
        c = float(self.Experimental_Setup.measure())
        self.Experimental_Setup.move(e, -f)
        d = float(self.Experimental_Setup.measure())
        self.Experimental_Setup.move(0, f)

        df_x1 = (current_value - a) / e
        df_y1 = (current_value - b) / f
        df_x2 = (current_value - c) / e
        df_y2 = (current_value - d) / f

        if df_x1 < 0:
            self.Experimental_Setup.move(e, 0)
            max = float(self.Experimental_Setup.measure())
        elif df_y1 < 0:
            self.Experimental_Setup.move(0, f)
            max = float(self.Experimental_Setup.measure())
        elif df_x2 < 0:
            self.Experimental_Setup.move(-e, 0)
            max = float(self.Experimental_Setup.measure())
        elif df_y2 < 0:
            self.Experimental_Setup.move(0, -f)
            max = float(self.Experimental_Setup.measure())
        elif a > c and b > d:
            if a > b:
                self.Experimental_Setup.move(e, 0)
                max = float(self.Experimental_Setup.measure())
            elif a == b:
                self.Experimental_Setup.move(e, f)
                max = float(self.Experimental_Setup.measure())
            else:
                self.Experimental_Setup.move(0, f)
                max = float(self.Experimental_Setup.measure())
        elif a < c and b < d:
            if c > d:
                self.Experimental_Setup.move(-e, 0)
                max = float(self.Experimental_Setup.measure())
            elif c == d:
                self.Experimental_Setup.move(-e, -f)
                max = float(self.Experimental_Setup.measure())
            else:
                self.Experimental_Setup.move(0, -f)
                max = float(self.Experimental_Setup.measure())
        elif a > c and b < d or (a == c and b < d):
            if a > d:
                self.Experimental_Setup.move(e, f)
                max = float(self.Experimental_Setup.measure())
            elif a == d:
                self.Experimental_Setup.move(e, -f)
                max = float(self.Experimental_Setup.measure())
            else:
                self.Experimental_Setup.move(-e, -f)
                max = float(self.Experimental_Setup.measure())
        elif (b > d and a < c) or (a == c and b > d):
            if b > c:
                self.Experimental_Setup.move(0, f)
                max = float(self.Experimental_Setup.measure())
            elif c == b:
                self.Experimental_Setup.move(-e, f)
                max = float(self.Experimental_Setup.measure())
            else:
                self.Experimental_Setup.move(-e, 0)
                max = float(self.Experimental_Setup.measure())
        elif a == b == c == d != 0:
            self.Experimental_Setup.move(-3 * e, f)
            max = float(self.Experimental_Setup.measure())
        return max


    def find(self):
        a = b = c = d = 0
        i = 0  # счетчик
        h, g = 1, 1
        n = 0
        df_x1, df_y1, df_x2, df_y2 = 0, 0, 0, 0
        x_max, y_max = 0, 0
        x_max1, y_max1 = 0, 0

        e, f = 1, 1
        h, g = 0, 0

        max = float(self.Experimental_Setup.measure())
        max_power = float(0)
        max_optic_power_1 = 0
        max_optic_power_2 = 0

        while True:
            # Итерация 1: поиск первого максимума
            self.Experimental_Setup.move(1, 1)
            # e = f = 1
            current_value = float(self.Experimental_Setup.measure())

            self.Experimental_Setup.move(e, 0)
            a = float(self.Experimental_Setup.measure())
            self.Experimental_Setup.move(-e, f)
            b = float(self.Experimental_Setup.measure())
            self.Experimental_Setup.move(-e, -f)
            c = float(self.Experimental_Setup.measure())
            self.Experimental_Setup.move(e, -f)
            d = float(self.Experimental_Setup.measure())
            self.Experimental_Setup.move(0, f)

            df_x1 = (current_value - a) / e
            df_y1 = (current_value - b) / f
            df_x2 = (current_value - c) / e
            df_y2 = (current_value - d) / f

            if df_x1 < 0:
                self.Experimental_Setup.move(e, 0)
                max = float(self.Experimental_Setup.measure())
            elif df_y1 < 0:
                self.Experimental_Setup.move(0, f)
                max = float(self.Experimental_Setup.measure())
            elif df_x2 < 0:
                self.Experimental_Setup.move(-e, 0)
                max = float(self.Experimental_Setup.measure())
            elif df_y2 < 0:
                self.Experimental_Setup.move(0, -f)
                max = float(self.Experimental_Setup.measure())
            elif a > c and b > d:
                if a > b:
                    self.Experimental_Setup.move(e, 0)
                    max = float(self.Experimental_Setup.measure())
                elif a == b:
                    self.Experimental_Setup.move(e, f)
                    max = float(self.Experimental_Setup.measure())
                else:
                    self.Experimental_Setup.move(0, f)
                    max = float(self.Experimental_Setup.measure())
            elif a < c and b < d:
                if c > d:
                    self.Experimental_Setup.move(-e, 0)
                    max = float(self.Experimental_Setup.measure())
                elif c == d:
                    self.Experimental_Setup.move(-e, -f)
                    max = float(self.Experimental_Setup.measure())
                else:
                    self.Experimental_Setup.move(0, -f)
                    max = float(self.Experimental_Setup.measure())
            elif a > c and b < d or (a == c and b < d):
                if a > d:
                    self.Experimental_Setup.move(e, f)
                    max = float(self.Experimental_Setup.measure())
                elif a == d:
                    self.Experimental_Setup.move(e, -f)
                    max = float(self.Experimental_Setup.measure())
                else:
                    self.Experimental_Setup.move(-e, -f)
                    max = float(self.Experimental_Setup.measure())
            elif (b > d and a < c) or (a == c and b > d):
                if b > c:
                    self.Experimental_Setup.move(0, f)
                    max = float(self.Experimental_Setup.measure())
                elif c == b:
                    self.Experimental_Setup.move(-e, f)
                    max = float(self.Experimental_Setup.measure())
                else:
                    self.Experimental_Setup.move(-e, 0)
                    max = float(self.Experimental_Setup.measure())
            elif a == b == c == d != 0:
                self.Experimental_Setup.move(-3 * e, f)
                max = float(self.Experimental_Setup.measure())

            if (max_power - max) == 1:  # если максимум долго не обновляется, то мы запускаем счетчик
                n = n + 1
                max_optic_power_1 = max_power
                x_max = float(self.Experimental_Setup.table.x)
                y_max = float(self.Experimental_Setup.table.y)
            elif n == 1:  # при его первом изменении фиксируем первый максимум и резко проверяем другую часть поля
                self.Experimental_Setup.move(e * 100, f * 100)
                current_value = float(self.Experimental_Setup.measure())

            elif n >= 2:  # при двойном увеличении мы запускаем дополнитльный поиск вокруг текущей координаты: рассматриваются два варианта
                if (max_power - max) >= 2:
                    # условие длительности проверки подлинности второго максимума в зависимости от количества итераций
                    print(f'optic_power_maximum 1 ', max_optic_power_1, 'x =', x_max, 'y=', y_max)
                    # print('optic_power_maximum 2=', max_optic_power_2, 'x =', x_max1, 'y=', y_max1)
                    break

            if max >= current_value:
                max = max

                if max > max_power:
                    max_power = max
                # print('current =', current_value, 'max =', max, 'x = ', self.Environment.table.x, 'y = ',
                #       self.Environment.table.y, 'n =', n, max_power)
                # print('current =', current_value, 'max =', max, 'df_x1 =', df_x1, 'df_y1 =', df_y1, 'df_x2 =', df_x2,
                #       'df_y2 =', df_y2, 'a =', a, 'b = ', b, 'c= ', c, 'd = ', d, 'x = ',
                #       self.Environment.table.x, 'y = ', self.Environment.table.y)
            else:
                max = current_value

                if max >= max_power:
                    max_power = max
                # print('current =', current_value, 'max =', max, 'x = ', self.Environment.table.x, 'y = ',
                #       self.Environment.table.y, 'n = ', n, max_power)
                # print('current =', current_value, 'max =', max, 'df_x1 =', df_x1, 'df_y1 =', df_y1, 'df_x2 =', df_x2,
                #       'df_y2 =', df_y2, 'a =', a, 'b = ', b, 'c= ', c, 'd = ', d, 'x = ',
                #       self.Environment.table.x, 'y = ', self.Environment.table.y)

            if df_y1 == df_x1 or df_y2 == df_x2:
                e += 2
                f += 2
            else:
                e = 1
                f = 1


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
