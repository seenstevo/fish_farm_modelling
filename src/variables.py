import numpy as np

weekly_weights = np.array([0.5, 2, 3.6, 5.6, 8, 11.2, 15.6, 21.6, 29.2, 38.4, 49.2, 61.2, 74.4, 90.4, 109.2, 130.8, 
                           154, 178.8, 205.6, 233.2, 260, 286, 311.74, 339.78, 366.98, 396.34, 424.08, 453.77])


fingerling_g = 2   # weight of each fingerling in grams
hothouse_max_d = 12 # maximum density in the hot house in kg/m3
hothouse_maxmin_d = 12   # the maximum that the lower bound can be, to reduce total moves at cost of space efficieny
batch_size = 9800    # how many fish do we start with in Hot House
hothhouse_weeks = 7 # total number of weeks spent in the hot house
jacks_max_d = 24  # maximum density in Jack's in kg/m3
jacks_maxmin_d = 24   # the maximum that the lower bound can be, to reduce total moves at cost of space efficieny
target_weight = 440    # target weight for each fish at harvest (450g)
harvest_freq = 1  # harvest frequency in weeks
hothouse_tank_vol = 1  # size in m3 of each tank
jacks_tank_vol = 16  # size in m3 of each tank
jacks_start_period_weeks = 4    # here we can specifiy that we want the fish to not be moved for x weeks upon arrival to Jacks
jacks_end_two_weeks = 19    # this is the week, after which we enforce 2 week growth periods between moves
#feed_schedule = 'specialised_aquatic_feeds_tilapia'
feed_schedule = 'skretting_tilapia'