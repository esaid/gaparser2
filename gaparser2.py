import numpy as np
import pyutil
from pyutil import inany, do, fileappend, fileoverwrite, filereplace, toDict
import re
import sys

directoryExamples = '/examples'
directoryBibliotheqque = 'Libraries/'
comserial = "com9"  # le port serie
compilega144 = True  # permet de voir sous forme json le resultat de la compilation
programga144 = False  # programmation du ga144

file_ga = "examples/ledpulse.ga"
file_ga_ = file_ga + '_'


# lecture fichier
def read_file(File_input):
    with open(File_input, 'r') as f:
        return f.read()


def list_find_(string_found, s_extension):
    list_require = []
    for i in list_code:
        if inany(i, string_found, True):
            list_require.append(re.sub(string_found, '', i).strip() + s_extension)
    return list_require


def find_between(s, start, end):
    return ': ' + (s.split(start))[1].split(end)[0] + " ;"


def creation_dictionnaire(code_bibliotheque_, s_fin):
    dict_code_bibliotheque = {}
    while code_bibliotheque_:
        cle_code_ = find_between(code_bibliotheque_, ': ', ' ;')

        cle_code_bibliotheque, code_ = cle_code_.split("\n")[0].replace(': ', ''), cle_code_
        # print(f" cle: {cle_code_bibliotheque} , code  {code_}")
        if inany(cle_code_bibliotheque, s_fin, True):
            break
        cle_code_bibliotheque = cle_code_bibliotheque.split(' ')[0]
        dict_code_bibliotheque[cle_code_bibliotheque] = code_
        # print(f" dictionnaire code bibliotheque {dict_code_bibliotheque}")

        # clean code_bibliotheque
        code_bibliotheque_ = code_bibliotheque_.replace(code_, '')
        # print(f"code biblioheque {code_bibliotheque_}")

    return dict_code_bibliotheque


def dictionnaire_bibliotheque_total(list_bibliotheque_):
    dict_bibliotheque_ = {}
    for ll in list_bibliotheque_:
        code_bibliotheque__ = read_file(directoryBibliotheqque + ll)
        dict_bibliotheque_.update(creation_dictionnaire(code_bibliotheque__, ll.replace('.ga', '')))
        # print(f"code_bibliotheque {code_bibliotheque__}")
    return dict_bibliotheque_


# code source
code = read_file(file_ga)
print(f"code:  {code}")
# liste_code , separation des lignes , suppression espaces
list_code = list(filter(lambda x: x != '', list(map(str.strip, code.splitlines()))))
print(f"list_code:  {list_code}")

# list_bibliotheque fichiers
list_bibliotheque = list_find_('require', '.ga')
print(f"list_bibliotheque {list_bibliotheque}")

list_code_bibliotheque = []
code_bibliotheque = ""

dict_bibliotheque = dictionnaire_bibliotheque_total(list_bibliotheque)
print(f"dictionnaire_bibliotheque {dict_bibliotheque}")

'''
list_mot_code_bibliotheque = list(filter(lambda x: x != '', list(map(str.strip, code_bibliotheque.splitlines()))))
list_mot_code_bibliotheque = list(map(lambda each: each.strip(": "), list_mot_code_bibliotheque))
list_mot_code_bibliotheque = list(map(lambda each: each.strip("( n )"), list_mot_code_bibliotheque))

print(f"list_mot_code_bibliotheque : {list_mot_code_bibliotheque}")
'''
code_to_add = []
code_to_replace = []
for lc in list_code:
    print(lc)
    if lc in dict_bibliotheque:
        if lc not in code_to_add:
            code_to_add.extend([lc, dict_bibliotheque[lc]])

    for key, value in dict_bibliotheque.items():
        if inany(lc, key, True):
            if (key not in code_to_replace) and (key not in code_to_add) :
                code_to_replace.extend([key, value.replace(key, '')])



print(f"code a ajouter : {code_to_add}")
print(f"code a remplacer: {code_to_replace}")

sys.exit()

fileoverwrite(file_ga_, code)
for s_code_to_add in code_to_add:
    fileappend(file_ga_, s_code_to_add)

# for s_code_to_replace in code_remplace:
# filereplace(file_ga_ , s_code_to_add, s_code_to_replace )
