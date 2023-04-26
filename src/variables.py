import numpy as np

weekly_weights = np.array([0.5, 2, 3.6, 5.6, 8, 11.2, 15.6, 21.6, 29.2, 38.4, 49.2, 61.2, 74.4, 90.4, 109.2, 130.8, 
                           154, 178.8, 205.6, 233.2, 260, 286, 311.74, 339.78, 366.98, 396.34, 424.08, 453.77])


fingerling_g = 2   # weight of each fingerling in grams
hothouse_max_d = 12 # maximum density in the hot house in kg/m3
batch_size = 10000    # how many fish do we start with in Hot House
hothhouse_weeks = 7 # total number of weeks spent in the hot house
jacks_max_d = 20  # maximum density in Jack's in kg/m3
target_weight = 440    # target weight for each fish at harvest (450g)
harvest_freq = 1  # harvest frequency in weeks