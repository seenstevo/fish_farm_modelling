# which feeding schedule

# based on weight, find the percentage feed

# return the percent, feed and the total kg per tank

import pandas as pd

# load in the variable with feed schedule file name
from variables import feed_schedule
from fit_feed_schedule_curve import percent_from_weight


def add_feed_schedule_columns(single_batch_report):
    # first we read in the wanted feed schedule
    single_batch_report[['Start Body Weight %', 'End Body Weight %', 'Start Feed Per Tank (kg)', 'End Feed Per Tank (kg)', 'Feed Type']] = single_batch_report.apply(apply_by_row, axis = 1, result_type = 'expand')
    
    return single_batch_report
    

def apply_by_row(row):
    start_weight = row['Batch Start Weights (g)']
    end_weight = row['Batch End Weights (g)']
    fish_per_tank = row['Fish Per Tank']
    feed_schedule_row = get_feed_schedule_row(end_weight)
    feed_type = feed_schedule_row['feed_type'].iloc[0]
    # now we use the start and end weights to get the feed body weight percent
    start_percentage_feed = percent_from_weight(start_weight)
    end_percentage_feed = percent_from_weight(end_weight)
    
    # now we calculate the total grams of feed per tank
    start_total_feed_per_tank = round(fish_per_tank * (start_weight / 1000) * (start_percentage_feed / 100), 2)
    end_total_feed_per_tank = round(fish_per_tank * (end_weight / 1000) * (end_percentage_feed / 100), 2)
    return start_percentage_feed, end_percentage_feed, start_total_feed_per_tank, end_total_feed_per_tank, feed_type


def get_feed_schedule_row(weight):
    # load feeding schedule file into pandas dataframe
    feed_schedule_df = pd.read_csv(f'./feed_schedules/{feed_schedule}.csv')
    return feed_schedule_df[(feed_schedule_df['fish_weight_lower'] < weight) & (feed_schedule_df['fish_weight_upper'] > weight)]
