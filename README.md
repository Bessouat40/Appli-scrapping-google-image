# Appli-scrapping-google-image
Application web permettant de scrapper des images de google images afin de se créer des bases de données.
Le code prend en entrée un ou des liens google image (ex : https://www.google.com/search?q=chat&rlz=1C1GCEA_enFR861FR861&source=lnms&tbm=isch&sa=X&ved=2ahUKEwialLT_3772AhV2jIkEHepkBhsQ_AUoAXoECAIQAw&biw=1366&bih=649&dpr=1).
Il prend aussi un chemin d'accès vers le dossier dans lequel enregistrer toutes les images. 
Le code crée un dossier dans lequel il enregistre toutes les images scrapées.

# Description de l'application :
Application web codée en python. 
Scrappeur codé à l'aide de la librairie python selenium.
Application web codée avec la librairie Dash de python.
Il est possible de renseigner plusieurs liens google image pour scrapper plus d'images en même temps. Il n'y a pas de doublons dans les images enregistrées.

# Nombre de scrolls :
Ce paramètre correspond au nombre de fois où l'algorithme descend la barre de recherche. Cela permet de charger plus d'images et donc d'en enregistrer plus.
Renseigner plusieurs liens google image avec des recherches similaire (ex : recherche de chat, de chat roux, de chat jeune, de chat adulte, ...) permet d'obtenir plus de résultats et donc plus d'images.
Sinon, le nombre de photos obtenues est assez faible.
Avec environ 3 liens renseignés, et un nombre de scroll égal à 30, on arrive à récupérer environ 700 images.

# Visuel de l'application :
![screenshot1](https://github.com/Bessouat40/Appli-scrapping-google-image/blob/main/capture_scrap.png?raw=true)
