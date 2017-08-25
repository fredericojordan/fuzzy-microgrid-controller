'''
Created on 15 de ago de 2017

@author: fvj
'''
class Controller():
    def __init__(self, grid, battery, load):
        self.grid = grid
        self.battery = battery
        self.load = load
        
        self.fuzzy_inputs = self.setup_inputs()
        self.fuzzy_outputs = self.setup_outputs()
        self.rules = self.setup_rules()
        
    def setup_inputs(self):
        model = {}
        model['battery_charge'] = TriangularFuzzySet(['NB', 'NS', 'ZE', 'PS', 'PB'], 0, self.battery.max_charge)
        model['load_power'] = TriangularFuzzySet(['NB', 'NS', 'ZE', 'PS', 'PB'], min(self.load.demand_prediction), max(self.load.demand_prediction))
        return model
    
    def setup_outputs(self):
        model = {}
        model['battery_power'] = TriangularFuzzySet(['NB', 'NS', 'ZE', 'PS', 'PB'], self.battery.min_power, self.battery.max_power)
        return model
    
    def setup_rules(self): # or and not
        rules = []
        
        rules.append( ({'load_power':'NB'}, {'battery_power':'PB'}) )        
        rules.append( ({'load_power':'NS'}, {'battery_power':'PS'}) )
        rules.append( ({'load_power':'ZE'}, {'battery_power':'ZE'}) )
        rules.append( ({'load_power':'PS'}, {'battery_power':'NS'}) )
        rules.append( ({'load_power':'PB'}, {'battery_power':'NB'}) )
         
        rules.append( ({'battery_charge':'NB'}, {'battery_power':'NB'}) )
        rules.append( ({'battery_charge':'PB'}, {'battery_power':'PS'}) )
        
        
        
        
        
        
#         rules.append( ({'load_power':'NB'}, {'battery_power':'PB'}) )
#         rules.append( ({'load_power':'NS'}, {'battery_power':'PS'}) )
#         rules.append( ({'load_power':'ZE'}, {'battery_power':'ZE'}) )
#         rules.append( ({'load_power':'PS'}, {'battery_power':'NS'}) )
#         rules.append( ({'load_power':'PB'}, {'battery_power':'NB'}) )
#          
#         rules.append( ({'battery_charge':'NB'}, {'battery_power':'NB'}) )
#         rules.append( ({'battery_charge':'PS'}, {'battery_power':'ZE'}) )
#         rules.append( ({'battery_charge':'PB'}, {'battery_power':'PS'}) )
        
        
        
        
        
#         rules.append( ({'battery_charge':'NB', 'load_power':'NB'}, {'battery_power':'ZE'}) )
#         rules.append( ({'battery_charge':'NB', 'load_power':'NS'}, {'battery_power':'ZE'}) )
#         rules.append( ({'battery_charge':'NB', 'load_power':'ZE'}, {'battery_power':'ZE'}) )
#         rules.append( ({'battery_charge':'NB', 'load_power':'PS'}, {'battery_power':'NS'}) )
#         rules.append( ({'battery_charge':'NB', 'load_power':'PB'}, {'battery_power':'NB'}) )
#          
#         rules.append( ({'battery_charge':'NS', 'load_power':'NB'}, {'battery_power':'PS'}) )
#         rules.append( ({'battery_charge':'NS', 'load_power':'NS'}, {'battery_power':'PS'}) )
#         rules.append( ({'battery_charge':'NS', 'load_power':'ZE'}, {'battery_power':'ZE'}) )
#         rules.append( ({'battery_charge':'NS', 'load_power':'PS'}, {'battery_power':'NS'}) )
#         rules.append( ({'battery_charge':'NS', 'load_power':'PB'}, {'battery_power':'NB'}) )
#          
#         rules.append( ({'battery_charge':'ZE', 'load_power':'NB'}, {'battery_power':'PS'}) )
#         rules.append( ({'battery_charge':'ZE', 'load_power':'NS'}, {'battery_power':'PS'}) )
#         rules.append( ({'battery_charge':'ZE', 'load_power':'ZE'}, {'battery_power':'ZE'}) )
#         rules.append( ({'battery_charge':'ZE', 'load_power':'PS'}, {'battery_power':'NS'}) )
#         rules.append( ({'battery_charge':'ZE', 'load_power':'PB'}, {'battery_power':'NS'}) )
#          
#         rules.append( ({'battery_charge':'PS', 'load_power':'NB'}, {'battery_power':'PB'}) )
#         rules.append( ({'battery_charge':'PS', 'load_power':'NS'}, {'battery_power':'PS'}) )
#         rules.append( ({'battery_charge':'PS', 'load_power':'ZE'}, {'battery_power':'ZE'}) )
#         rules.append( ({'battery_charge':'PS', 'load_power':'PS'}, {'battery_power':'NS'}) )
#         rules.append( ({'battery_charge':'PS', 'load_power':'PB'}, {'battery_power':'NS'}) )
#          
#         rules.append( ({'battery_charge':'PB', 'load_power':'NB'}, {'battery_power':'PB'}) )
#         rules.append( ({'battery_charge':'PB', 'load_power':'NS'}, {'battery_power':'PS'}) )
#         rules.append( ({'battery_charge':'PB', 'load_power':'ZE'}, {'battery_power':'ZE'}) )
#         rules.append( ({'battery_charge':'PB', 'load_power':'PS'}, {'battery_power':'ZE'}) )
#         rules.append( ({'battery_charge':'PB', 'load_power':'PB'}, {'battery_power':'ZE'}) )

        return rules
        
    def dispatch_battery(self):
#         self.rule_based_controller()
        self.fuzzy_inference_sytem()
        
    def get_control_output(self, f_load_power, f_battery_charge):
        result = { str(set_name):0 for set_name in self.fuzzy_outputs['battery_power'].fuzzy_sets.keys() }
        
        for rule in self.rules:
            if 'load_power' in rule[0]:
                load_power_membership = f_load_power[rule[0]['load_power']]
            else:
                load_power_membership = 1
            
            if 'battery_charge' in rule[0]:
                battery_charge_membership = f_battery_charge[rule[0]['battery_charge']]
            else:
                battery_charge_membership = 1
            
            and_membership = min(load_power_membership, battery_charge_membership)
            result[rule[1]['battery_power']] = max(and_membership, result[rule[1]['battery_power']])
            
        return result

    def fuzzy_inference_sytem(self):
        f_load_power = self.fuzzy_inputs['load_power'].fuzzify(self.load.power)
        f_battery_charge = self.fuzzy_inputs['battery_charge'].fuzzify(self.battery.current_charge)
        
        f_battery_power = self.get_control_output(f_load_power, f_battery_charge)
        battery_power = self.fuzzy_outputs['battery_power'].defuzzify(f_battery_power)
        
        self.battery.power = battery_power
    
    def rule_based_controller(self):
        bat_soc = self.battery.current_charge/self.battery.max_charge
        if self.load.power > 0 and bat_soc < 0.9:
            self.battery.power = self.battery.min_power
        elif self.load.power < 0 and bat_soc > 0.1:
            self.battery.power = self.battery.max_power
        else:
            self.battery.power = 0
        
    def balance_with_grid(self):
        self.grid.power -= self.get_power_sum()
                    
    def get_power_sum(self):
        power_sum = 0
        power_sum += self.grid.power
        power_sum += self.battery.power
        power_sum += self.load.power 
        return power_sum
    
    def dispatch(self):
        self.dispatch_battery()
        self.balance_with_grid()

class TriangularFuzzySet():
    def __init__(self, fuzzy_sets, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value
        self.fuzzy_sets = self.setup_sets(fuzzy_sets)
        
    def setup_sets(self, set_names):
        result = {}
        n = len(set_names)
        value_range = self.max_value - self.min_value
        for i in range(n):
            ramp_len = value_range/(n-1)
            high_v = self.min_value + i*ramp_len
            min_v = high_v - ramp_len
            max_v = high_v + ramp_len
            result[set_names[i]] = TriangularFunction(min_v,high_v,max_v)
        return result
            
    def fuzzify(self, value):
        result = {}
        for set_name, fuzzy_function in self.fuzzy_sets.items():
            result[set_name] = fuzzy_function.interpolate(value)
        return result
    
    def defuzzify(self, fuzzy_memberships):
        return self.centroid(fuzzy_memberships)
                             
    def centroid(self, fuzzy_memberships):
        
        points = self.get_sampled_membership(fuzzy_memberships, 300)

        membership_total_sum = sum(point[1] for point in points)
        membership_area_sum = sum(point[0]*point[1] for point in points)
        
#         if membership_total_sum == 0:
#             raise Exception('TODO')        
        return membership_area_sum/membership_total_sum
    
    def get_sampled_membership(self, fuzzy_memberships, sample_points):
        value_range = self.max_value - self.min_value
        value = self.min_value - value_range 
        
        points = []
        while (value < self.max_value + value_range):
            membership = 0 
            for set_name, fuzzy_function in self.fuzzy_sets.items():
                membership = max(membership, fuzzy_function.saturate(value, fuzzy_memberships[set_name]))
                
            points.append( (value,membership) )
            value += value_range/sample_points
        return points
        

    
    def get_membership(self, value, set_name):
        for name, fuzzy_function in self.fuzzy_sets.items():
            if name == set_name:
                return fuzzy_function.interpolate(value)
        raise Exception('No such set: \'{}\' ({})'.format(set_name, self.fuzzy_sets.keys()))

class TriangularFunction():
    def __init__(self, min_value, high_point, max_value):
        self.min_value = min_value
        self.high_point = high_point
        self.max_value = max_value
        
    def interpolate(self, value):
        if value >= self.min_value and value < self.high_point:
            return (value-self.min_value)/(self.high_point-self.min_value)
        elif value >= self.high_point and value < self.max_value:
            return (self.max_value-value)/(self.max_value-self.high_point)
        else:
            return 0
        
    def saturate(self, value, membership):
        return min(membership, self.interpolate(value))
        
            
            
            
            
            