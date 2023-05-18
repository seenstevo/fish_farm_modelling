# so we should run the simulation using the parameters set and with a random batch size.
# then we find the number of "steady state" tanks occupied in Jacks which is the limiting factor
# if this number is less than 112, we increase the batch size

from simulation import simulation

batch_size = 10000

while True:

    steady_state_total_tanks = simulation(batch_size = batch_size).tail(1)[['Hot House Total Tanks', 'Jacks Total Tanks']]
    hot_house_total_tanks = steady_state_total_tanks['Hot House Total Tanks'].values[0]
    jacks_total_tanks = steady_state_total_tanks['Jacks Total Tanks'].values[0]
    
    print(hot_house_total_tanks, jacks_total_tanks)
    
    if jacks_total_tanks < 112:
        batch_size += 50
    elif jacks_total_tanks > 112:
        batch_size -= 50
    else:
        break

