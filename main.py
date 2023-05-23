import pandas as pd
import sys

sys.path.append('src')

from simulation import simulation
from batch_size_calculation import find_batch_size
import single_batch_report
import fish_moves_distribution
import feeding_schedule_calculation


if __name__ == "__main__":
    '''
    In the main function, we generate the 3 files that contain the data on the simulation:
    1) A summary of a full year (52 weeks)
    2) A summary of a single batch
    3) The distribution of the frequency of moves allowing estimates of the trade off between greater space optimising and this source of fish stress
    '''
    ####################################################################
    # run the batch_size_calculation function which uses the simulation to find max batch size that fits in Jacks
    year_output, _ = find_batch_size()
    # save the full Year Report
    year_output.to_csv("Year_Output.csv", index = False)
    
    ####################################################################
    # Generate single batch dataframe
    batch_report = single_batch_report.select_area(year_output)
    # add the column which shows the probability of a given fish being moved in a given week
    batch_report['Fish Move Probs'] = (batch_report['Fish Moved Per Tank'] / batch_report['Fish Per Tank'])
    # Round non-zero values in the column
    batch_report['Fish Move Probs'] = batch_report['Fish Move Probs'].apply(lambda x: round(x, 2) if x != 0 else 0)
    # Add the feed schedule columns to the single batch report
    batch_report = feeding_schedule_calculation.add_feed_schedule_columns(batch_report)
    # Add the culmulative feed and FCR columns
    batch_report = feeding_schedule_calculation.culmulative_feed(batch_report)
    
    # save the single batch details to file
    batch_report.to_csv("Single_Batch_Report_Card.csv")
    
    ####################################################################
    # Calculate the Probability of 0-n fish moves where n is the total weeks of growth for a batch
    fish_move_freq_probs = fish_moves_distribution.convolve_binomial(batch_report['Fish Move Probs'])
    fish_move_freq_df = pd.DataFrame({'Number of Times Moved': range(len(fish_move_freq_probs)),
                                      'Percentage': fish_move_freq_probs})
    # save the distribution of fish moves to file
    fish_move_freq_df.to_csv("Fish_Moved_Percentage_Distribution.csv", index = False)