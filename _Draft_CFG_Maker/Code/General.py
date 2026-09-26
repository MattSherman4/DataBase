import configparser

config = configparser.ConfigParser()

config['General'] = {
    'MODERN_ERA' : 1970,
    'PASSING_ERA' : 2004,
    'DEFAULT_DIV' : 'FBS',
    'DEFAULT_CONF' : 'SEC',
    'POWER_CONF' : {'SEC' : 0.25, 'Big Ten' : 0.25, 'ACC' : 0.25, 'Big 12' : 0.25},
    'POWER_DIV' : {'FBS' : 0.90, 'FCS' : 0.09, 'DII' : 0.01},
    'Years_With_Full_Beast_Data' : [2025],
    'Primary_Positions' : ['QB', 'HB', 'WR', 'TE', 'OT', 'OG', 'C', 'EDGE', 'DT', 'MLB', 'CB', 'S', 'K', 'P', 'LS'], # Currently available positions. Could be changed with storylines later on
                     
}


with open("C:/Users/pensh/Desktop/VSCode/DataBase/_Draft_CFG_Maker/Data/General.cfg", "w+", encoding = "utf-8") as configfile:
    config.write(configfile)