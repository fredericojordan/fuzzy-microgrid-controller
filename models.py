'''
Created on 15 de ago de 2017

@author: fvj
'''

class Grid():
    def __init__(self, description, min_power, max_power):
        self.description = description
        self.min_power = min_power
        self.max_power = max_power
        self.power = 0
        
    def step(self, time, time_delta):
        pass
        
class Battery():
    def __init__(self, description, min_power, max_power, max_charge, current_charge):
        self.description = description
        self.min_power = min_power
        self.max_power = max_power
        self.max_charge = max_charge
        self.current_charge = current_charge
        self.power = 0
        
    def step(self, time, time_delta):
        self.current_charge -= self.power*time_delta/60.0
        if self.current_charge > self.max_charge:
            raise Exception('Battery exceeded max charge!')
        if self.current_charge < 0:
            raise Exception('Battery depleted all charge!')
        
class Load():
    def __init__(self, description, demand_prediction):
        self.description = description
        self.demand_prediction = demand_prediction
        self.power = 0
        
    def step(self, time, time_delta):
        try:
            self.power = self.demand_prediction[time]
        except:
            self.power = 0