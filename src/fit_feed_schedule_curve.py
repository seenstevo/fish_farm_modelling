from scipy.optimize import curve_fit
import pandas as pd
import numpy as np

from variables import feed_schedule

# read in the data from feed schedule to fit data
feed_schedule_df = pd.read_csv(f'./feed_schedules/{feed_schedule}.csv')
# now set the x and y values
weights = feed_schedule_df['fish_weight_upper']
percentages = feed_schedule_df['percent_body_weight']
sigmas = feed_schedule_df['point_importance']

# Fit and find equation for the feed data
def get_equation():
    # Define the curve equation
    def growth_curve(weight, a, b, c, d):
        # best formula is a rational function
        return (a * weight + b) / (c * weight + d)

    # Fit the growth curve equation to your real data
    popt, _ = curve_fit(growth_curve, weights, percentages, sigma = sigmas)
    
    return popt


# Extract the fitted parameters
a, b, c, d = get_equation()


def percent_from_weight(weight):
    '''
    Using the fitted curve and given a certain weight, what is the percentage body wight for feed
    '''
    return round((a * weight + b) / (c * weight + d), 2)


# #to delete once built
# # here we can get and compare the values with the guide
# import sys
# import pandas as pd
# import numpy as np
# from scipy.optimize import curve_fit
# sys.path.append('../src')
# from variables import feed_schedule
# feed_schedule_df = pd.read_csv(f'../feed_schedules/{feed_schedule}.csv')

# ws = [1, 5, 15, 30, 60, 100, 200, 400, 700]
# #ws = [0.99, 2.76, 5.2, 10.7, 16.1, 25, 200, 400, 700]
# ps = []
# for w in ws:
#     p = percent_from_weight(w)
#     ps.append(p)
#     print(p)

