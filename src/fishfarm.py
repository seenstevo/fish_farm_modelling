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
        self.n_tanks = None
        self.n_fish_tank = None
        self.initialise_tanks()
        
        
    def initialise_tanks(self):
        '''
        Based on the batch size and the weight of the fish, how many tanks are needed to start with
        '''
        # first find the t value based on weight before time step
        t = time_from_weight(self.weight)
        # what is the end weight after 1 week time step
        weight_after_week = round(weight_from_time(t+1), 2)
        # therefore what is max fish per tank
        max_n_fish_tank = int(n_for_max_density(self.max_stock_den, weight_after_week, self.tank_vol))
        # Now we set the two 
        self.n_tanks = ceil(self.BATCH_SIZE / max_n_fish_tank)
        self.n_fish_tank = int(self.BATCH_SIZE / self.n_tanks)
    
    
    def week_move_calculations(self):
        '''
        When time to move fish, we calculate what a single week growth period would look like.
        Crucially, we return the start_den to decide whether we should increase growth for two weeks and recalculate
        '''
        # save the previous weight
        start_weight = self.weight
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
        start_den = round(((self.n_fish_tank * (start_weight / 1000)) / self.tank_vol), 2)
        
        return start_den, start_weight
    
    
    def two_week_setup(self, start_weight):
        # first find the t value based on weight before time step
        t = time_from_weight(self.weight)
        # update the weight after 2 weeks growth
        two_week_weight = round(weight_from_time(t + 2), 2)
        # max fish are needed per tank
        max_n_fish_tank = int(n_for_max_density(self.max_stock_den, two_week_weight, self.tank_vol))
        # update the number of tanks needed
        self.n_tanks = ceil(BaseBatch.BATCH_SIZE / max_n_fish_tank)
        # and divide the fish accordingly
        self.n_fish_tank = int(BaseBatch.BATCH_SIZE / self.n_tanks)
        # get the actual stocking density at start and end of time step
        start_den = self.stocking_density(start_weight)
        # now set move to False so we simply get densities for next time step
        self.move = False
        
        return start_den
    
    
    def stocking_density(self, weight):
        '''
        Calculate the stocking density
        '''
        return round(((self.n_fish_tank * (weight / 1000)) / self.tank_vol), 2)
    
    
    def start_end_stocking_density(self, start_weight, end_weight):
        '''
        Return the stocking density tuple for each week time step
        '''
        start_den = self.stocking_density(start_weight)
        end_den = self.stocking_density(end_weight)
        return (start_den, end_den)
        
    
    def no_move(self):
        '''
        When we are not moving the batch, we simply calculate the new weight at week end, and the new densities
        We reset back self.move to True to carry out the move the following week
        '''
        # save the previous weight
        start_weight = self.weight
        # first find the t value based on weight before time step
        t = time_from_weight(self.weight)
        # update the weight after 1 week growth
        self.weight = round(weight_from_time(t + 1), 2)
        # get the actual stocking density at start and end of time step
        self.stocking_den = self.start_end_stocking_density(start_weight, self.weight)
        # now set move back to True so we re-calculate the move
        self.move = True

        return self.n_fish_tank, self.weight, self.n_tanks, self.stocking_den
    
    
    def total_fish_moved_tank(self, prev_step_n_fish_tank):
        '''
        After each time step, how many fish are taken from each tank
        '''
        return prev_step_n_fish_tank - self.n_fish_tank
    
    
    
class BatchHotHouse(BaseBatch):
    
    MAX_WEEKS = variables.hothhouse_weeks
    
    def week_step_updates(self):
        '''
        After one week time step, we first check whether a move is needed self.move == True?
        If so, we first check whether we move fish for a single week of growth based on the "max min" or max starting density.
        If not above this, we calculate the moves for single week of growth, if above and if > 1 week left in hot house, for 2 weeks
        If self.move == False, we simply update the weight and densities but do not move any fish as they are in a 2 week cycle
        '''
        self.weeks += 1
        
        if self.move:
            
            start_den, start_weight = self.week_move_calculations()
            
            # if starting density is too high (using a "max min") we will thin fish for 2 weeks growth
            # also checking if we have two weeks left in the hot house
            if (start_den > self.maxmin_stock_den) and (self.weeks < (BatchHotHouse.MAX_WEEKS)):
                
                start_den = self.two_week_setup(self, start_weight)

            end_den = self.stocking_density(self.weight)
            self.stocking_den = (start_den, end_den)

            return self.n_fish_tank, self.weight, self.n_tanks, self.stocking_den
        
        else:
            self.no_move()
          
          
    
class BatchJacks(BaseBatch):
    
    def week_step_updates(self):
        '''
        After one week time step, we first check whether a move is needed self.move == True?
        If so, we first check whether we move fish for a single week of growth based on the "max min" or max starting density.
        If not above this, we calculate the moves for single week of growth, if above, for 2 weeks
        If self.move == False, we simply update the weight and densities but do not move any fish as they are in a 2 week cycle
        '''
        if self.move:
            
            start_den, start_weight = self.week_move_calculations()
            
            # if starting density from 1 week growth is too high (using a max min) we will thin fish for 2 weeks growth
            if start_den > self.maxmin_stock_den:
                
                start_den = self.two_week_setup(self, start_weight)
                
            end_den = self.stocking_density(self.weight)
            self.stocking_den = (start_den, end_den)
            
            return self.n_fish_tank, self.weight, self.n_tanks, self.stocking_den
        
        else:
            self.no_move()
    

