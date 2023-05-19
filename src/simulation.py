import pandas as pd

import variables
from fishfarm import BatchHotHouse, BatchJacks

batch_size_value = None

def simulation(batch_size, fingerling_g = variables.fingerling_g, hothouse_max_d = variables.hothouse_max_d, hothouse_maxmin_d = variables.hothouse_maxmin_d,
               hothouse_tank_vol = variables.hothouse_tank_vol, harvest_freq = variables.harvest_freq, jacks_max_d = variables.jacks_max_d, 
               jacks_maxmin_d = variables.jacks_maxmin_d, jacks_tank_vol = variables.jacks_tank_vol, hothhouse_weeks = variables.hothhouse_weeks,
               target_weight = variables.target_weight, custom_round_denominator = variables.custom_round_denominator, 
               jacks_start_period_weeks = variables.jacks_start_period_weeks, jacks_end_two_weeks = variables.jacks_end_two_weeks):
    
    # set global variable batch_size
    global batch_size_value
    batch_size_value = batch_size
    # set week 1
    week = 0

    # initialise dictionaries for storing the batches used to loop through and update each time step
    hot_house_batch_dic = {}
    jacks_batch_dic = {}

    # initialise list in which each week becomes a row in final dataframe
    dataframe_lists = []

    while True:
        # create a new batch at the frequency set by harvest freq
        if (week % harvest_freq) == 0:
            batch_name = "batch" + str(week)
            batch_instance = BatchHotHouse(weight = fingerling_g,
                                           max_stock_den = hothouse_max_d,
                                           maxmin_stock_den = hothouse_maxmin_d,
                                           tank_vol = hothouse_tank_vol,
                                           weeks = 0,
                                           batch_size = batch_size,
                                           custom_round_denominator = custom_round_denominator,
                                           hothhouse_weeks = hothhouse_weeks)
            # add the Hot House batch instance to dictionary
            hot_house_batch_dic[batch_name] = batch_instance
            
        ############################# Jacks ################################
        jacks_row, batch_terminated = all_batch_update(jacks_batch_dic, hothhouse_weeks, target_weight)
        
        if batch_terminated != "":
            to_delete_j = batch_terminated

        ######################### Hot House ###########################    
        hothouse_row, batch_terminated = all_batch_update(hot_house_batch_dic, hothhouse_weeks, target_weight)
        
        if batch_terminated != "":
            # set to remove batch from hot house 
            to_delete_hh = batch_terminated
            # and "move" it to Jacks
            weight = hot_house_batch_dic[batch_terminated].weight
            weeks = hot_house_batch_dic[batch_terminated].weeks
            j_batch_instance = BatchJacks(weight = weight,
                                          max_stock_den = jacks_max_d,
                                          maxmin_stock_den = jacks_maxmin_d,
                                          tank_vol = jacks_tank_vol,
                                          weeks = weeks,
                                          batch_size = batch_size,
                                          custom_round_denominator = custom_round_denominator,
                                          hothhouse_weeks = hothhouse_weeks,
                                          jacks_start_period_weeks = jacks_start_period_weeks,
                                          jacks_end_two_weeks = jacks_end_two_weeks)
            jacks_batch_dic[batch_terminated] = j_batch_instance
        
        ############################ Final Steps per Week ###################################
        
        # append values for each week to lists
        row = [week] + hothouse_row + jacks_row
        dataframe_lists.append(row)
        
        # increment one week 
        week += 1
        
        # delete the batch from hot house dict
        try:
            del hot_house_batch_dic[to_delete_hh]
        except:
            pass
        
        # delete the batch from jack_dict
        try:
            del jacks_batch_dic[to_delete_j]
        except:
            pass

        # break out after 1 year
        if week > 52:
            break
    
    # now convert to Dataframe and give sensible column names
    return make_dataframe(dataframe_lists)


def total_tonne(batch_end_weight: list):
    '''
    Sum up the total of all fish across all batches in a given week
    '''
    total = 0
    # get the global variable batch_size
    global batch_size_value
    for w in batch_end_weight:
        total += (w * batch_size_value)
    return total / 1000


def all_batch_update(batch_dic: dict, hothhouse_weeks, target_weight):
    '''
    For Hot House or Jacks batches, we loop through each updating and saving values for the week
    We also return the name of a batch that has terminated (either time in hot house or reached size in Jacks)
    '''
    batch_names = []
    batch_start_weight = []
    batch_end_weight = []
    batch_tanks = []
    batch_fish_per_tank = []
    batch_densities = []
    fish_moved = []
    
    batch_terminated = ""
    
    # loop through all hot house batches
    for batch_name in batch_dic:
        # load in the instance
        batch_instance = batch_dic[batch_name]
        
        # update values pre step update
        batch_names.append(batch_name)
        batch_start_weight.append(batch_instance.weight)
        # save pre-step values
        prev_n_fish_tank = batch_instance.n_fish_tank

        
        # update the instance
        batch_instance.week_step_updates()
        
        # update values for each time step
        batch_end_weight.append(batch_instance.weight)
        batch_densities.append(batch_instance.stocking_den)
        batch_tanks.append(batch_instance.n_tanks)
        batch_fish_per_tank.append(batch_instance.n_fish_tank)
        fish_moved.append(batch_instance.total_fish_moved_tank(prev_n_fish_tank))
        
        if (batch_instance.weeks == hothhouse_weeks) or (batch_instance.weight > target_weight):
            batch_terminated = batch_name

    # summary calculations for all batches
    total_tanks = sum(batch_tanks)
    total_weight = total_tonne(batch_end_weight)

    return ([batch_names, batch_start_weight, batch_end_weight, batch_tanks, batch_fish_per_tank, batch_densities, total_tanks, total_weight, fish_moved], batch_terminated)


def make_dataframe(dataframe):
    '''
    Simply take the list of lists and make a dataframe with column names
    '''
    year_output = pd.DataFrame(dataframe,
                               columns = ['Week',
                                          'Hot House Batch Names',
                                          'Hot House Batch Start Weights (g)',
                                          'Hot House Batch End Weights (g)',
                                          'Hot House Batch Tanks',
                                          'Hot House Fish Per Tank',
                                          'Hot House Batch Densities',
                                          'Hot House Total Tanks',
                                          'Hot House Total Weight (kg)',
                                          'Hot House Fish Moved Per Tank',
                                          'Jacks Batch Names',
                                          'Jacks Batch Start Weights (g)',
                                          'Jacks Batch End Weights (g)',
                                          'Jacks Batch Tanks',
                                          'Jacks Fish Per Tank',
                                          'Jacks Batch Densities',
                                          'Jacks Total Tanks',
                                          'Jacks Total Weight (kg)',
                                          'Jacks Fish Moved Per Tank'])
    # shift the fish moved column up one row to match up with the week end
    year_output['Hot House Fish Moved Per Tank'] = (year_output['Hot House Fish Moved Per Tank']
                                                    .shift(periods = -1, fill_value = 0))
    year_output['Jacks Fish Moved Per Tank'] = (year_output['Jacks Fish Moved Per Tank']
                                                    .shift(periods = -1, fill_value = 0))
    
    return year_output