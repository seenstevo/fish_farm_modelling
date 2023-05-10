from math import ceil

from growth_curve_functions import weight_from_time, time_from_weight, n_for_max_density
import variables

class BaseBatch():
    
    BATCH_SIZE = variables.batch_size
    
    def __init__(self, weight, max_stock_den, maxmin_stock_den, tank_vol):
        self.weight = weight
        self.max_stock_den = max_stock_den
        self.maxmin_stock_den = maxmin_stock_den
        self.tank_vol = tank_vol
        self.weeks = 0
        self.stocking_den = None
        self.move = True
        self.n_tanks = self.initial_n_tanks()
        self.n_fish_tank = self.initial_n_fish_tank()
        
        
    def initial_n_tanks(self):
        '''
        Based on the batch size and the weight of the fish, how many tanks are needed to start with
        '''
        # first find the t value based on weight before time step
        t = time_from_weight(self.weight)
        # what is the end weight after 1 week time step
        weight_after_week = round(weight_from_time(t+1), 2)
        # therefore what is max fish per tank
        max_n_fish_tank = int(n_for_max_density(self.max_stock_den, weight_after_week, self.tank_vol))
        return ceil(self.BATCH_SIZE / max_n_fish_tank)
    
    
    def initial_n_fish_tank(self):
        '''
        Based on min tanks needed, how should we split the fish into these tanks
        '''
        return int(self.BATCH_SIZE / self.n_tanks)

        
    def total_fish_moved_tank(self, prev_step_n_fish_tank):
        '''
        After each time step, how many fish are taken from each tank
        '''
        # first we calculate how many fish are removed per tank
        n_fish_remove_tank = prev_step_n_fish_tank - self.n_fish_tank
        return n_fish_remove_tank
    
    def get_starting_density(self):
        '''
        
        '''
        # save the previous weight
        previous_weight = self.weight
        # first find the t value based on weight before time step
        t = time_from_weight(self.weight)
        # update the weight after 1 week growth
        self.weight = round(weight_from_time(t + 1), 2)
        # max fish are needed per tank
        max_n_fish_tank = int(n_for_max_density(self.max_stock_den, self.weight, self.tank_vol))
        # update the number of tanks needed
        self.n_tanks = ceil(BaseBatch.BATCH_SIZE / max_n_fish_tank)
        # and divide the fish accordingly
        self.n_fish_tank = int(BaseBatch.BATCH_SIZE / self.n_tanks)
        # get the actual stocking density at start and end of time step
        start_den = round(((self.n_fish_tank * (previous_weight / 1000)) / self.tank_vol), 2)
        
        return start_den, t, previous_weight
    
    def two_week_setup(self, t, previous_weight):
        # update the weight after 2 weeks growth
        two_week_weight = round(weight_from_time(t + 2), 2)
        # max fish are needed per tank
        max_n_fish_tank = int(n_for_max_density(self.max_stock_den, two_week_weight, self.tank_vol))
        # update the number of tanks needed
        self.n_tanks = ceil(BaseBatch.BATCH_SIZE / max_n_fish_tank)
        # and divide the fish accordingly
        self.n_fish_tank = int(BaseBatch.BATCH_SIZE / self.n_tanks)
        # get the actual stocking density at start and end of time step
        start_den = round(((self.n_fish_tank * (previous_weight / 1000)) / self.tank_vol), 2)
        # now set move to False so we simply get densities for next time step
        self.move = False
        
        return start_den
    
    
    def no_move(self):
        '''
        When we are not moving the batch, we simply calculate the new weight at week end, and the new densities
        We reset back self.move to True to carry out the move the following week
        '''
        # save the previous weight
        previous_weight = self.weight
        # first find the t value based on weight before time step
        t = time_from_weight(self.weight)
        # update the weight after 1 week growth
        self.weight = round(weight_from_time(t + 1), 2)
        # get the actual stocking density at start and end of time step
        start_den = round(((self.n_fish_tank * (previous_weight / 1000)) / self.tank_vol), 2)
        end_den = round(((self.n_fish_tank * (self.weight / 1000)) / self.tank_vol), 2)
        self.stocking_den = (start_den, end_den)
        # now set move back to True so we re-calculate the move
        self.move = True

        return self.n_fish_tank, self.weight, self.n_tanks, self.stocking_den
    
    
    
class BatchHotHouse(BaseBatch):
    
    MAX_WEEKS = variables.hothhouse_weeks
    
    def week_step_updates(self):
        '''
        Carry out time step of one week and update values for self.weight, self.n_fish_tank and self.n_tanks
        '''
        self.weeks += 1
        
        if self.move:
            
            start_den, t, previous_weight = self.get_starting_density()
            
            # if starting density is too high (using a max min) we will thin fish for 2 weeks growth
            # also checking if we have two weeks left in the hot house
            if (start_den > self.maxmin_stock_den) and (self.weeks < (BatchHotHouse.MAX_WEEKS)):
                
                start_den = self.two_week_setup(self, t, previous_weight)

            end_den = round(((self.n_fish_tank * (self.weight / 1000)) / self.tank_vol), 2)
            self.stocking_den = (start_den, end_den)

            return self.n_fish_tank, self.weight, self.n_tanks, self.stocking_den
        
        else:
            self.no_move()
          
          
    
class BatchJacks(BaseBatch):
    
    def week_step_updates(self):
        '''
        Carry out time step of one week and update values for self.weight, self.n_fish_tank and self.n_tanks
        '''
        if self.move:
            
            start_den, t, previous_weight = self.get_starting_density()
            
            # if starting density is too high (using a max min) we will thin fish for 2 weeks growth
            if start_den > self.maxmin_stock_den:
                
                start_den = self.two_week_setup(self, t, previous_weight)
                
            end_den = round(((self.n_fish_tank * (self.weight / 1000)) / self.tank_vol), 2)
            self.stocking_den = (start_den, end_den)
            
            return self.n_fish_tank, self.weight, self.n_tanks, self.stocking_den
        
        else:
            self.no_move()
    

