import numpy as np
import pyutil
from bibliotheque_create import read_file, find_string_in_list, dictionnaire_bibliotheque_total
from pyutil import inany, fileappend, fileoverwrite, filereplace
import re
import sys
import os

directoryExamples = '/examples'
directoryBibliotheque = 'Libraries/'
comserial = "com9"  # le port serie
compilega144 = True  # permet de voir sous forme json le resultat de la compilation
programga144 = False  # programmation du ga144

file_ga = "examples/ledpulse.ga"
# file_ga = "examples/inputwakeup.ga"
file_ga_ = file_ga + '_'

# code source
code = read_file(file_ga)
print(f"code: \n{code}")
# liste_code , separation des lignes , suppression espaces
list_code = list(filter(lambda x: x != '', list(map(str.strip, code.splitlines()))))  # separation lignes
# list_code = list(filter(lambda x: x != '', list(map(str.strip, code.split()))))
# print(f"list_code:  {list_code}")
list_node = find_string_in_list(list_code, 'node', '')
print(f"liste node : {list_node}")

# liste fichier bibliotheque
list_bibliotheque = find_string_in_list(list_code, 'require', '.ga')
#print(f"list_bibliotheque : {list_bibliotheque}")
# dictionnaire
dict_bibliotheque = dictionnaire_bibliotheque_total(list_bibliotheque, directoryBibliotheque)
# print(f"dictionnaire_bibliotheque {dict_bibliotheque}")

def code_to_add_to_replace(list_code):
    code_to_add = []
    code_to_replace = []
    for lc in list_code:

        if lc in dict_bibliotheque:
            if lc not in code_to_add:
                code_to_add.extend([lc, ': ' + dict_bibliotheque[lc]])
                #print(lc)

        for key, value in dict_bibliotheque.items():
            if inany(lc, key):
                if (key not in code_to_replace) and (key not in code_to_add):
                    code_to_replace.extend([key, str(value.removeprefix(key)).replace(';', '')])
    # clean code_to_replace
    code_to_add = code_to_add[1::2]  # odd element
    return code_to_add, code_to_replace

code_to_add , code_to_replace = code_to_add_to_replace(list_code)

#print(f"code a ajouter : {code_to_add}")
#print(f"code a remplacer: {code_to_replace}")

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
newcode = read_file(file_ga_)
print(f" nouveau code: \n{newcode}")

if compilega144:
    # "python ga.py examples/boutoninput_.ga --json"

    commandecompile = "python ga.py " + file_ga_
    os.system(commandecompile)
if programga144:
    commandprogram = "python ga.py " + file_ga_ + " --port " + comserial
    os.system(commandprogram)
