from _Load_Data import *
from _Load_Variables import *
import configparser

config = configparser.ConfigParser()
df = load_college()

for division in sorted(df['Division'].unique(), reverse = True):
    config[division] = {}
    df_div_level = df[df['Division'] == division]
    for conference in df_div_level['Conference'].unique():
        config[division][conference] = ''
        df_conf_level = df_div_level[df_div_level['Conference'] == conference]
        college_list = []
        for school in df_conf_level['College'].unique():
            college_list.append(school)
        config[division][conference] = str(college_list)



with open("C:/Users/pensh/Desktop/VSCode/DataBase/_Draft_CFG_Maker/Data/CollegeByDivAndConf.cfg", "w", encoding = "utf-8") as configfile:
    config.write(configfile)