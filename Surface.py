import numpy as np

#1. находим элементы больше среднего в массиве
#2. в массив записываем координаты этих элементов

S = np.array([[1, 2, 4, 3, 2],
              [2, 3, 6, 7, 3],
              [2, 4, 6, 9, 9],
              [5, 4, 5, 3, 2],
              [1, 4, 5, 4, 3]])  # массив 5х5 - плоскость с разными оптическими мощностями
N = np.size(S)
i = 0  # строка
j = 0  # столбец
S_coord = []  # массив для координат (думаю, что потом эта переменная понадобится)

minimum = S.min()  # минимальное значение в массиве
maximum = S.max()  # максимальный значение коэффициент в массиве
# light_power_intensity == lpi - мощность излучения
lpi = 537

i, j = np.where(S == maximum)  # нахождение координаты максимального значения
print('Координаты', i, j, '\n', 'Оптическая мощность = ', maximum*lpi)


class Search:  # поиск максимального элемента массива
    def __init__(self, i , j, shag):
        i = 0
        j = 0
        shag = 0

    def poisk(self):
        maximum = 0

        shag = 0
        if shag <= self.vvod.step:
            for i in range(self.np.array):
                for j in range(self.np.array):
                    if np.array[i][j] > maximum:
                        maximum = np.array[i][j]

                else:
                    break

        i, j = np.where(np.array[i][j] == maximum)

        return print(maximum, '[', i, ']', '[', j, ']')

    pass






