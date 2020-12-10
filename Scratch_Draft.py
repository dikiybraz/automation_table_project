from numpy.ma import sqrt


class Experimental:
    def __init__(self, table, power_meter):
        self.table = table
        self.power_meter = power_meter

    def move_table(self, dx, dy):
        self.table.move(dx, dy)

    def measure(self):
        return self.power_meter.measure()


class Environment:
    def __init__(self, mocktable ,chip):
        self.table = mocktable
        self.chip = chip

    def move(self, dx , dy):
        self.table.move(dx, dy)

    def measure(self):
        return self.chip.value(self.table.x, self.table.y)

    pass




class Table:
    def __init__(self, motor_x, motor_y):
        self.motor_x = motor_x
        self.motor_y = motor_y

    def move(self, dx, dy):
        ax = self.motor_x.
        ay = self.motor_y
        angle_goal_point = sqrt((ax**2)+(ay**2)) # Черновик:пример может быть перенесен
        self.motor_x.rotate(ax)
        self.motor_y.rotate(ay)

    pass


class MockMotor: # Проработать
    def __init__(self):
        pass


    def rotate(self, da):
        da += 1

    pass
class Chip:  # Проработать
    def __init__(self, ax, ay):
        pass
    #realization
    def value(self, x, y):
        pass

motor_x = MockMotor()
motor_y = MockMotor()

table = Table(motor_x, motor_y)
env = Environment(motor_x,motor_y, Table, Chip())
power_meter =env

