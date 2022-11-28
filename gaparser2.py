import pyutil
from pyutil import inany

directoryExamples = '/examples'
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
        if inany(i, 'require', True):
            list_require.append(i)
    return list_require


code = read_file(file_ga)
print(code)
list_code = list(map(str.strip, code.splitlines()))
print(list_code)

print(list_find_('require'))
