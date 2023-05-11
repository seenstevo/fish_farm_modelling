import pandas as pd

import variables
from fishfarm import BatchHotHouse, BatchJacks


def simulation():

    # set week 1
    week = 0

    # initialise dictionaries for storing the batches used to loop through and update each time step
    hot_house_batch_dic = {}
    jacks_batch_dic = {}

    # initialise list in which each week becomes a row in final dataframe
    dataframe_lists = []

    while True:
        # create a new batch at the frequency set by harvest freq
        if (week % variables.harvest_freq) == 0:
            batch_name = "batch" + str(week)
            batch_instance = BatchHotHouse(weight = variables.fingerling_g,
                                           max_stock_den = variables.hothouse_max_d,
                                           maxmin_stock_den = variables.hothouse_maxmin_d,
                                           tank_vol = variables.hothouse_tank_vol,
                                           weeks = 0)
            # add the Hot House batch instance to dictionary
            hot_house_batch_dic[batch_name] = batch_instance
            
        ############################# Jacks ################################
        jacks_row, batch_terminated = all_batch_update(jacks_batch_dic)
        
        if batch_terminated != "":
            to_delete_j = batch_terminated

        ######################### Hot House ###########################    
        hothouse_row, batch_terminated = all_batch_update(hot_house_batch_dic)
        
        if batch_terminated != "":
            # set to remove batch from hot house 
            to_delete_hh = batch_terminated
            # and "move" it to Jacks
            weight = hot_house_batch_dic[batch_terminated].weight
            weeks = hot_house_batch_dic[batch_terminated].weeks
            j_batch_instance = BatchJacks(weight = weight,
                                          max_stock_den = variables.jacks_max_d,
                                          maxmin_stock_den = variables.jacks_maxmin_d,
                                          tank_vol = variables.jacks_tank_vol,
                                          weeks = weeks)
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
        except UnboundLocalError:
            pass
        
        # delete the batch from jack_dict
        try:
            del jacks_batch_dic[to_delete_j]
        except UnboundLocalError:
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
    for w in batch_end_weight:
        total += (w * variables.batch_size)
    return total / 1000


def all_batch_update(batch_dic: dict):
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
        
        if (batch_instance.weeks == variables.hothhouse_weeks) or (batch_instance.weight > variables.target_weight):
            batch_terminated = batch_name

    # summary calculations for all batches
    total_tanks = sum(batch_tanks)
    total_weight = total_tonne(batch_end_weight)

    return ([batch_names, batch_start_weight, batch_end_weight, batch_tanks, batch_fish_per_tank, batch_densities, total_tanks, total_weight, fish_moved], batch_terminated)


def make_dataframe(dataframe):
    '''
    Simply take the list of lists and make a dataframe with column names
    '''
    return pd.DataFrame(dataframe,
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