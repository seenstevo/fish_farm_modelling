from scipy.optimize import curve_fit, root_scalar
import pandas as pd

from variables import feed_schedule

# read in the data from feed schedule to fit data
feed_schedule_df = pd.read_csv(f'./feed_schedules/{feed_schedule}.csv')
weights = feed_schedule_df['fish_weight_upper']
percentages = feed_schedule_df['percent_body_weight']

# Fit and find equation for the feed data
def get_equation():
    # Define the curve equation
    def growth_curve(weight, a, b, c, d):
        # best formula is a rational function
        return (a * weight + b) / (c * weight + d)

    # Fit the growth curve equation to your real data
    popt, _ = curve_fit(growth_curve, weights, percentages)
    
    return popt


# Extract the fitted parameters
a, b, c, d = get_equation()


def percent_from_weight(weight):
    '''
    Using the fitted curve and given a certain weight, what is the percentage body wight for feed
    '''
    return round((a * weight + b) / (c * weight + d), 2)


# to delete once built
# # here we can get and compare the values with the guide
# import sys
# sys.path.append('../src')
# ws = [0.5, 1, 5, 15, 30, 60, 100, 200, 400, 1000]
# #ws = [0.21, 0.39, 0.99, 2.76, 5.2, 10.7, 16.1, 25, 200, 700, 1000]
# ps = []
# for w in ws:
#     p = percent_from_weight(w)
#     ps.append(p)
#     print(p)

