# so we should run the simulation using the parameters set and with a random batch size.
# then we find the number of "steady state" tanks occupied in Jacks which is the limiting factor
# if this number is less than 112, we increase the batch size
import pandas as pd

from simulation import simulation

def find_batch_size(**kwargs):

    batch_size = 9800
    print(f'Starting off with batch size of {batch_size}')
    from_below = True
    below = False
    above = False

    while True:
        # we save the year output dataframe
        year_output = simulation(batch_size = batch_size, **kwargs)
        # then we extract the total tanks used at steady state
        steady_state_total_tanks = year_output.tail(1)[['Hot House Total Tanks', 'Jacks Total Tanks', 'Jacks Batch End Weights (g)']]
        hot_house_total_tanks = steady_state_total_tanks['Hot House Total Tanks'].values[0]
        jacks_total_tanks = steady_state_total_tanks['Jacks Total Tanks'].values[0]
        end_weight = steady_state_total_tanks['Jacks Batch End Weights (g)'].values[0][0]
        
        distance_sq = (((112 - jacks_total_tanks) ** 4))
        if distance_sq > 1000:
            distance_sq = 1000
        elif distance_sq > 1:
            print(f'Batch Size Step: {distance_sq}; Current Jacks Tanks: {jacks_total_tanks}')
             
        # then we increase or decrease the batch size by 5 fish until we pass the 
        if (jacks_total_tanks < 112) and (below == False or above == False):
            if not below:
                print('Increasing batch size....')
                below = True
            if above:
                batch_size += int(distance_sq / 2)
            else:
                batch_size += distance_sq
            from_below = True
            
        elif jacks_total_tanks > 112 and (below == False or above == False):
            if not above:
                print('Decreasing batch size....')
                above = True
            if below:
                batch_size -= int(distance_sq / 2)
            else:
                batch_size -= distance_sq
            from_below = False
            
        else:
            # need to add in some logic to catch the cases when we are still dropping down
            if (below == False) and (above == False):
                batch_size -= distance_sq
            break
        
    # Second while loop to nudge batch size up to point before we cross 112 threshold
    if from_below:
        print('Nudging Batch Size Up')
        while True:
            year_output = simulation(batch_size = batch_size)
            # then we extract the total tanks used at steady state
            steady_state_total_tanks = year_output.tail(1)[['Hot House Total Tanks', 'Jacks Total Tanks', 'Jacks Batch End Weights (g)']]
            hot_house_total_tanks = steady_state_total_tanks['Hot House Total Tanks'].values[0]
            jacks_total_tanks = steady_state_total_tanks['Jacks Total Tanks'].values[0]
            end_weight = steady_state_total_tanks['Jacks Batch End Weights (g)'].values[0][0]
            
            if jacks_total_tanks < 113:
                batch_size += 1
            else:
                break
        # drop back below limit
        batch_size -= 1
        year_output = simulation(batch_size = batch_size)
        steady_state_total_tanks = year_output.tail(1)[['Hot House Total Tanks', 'Jacks Total Tanks', 'Jacks Batch End Weights (g)']]
        hot_house_total_tanks = steady_state_total_tanks['Hot House Total Tanks'].values[0]
        jacks_total_tanks = steady_state_total_tanks['Jacks Total Tanks'].values[0]
        end_weight = steady_state_total_tanks['Jacks Batch End Weights (g)'].values[0][0]
            
        
    optimal = {'Batch Size': batch_size,
               'Batch Tonnes': ((batch_size * (end_weight / 1000)) / 1000),
               'Hot House Total Tanks': hot_house_total_tanks,
               'Jacks Total Tanks': jacks_total_tanks}

    summary = pd.DataFrame(optimal, index = ['Optimal Values'])
    print(summary)
    
    return year_output, summary