# trainTesseract

Ce dépot Git contient les fichiers nécessaire à l'entrainement de Tesseract-OCR en utilisant la technique d'entrainement LSTM Training. L'objectif de ce script est de pouvoir entrainer tesseract avec un custom dataset.


## Prérequis
- Tesseract-OCR
- la librairie scikit-learn pour python

## Setup
  1. Install depot

Installer le depot git dans un environnement pyCharm ou en local
  ```bash
   git clone https://github.com/matyji/trainTesseract.git
   ```
  2. Créer votre jeu de données
 
 Modifier le dossier data/ en y ajoutant votre jeu d'images sous format .tiff
 
 ## Script

Pour executer le script il faut passer en argument supplémentaire la fonction que vous voulez executer. Voici les arguments existant :

  #### 1) PréTraitement
  
          python main.py postTraitement
              
   Cette fonction permettra de générer les matrices de textes correspondant a vos images sous format .box
   Si votre jeu de données contient déja les .box n'executer pas cette commande.
   
   Attention !!! Vérifiez vos fichiers .box que le texte correspondent bien à celui de l'image. Pour que l'entrainement puisse être le plus efficace possible. 

  #### 2) Création du fichier traineddata

         python main.py generation
         
   Cette fonction génère les fichiers lstmf correspondant a vos .tiff et les .box créé précedemment.


         python main.py lister
         
   Cette fonction génère un fichier txt contenant tous les fichiers lstmf générés.


          python main.py separationData
          
   Cette fonction va spliter en deux le jeux de données. 80% pour les données d'entrainements et 20% pour les données de tests.

          python main.py extraction
          
   Cette fonction va extraire le fichier lstm du traineddata francais de la librairie Tesseract.

          python main.py create
          
   Cette fonction va créer les checkpoints de notre modèle a partir du fichier lstm créé précédemment 

          python main.py combine
          
   Cette fonction va combiner les checkpoints entre eux afin de générer un seul traineddata

          python main.py deplacer
              
   Cette fonction va déplacer le fichier traineddata généré dans la librairie Tesseract
              
  #### 3) Evaluation
              
          python main.py evalFra
          
   Cette fonction va evaluer le modèle francais de base
              
          python main.py evalModel
          
   Cette fonction va évaluer le modèle que l'on a créé
              
              
              
      
      
