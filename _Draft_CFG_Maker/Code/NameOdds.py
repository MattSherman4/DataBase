from Load_Data import *
from Load_Variables import *
import configparser

def setNameOdds():
    DEFAULT_NORMAL = 1
    DEFAULT_SPECIAL = 0
    INCREASE_PER_INSTANCE = 1


    history_draft = load_draft_all()
    history_draft = history_draft[history_draft['Year'] >= MODERN_ERA].copy()

    #  Does the math to get the weighted name dictionaries
    def name_data(history_draft, first_count, first_hyphen_total, last_count, last_hyphen_total, suffix_count, suffix_total):
        history_draft['Name'] = history_draft['Name'].str.title()
        nameCol = history_draft['Name'].str.split(' ')
        for i in nameCol:
            if len(i) == 2:
                first_count, first_hyphen_total = first_name(i[0], first_count, first_hyphen_total)
                last_count, last_hyphen_total = last_name(i[1], last_count, last_hyphen_total)
            elif len(i) == 3:
                first_count, first_hyphen_total = first_name(i[0], first_count, first_hyphen_total)
                #TODO: Does this work?
                if i[1] in double_name:
                    last_count, last_hyphen_total = last_name(' '.join(i[1:3]), last_count, last_hyphen_total)
                else:
                    last_count, last_hyphen_total = last_name(i[1], last_count, last_hyphen_total)
                    suffix_count, suffix_total,last_count, last_hyphen_total = suffix(i[2], suffix_count, suffix_total, last_count, last_hyphen_total)
        return first_count, first_hyphen_total, last_count, last_hyphen_total, suffix_count, suffix_total


    #- Data for a name -#
    #_ Data for a first name _#
    #  Fills the first_count and first_hyphen_total variables, calculating statistical weights for first names
    def first_name(s, first_count, first_hyphen_total):
        if '-' not in s:
            s = check_special(s)
            # Non-hyphenated names default to a weight of 2 to lessen the chance of a non-unique hyphenated name
            first_count[s] = first_count.get(s, DEFAULT_NORMAL) + INCREASE_PER_INSTANCE
        else:
            first_hyphen_total += 1
            #  Seperate hyphenated names since they are not last names
            s = s.split('-')
            for name in s:
                name = check_special(name)
                first_count, first_hyphen_total = last_name(name, first_count, first_hyphen_total)
        return first_count, first_hyphen_total

    #_ Data for a last name _#
    #  Fills the last_count and last_hyphen_total variables, calculating statistical weights for last names
    def last_name(s, last_count, last_hyphen_total):
        if '-' not in s:
            s = check_special(s)
            # Non-hyphenated names default to a weight of 2 to lessen the chance of a non-unique hyphenated name
            last_count[s] = last_count.get(s, DEFAULT_NORMAL) + INCREASE_PER_INSTANCE
        else:
            last_hyphen_total += 1
            #  Keep hyphenated names together for story line puropses
            last_count[s] = last_count.get(s, DEFAULT_SPECIAL) + INCREASE_PER_INSTANCE
            #  Also split the name and use both halves independantly in the dictionary 
            s = s.split('-')
            for name in s:
                name = check_special(name)
                last_count, last_hyphen_total = last_name(name, last_count, last_hyphen_total)
        return last_count, last_hyphen_total

    #_ Data for a suffix _#
    #  Fills the suffix_count and suffix_total variables, calculating statistical weights for suffixes
    def suffix(s, suffix_count, suffix_total, last_count, last_hyphen_total):
        if s not in generational_suffixes:
            last_count, last_hyphen_total = last_name(s, last_count, last_hyphen_total)
            return suffix_count, suffix_total, last_count, last_hyphen_total
        s = check_special(s)
        suffix_total += 1
        suffix_count[s] = suffix_count.get(s, DEFAULT_SPECIAL) + INCREASE_PER_INSTANCE
        return suffix_count, suffix_total, last_count, last_hyphen_total

    #_ Quick fix for name grammar error _#
    #  Changes special names
    #TODO: Combine this with util_Data
    def check_special(s:str):
        if len(s) > 2 and s[-2] == "'":
            s = s[:-1] + s[-1].lower()
        if s[:2] == 'Mc':
            return 'Mc' + s[2:].title()
        if s in special:
            if s == 'J':
                return ''
            elif s == 'K':
                return ''
            elif s == 'Lequint':
                return 'LeQuint'
        if s in Upper:
            return s.upper()
        return s
    
    first_count = {}
    first_hyphen_total = 0
    last_count = {}
    last_hyphen_total = 0
    suffix_count = {}
    suffix_total = 0

    first_count, first_hyphen_total, last_count, last_hyphen_total, suffix_count, suffix_total = name_data(history_draft, first_count, first_hyphen_total, last_count, last_hyphen_total, suffix_count, suffix_total)

    try:
        del first_count['']
    except:
        pass
    try:
        del last_count['']
    except:
        pass
    try:
        del suffix_count['']
    except:
        pass

    total = float(len(history_draft))
    first_hyphen_percentage = round((first_hyphen_total / total) * 10.0, 5)
    last_hyphen_percentage = round((last_hyphen_total / total) * 10.0, 5)
    suffix_percentage = round((suffix_total / total) * 10.0, 5)

    config = configparser.ConfigParser()
    config["Percentages"] = {"first_hyphen_percentage" : first_hyphen_percentage,
                             "last_hyphen_percentage" : last_hyphen_percentage,
                             "suffix_percentage" : suffix_percentage}
    config["Names"] = {"first_count" : first_count, "last_count" : last_count, "suffix_count" : suffix_count}
    with open("C:/Users/pensh/Desktop/VSCode/DataBase/_Draft_CFG_Maker/Data/names.cfg", "w", encoding = "utf-8") as configfile:
        config.write(configfile)

setNameOdds()   
