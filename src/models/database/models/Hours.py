from .Keys import Key
from functools import reduce
import numpy as np

# ? la clase de Infomateria es donde se recaba la informacion para poder meterla en la base 
# de datos 

def get_avaible_hours_slots(min_val: float, max_val: float, sum_: float):
    # todos los posibles valores iniciales
    if sum_ < min_val:
        return [0]
    
    # posibles valores en principio 
    possible_hours = [x * 0.5 for x in range(int(min_val * 2), int(max_val * 2) + 1)]
    
    # filtro para verificar si un valor puede ser escogido 
    def filter_hours(x: float, sum_: float, min_val: float, max_val: float) -> bool:
        if sum_ - x == 0:
            return True
        if sum_ - x < min_val:
            return False
        elif x > sum_:
            return False
        return True

    possible_hours = [x for x in possible_hours if filter_hours(x, sum_, min_val, max_val)]
    possible_hours= [0] + possible_hours

    return possible_hours



class WeeklyHoursDistribution():

    def __init__(self, avaible_hours) -> None:
        self.__avaible_hours_slots = avaible_hours
        pass 

    def get_avaible_hours(self):
        return self.__avaible_hours_slots
    
    def set_avaible_hours(self, new_avaible_hours_slots):
        self.__avaible_hours_slots = new_avaible_hours_slots

class HoursComposition(WeeklyHoursDistribution):

    def __init__(self, minimum, maximum, total) -> None:
        self.__min = minimum
        self.__max = maximum
        self.__total = total 
        self.__hours_completed = 0

        avaible_hours  = get_avaible_hours_slots(minimum, maximum, total)
        super().__init__(avaible_hours) 

    def update_hours_slots(self):
        avaible_hours = get_avaible_hours_slots(
            self.__min, 
            self.__max, 
            self.__total-self.__hours_completed
            )
        
        self.set_avaible_hours(avaible_hours)

    def add_block_hour(self, length_block):
        self.__hours_completed += length_block / 2
        self.update_hours_slots()

    def remove_length_hour(self, length_block):
        self.__hours_completed -= length_block / 2
        self.update_hours_slots()

    def restart(self):
        self.__hours_completed = 0
        self.update_hours_slots()

    def total(self):
        return self.__total 
    
    def remaining(self):
        return self.__total - self.__hours_completed
    
    def maximum(self):
        return self.__max
    
    def minimum(self):
        return self.__min


    

class HoursSlotsComposition(WeeklyHoursDistribution):

    def __init__(self, avaible_hours_slots) -> None:
        super().__init__(avaible_hours_slots)
        self.assigned_slots_hours = []

    def update_hours_slots(self):
        new_avaiblity_slots_hours = list(set(self.bloques) - set(self.bloques_puestas))
        self.avaible_hours_slots = new_avaiblity_slots_hours

    def add_hour_slot(self, length_hour_slot):
        self.bloques_puestas.append(length_hour_slot)
        self.update_hours_slots()

    def remove_hour_slot(self, length_hour_slot):
        self.bloques_puestas.remove(length_hour_slot)
        self.update_hours()

    def restart(self):
        self.bloques_puestas = []
        self.update_hours()
    
    def total(self):
        return sum(self.bloques)
    
    def remaining(self):
        return sum(self.bloques) - sum(self.bloques_puestas)
    