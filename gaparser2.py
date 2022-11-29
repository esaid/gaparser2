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

        cle_code_bibliotheque , code_ = cle_code_.split("\n")[0].replace(': ',''), cle_code_
        print(f" cle: {cle_code_bibliotheque} , code  {code_}")
        dict_code_bibliotheque[cle_code_bibliotheque] = code_
        print(f" dictionnaire code bibliotheque {dict_code_bibliotheque}")

        # clean code_bibliotheque
        code_bibliotheque_ = code_bibliotheque_.replace(code_, '')
        print(f"code biblioheque {code_bibliotheque_}")
        if inany(cle_code_bibliotheque, s_fin):
            break
    return dict_code_bibliotheque


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

dict_bibliotheque ={}

for ll in list_bibliotheque:
    code_bibliotheque = read_file(directoryBibliotheqque + ll)
    dict_bibliotheque.update(creation_dictionnaire(code_bibliotheque, ll.replace('.ga','')))
    print(f"code_bibliotheque {code_bibliotheque}")



    # print(f"code_bibliotheque {ll}  {code_bibliotheque}")
    #list_code_bibliotheque.append(re.split(r":", code_bibliotheque))
#list_code_bibliotheque = list(filter(lambda x: x != '', list(map(str.strip, code_bibliotheque.splitlines()))))



#list_code_bibliotheque = sum(list_code_bibliotheque, [])  # remove list [[][]]
# print(f"code_bibliotheque : {code_bibliotheque}")

#dict_bibliotheque ={}
#dict_bibliotheque = creation_dictionnaire(code_bibliotheque, list_bibliotheque[0])
print(dict_bibliotheque)
sys.exit()
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
        m = " " + m
        for ind in list_code_bibliotheque:
            if inany(ind, m, True):
                code.append(ind)
                break
    return code


find_index(code_remplace)
print(f"code a remplacer {code_remplace}")

print(type(code_to_replace))
print(type(code_remplace))

dict_a_remplacer = toDict(list(code_to_replace), code_remplace)
for cle, valeur in dict_a_remplacer.items():
    print("l'élément de clé", cle, "vaut", valeur)

fileoverwrite(file_ga_, code)
for s_code_to_add in code_to_add:
    fileappend(file_ga_, s_code_to_add)

# for s_code_to_replace in code_remplace:
# filereplace(file_ga_ , s_code_to_add, s_code_to_replace )
