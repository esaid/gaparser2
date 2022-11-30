import numpy as np
import pyutil
from pyutil import inany, do, fileappend, fileoverwrite, filereplace, toDict
import re
import sys
import os

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


# list bibliotheque
def list_find_(string_found, s_extension):
    list_require = []
    for i in list_code:
        if inany(i, string_found, True):
            list_require.append(re.sub(string_found, '', i).strip() + s_extension)
    return list_require


# decoupage definition et code
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
        dict_code_bibliotheque[cle_code_bibliotheque] = code_.replace(': ', '')
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


dict_bibliotheque = dictionnaire_bibliotheque_total(list_bibliotheque)
print(f"dictionnaire_bibliotheque {dict_bibliotheque}")

code_to_add = []
code_to_replace = []
for lc in list_code:
    print(lc)
    if lc in dict_bibliotheque:
        if lc not in code_to_add:
            code_to_add.extend([lc, ': ' + dict_bibliotheque[lc]])
    for key, value in dict_bibliotheque.items():
        if inany(lc, key):
            if (key not in code_to_replace) and (key not in code_to_add):
                code_to_replace.extend([key, str(value.replace(key, '')).replace(';', '')])

code_to_add = code_to_add[1::2]  # odd element

# clean code_to_replace


print(f"code a ajouter : {code_to_add}")
print(f"code a remplacer: {code_to_replace}")

# init code
fileoverwrite(file_ga_, code)
# clean require
filereplace(file_ga_, 'require', '\ require')

# ajout code complet a la fin
for s_code_to_add in code_to_add:
    fileappend(file_ga_, s_code_to_add + '\n')

# remplace la definition du code par sa definition
for i in range(len(code_to_replace) - 1, -1, -2):
    s_code_to_found = code_to_replace[i - 1]
    s_code_to_replace = code_to_replace[i]
    filereplace(file_ga_, ' ' + s_code_to_found, s_code_to_replace)

# code source
code = read_file(file_ga_)
print(code)

if compilega144:
    # "python ga.py examples/boutoninput_.ga --json"

    commandecompile = "python ga.py " + file_ga_
    os.system(commandecompile)
    if programga144:
        commandprogram = "python ga.py " + file_ga_ + " --port " + comserial
        os.system(commandprogram)
