import os
import sys

from sklearn.model_selection import train_test_split

chemin_trainingData = "./trainingData"
chemin_testData = "./testData"
chemin_dataSet = "./data"
chemin_traineddatas = "./traineddata/"
paramPSM = "6"
paramOEM = "3"


def postTraitement():
    """
    fonction permettant de créer des fichiers .box et .lstmf pour chaque image .tiff contenu dans le Dataset
    :return: rien
    """
    for eachfile in os.listdir(chemin_dataSet):
        if eachfile.endswith(".tiff"):
            fichier = chemin_dataSet + "/" + eachfile
            # tesseract command
            os.system(f"tesseract {fichier} {fichier[:-5]} --psm 6 lstmbox")
            os.system(f"tesseract {fichier} {fichier[:-5]} --psm 6 lstm.train")


fichiersEntree = chemin_dataSet + "/*.lstmf"
listeFichiers = chemin_dataSet + "/all-lstmf.txt"
all_train_data = chemin_trainingData + "/liste_train.txt"
all_test_data = chemin_testData + "/liste_test.txt"


def listerFichiers():
    """
    :return: répertorie tous les fichiers .lstmf dans le fichier all-lstmf.txt
    """
    os.system(f"ls -1 {fichiersEntree} | sort -R > {listeFichiers}")


def separationData():
    os.system(f"mkdir trainingData")
    os.system(f"mkdir testData")
    """
    :return: sépare les fichiers .lstmf en 80% de train_data contenu dans le fichier liste_train.txt et 20% de test_data
    contenu dans le fichier liste_test.txt
    """
    with open(listeFichiers, "r") as f:
        # Lire toutes les lignes du fichier et les stocker dans une liste
        data = f.readlines()
    # Diviser les données en un ensemble d'entraînement et un ensemble de test
    train_data, test_data = train_test_split(data, test_size=0.2)

    # Afficher le nombre de lignes dans chaque ensemble
    print("Nombre de lignes dans l'ensemble d'entraînement :", len(train_data))
    # Écrire les données d'entraînement dans un fichier texte
    with open(all_train_data, 'w') as f:
        for line in train_data:
            f.write(line)

    print("Nombre de lignes dans l'ensemble de test :", len(test_data))
    # Écrire les données de test dans un fichier texte
    with open(all_test_data, 'w') as f:
        for line in test_data:
            f.write(line)


# a changer si l'on veut sur entrainer le modèle que l'on à créer
traineddata = "fra.traineddata"
location_traineddata = "/usr/share/tesseract-ocr/4.00/tessdata/" + traineddata
fraLSTM = chemin_trainingData + "/fra.lstm"


def extractionTraineddata():
    """
    :return: créer un fichier fra.lstm en faisant l'extraction du fichier fra.traineddata
    """
    os.system(f"combine_tessdata -e {location_traineddata} {fraLSTM}")


modele = "./model/tesseractThales"
log = chemin_trainingData + "/basetrain.log"


def evalModelFRA():
    """
    :return: l'évaluation du modèle actuel
    """
    os.system(f"lstmeval --model {fraLSTM} \
      --traineddata {location_traineddata} \
      --eval_listfile {all_test_data} ")


def creationModel():
    """
    supprime les checkpoints si il y en a dans le dossier model/
    :return: créer les checkpoints de notre nouveau modèle en affichant le taux d'erreur
    """
    os.system(f"mkdir model")
    os.system("rm -rf ./model/*")
    os.system(f"OMP_THREAD_LIMIT=8 lstmtraining \
      --continue_from {fraLSTM} \
      --model_output {modele} \
      --traineddata {location_traineddata} \
      --train_listfile {listeFichiers} \
      --max_iterations 10000 ")


modele_checkpoint = "./model/tesseractThales_checkpoint"
modele_output = "./traineddatas/tesseractThales.traineddata"


def combineCheckpoints():
    """
    :return: combine les checkpoints entre eux afin de générer un .traineddata dans le dossier traineddatas
    """
    os.system(f"mkdir traineddatas")
    os.system(f"lstmtraining --stop_training\
      --continue_from {modele_checkpoint} \
      --traineddata {location_traineddata} \
      --model_output {modele_output}")


def deplacerTraineddata():
    chemin_libTraineddata = "/usr/share/tesseract-ocr/4.00/tessdata/"
    """

    :return: l'évaluation de notre nouveau modèle
    """
    os.system(f"cp {modele_output} {chemin_libTraineddata}")


def evalModel():
    """

    :return: l'évaluation de notre nouveau modèle
    """
    os.system(f"lstmeval --model {modele_checkpoint} \
      --traineddata {location_traineddata} \
      --eval_listfile {all_test_data} ")


def test():
    """

    :return: créer un fichier ouput contenant la prédiction de notre modèle sur une image
    """
    nom_modele = "tesseractThales"
    image_test = chemin_dataSet + "/Template24_107.tiff"
    output_text = "./output_text"
    os.system(f"tesseract -l {nom_modele} {image_test} {output_text} --psm {paramPSM} --oem {paramOEM}")


for arg in sys.argv:
    if arg == "postTraitement":
        postTraitement()
    elif arg == "lister":
        listerFichiers()
    elif arg == "separationData":
        separationData()
    elif arg == "extraction":
        extractionTraineddata()
    elif arg == "evalFra":
        evalModelFRA()
    elif arg == "create":
        creationModel()
    elif arg == "combine":
        combineCheckpoints()
    elif arg == "deplacer":
        deplacerTraineddata()
    elif arg == "evalModel":
        evalModel()
    elif arg == "test":
        test()
