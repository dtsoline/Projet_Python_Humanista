# Humanista

Humanista est une application Flask réalisée dans le cadre de la seconde année du Master 
"Technologies Numériques Appliquées à l'Histoire" de l'École Nationale des Chartes. 


Celle-ci vise à proposer des correspondances humanistes présentes dans l'ouvrage [_Life and letters of Erasmus_](https://archive.org/details/cu31924026502793/)
de James Anthony Froude paru en 1894.
Les lettres se trouvent dans le fichier XML-TEI corpus_humanistes.xml.
Plusieurs feuilles de transformation XSL sont appliquées au fichier XML afin de produire 
des index dynamiques pour les personnes et les lieux mentionnés ainsi que l'affichage
de chacune des lettres.

Une connexion internet est requise pour le bon fonctionnement de cette application.

## Installation 


  * Cloner le dépot Github : ```git clone https://github.com/dtsoline/Projet_Python_Humanista ```
  * Vérifier que la version de Python corresponde à Python 3.X : ```python --version```;
  * Lancement de l'environnement virtuel : 
    * Se placer dans le dossier App : ```cd App/```
    * Installer l'environnement virtuel : ```python3 -m venv [nom environnement virtuel]```
    * Activation de l'environnement virtuel : ```source [nom environnement virtuel]/bin/activate```
  * Installation des librairies et packages nécessaires au bon fonctionnement de l'application : ```pip install -r requirements.txt```



## Lancement de l'application

 * Lancement : ```python run.py```

 * Se rendre sur ```http://127.0.0.1:5000/```

 * Pour stopper l'exécution : ```^C```

 * Sortie de l'environnement virtuel : ```deactivate```
