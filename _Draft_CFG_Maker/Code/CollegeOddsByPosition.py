from _Load_Data import *
from _Load_Variables import *
import configparser
import heapq
from operator import itemgetter

config = configparser.ConfigParser()
history_draft = load_draft_all()
history_draft = history_draft[history_draft['Year'] >= PASSING_ERA]
history_draft = history_draft.dropna(subset = ['College'])

for position in history_draft['POS'].unique():
    # Get positional draft frequencies
    history_draft_pos = history_draft[history_draft['POS'] == position]
    pos_freq = add_missing_divisions((history_draft_pos['College'].value_counts(normalize = True)).to_dict())

    # Get top rounds frequencies. Use Conf instead of Div to narrow the field more in early rounds
    history_draft_data_top = history_draft_pos[history_draft_pos['Rnd'] <= draft_grades_round_cutoff['Top']]
    top_freq = history_draft_data_top['Conference'].value_counts(normalize = True).to_dict()
    if len(top_freq):
        top_freq = weights_to_one_dict(top_freq, max(top_freq, key = top_freq.get))
    else:
        top_freq = POWER_CONF

    # Get Middle rounds frequencies
    history_draft_data_mid = history_draft_pos[history_draft_pos['Rnd'] > draft_grades_round_cutoff['Top']]
    history_draft_data_mid = history_draft_data_mid[history_draft_data_mid['Rnd'] <= draft_grades_round_cutoff['Middle']]
    if len(history_draft_data_mid):
        mid_freq = add_missing_divisions((history_draft_data_mid['Division'].value_counts(normalize = True)).to_dict())
    else:
        mid_freq = POWER_DIV

    # Get Bottom rounds frequencies
    history_draft_data_bot = history_draft_pos[history_draft_pos['Rnd'] > draft_grades_round_cutoff['Middle']]
    if len(history_draft_data_bot):
        bot_freq = add_missing_divisions((history_draft_data_bot['Division'].value_counts(normalize = True)).to_dict())
    else:
        bot_freq = POWER_DIV

    # Get FA rounds frequencies
    #TODO: Get actual UDFA Data?
    history_draft_data_FA = history_draft[history_draft['Grade'] == 'FA']
    if len(history_draft_data_FA):
        FA_freq = add_missing_divisions((history_draft_data_FA['Division'].value_counts(normalize = True)).to_dict())
    else:
        FA_freq = POWER_DIV

    # Get RMC rounds frequencies
    history_draft_data_RMC = history_draft[history_draft['Grade'] == 'RMC']
    if len(history_draft_data_RMC):    
        RMC_freq = add_missing_divisions((history_draft_data_RMC['Division'].value_counts(normalize = True)).to_dict())
    else:
        RMC_freq = POWER_DIV

    # Spin top 10 + 'Random'
    top_10 = weights_to_one_dict(dict(heapq.nlargest(10, pos_freq.items(), key = itemgetter(1))))

    # Data to write into the config
    config[position] = {"top_10" : top_10,
                                "top_freq" : top_freq,
                                "mid_freq" : mid_freq,
                                "bot_freq" : bot_freq,
                                "FA_freq" : FA_freq,
                                "RMC_freq" : RMC_freq}
with open("C:/Users/pensh/Desktop/VSCode/DataBase/_Draft_CFG_Maker/Data/CollegeOddsByPosition.cfg", "w", encoding = "utf-8") as configfile:
    config.write(configfile)
