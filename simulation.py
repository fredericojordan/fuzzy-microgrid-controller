'''
Created on 15 de ago de 2017

@author: fvj
'''
import models
import math
import fuzzy_controller as fuzzy
from pprint import pprint
# from time import sleep

class Simulation():
    def __init__(self, components, controller):
        self.time = 0
        self.components = components
        self.controller = controller
        self.output = open('results.csv', 'w')
    
    def run(self, time_length, time_delta):
        self.write_headers_to_file()
            
        for i in range(time_length):
            self.controller.dispatch()
            
            if i % 100 == 0:
                print('.')
            if i == 2736:
                self.print_step()
            self.write_step_to_file()
            
            self.step(time_delta)
            
#             sleep(0.3)
            
        self.output.close()

    def write_headers_to_file(self):
        self.output.write('t ')
        for c in self.components:
            self.output.write('{}_power '.format(c.description))
            if isinstance(c, models.Battery):
                self.output.write('{}_SOC '.format(c.description))
        self.output.write('\n')
        
    def write_step_to_file(self):
        self.output.write('{} '.format(self.time/(24*60)))
        for c in self.components:
            self.output.write('{} '.format(c.power))
            if isinstance(c, models.Battery):
                self.output.write('{} '.format(c.current_charge/c.max_charge))
        self.output.write('\n')
    
    def step(self, time_delta):
        self.time += time_delta
        for c in self.components:
            c.step(self.time, time_delta)
    
    def print_step(self):
        print('[PRINTING STEP t={}]'.format(self.time))
        for comp in self.components:
            print('{} power:\t {}'.format(comp.description, comp.power))
            if isinstance(comp, models.Battery):
                print('{} charge:\t {}'.format(comp.description, comp.current_charge))
        
        f_load_power = self.controller.fuzzy_inputs['load_power'].fuzzify(self.controller.load.power)
        f_battery_charge = self.controller.fuzzy_inputs['battery_charge'].fuzzify(self.controller.battery.current_charge)
        f_battery_power = self.controller.get_control_output(f_load_power, f_battery_charge)
        
        print('load_power: ')
        print_fuzzy_set(f_load_power)
        print('battery_charge: ')
        print_fuzzy_set(f_battery_charge)
        print('battery_power: ')
        print_fuzzy_set(f_battery_power)
        
def print_fuzzy_set(f_set):
    pprint(f_set, width=1, indent=4)
            
def generate_sine_load():
#     return [10*(-1-math.sin(0.003*x)+math.sin(0.005*x+.1)-math.sin(0.019*x+.3)) for x in range(60*24*366)]
    return [-8*(1+math.sin(2*math.pi*(x-360)/(24*60))-0.5*math.sin(6*math.pi*(x+231)/(24*60))-0.2*math.sin(19*math.pi*(x+33)/(24*60))) for x in range(60*24*30)]
            
if __name__ == '__main__':
    print('Starting simulation!')
    
    grid = models.Grid('Grid', -75, 75)
    battery = models.Battery('Battery', -10, 10, 50, 40)
    load = models.Load('Load', generate_sine_load())
    
    mgcc = fuzzy.Controller(grid, battery, load)
    sim = Simulation([grid, battery, load], mgcc)
    
    sim.run(60*24*6, 1)
    
    print('Done!')