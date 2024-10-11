import os
import subprocess
from bibliotheque_create import read_file, generation_code

# -------------------------------------------------------------------
# repertoire / initialisation
directoryExamples = '/examples'
directoryBibliotheque = 'Libraries/'
comserial = "/dev/ttyUSB0"  # le port serie
compilega144 = True  # permet de voir sous forme json le resultat de la compilation
programga144 = False  # programmation du ga144

# -------------------------------------------------------------------

# fichiers code source
dir_source = "examples/"
file_source = "ledpulse.ga"
# file_source = "inputwakeup.ga"
# file_source = "fibonacci.ga"
file_ga = dir_source + file_source



file_ga_ = file_ga.replace('.ga', '_.ga')

# read code source
code = read_file(file_ga)
print(f"file source: {file_ga}\n")
print(f"code: \n{code}")


# new code
generation_code(code, directoryBibliotheque, file_ga_)
newcode = read_file(file_ga_)
print(f"file modifiee : {file_ga_}\n")
print(f"nouveau code: \n{newcode}")


# -------------------------------------------------------------------
def ecrire_fichier(result_ , file_):
    # Vérifier si la commande s'est exécutée avec succès
    if result_.returncode == 0:
        # Ouvrir le fichier en mode écriture
        with open(dir_source + file_ , "w") as file:
            file.write(result_.stdout)  # Écrire la sortie standard dans le fichier
    else:
        print("La commande a échoué avec le code de retour:", result_.returncode)
        print("Erreur:", result_.stderr)

# compilation / programmation
if compilega144:
    # "python ga.py examples/boutoninput_.ga --json"

    commandecompile = "python ga.py " + file_ga_

    # Exécuter la commande et capturer la sortie
    result = subprocess.run(commandecompile, shell=True, capture_output=True, text=True)
    ecrire_fichier(result, "assembleur_" + file_source  )
    # os.system(commandecompile)
if programga144:
    commandprogram = "python ga.py " + file_ga_ + " --port " + comserial
    result = subprocess.run(commandprogram, shell=True, capture_output=True, text=True)
    ecrire_fichier(result, "prg_" + file_source)

    # os.system(commandprogram)
# -------------------------------------------------------------------
