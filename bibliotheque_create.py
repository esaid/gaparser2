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


def creation_dictionnaire(code_bibliotheque_):
    dict_code_bibliotheque = {}
    code_bibli = []
    l1 = find_all_index_in_list(code_bibliotheque_, ": ")
    l2 = find_all_index_in_list(code_bibliotheque_, ";")

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

    for i in range(len(l1) - 1):
        code_bibli = (code_bibliotheque_[l1[i]:l2[i] + 1])
        cle_code_bibliotheque, code_ = code_bibli.split()[1], code_bibli
        # print(code_bibli)
        dict_code_bibliotheque[cle_code_bibliotheque] = code_bibli.replace(': ', '')
    return dict_code_bibliotheque


def dictionnaire_bibliotheque_total(list_bibliotheque_, directoryBibliotheque_):
    dict_bibliotheque_ = {}
    for ll in list_bibliotheque_:
        code_bibliotheque__ = read_file(directoryBibliotheque_ + ll)
        dict_bibliotheque_.update(creation_dictionnaire(code_bibliotheque__))
        # print(f"code_bibliotheque {code_bibliotheque__}")
    return dict_bibliotheque_
