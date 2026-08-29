import _Load_Data as LoadData
import _Load_Variables as LoadVars
import configparser
import heapq
from operator import itemgetter

config = configparser.ConfigParser()
history_draft = LoadData.load_draft_all()
history_draft = history_draft[history_draft['Year'] >= LoadVars.PASSING_ERA]
history_draft = history_draft.dropna(subset = ['College'])
beast = LoadData.load_beast()
beast = beast.dropna(subset = ['College'])

#! Below is general draft data: !#
# Get the historical draft rankings by position
grade_count_total = beast['Grade'].value_counts().to_dict()
grade_count_pos = {}
FA_count_pos = {}
RMC_count_pos = {}
total_count_pos = {}
for pos in beast['POS'].unique():
    temp = beast[beast['POS'] == pos].copy()
    grade_count_pos[pos] = temp[(temp['Grade'] != 'FA') & (temp['Grade'] != 'RMC')]['Grade'].count()
    FA_count_pos[pos] = temp[temp['Grade'] == 'FA']['Grade'].count()
    RMC_count_pos[pos] = temp[temp['Grade'] == 'RMC']['Grade'].count()
    total_count_pos[pos] = temp['Grade'].count()
# Data to write into the config
config["TotalCount"] = {"TotalGraded" : grade_count_pos,
                            "TotalFA" : FA_count_pos,
                            "TotalRMC" : RMC_count_pos,
                            "Total" : total_count_pos}


#! Below is the college odds by position: !#
for position in history_draft['POS'].unique():
    # Get positional draft frequencies
    history_draft_pos = history_draft[history_draft['POS'] == position]
    print(history_draft_pos)
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
    history_draft_data_FA = history_draft_data_FA[history_draft_data_FA['Division'] != 'DNP']
    if len(history_draft_data_FA):
        FA_freq = add_missing_divisions((history_draft_data_FA['Division'].value_counts(normalize = True)).to_dict())
    else:
        FA_freq = POWER_DIV

    # Get RMC rounds frequencies
    history_draft_data_RMC = history_draft[history_draft['Grade'] == 'RMC']
    history_draft_data_RMC = history_draft_data_RMC[history_draft_data_RMC['Division'] != 'DNP']
    if len(history_draft_data_RMC):    
        RMC_freq = add_missing_divisions((history_draft_data_RMC['Division'].value_counts(normalize = True)).to_dict())
    else:
        RMC_freq = POWER_DIV

    # Spin top 10 + 'Random'
    top_10 = weights_to_one_dict(dict(heapq.nlargest(10, pos_freq.items(), key = itemgetter(1))))

    # Data to write into the config
    position = "CollegeOdds" + position
    config[position] = {"top_10" : top_10,
                                "top_freq" : top_freq,
                                "mid_freq" : mid_freq,
                                "bot_freq" : bot_freq,
                                "FA_freq" : FA_freq,
                                "RMC_freq" : RMC_freq}
with open("C:/Users/pensh/Desktop/VSCode/DataBase/_Draft_CFG_Maker/Data/DraftGeneral.cfg", "w+", encoding = "utf-8") as configfile:
    config.write(configfile)
