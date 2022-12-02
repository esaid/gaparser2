# lecture fichier
import re

from pyutil import inany


def read_file(File_input):
    with open(File_input, 'r') as f:
        return f.read()


# list bibliotheque
def find_string_in_list(list_, string_found, s_extension):
    # cherche index de string_found dans list_, et retourne la liste des fichiers ( sans string_found )  + s_extension
    # exemple require delay ( index 0 ) require gpio ( index 1 ) , retourne [delay.ga, gpio.ga]
    return list(
        map(lambda s_: (list_[s_].replace(string_found, '').strip() + s_extension),
            [i_ for i_, value_ in enumerate(list_) if inany(value_, string_found, True)]))


def find_all_index_in_list(s, string_found):
    return [index for index in range(len(s)) if s.startswith(string_found, index)]


'''
# decoupage definition et code
def find_between(s, start, end):
    u = s.find(start)
    k = s.find(end.strip()) + 1
    y = f"{s[u:k]}"
    l = ': ' + (s.split(start))[1].split(end)[0] + " ;"
    o = y == l
    return y
    # return ': ' + (s.split(start))[1].split(end)[0] + " ;"
'''


def creation_dictionnaire(code_bibliotheque_):
    dict_code_bibliotheque = {}
    code_bibli = []
    l1 = find_all_index_in_list(code_bibliotheque_, ": ")
    l2 = find_all_index_in_list(code_bibliotheque_, ";")
    print(l1)
    print(l2)
    m = min(len(l1), len(l2))
    print(m)
    i = 0
    while i < (min(len(l1), len(l2)) - 1):
        # print(l1[i],l1[i+1])
        # print(l2[i], l2[i+1])
        while l1[i + 1] < l2[i]:
            l1.pop(i + 1)
            # print(l1)
        while l2[i + 1] < l1[i + 1]:
            l2.pop(i)
            # print(l2)
        i += 1
        print(f"i = {i}")
        print(f"l1 = {l1}")
        print(f"l2 = {l2}")
    for i in range(len(l1) - 1):
        code_bibli = (code_bibliotheque_[l1[i]:l2[i] + 1])
        cle_code_bibliotheque, code_ = code_bibli.split("\n")[0].replace(': ', ''), code_bibli
        print(code_bibli)
        dict_code_bibliotheque[cle_code_bibliotheque] = code_bibli.replace(': ', '')
    return dict_code_bibliotheque


'''


        cle_code_ = find_between(code_bibliotheque_, ': ', ' ;')

        cle_code_bibliotheque, code_ = cle_code_.split("\n")[0].replace(': ', ''), cle_code_
        # print(f" cle: {cle_code_bibliotheque} , code  {code_}")
        if inany(cle_code_bibliotheque, s_fin, True):
            break
        cle_code_bibliotheque = cle_code_bibliotheque.split(' ')[0]
        dict_code_bibliotheque[cle_code_bibliotheque] = code_.replace(': ', '')
        # print(f" dictionnaire code bibliotheque {dict_code_bibliotheque}")

        # clean code_bibliotheque
        code_bibliotheque_ = code_bibliotheque_.replace(code_, '')
        # print(f"code biblioheque {code_bibliotheque_}")

        return dict_code_bibliotheque
'''


def dictionnaire_bibliotheque_total(list_bibliotheque_, directoryBibliotheque_):
    dict_bibliotheque_ = {}
    for ll in list_bibliotheque_:
        code_bibliotheque__ = read_file(directoryBibliotheque_ + ll)
        dict_bibliotheque_.update(creation_dictionnaire(code_bibliotheque__))
        print(f"code_bibliotheque {code_bibliotheque__}")
    return dict_bibliotheque_
