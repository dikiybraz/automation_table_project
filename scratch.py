class table:
    def turn_cw(self):
        print('Table was turned cw')

    def turn_ccw(self):
        print('Table was turned ccw')
    pass

class piezo_motor_x: #поворот столика по часовой стрелке


    def __init__(self):
        self.x=0
    def turn_cw(self):
        self.x+=1
    def turn_ccw(self):
        self.x-=1

    pass
class piezo_motor_y: #поворот столика против часовой стрелки
    def __init__(self):
        self.y=0
    def turn_cw(self):
        self.y+=1
    def turn_ccw(self):
        self.y-=1
class chip():

    def progressbar(self):
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

class connect to program:# протокол управления установкой программой
    pass