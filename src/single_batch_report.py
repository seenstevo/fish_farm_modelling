import pandas as pd
import numpy as np


def select_batch0(row):
        new_row = []
        for col in row:
            if type(col) == list:
                if len(col) > 0:
                    new_row.append(col[0])
                else:
                    new_row.append("-")
            else:
                new_row.append(col)
        return new_row


def select_area(full_df):
    '''
    To just select rows and columns relating to single batch in hot house
    '''
    hh_mask_row = full_df['Hot House Batch Names'].apply(lambda x: 'batch0' in x)
    hh_mask_col = [(('Hot House' in col) and ('Batch Names' not in col)) for col in full_df.columns]
    hh_df = full_df.loc[hh_mask_row, hh_mask_col]
    hh_df['Farm_Area'] = 'Hot House'
    hh_df = hh_df.apply(select_batch0, axis = 0).values
    
    j_mask_row = full_df['Jacks Batch Names'].apply(lambda x: 'batch0' in x)
    j_mask_col = [(('Jacks' in col) and ('Batch Names' not in col)) for col in full_df.columns]
    j_df = full_df.loc[j_mask_row, j_mask_col]
    j_df['Farm_Area'] = 'Jacks'
    j_df = j_df.apply(select_batch0, axis = 0).values
    
    df = pd.DataFrame(np.concatenate([hh_df, j_df], axis = 0), 
                      columns = ['Batch Start Weights (g)',
                                 'Batch End Weights (g)',
                                 'Batch Tanks',
                                 'Fish Per Tank',
                                 'Batch Densities',
                                 'Total Tanks',
                                 'Total Weight (kg)',
                                 'Fish Moved Per Tank',
                                 'Farm Area'])
    
    return df




    #tmp.to_csv("SingleBatch.csv", index = False)
    
    
    
    
# maskj = year_output['Jacks Batch Names'].apply(lambda x: 'batch0' in x)
# mask = (maskhh | maskj)
# tmp = year_output[mask]