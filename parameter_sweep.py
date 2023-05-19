import itertools
import sys

sys.path.append('src')

from batch_size_calculation import find_batch_size


def parameter_sweep():
    parameters = {
        'hothhouse_weeks': [6, 7, 8],
        'jacks_start_period_weeks': [4],
        'jacks_end_two_weeks': [19, 25],
        'custom_round_denominator': [12, 24],
        'fingerling_g': [2, 1.6],
        'hothouse_maxmin_d': [12, 8],
        'jacks_maxmin_d': [24, 16],
        'target_weight': [440, 360]
    }

    max_tonnes = float('-inf')
    best_combination = None

    parameter_combinations = itertools.product(*parameters.values())
    print(f'We have {len(list(parameter_combinations))} parameter combinations')
    parameter_combinations = itertools.product(*parameters.values())
    x = 1

    for combination in parameter_combinations:
        print('#'*50)
        print(f'Combination {x}')
        x += 1
        # Unpack the combination into individual parameter values
        print(combination)
        hothhouse_weeks, jacks_start_period_weeks, jacks_end_two_weeks, \
            custom_round_denominator, fingerling_g, \
                hothouse_maxmin_d, jacks_maxmin_d, \
                    target_weight = combination

        # Call your function or calculation here to get the output value
        _, summary = find_batch_size(hothhouse_weeks = hothhouse_weeks, jacks_start_period_weeks = jacks_start_period_weeks, 
                                     jacks_end_two_weeks = jacks_end_two_weeks, custom_round_denominator = custom_round_denominator, 
                                     fingerling_g = fingerling_g, hothouse_maxmin_d = hothouse_maxmin_d, jacks_maxmin_d = jacks_maxmin_d,
                                     target_weight = target_weight)
        tonnes = summary['Batch Tonnes'].values[0]
        if tonnes > max_tonnes:
            max_tonnes = tonnes
            best_combination = combination

    return best_combination, max_tonnes

best_combination, max_tonnes = parameter_sweep()


#        'harvest_freq': [1, 2]