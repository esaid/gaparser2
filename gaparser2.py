import pyutil

directoryExamples = '/examples'
comserial = "com9"  # le port serie
compilega144 = True  # permet de voir sous forme json le resultat de la compilation
programga144 = False  # programmation du ga144

file_ga = "examples/ledpulse.ga"


# lecture fichier
def read_file(File_input):
    with open(File_input, 'r') as f:
        return f.read()


code = read_file(file_ga)
print(code)
l = list(map(str.strip, code.splitlines()))
print(l)




