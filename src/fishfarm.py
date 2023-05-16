# from math import ceil

from growth_curve_functions import weight_from_time, time_from_weight, n_for_max_density
import variables


class BaseBatch():
    
    BATCH_SIZE = variables.batch_size
    
    def __init__(self, weight, max_stock_den, maxmin_stock_den, tank_vol, weeks = 0, extra_weeks = 0):
        self.weight = weight
        self.max_stock_den = max_stock_den
        self.maxmin_stock_den = maxmin_stock_den
        self.tank_vol = tank_vol
        self.weeks = weeks
        self.extra_weeks = extra_weeks
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
        # Now we set the two values
        self.n_tanks = self.custom_tank_round(self.BATCH_SIZE / max_n_fish_tank)
        self.n_fish_tank = int(self.BATCH_SIZE / self.n_tanks)
    
    
    def week_move_calculations(self, start_weight):
        '''
        When time to move fish, we calculate what a single week growth period would look like.
        Crucially, we return the start_den to decide whether we should increase growth for two weeks and recalculate
        '''
        # first find the t value based on weight before time step
        t = time_from_weight(self.weight)
        # update the weight after 1 week growth
        self.weight = round(weight_from_time(t + 1), 2)
        # max fish are needed per tank
        max_n_fish_tank = int(n_for_max_density(self.max_stock_den, self.weight, self.tank_vol))
        # update the number of tanks needed
        self.n_tanks = self.custom_tank_round(BaseBatch.BATCH_SIZE / max_n_fish_tank)
        # and divide the fish accordingly
        self.n_fish_tank = int(BaseBatch.BATCH_SIZE / self.n_tanks)
        # get the actual stocking density at start and end of time step
        self.start_end_stocking_density(start_weight, self.weight)
    
    
    def extra_week_setup(self, start_weight):
        # first find the t value based on weight before time step
        t = time_from_weight(self.weight)
        # update the weight after 1 week growth
        self.weight = round(weight_from_time(t + 1), 2)
        # update the weight after x extra weeks growth
        extra_weeks_weight = round(weight_from_time(t + self.extra_weeks), 2)
        # max fish are needed per tank
        max_n_fish_tank = int(n_for_max_density(self.max_stock_den, extra_weeks_weight, self.tank_vol))
        # update the number of tanks needed
        self.n_tanks = self.custom_tank_round(BaseBatch.BATCH_SIZE / max_n_fish_tank)
        # and divide the fish accordingly
        self.n_fish_tank = int(BaseBatch.BATCH_SIZE / self.n_tanks)
        # get the actual stocking densities at start and end of time step
        self.start_end_stocking_density(start_weight, self.weight)
        # now set move to False so we simply get densities for next time step
        self.move = False
    
    
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
        self.stocking_den = (start_den, end_den)
        
    
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
        self.start_end_stocking_density(start_weight, self.weight)
        # now set move back to True so we re-calculate the move
        if self.extra_weeks < 1:
            self.move = True
    
    
    def total_fish_moved_tank(self, prev_step_n_fish_tank):
        '''
        After each time step, how many fish are taken from each tank
        '''
        return (prev_step_n_fish_tank - self.n_fish_tank)
    
    
    def custom_tank_round(self, n_tank_float: float):
        '''
        A way to set tank numbers with more fine grain
        '''
        int_part = int(n_tank_float)
        decimal_part = n_tank_float - int_part
        if decimal_part > 0.2:
            return (int_part + 1)
        else:
            if int_part == 0:
                return 1
            else:
                return int_part
    
    
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
        start_weight = self.weight
        
        if self.move:
            
            self.week_move_calculations(start_weight)
            
            # if starting density is too high (using a "max min") we will thin fish for 2 weeks growth
            # also checking if we have two weeks left in the hot house
            if (self.stocking_den[0] > self.maxmin_stock_den) and (self.weeks < (BatchHotHouse.MAX_WEEKS - 1)):
                self.extra_weeks = 2
                self.extra_week_setup(start_weight)
                self.extra_weeks -= 1
        
        else:            
            self.extra_weeks -= 1
            self.no_move()
          
    
class BatchJacks(BaseBatch):
    
    def week_step_updates(self):
        '''
        After one week time step, we first check whether a move is needed self.move == True?
        If so, we first check whether we move fish for a single week of growth based on the "max min" or max starting density.
        If not above this, we calculate the moves for single week of growth, if above, for 2 weeks
        If self.move == False, we simply update the weight and densities but do not move any fish as they are in a 2 week cycle
        
        first check self.move == True
            then we check if we are in a 
        
        '''
        self.weeks += 1
        start_weight = self.weight
        
        if self.move:
            
            # then we hard code the first period in Jacks to be x weeks
            if self.weeks == (variables.hothhouse_weeks + 1):
                self.extra_weeks = variables.jacks_start_period_weeks
                self.extra_week_setup(self.weight)
                self.extra_weeks -= 1
            
            elif self.weeks >= variables.jacks_end_two_weeks:
                self.extra_weeks = 2
                self.extra_week_setup(self.weight)
                self.extra_weeks -= 1
                
            else:
                # first we make a one week move saving the start density and weight
                self.week_move_calculations(start_weight)

                # if starting density from 1 week growth is too high (using a max min) we will thin fish for 2 weeks growth
                if self.stocking_den[0] > self.maxmin_stock_den:
                    self.extra_weeks = 2
                    self.extra_week_setup(start_weight)
                    self.extra_weeks -= 1
                    
        else:
            self.extra_weeks -= 1
            self.no_move()

