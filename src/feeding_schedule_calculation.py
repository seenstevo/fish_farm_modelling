# which feeding schedule

# based on weight, find the percentage feed

# return the percent, feed and the total kg per tank

import pandas as pd

# load in the variable with feed schedule file name
from variables import feed_schedule


def add_feed_schedule_columns(single_batch_report):
    # first we read in the wanted feed schedule
    single_batch_report[['Body Weight %', 'Feed Type', 'Feed Per Tank (kg)']] = single_batch_report.apply(apply_by_row, axis = 1, result_type = 'expand')
    
    return single_batch_report
    

def apply_by_row(row):
    weight = row['Batch End Weights (g)']
    fish_per_tank = row['Fish Per Tank']
    feed_schedule_row = get_feed_schedule_row(weight)
    percentage_feed = feed_schedule_row['percent_body_weight'].iloc[0]
    feed_type = feed_schedule_row['feed_type'].iloc[0]
    # now we calculate the total grams of feed per tank
    total_feed_per_tank = round(fish_per_tank * (weight / 1000) * (percentage_feed / 100), 2)
    return percentage_feed, feed_type, total_feed_per_tank


def get_feed_schedule_row(weight):
    # load feeding schedule file into pandas dataframe
    feed_schedule_df = pd.read_csv(f'./feed_schedules/{feed_schedule}.csv')
    return feed_schedule_df[(feed_schedule_df['fish_weight_lower'] < weight) & (feed_schedule_df['fish_weight_upper'] > weight)]

