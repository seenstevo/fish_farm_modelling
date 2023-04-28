
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


def select_area(full_df, area: str):
    '''
    To just select rows and columns relating to single batch in hot house
    '''
    mask_row = full_df[f'{area} Batch Names'].apply(lambda x: 'batch0' in x)
    mask_col = [area in col for col in full_df.columns]
    area_df = full_df.loc[mask_row, mask_col]  
    
    area_df = area_df.apply(select_batch0, axis = 0)
    
    return area_df




    #tmp.to_csv("SingleBatch.csv", index = False)
    
    
    
    
# maskj = year_output['Jacks Batch Names'].apply(lambda x: 'batch0' in x)
# mask = (maskhh | maskj)
# tmp = year_output[mask]