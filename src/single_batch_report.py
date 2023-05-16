import pandas as pd
import numpy as np

from variables import feed_schedule


def select_first_batch(row):
    '''
    function to grab the first item in each column
    this belongs to the first batch ("batch0")
    '''
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


def select_farm_area_single_batch(df: pd.DataFrame, farm_area: str):
    '''
    Given the full year dataframe and a farm area, subset only rows and columns relating to this farm area
    '''
    mask_row = df[f'{farm_area} Batch Names'].apply(lambda x: 'batch0' in x)
    mask_col = [((farm_area in col) and ('Batch Names' not in col)) for col in df.columns]
    farm_area_df = df.loc[mask_row, mask_col]
    farm_area_df['Farm_Area'] = farm_area
    
    return farm_area_df.apply(select_first_batch, axis = 0).values
    

def select_area(full_df):
    '''
    To just select rows and columns relating to single batch in each farm area
    '''
    hh_df = select_farm_area_single_batch(full_df, 'Hot House')
    j_df = select_farm_area_single_batch(full_df, 'Jacks')
    
    return pd.DataFrame(np.concatenate([hh_df, j_df], axis = 0),
                        columns = ['Batch Start Weights (g)',
                                   'Batch End Weights (g)',
                                   'Batch Tanks',
                                   'Fish Per Tank',
                                   'Batch Densities',
                                   'Total Tanks',
                                   'Total Weight (kg)',
                                   'Fish Moved Per Tank',
                                   'Farm Area'])