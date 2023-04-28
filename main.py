import pandas as pd
import numpy as np
import sys

sys.path.append('src')

import variables
from growth_curve_functions import weight_from_time, time_from_weight, a, b, c, d, e, f
from fishfarm import BatchHotHouse, BatchJacks
import single_batch_report

def main(fingerling_g = variables.fingerling_g, hothouse_max_d = variables.hothouse_max_d, hothhouse_weeks = variables.hothhouse_weeks,
         jacks_max_d = variables.jacks_max_d, target_weight = variables.target_weight, harvest_freq = variables.harvest_freq,
         batch_size = variables.batch_size):

    # set week 1
    week = 0

    # initialise dictionaries for storing the batches
    hot_house_batch_dic = {}
    jacks_batch_dic = {}

    # initialise list for tracking the stats for each week
    dataframe = []

    while True:
        # create a new batch at the frequency set by harvest freq
        if (week % harvest_freq) == 0:
            batch_name = "batch" + str(week)
            batch_instance = BatchHotHouse(fingerling_weight = fingerling_g, 
                                        max_stock_den = hothouse_max_d, 
                                        batch_size = batch_size)
            hot_house_batch_dic[batch_name] = batch_instance
            
        ############################# Jacks ################################    
        j_batch_names = []
        j_batch_start_weight = []
        j_batch_end_weight = []
        j_batch_tanks = []
        j_batch_fish_per_tank = []
        j_batch_densities = []
        j_fish_moved = []

        # initialise batch name to delete
        to_delete_j = ''

        # loop through the Jack's batches    
        for j_batch_name in jacks_batch_dic:
            # load in the instance
            j_batch_instance = jacks_batch_dic[j_batch_name]
            
            # update values pre step update
            j_batch_names.append(j_batch_name)
            j_batch_start_weight.append(j_batch_instance.weight)
            # save pre-step values
            j_prev_n_fish_tank = j_batch_instance.n_fish_tank
            j_prev_n_tanks = j_batch_instance.n_tanks
            
            # update the instance
            j_batch_instance.week_step_updates()
            
            # update values for each time step
            j_batch_end_weight.append(j_batch_instance.weight)
            j_batch_densities.append(j_batch_instance.stocking_den)
            j_batch_tanks.append(j_batch_instance.n_tanks)
            j_batch_fish_per_tank.append(j_batch_instance.n_fish_tank)
            j_fish_moved.append(j_batch_instance.total_fish_moved_tank(j_prev_n_fish_tank))
        
            
            if j_batch_instance.weight > target_weight:
                # set this batch name to be deleted
                to_delete_j = j_batch_name
        
        ######################### Hot House ###########################    
        # initialise values we want to sum across all batches 
        hh_batch_names = []
        hh_batch_start_weight = []
        hh_batch_end_weight = []
        hh_batch_tanks = []
        hh_batch_fish_per_tank = []
        hh_batch_densities = []
        hh_fish_moved = []
        
        # initialise batch name to delete
        to_delete_hh = ''
        
        # loop through all hot house batches
        for hh_batch_name in hot_house_batch_dic:
            # load in the instance
            hh_batch_instance = hot_house_batch_dic[hh_batch_name]
            
            # update values pre step update
            hh_batch_names.append(hh_batch_name)
            hh_batch_start_weight.append(hh_batch_instance.weight)
            # save pre-step values
            hh_prev_n_fish_tank = hh_batch_instance.n_fish_tank
            hh_prev_n_tanks = hh_batch_instance.n_tanks
            
            # update the instance
            hh_batch_instance.week_step_updates()
            
            # update values for each time step
            hh_batch_end_weight.append(hh_batch_instance.weight)
            hh_batch_densities.append(hh_batch_instance.stocking_den)
            hh_batch_tanks.append(hh_batch_instance.n_tanks)
            hh_batch_fish_per_tank.append(hh_batch_instance.n_fish_tank)
            hh_fish_moved.append(hh_batch_instance.total_fish_moved_tank(hh_prev_n_fish_tank))


            # create a Jacks instance when Hot House time ends
            if hh_batch_instance.weeks == hothhouse_weeks:
                j_batch_instance = BatchJacks(arrival_weight = hh_batch_instance.weight,
                                            max_stock_den = jacks_max_d,
                                            batch_size = hh_batch_instance.batch_size)
                jacks_batch_dic[hh_batch_name] = j_batch_instance
                # set this batch name to be deleted
                to_delete_hh = hh_batch_name
        
        ############################ Final Steps per Week ###################################
        
        hh_total_weight = 0
        for w in hh_batch_end_weight:
            hh_total_weight += (w * batch_size)
        
        j_total_weight = 0
        for w in j_batch_end_weight:
            j_total_weight += (w * batch_size)

        
        # append values for each week to lists
        dataframe.append([week,
                        hh_batch_names,
                        hh_batch_start_weight,
                        hh_batch_end_weight,
                        hh_batch_tanks,
                        hh_batch_fish_per_tank,
                        hh_batch_densities,
                        sum(hh_batch_tanks),
                        (hh_total_weight / 1000),
                        hh_fish_moved,
                        j_batch_names,
                        j_batch_start_weight,
                        j_batch_end_weight,
                        j_batch_tanks,
                        j_batch_fish_per_tank,
                        j_batch_densities,
                        sum(j_batch_tanks),
                        (j_total_weight / 1000),
                        j_fish_moved
                        ])
        
        
        # increment one week 
        week += 1
        
        # delete the batch from hot house dict
        if to_delete_hh in hot_house_batch_dic:
            del hot_house_batch_dic[to_delete_hh]
        
        # delete the batch from jack_dict
        if to_delete_j in jacks_batch_dic:
            del jacks_batch_dic[to_delete_j]

        # break out after 1 year
        if week > 52:
            break
    return dataframe


if __name__ == "__main__":
    
    
    dataframe = main()

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
                                        'Hot House Total Fish Moved',
                                        'Jacks Batch Names',
                                        'Jacks Batch Start Weights (g)',
                                        'Jacks Batch End Weights (g)',
                                        'Jacks Batch Tanks',
                                        'Jacks Fish Per Tank',
                                        'Jacks Batch Densities',
                                        'Jacks Total Tanks',
                                        'Jacks Total Weight (kg)',
                                        'Jacks Total Fish Moved'])

    year_output.to_csv("Year_Output.csv", index = False)
    
    tmp = single_batch_report.select_area(year_output, 'Hot House')
    print(tmp)
    tmp = single_batch_report.select_area(year_output, 'Jacks')
    print(tmp)


