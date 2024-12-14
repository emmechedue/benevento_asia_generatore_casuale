import pandas as pd
import numpy as np

####################################
### Genera numeri casuali
####################################


def _check_if_common_streets_and_return_new_chosen(chosen_nums, current_tipo, elenco_punti_prelievo):
    any_nums_overlap = elenco_punti_prelievo.loc[(current_tipo, chosen_nums),:].duplicated(subset='nome_strada_senza_punti').any()
    
    if(not any_nums_overlap):
        final_chosen = chosen_nums
    else:
        final_chosen = elenco_punti_prelievo.loc[current_tipo].loc[chosen_nums].drop_duplicates(subset='nome_strada_senza_punti').index.values

    return any_nums_overlap, final_chosen


def _return_new_chosen_values(any_nums_overlap, kept_chosen, total_num_of_choices, nums_from_which_to_choose, rng):
    if(not any_nums_overlap):
        final_chosen =  kept_chosen
    else:
        new_num_to_sample = total_num_of_choices - len(kept_chosen)
        new_sampled_nums = rng.choice(nums_from_which_to_choose, new_num_to_sample)
        final_chosen = np.append(kept_chosen, new_sampled_nums)

    return final_chosen


def _return_final_choice_without_street_overlap(inital_choice, current_tipo, nums_from_which_to_choose, elenco_punti_prelievo, rng):
    total_num_of_choices = len(inital_choice)
    any_nums_overlap = True
    current_chosen = inital_choice

    while(any_nums_overlap):
        any_nums_overlap, kept_chosen = _check_if_common_streets_and_return_new_chosen(current_chosen, current_tipo, elenco_punti_prelievo)
        current_chosen = _return_new_chosen_values(any_nums_overlap, kept_chosen, total_num_of_choices, nums_from_which_to_choose, rng)
        print('\n')

    return current_chosen


def return_final_set_of_chosen_numbers(current_tipo, the_error_choice,dict_with_the_number_of_things_to_sample, elenco_punti_prelievo,rng, alllow_same_street=False):
    nums_from_which_to_choose = elenco_punti_prelievo.loc[current_tipo].index
    how_many_nums_to_choose = dict_with_the_number_of_things_to_sample[the_error_choice][current_tipo]
    chosen_nums = rng.choice(nums_from_which_to_choose,how_many_nums_to_choose)

    if(alllow_same_street):
        return chosen_nums
    else:
        return _return_final_choice_without_street_overlap(chosen_nums, current_tipo, nums_from_which_to_choose, elenco_punti_prelievo, rng)
    

####################################
### Genera e separa seme
####################################

def put_together_seed_and_params(seed_int,  the_error_choice, allow_same_street):
    seed_str = str(seed_int)
    
    if(allow_same_street):
        street_str = '1'
    else:
        street_str = '0'
    if(the_error_choice=='1%'):
        error_str = '1'
    else:
        error_str = '5'

    return int(error_str+seed_str+street_str)

def extract_error_and_str_params(entire_seed):
    seed_str = str(entire_seed)
    error_str = seed_str[0]
    allow_str = seed_str[-1]

    print(error_str)

    if(error_str=='1'):
        the_error_choice='1%'
    else:
        the_error_choice='5%'

    if(allow_str=='1'):
        allow_same_street = True
    else:
        allow_same_street = False

    return the_error_choice, allow_same_street