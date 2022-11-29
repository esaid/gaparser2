import numpy as np
import pyutil
from pyutil import inany, do
import re

directoryExamples = '/examples'
directoryBibliotheqque = 'Libraries/'
comserial = "com9"  # le port serie
compilega144 = True  # permet de voir sous forme json le resultat de la compilation
programga144 = False  # programmation du ga144

file_ga = "examples/ledpulse.ga"


# lecture fichier
def read_file(File_input):
    with open(File_input, 'r') as f:
        return f.read()


def list_find_(string_found):
    list_require = []
    for i in list_code:
        if inany(i, string_found, True):
            list_require.append(re.sub(string_found, '', i).strip() + '.ga')
    return list_require


code = read_file(file_ga)
print(f"code:  {code}")
list_code = list(filter(lambda x: x != '', list(map(str.strip, code.splitlines()))))

print(f"list_code:  {list_code}")
list_bibliotheque = list_find_('require')
print(f"list_bibliotheque {list_bibliotheque}")
list_code_bibliotheque = []
code_bibliotheque = ""
for ll in list_bibliotheque:
    code_bibliotheque += read_file(directoryBibliotheqque + ll)
    # print(f"code_bibliotheque {ll}  {code_bibliotheque}")
    list_code_bibliotheque.append(re.split(r":", code_bibliotheque))
list_code_bibliotheque = sum(list_code_bibliotheque, [])  # remove list [[][]]
print(f"list_code_bibliotheque : {list_code_bibliotheque}")
list_mot_code_bibliotheque = list(filter(lambda x: x != '', list(map(str.strip, code_bibliotheque.splitlines()))))
list_mot_code_bibliotheque = list(map(lambda each: each.strip(": "), list_mot_code_bibliotheque))
list_mot_code_bibliotheque = list(map(lambda each: each.strip("( n )"), list_mot_code_bibliotheque))

print(f"list_mot_code_bibliotheque : {list_mot_code_bibliotheque}")

code_to_add = []
code_to_replace = []
for lc in list_code:
    print(lc)
    for lcb in list_code_bibliotheque:
        if inany(lcb, lc, True):
            print(lc, lcb)
            code_to_add.append(": " + lcb)
            break
    for lmcb in list_mot_code_bibliotheque:
        if inany(lc, lmcb, True):
            print(lmcb, lc)
            code_to_replace.append(lmcb)
code_to_add = set(code_to_add)
code_to_replace = set(code_to_replace)
print(f"code a ajouter : {code_to_add}")
print(f"code a remplacer: {code_to_replace}")

code_remplace = []
def find_index(code):
    for m in code_to_replace:
        m = " " + m + ' '
        for ind in list_code_bibliotheque:
            if inany(ind, m, True):
                code.append(ind)
                break
    return code


find_index(code_remplace)
print(f"code a remplacer {code_remplace}")
