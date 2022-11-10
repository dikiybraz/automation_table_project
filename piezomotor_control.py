from pylablib.devices import Newport
import time
import os
import subprocess
# import optic_power_search_engine


# def info(self):
#     Newport.picomotor.Picomotor8742.get_usb_devices_number()
#     Newport.picomotor.Picomotor8742.autodetect_motors()
#
#
# def preconditions(self):
#     Newport.picomotor.Picomotor8742.get_position
#
#
# # def setup(self, step):
# #     self.setup_velocity(step)
#
# def move_first_motor(steps):
#     Newport.picomotor.Picomotor8742(0).move_by(1, steps)
#
#
# def move_second_motor(steps_2):
#     Newport.picomotor.Picomotor8742(0).move_by(2, steps_2)


# if __name__ == "__main__":
#     steps = 400
#     steps_2 = 600
#     move_first_motor(steps)
#     time.sleep(2)
#     move_second_motor(steps_2)

#
#
# else:
#
#     stage1.stop()

# Newport Detection
stage1 = Newport.picomotor.Picomotor8742(0)
stage1.autodetect_motors()
stage1.set_motor_type("all", "standard", None)


def test_map_walking(count, coordinates):
    # функция прохода по площади чипа по полученным из GDS файла координатам

    print(f' {count} итерация')
    print(f'position before:[{stage1.get_position(1)}, {stage1.get_position(2)}] \n')  # проверка положения моторов

    time.sleep(2)

    stage1.move_by(1, coordinates[0])
    time.sleep(1)
    stage1.wait_move(1)
    stage1.move_by(2, coordinates[1])
    stage1.wait_move(2)

    print(f'geolocation:[{stage1.get_position(1)}, {stage1.get_position(2)}]')
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

        # subprocess.call(['python', 'optic_power_search_engine_draft.py'])
    print("Test completed")
    exit()
