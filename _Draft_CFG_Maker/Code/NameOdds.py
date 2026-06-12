from Load_Data import *
from Load_Variables import *

def setNameOdds():
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
            # Non-hyphenated names default to a weight of 2 to lessen the chance of a non-unique hyphenated name
            first_count[s] = first_count.get(s, 99) + 50
        else:
            first_hyphen_total += 1
            #  Seperate hyphenated names since they are not last names
            s = s.split('-')
            first_count[s[0]] = first_count.get(s[0], 0) + 50
            first_count[s[-1]] = first_count.get(s[-1], 0) + 50
        return first_count, first_hyphen_total

    #_ Data for a last name _#
    #  Fills the last_count and last_hyphen_total variables, calculating statistical weights for last names
    def last_name(s, last_count, last_hyphen_total):
        if '-' not in s:
            # Non-hyphenated names default to a weight of 2 to lessen the chance of a non-unique hyphenated name
            last_count[s] = last_count.get(s, 99) + 50
        else:
            last_hyphen_total += 1
            #  Keep hyphenated names together for story line puropses
            last_count[s] = last_count.get(s, 0) + 50
            #  Also split the name and use both halves independantly in the dictionary 
            s = s.split('-')
            for name in s:
                last_count, last_hyphen_total = last_name(name, last_count, last_hyphen_total)
        return last_count, last_hyphen_total

    #_ Data for a suffix _#
    #  Fills the suffix_count and suffix_total variables, calculating statistical weights for suffixes
    def suffix(s, suffix_count, suffix_total, last_count, last_hyphen_total):
        if s not in generational_suffixes:
            last_count, last_hyphen_total = last_name(s, last_count, last_hyphen_total)
            return suffix_count, suffix_total, last_count, last_hyphen_total
        suffix_total += 1
        suffix_count[s] = suffix_count.get(s, 0) + 50
        return suffix_count, suffix_total, last_count, last_hyphen_total

    # #_ Quick fix for str title error _#
    # #  Special title to fix str.title()'s apostrophe problem
    # def special_title(s:str):
    #     s = s.title()
    #     return s

    #_ Quick fix for name grammar error _#
    #  Changes special names
    #TODO: Combine this with util_Data
    def check_special(s:str, first_count, last_count, suffix_count):
        if len(s) > 2 and s[-2] == "'":
            s = s[:-1] + s[-1].lower()
        if s[:2] == 'Mc':
            return 'Mc' + s[2:].title()
        if s in special:
            if s == 'J':
                return random_name(0, first_count, last_count, suffix_count)
            elif s == 'K':
                return random_name(0, first_count, last_count, suffix_count)
            elif s == 'Lequint':
                return 'LeQuint'
            elif s == 'Rock':
                return random_name(0, first_count, last_count, suffix_count)
        return s        

    #  Will re-spin the name if there is more than one hyphen
    def check_hyphenated_grammar(arr, i, first_count, last_count, suffix_count):
        ret = []
        #  Avoid using any more than one hyphen
        for name in arr:
            while "-" in name:
                name = random_name(i, first_count, last_count, suffix_count)
            ret.append(name)
        # Avoid using names that end in an apostrophe as teh first numae in a hyphenated name
        if ret[0][-1] == "'":
            ret[0] = ret[0][:-1]
        return ret
