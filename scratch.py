import numpy as np

int(vvod)

# noinspection PyTypeChecker


class PiezoMotor:  # поворот столика по часовой стрелке

    def __init__(self):
        self.x = 0

    def turn_cw(self):
        self.x += 1
        return self.x

    def turn_ccw(self):
        self.x -= 1
        return self.x

    pass

class chip:  # структура чипа
    a = np.array([[1, 2, 4, 3, 2],
                  [2, 3, 6, 7, 3],
                  [2, 4, 6, 9, 9],
                  [5, 4, 5, 3, 2],
                  [1, 4, 5, 4, 3]])
    b = np.array([[2, 4, 14, 3, 2],
                  [5, 6, 11, 7, 8],
                  [11, 8, 6, 9, 1],
                  [12, 8, 5, 1, 2],
                  [10, 9, 5, 4, 3]])
    c = np.array([[1, 2, 4, 3, 2],
                  [2, 3, 6, 7, 3],
                  [2, 4, 6, 9, 9],
                  [5, 4, 5, 3, 2],
                  [1, 4, 5, 4, 3]])
    pass

class element:
    pass

class light_intensivity:  # формулы и тд
    k = 14
    pass
class Location:  # актуальное местоположение цели
       def location_update(self,loc):
           self.loc
           print(loc)
    pass
class Table:
    def turn_cw(self):
        print('Table was turned cw')

    def turn_ccw(self):
        print('Table was turned ccw')

    pass

# me = Location() #поиск местоположения по введенной координате), но пока что используются две строчки ниже
pz_x:int = input()
pz_y:int = input()
pz_x = PiezoMotor()
pz_y = PiezoMotor()

if pz_x > 0:
    pz_x = PiezoMotor.turn_cw() * vvod
else:
    pz_x = PiezoMotor.turn_ccw() * vvod

if pz_y > 0:
    pz_y = PiezoMotor.turn_cw() * vvod
else:
    pz_y = PiezoMotor.turn_ccw() * vvod

kapler = chip.a  # выбираем один из лобъектов чипа: a,b,c
N = np.size(kapler)
print(kapler)
Search.poisk(kapler) #

