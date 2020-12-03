
class table:
    def turn_cw(self):
        print('Table was turned cw')

    def turn_ccw(self):
        print('Table was turned ccw')
    pass

class PiezoMotor: #поворот столика по часовой стрелке


    def __init__(self):
        self.x=0
    def turn_cw(self):
        self.x+=1
    def turn_ccw(self):
        self.x-=1

    pass
class chip(): # модель "структуры"(характеристики) чипа: площадь, минимальная оптическая мощность, количество максимумов
    # максимумы, их расположение на площади)
    area=100 #площадь

    def __init__(self):
        self.first_max=chip()
        self.second_max=chip()
        self.third_max=chip()
        pass

    def __init__(self):
        pass

    pass

class optic_power_meter:

    def __init__(self):
        self.meter=0
    def progressbar(self):
        for self.meter in 100:
            self.meter+=1
        pass

    pass

class visualization: #иллюстрация активности (графики и тд)
    pass
class light_intensivity: #
    pass

class connecttoprogram:# протокол управления установкой программой
    pass

