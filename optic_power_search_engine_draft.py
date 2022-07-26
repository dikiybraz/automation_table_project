from pylablib.devices import Newport
import time
import os
import subprocess

# ______check_piezomotors_connection_AND_REMOTE_CONTROL___________
stage1 = Newport.picomotor.Picomotor8742(0)
stage1.autodetect_motors()
stage1.set_motor_type("all", "standard", None)


def test_map_walking(count, coordinates):
    # функция прохода по площади чипа по полученным из GDS файла координатам

    print(f' {count} итерация')
    print('position before:[', stage1.get_position(1), stage1.get_position(2), ']\n')  # проверка положения моторов

    time.sleep(2)

    stage1.move_by(1, coordinates[0])
    time.sleep(1)
    stage1.wait_move(1)
    stage1.move_by(2, coordinates[1])
    stage1.wait_move(2)

    print('geolocation:[', stage1.get_position(1), stage1.get_position(2), ']')
    print('\n')
    time.sleep(1)


class Inner_values:
    def __init__(self, filename):
        self.array = self.read_coords_from_file(filename)

    def read_coords_from_file(self, filename):

        file = open(str(filename) + '.txt', 'r')
        maps = file.readlines()
        # print(maps)

        for lines in maps:
            lines = lines[2:-2]
            lines = lines.replace('], [', '\n')
            coords = []
            for row in lines.split('\n'):
                for value in row.split(','):
                    coords.append(float(value))

        delta = []

        for i in range(23):
            dx = coords[2 * i + 2] - coords[2 * i]
            dy = coords[2 * i + 3] - coords[2 * i + 1]
            delta.append((dx, dy))

        return delta


# _____________RESEARCH_TABLE_EQUIPMENT_____________________
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

        stage1.move_by(1, dx)
        time.sleep(0.01)
        self.y += dy
        stage1.move_by(2, dy)
        time.sleep(0.01)
        print('position:[', stage1.get_position(1), stage1.get_position(2), ']\n')
        time.sleep(0.01)


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


# ____________PIEZOMOTOR_CONTROL_SYSTEM_________________
class Motor:
    def __init__(self, angle):
        self.angle = angle

    def rotate(self):
        return self.angle + 1


class Converter:
    def __init__(self, rotate):
        self.rotate = rotate

    def delta_coord(self):
        return self.rotate * 0.01


# _________________________________
class Search:
    def __init__(self, Environment, Chip):
        self.Environment = Environment
        self.Chip = Chip

    def find(self):
        a = b = c = d = 0
        i = 0  # счетчик
        h = 1  #
        g = 1
        n = 0
        df_x1 = 0
        df_y1 = 0
        df_x2 = 0
        df_y2 = 0
        x_max = 0
        x_max1 = 0
        y_max = 0
        y_max1 = 0

        e = 1
        f = 1
        h = 0
        g = 0
        max = float(self.Environment.measure())
        max_power = float(0)
        max_optic_power_1 = 0
        max_optic_power_2 = 0

        while True:
            # Итерация 1: поиск первого максимума
            self.Environment.move(1, 1)
            # e = f = 1
            current_value = float(self.Environment.measure())

            self.Environment.move(e, 0)
            a = float(self.Environment.measure())
            self.Environment.move(-e, f)
            b = float(self.Environment.measure())
            self.Environment.move(-e, -f)
            c = float(self.Environment.measure())
            self.Environment.move(e, -f)
            d = float(self.Environment.measure())
            self.Environment.move(0, f)

            df_x1 = (current_value - a) / e
            df_y1 = (current_value - b) / f
            df_x2 = (current_value - c) / e
            df_y2 = (current_value - d) / f

            if df_x1 < 0:
                self.Environment.move(e, 0)
                max = float(self.Environment.measure())
            elif df_y1 < 0:
                self.Environment.move(0, f)
                max = float(self.Environment.measure())
            elif df_x2 < 0:
                self.Environment.move(-e, 0)
                max = float(self.Environment.measure())
            elif df_y2 < 0:
                self.Environment.move(0, -f)
                max = float(self.Environment.measure())
            elif a > c and b > d:
                if a > b:
                    self.Environment.move(e, 0)
                    max = float(self.Environment.measure())
                elif a == b:
                    self.Environment.move(e, f)
                    max = float(self.Environment.measure())
                else:
                    self.Environment.move(0, f)
                    max = float(self.Environment.measure())
            elif a < c and b < d:
                if c > d:
                    self.Environment.move(-e, 0)
                    max = float(self.Environment.measure())
                elif c == d:
                    self.Environment.move(-e, -f)
                    max = float(self.Environment.measure())
                else:
                    self.Environment.move(0, -f)
                    max = float(self.Environment.measure())
            elif a > c and b < d or (a == c and b < d):
                if a > d:
                    self.Environment.move(e, f)
                    max = float(self.Environment.measure())
                elif a == d:
                    self.Environment.move(e, -f)
                    max = float(self.Environment.measure())
                else:
                    self.Environment.move(-e, -f)
                    max = float(self.Environment.measure())
            elif (b > d and a < c) or (a == c and b > d):
                if b > c:
                    self.Environment.move(0, f)
                    max = float(self.Environment.measure())
                elif c == b:
                    self.Environment.move(-e, f)
                    max = float(self.Environment.measure())
                else:
                    self.Environment.move(-e, 0)
                    max = float(self.Environment.measure())
            elif a == b == c == d != 0:
                self.Environment.move(-3 * e, f)
                max = float(self.Environment.measure())

            if (max_power - max) == 1:  # если максимум долго не обновляется, то мы запускаем счетчик
                n = n + 1
                max_optic_power_1 = max_power
                x_max = float(self.Environment.table.x)
                y_max = float(self.Environment.table.y)
            elif n == 1:  # при его первом изменении фиксируем первый максимум и резко проверяем другую часть поля
                self.Environment.move(e * 100, f * 100)
                current_value = float(self.Environment.measure())

            elif n > 2:  # при двойном увеличении мы запускаем дополнитльный поиск вокруг текущей координаты: рассматриваются два варианта
                if (max_power - max) >= 15:
                    # 1-й вариант: если текущее значение мощности много меньше фиксированного значения, то
                    # мы увеличиваем поле поиска в 10 раз
                    e = 2
                    f = 2
                    self.Environment.move(e, 4 * f)

                    current_value = float(self.Environment.measure())

                    self.Environment.move(10 * e, 0)
                    a = float(self.Environment.measure())
                    self.Environment.move(-10 * e, 10 * f)
                    b = float(self.Environment.measure())
                    self.Environment.move(-10 * e, -10 * f)
                    c = float(self.Environment.measure())
                    self.Environment.move(10 * e, -10)
                    d = float(self.Environment.measure())
                    self.Environment.move(0, 10 * f)
                    e = 1
                    f = 1

                    df_x1 = (current_value - a) / e
                    df_y1 = (current_value - b) / f
                    df_x2 = (current_value - c) / e
                    df_y2 = (current_value - d) / f

                    if df_x1 < 0:
                        self.Environment.move(10 * e, 0)
                        max = float(self.Environment.measure())
                    elif df_y1 < 0:
                        self.Environment.move(0, 10 * f)
                        max = float(self.Environment.measure())
                    elif df_x2 < 0:
                        self.Environment.move(-10 * e, 0)
                        max = float(self.Environment.measure())
                    elif df_y2 < 0:
                        self.Environment.move(0, -10 * f)
                        max = float(self.Environment.measure())
                    elif a > c and b > d:
                        if a > b:
                            self.Environment.move(10 * e, 0)
                            max = float(self.Environment.measure())
                        else:
                            self.Environment.move(0, 10 * f)
                            max = float(self.Environment.measure())
                    elif a < c and b < d:
                        if c > d:
                            self.Environment.move(-10 * e, 0)
                            max = float(self.Environment.measure())
                        else:
                            self.Environment.move(0, -10 * f)
                            max = float(self.Environment.measure())
                    elif a > c and b < d or (a == c and b < d):
                        if a > d:
                            self.Environment.move(10 * e, 10 * f)
                            max = float(self.Environment.measure())
                        elif a == d:
                            self.Environment.move(10 * e, -10 * f)
                            max = float(self.Environment.measure())
                        else:
                            self.Environment.move(0, -10 * f)
                            max = float(self.Environment.measure())
                    elif (b > d and a < c) or (a == c and b > d):
                        if b > c:
                            self.Environment.move(0, 10 * f)
                            max = float(self.Environment.measure())
                        elif c == d:
                            self.Environment.move(-10 * e, 10 * f)
                            max = float(self.Environment.measure())
                        else:
                            self.Environment.move(-10 * e, 0)
                            max = float(self.Environment.measure())
                    elif a == b == c == d != 0:
                        self.Environment.move(-3 * e, f)
                        max = float(self.Environment.measure())

                    if (max_power - current_value) >= 1000:
                        # здесь мы проверяем есть ли резкое уменьшение текущего значения относительно новой оптической мощности (если она вообще изменилась), счетчик снова работает
                        n = n + 1
                        max_optic_power_2 = max_power
                        if n > 20:
                            # условие длительности проверки подлинности второго максимума в зависимости от количества итераций
                            print('optic_power_maximum 1=', max_optic_power_1)
                            print('optic_power_maximum 2=', max_optic_power_2)
                            break
                elif max_power - max <= 15:
                    # 2-й вариант: если текущее значение мощности имеет небольшое отклонение от фиксированного значения, то
                    # мы уменьшим поле поиска в 10 раз
                    e = 1
                    f = 1

                    self.Environment.move(-8 * e, -f)

                    current_value = float(self.Environment.measure())

                    self.Environment.move(e, 0)
                    a = float(self.Environment.measure())
                    self.Environment.move(-e, f)
                    b = float(self.Environment.measure())
                    self.Environment.move(-e, -f)
                    c = float(self.Environment.measure())
                    self.Environment.move(e, -f)
                    d = float(self.Environment.measure())
                    self.Environment.move(0, f)

                    df_x1 = (current_value - a) / e
                    df_y1 = (current_value - b) / f
                    df_x2 = (current_value - c) / e
                    df_y2 = (current_value - d) / f

                    if df_x1 < 0:
                        self.Environment.move(e, 0)
                        max = float(self.Environment.measure())
                    elif df_y1 < 0:
                        self.Environment.move(0, f)
                        max = float(self.Environment.measure())
                    elif df_x2 < 0:
                        self.Environment.move(-e, 0)
                        max = float(self.Environment.measure())
                    elif df_y2 < 0:
                        self.Environment.move(0, -f)
                        max = float(self.Environment.measure())
                    elif a > c and b > d:
                        if a > b:
                            self.Environment.move(e, 0)
                            max = float(self.Environment.measure())
                        else:
                            self.Environment.move(0, f)
                            max = float(self.Environment.measure())
                    elif a < c and b < d:
                        if c > d:
                            self.Environment.move(-e, 0)
                            max = float(self.Environment.measure())
                        else:
                            self.Environment.move(0, -f)
                            max = float(self.Environment.measure())
                    elif a > c and b < d or (a == c and b < d):
                        if a > d:
                            self.Environment.move(e, 0)
                            max = float(self.Environment.measure())
                        elif a == d:
                            self.Environment.move(e, f)
                            max = float(self.Environment.measure())
                        else:
                            self.Environment.move(0, -f)
                            max = float(self.Environment.measure())
                    elif (b > d and a < c) or (a == c and b > d):
                        if b > c:
                            self.Environment.move(0, f)
                            max = float(self.Environment.measure())
                        elif c == b:
                            self.Environment.move(-e, f)
                            max = float(self.Environment.measure())
                        else:
                            self.Environment.move(-e, 0)
                            max = float(self.Environment.measure())
                    elif a == b == c == d != 0:
                        self.Environment.move(-2 * e, f)
                        max = float(self.Environment.measure())

                    if (max_power == current_value):
                        max_optic_power_2 = max_power
                        x_max1 = float(self.Environment.table.x)
                        y_max1 = float(self.Environment.table.y)
                    if (max_power - current_value) >= 1000:
                        # здесь мы проверяем есть ли резкое уменьшение текущего значения относительно новой оптической мощности (если она вообще изменилась), счетчик снова работает
                        n = n + 1
                        if n > 20:
                            # условие длительности проверки подлинности второго максимума в зависимости от количества итераций
                            print('optic_power_maximum 1=', max_optic_power_1, 'x =', x_max, 'y=', y_max)
                            print('optic_power_maximum 2=', max_optic_power_2, 'x =', x_max1, 'y=', y_max1)
                            break

            if max >= current_value:
                max = max

                if max > max_power:
                    max_power = max
                print('current =', current_value, 'max =', max, 'x = ', self.Environment.table.x, 'y = ',
                      self.Environment.table.y, 'n =', n, max_power)
                # print('current =', current_value, 'max =', max, 'df_x1 =', df_x1, 'df_y1 =', df_y1, 'df_x2 =', df_x2,
                #       'df_y2 =', df_y2, 'a =', a, 'b = ', b, 'c= ', c, 'd = ', d, 'x = ',
                #       self.Environment.table.x, 'y = ', self.Environment.table.y)
            else:
                max = current_value

                if max >= max_power:
                    max_power = max
                print('current =', current_value, 'max =', max, 'x = ', self.Environment.table.x, 'y = ',
                      self.Environment.table.y, 'n = ', n, max_power)
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
# обявление входных данных для поиска максимума по файлу
motor_x = Motor(100)
motor_y = Motor(100)
dx = Converter(motor_x.rotate())
dy = Converter(motor_y.rotate())

chip = Chip('Coupler_Simulation_data_2000')
table = Table(motor_x, motor_y, int(dx.delta_coord()), int(dy.delta_coord()))
env = Environment(table, chip)
a = Search(env, chip)

if __name__ == "__main__":
    check_GDS = Inner_values('file')
    count = 0

    print('________________START________________')
    time.sleep(1)
    print('start position:[', stage1.get_position(1), stage1.get_position(2), ']\n')  # проверка положения моторов
    time.sleep(1)

    for x in range(0, len(check_GDS.array), 1):
        count = count + 1
        print(check_GDS.array[x])
        test_map_walking(count, check_GDS.array[x])
        a.find()

        # subprocess.call(['python', 'optic_power_search_engine_draft.py'])
    print("Test completed")

    exit()
