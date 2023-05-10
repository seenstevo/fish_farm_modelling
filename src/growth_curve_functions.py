from scipy.optimize import curve_fit, root_scalar
import numpy as np

from variables import weekly_weights


# create the weeks for the growth data
weeks = np.arange(len(weekly_weights))

# Fit and find equation for the growth data
def get_equation():
    # Define the growth curve equation
    def growth_curve(t, a, b, c, d, e, f):
        return (a * t) + (b * t**2) + (c * t**3) + (d * t**4) + (e * t**5) + f


    # Fit the growth curve equation to your real data
    popt, _ = curve_fit(growth_curve, weeks, weekly_weights)
    
    return popt



# Extract the fitted parameters
a, b, c, d, e, f = get_equation()


# final equation fitted to growth data
def weight_from_time(t):
    '''
    Given a certain time, what is the weight
    '''
    return (a * t) + (b * t**2) + (c * t**3) + (d * t**4) + (e * t**5) + f


# inverse equation to find time (weeks) from a given weight
def time_from_weight(weight):
    '''
    Given a certain weight, what is the time
    '''
    def poly_growth_curve(t):
        return (a * t) + (b * t**2) + (c * t**3) + (d * t**4) + (e * t**5) + f - weight
    sol = root_scalar(poly_growth_curve, bracket=[0, 27])
    return sol.root



# how many fish are needed to occupy tank with maximum stocking density
def n_for_max_density(md, g, vol):
    '''
    To calculate how many fish "n" of size g are needed to reach the max density
    '''
    return (md * vol) / (g / 1000)