import pandas as pd
import sys

sys.path.append('src')

import simulation
import single_batch_report
import fish_moves_distribution


if __name__ == "__main__":
    '''
    In the main function, we generate the 3 files that contain the data on the simulation:
    1) A summary of a full year (52 weeks)
    2) A summary of a single batch
    3) The distribution of the frequency of moves allowing estimates of the trade off between greater space optimising and this source of fish stress
    '''
    # get the dataframe returned by the simulation function
    year_output = simulation.simulation()
    
    # shift the fish moved column up one row
    year_output['Hot House Fish Moved Per Tank'] = (year_output['Hot House Fish Moved Per Tank']
                                                    .shift(periods = -1, fill_value = 0))
    year_output['Jacks Fish Moved Per Tank'] = (year_output['Jacks Fish Moved Per Tank']
                                                    .shift(periods = -1, fill_value = 0))
    # save the full Year Report
    year_output.to_csv("Year_Output.csv", index = False)
    
    
    # Generate single batch dataframe
    batch_report = single_batch_report.select_area(year_output)
    batch_report['Fish Move Probs'] = (batch_report['Fish Moved Per Tank'] / 
                                       batch_report['Fish Per Tank'])
    # save the single batch details to file
    batch_report.to_csv("Single_Batch_Report_Card.csv")
    
    
    # Calculate the Probability of 0-n fish moves where n is the weeks of batch
    fish_move_freq_probs = fish_moves_distribution.convolve_binomial(batch_report['Fish Move Probs'])
    fish_move_freq_df = pd.DataFrame({'Number of Times Moved': range(len(fish_move_freq_probs)),
                                    'Percentage': fish_move_freq_probs})
    # save the distribution of fish moves to file
    fish_move_freq_df.to_csv("Fish_Moved_Percentage_Distribution.csv", index = False)