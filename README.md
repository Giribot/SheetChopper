French/English
-----
# SheetChopper
Un script python basique qui détoure automatiquement un image: genre une planche avec des objets dessus de tailles différentes puis découpe la planche image par image,
Un outil sympa qui peut être complémentaire à mon autre script pour faire des corpus zippé pour l'application de création de Bandes dessinées "BDNF" ici: https://github.com/Giribot/Createur-de-Corpus-zip-pour-BDNF

Exemple:
![00082-1771719671](https://github.com/user-attachments/assets/8d47ec10-7a68-4b97-b9a0-48b710e3d7b3)

le résultat sera:

![object_8](https://github.com/user-attachments/assets/3c4dee16-fe5f-4d4e-9688-36c78c4ff45b)
puis...
![object_7](https://github.com/user-attachments/assets/28560715-cbc1-410f-8c4d-58643379f2f3)
puis...
![object_6](https://github.com/user-attachments/assets/a33c3359-147b-47cf-9ca0-e4715f586006)
puis...
![object_5](https://github.com/user-attachments/assets/c60020b6-ae22-4ff7-8a14-734540a0655c)
puis...
![object_4](https://github.com/user-attachments/assets/f9f06382-0189-4d8e-916f-026224fa1e4e)
puis...
![object_3](https://github.com/user-attachments/assets/59d8507d-751c-461d-be5c-feb417955a92)
puis...
![object_2](https://github.com/user-attachments/assets/babbe988-fed1-48d6-b134-4f0aebef537a)
puis...
![object_1](https://github.com/user-attachments/assets/7db863f7-05fb-4bfd-a463-92ab4907c9f7)
puis...
![object_9](https://github.com/user-attachments/assets/7da9fe90-c1d5-4834-bf91-41db7e8b9b4c)

Mode d'emploi:

Il faut avoir python installé.
Mettre les deux fichiers dans un répertoire quelconque.
RunMeFirst.bat
decoup.py

Sur Windows: lancez le programme 'RunMeFirst.bat'
Ce fichier batch installera au besoin les librairies manquantes de python (si besoin) puis lancera le script python decoup.py

Ailleurs: Linux, Mac,
Si le fichier batch "RunMeFirst.bat" ne se lance pas:
Ouvrez le avec un blocnote et installez manuellement les librairies manquantes qui sont notées dedans:
(au 10/01/2025: il suffit de faire juste
pip install opencv-python pillow numpy 
Mais vérifiez si je n'ai pas rajouté par la suite des choses dedans)
Puis de lancer le script python
decoup.py.

Le script vous demandera le dossier où vous avez mis vos images que vous avez sélectionnées à détourer/découper.
Choississez le puis valider.
le processus est automatique et dans le répertoire que vous avez choisi, le script créera des noms de dossiers correspondant au nom de l'image de type planche (avec des élements distincts que le script détourera et découpera de manière procédurale)....

Voilà !

-----

# SheetChopper
A basic python script that automatically cuts out an image: like a board with objects on it of different sizes then cuts the board image by image,
A nice tool that can be complementary to my other script to make zipped corpus for BDNF (an app) for comics here: https://github.com/Giribot/Createur-de-Corpus-zip-pour-BDNF

Example:
![00082-1771719671](https://github.com/user-attachments/assets/8d47ec10-7a68-4b97-b9a0-48b710e3d7b3)

the result will be:

![object_8](https://github.com/user-attachments/assets/3c4dee16-fe5f-4d4e-9688-36c78c4ff45b)
Then...
![object_7](https://github.com/user-attachments/assets/28560715-cbc1-410f-8c4d-58643379f2f3)
Then...
![object_6](https://github.com/user-attachments/assets/a33c3359-147b-47cf-9ca0-e4715f586006)
Then...
![object_5](https://github.com/user-attachments/assets/c60020b6-ae22-4ff7-8a14-734540a0655c)
Then...
![object_4](https://github.com/user-attachments/assets/f9f06382-0189-4d8e-916f-026224fa1e4e)
Then...
![object_3](https://github.com/user-attachments/assets/59d8507d-751c-461d-be5c-feb417955a92)
Then...
![object_2](https://github.com/user-attachments/assets/babbe988-fed1-48d6-b134-4f0aebef537a)
Then...
![object_1](https://github.com/user-attachments/assets/7db863f7-05fb-4bfd-a463-92ab4907c9f7)
Then...
![object_9](https://github.com/user-attachments/assets/7da9fe90-c1d5-4834-bf91-41db7e8b9b4c)

Instructions:

You must have python installed.
Put the two files in any directory.
RunMeFirst.bat
decoup.py

On Windows: launch the program 'RunMeFirst.bat'
This batch file will install the missing python libraries (if necessary) and then launch the python script decoup.py

Elsewhere: Linux, Mac,
If the batch file "RunMeFirst.bat" does not launch:
Open it with a notepad and manually install the missing libraries that are noted in it:
(as of 01/10/2025: just do
pip install opencv-python pillow numpy
But check if I have not added things in it later)
Then launch the python script
decoup.py.

The script will ask you for the folder where you put your images that you selected to crop/cut out.
Choose it and validate.
the process is automatic and in the directory you have chosen, the script will create folder names corresponding to the name of the board type image (with distinct elements that the script will procedurally cut out and trim)....

There you go!
