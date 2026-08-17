from _Load_Data import *
from _Load_Variables import *
import configparser

config = configparser.ConfigParser()
beast = load_beast(site = 'p')
print(beast)



with open("C:/Users/pensh/Desktop/VSCode/DataBase/_Draft_CFG_Maker/Data/DraftTestingByPosition.cfg", "w+", encoding = "utf-8") as configfile:
    config.write(configfile)