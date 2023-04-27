from math import ceil

from growth_curve_functions import weight_from_time, time_from_weight, n_for_max_density, a, b, c, d, e, f


class BatchHotHouse():
    
    TANK_VOL = 1
    
    def __init__(self, fingerling_weight, max_stock_den, batch_size):
        self.batch_size = batch_size    # initialize the batch_size variable
        self.weight = fingerling_weight    # intially set as fingerling weight from hatchery
        self.max_stock_den = max_stock_den  # set the max density
        self.weeks = 0  # initialise weeks to 0        
        self.n_tanks = self.initial_n_tanks()  # how many tanks will we start with, updated
        self.n_fish_tank = self.initial_n_fish_tank()    # initialise number of fish per tank
        self.stocking_den = None    # what is the exact starting and finishing stocking den for each week         

    
    def initial_n_tanks(self):
        '''
        Based on the batch size and the weight of the fish, how many tanks are needed to 
        '''
        # first find the t value based on weight before time step
        t = time_from_weight(self.weight, a, b, c, d, e, f)
        # what is the end weight after 1 week time step
        weight_after_week = round(weight_from_time(t+1), 2)
        # therefore what is max fish per tank
        max_n_fish_tank = int(n_for_max_density(self.max_stock_den, weight_after_week, BatchHotHouse.TANK_VOL))
        return ceil(self.batch_size / max_n_fish_tank)
    
    
    def initial_n_fish_tank(self):
        '''
        Based on min tanks needed, how should we split the fish into these tanks
        '''
        return int(self.batch_size / self.n_tanks)
    
# need to sort the density calculations so we get the density with a given number of fish and the weight at the start and end
    def week_step_updates(self):
        '''
        Carry out time step of one week and update values for self.weight, self.n_fish_tank and self.n_tanks
        '''
        # save the previous weight
        previous_weight = self.weight
        # first find the t value based on weight before time step
        t = time_from_weight(self.weight, a, b, c, d, e, f)
        # update the weight after 1 week growth
        self.weight = round(weight_from_time(t+1), 2)
        # max fish are needed per tank
        max_n_fish_tank = int(n_for_max_density(self.max_stock_den, self.weight, BatchHotHouse.TANK_VOL))
        # update the number of tanks needed
        self.n_tanks = ceil(self.batch_size / max_n_fish_tank)
        # and divide the fish accordingly
        self.n_fish_tank = int(self.batch_size / self.n_tanks)
        # get the actual stocking density at start and end of time step
        start_den = round(((self.n_fish_tank * (previous_weight / 1000)) / BatchHotHouse.TANK_VOL), 2)
        end_den = round(((self.n_fish_tank * (self.weight / 1000)) / BatchHotHouse.TANK_VOL), 2)
        self.stocking_den = (start_den, end_den)
        # update the weeks by 1
        self.weeks = self.weeks + 1
        return self.n_fish_tank, self.weight, self.n_tanks, self.stocking_den
    
    
    def total_fish_moved(self, prev_n_fish_tank, prev_n_tanks):
        '''
        After each time step, how many fish should be taken from each tank and to how many new ones and therefore how many tanks do we pool
        '''
        # first we calculate how many fish are removed per tank
        n_fish_remove_tank = prev_n_fish_tank - self.n_fish_tank
        # and finally we get the total fish moved per week
        total_fish_moved = (prev_n_tanks * n_fish_remove_tank)
        return total_fish_moved



class BatchJacks():
    
    TANK_VOL = 16
    
    def __init__(self, arrival_weight, max_stock_den, batch_size):
        self.weight = arrival_weight    # weight from hot house
        self.max_stock_den = max_stock_den  # set the max density
        self.batch_size = batch_size  # size of batch arriving at Jack's
        self.n_tanks = self.initial_n_tanks()   # calculate the starting number of tanks
        self.n_fish_tank = self.initial_n_fish_tank()     # initialise as None
        self.stocking_den = None    # initialise density
                
    
    def initial_n_tanks(self):
        '''
        Based on the batch size and the weight of the fish, how many tanks are needed to 
        '''
        # first find the t value based on weight before time step
        t = time_from_weight(self.weight, a, b, c, d, e, f)
        # what is the end weight after 1 week time step
        weight_after_week = round(weight_from_time(t+1), 2)
        # therefore how many fish are needed for each tank
        max_n_fish_tank = int(n_for_max_density(self.max_stock_den, weight_after_week, BatchJacks.TANK_VOL))
        return ceil(self.batch_size / max_n_fish_tank)
    
        
    def initial_n_fish_tank(self):
        '''
        Based on min tanks needed, how should we split the fish into these tanks
        '''
        return int(self.batch_size / self.n_tanks)
    
    
    
    def week_step_updates(self):
        '''
        Carry out time step of one week and update values for self.weight, self.n_fish_tank and self.n_tanks
        '''
        # save the previous weight
        previous_weight = self.weight
        # first find the t value based on weight before time step
        t = time_from_weight(self.weight, a, b, c, d, e, f)
        # update the weight after 1 week growth
        self.weight = round(weight_from_time(t+1), 2)
        # max fish are needed per tank
        max_n_fish_tank = int(n_for_max_density(self.max_stock_den, self.weight, BatchJacks.TANK_VOL))
        # update the number of tanks needed
        self.n_tanks = ceil(self.batch_size / max_n_fish_tank)
        # and divide the fish accordingly
        self.n_fish_tank = int(self.batch_size / self.n_tanks)
        # get the actual stocking density at start and end of time step
        start_den = round(((self.n_fish_tank * (previous_weight / 1000)) / BatchJacks.TANK_VOL), 2)
        end_den = round(((self.n_fish_tank * (self.weight / 1000)) / BatchJacks.TANK_VOL), 2)
        self.stocking_den = (start_den, end_den)
        return self.n_fish_tank, self.weight, self.n_tanks, self.stocking_den
    
    
    def total_fish_moved(self, prev_n_fish_tank, prev_n_tanks):
        '''
        After each time step, how many fish should be taken from each tank and to how many new ones and therefore how many tanks do we pool
        '''
        # first we calculate how many fish are removed per tank
        n_fish_remove_tank = prev_n_fish_tank - self.n_fish_tank
        # and finally we get the total fish moved per week
        total_fish_moved = (prev_n_tanks * n_fish_remove_tank)
        return total_fish_moved
