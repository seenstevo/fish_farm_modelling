# so we should run the simulation using the parameters set and with a random batch size.
# then we find the number of "steady state" tanks occupied in Jacks which is the limiting factor
# if this number is less than 112, we increase the batch size
import pandas as pd

from simulation import simulation

def find_batch_size():

    batch_size = 9500
    print(f'Starting off with batch size of {batch_size}')
    from_below = True

    while True:
        # we save the year output dataframe
        year_output = simulation(batch_size = batch_size)
        # then we extract the total tanks used at steady state
        steady_state_total_tanks = year_output.tail(1)[['Hot House Total Tanks', 'Jacks Total Tanks']]
        hot_house_total_tanks = steady_state_total_tanks['Hot House Total Tanks'].values[0]
        jacks_total_tanks = steady_state_total_tanks['Jacks Total Tanks'].values[0]
        
        distance_sq = (((112 - jacks_total_tanks) ** 2) + 20)
        print(f'Batch Size step: {distance_sq}')
             
        # then we increase or decrease the batch size by 5 fish until we pass the 
        if jacks_total_tanks < 112:
            if batch_size == 9500:
                print('Increasing batch size....')
            batch_size += distance_sq
            from_below = True
        elif jacks_total_tanks > 112:
            if batch_size == 9500:
                print('Decreasing batch size....')
            batch_size -= distance_sq
            from_below = False 
        else:
            break

    if from_below:
        while True:
            year_output = simulation(batch_size = batch_size)
            # then we extract the total tanks used at steady state
            steady_state_total_tanks = year_output.tail(1)[['Hot House Total Tanks', 'Jacks Total Tanks']]
            hot_house_total_tanks = steady_state_total_tanks['Hot House Total Tanks'].values[0]
            jacks_total_tanks = steady_state_total_tanks['Jacks Total Tanks'].values[0]
            
            if jacks_total_tanks < 113:
                batch_size += 2
            else:
                break
        # drop back below limit
        batch_size -= 2
        year_output = simulation(batch_size = batch_size)
        steady_state_total_tanks = year_output.tail(1)[['Hot House Total Tanks', 'Jacks Total Tanks']]
        hot_house_total_tanks = steady_state_total_tanks['Hot House Total Tanks'].values[0]
        jacks_total_tanks = steady_state_total_tanks['Jacks Total Tanks'].values[0]
            
        
    optimal = {'Batch Size': batch_size,
               'Batch Tonnes': ((batch_size * 0.45) / 1000),
               'Hot House Total Tanks': hot_house_total_tanks,
               'Jacks Total Tanks': jacks_total_tanks}

    print(pd.DataFrame(optimal, index = ['Optimal Values']))
    
    return year_output