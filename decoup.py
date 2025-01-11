import os
import cv2
from rembg import remove
from PIL import Image
from tkinter import Tk
from tkinter.filedialog import askdirectory

def process_image(image_path):
    print(f"Traitement de l'image : {image_path}")

    # Charger l'image
    with open(image_path, "rb") as input_file:
        input_image = input_file.read()

    # Supprimer le fond avec rembg
    output_image = remove(input_file)

    # Sauvegarder l'image avec fond transparent temporaire
    temp_output_path = "temp_transparent.png"
    with open(temp_output_path, "wb") as temp_file:
        temp_file.write(output_image)

    # Charger l'image transparente avec OpenCV
    transparent_image = cv2.imread(temp_output_path, cv2.IMREAD_UNCHANGED)

    # Vérifier si le canal alpha existe
    if transparent_image.shape[2] < 4:
        print("Erreur : L'image ne contient pas de canal alpha.")
        os.remove(temp_output_path)
        return

    # Utiliser le canal alpha pour créer un masque binaire
    alpha_channel = transparent_image[:, :, 3]
    _, binary = cv2.threshold(alpha_channel, 1, 255, cv2.THRESH_BINARY)

    # S'assurer que le masque est bien en format CV_8UC1
    binary = binary.astype('uint8')

    # Appliquer une ouverture morphologique pour affiner les bords
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    refined_binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

    # Appliquer une érosion supplémentaire pour réduire les artefacts
    refined_binary = cv2.erode(refined_binary, kernel, iterations=1)

    # Trouver les contours des objets
    contours, _ = cv2.findContours(refined_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Créer un répertoire pour les sorties
    output_dir = os.path.splitext(image_path)[0]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Extraire et sauvegarder chaque objet détecté
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)

        # Ignorer les très petits objets
        if w < 50 or h < 50:
            continue

        # Extraire l'objet
        cropped_object = transparent_image[y:y+h, x:x+w]

        # Sauvegarder l'objet extrait
        object_output_path = os.path.join(output_dir, f"object_{i+1}.png")
        cv2.imwrite(object_output_path, cropped_object)

    # Supprimer le fichier temporaire
    os.remove(temp_output_path)

    print(f"Traitement terminé pour {image_path}. Objets sauvegardés dans : {output_dir}")

def process_directory(directory_path):
    print(f"Démarrage du traitement pour le répertoire : {directory_path}")
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(directory_path, filename)
            process_image(image_path)

if __name__ == "__main__":
    Tk().withdraw()  # Masquer la fenêtre Tkinter
    directory_path = askdirectory(title="Choisissez un répertoire contenant les planches d'images")

    if directory_path:
        process_directory(directory_path)
        print("\nTraitement terminé !")
        print("Les objets extraits ont été sauvegardés dans des sous-dossiers portant le nom des fichiers originaux.")
        print("Vérifiez le répertoire suivant :")
        print(directory_path)
    else:
        print("Aucun répertoire sélectionné. Fin du programme.")
import os
import cv2
from rembg import remove
from PIL import Image
from tkinter import Tk
from tkinter.filedialog import askdirectory

def process_image(image_path):
    print(f"Traitement de l'image : {image_path}")

    # Charger l'image
    with open(image_path, "rb") as input_file:
        input_image = input_file.read()

    # Supprimer le fond avec rembg
    output_image = remove(input_image)

    # Sauvegarder l'image avec fond transparent temporaire
    temp_output_path = "temp_transparent.png"
    with open(temp_output_path, "wb") as temp_file:
        temp_file.write(output_image)

    # Charger l'image transparente avec OpenCV
    transparent_image = cv2.imread(temp_output_path, cv2.IMREAD_UNCHANGED)

    # Vérifier si le canal alpha existe
    if transparent_image.shape[2] < 4:
        print("Erreur : L'image ne contient pas de canal alpha.")
        os.remove(temp_output_path)
        return

    # Utiliser le canal alpha pour créer un masque binaire
    alpha_channel = transparent_image[:, :, 3]  # Utiliser le canal alpha
    _, binary = cv2.threshold(alpha_channel, 1, 255, cv2.THRESH_BINARY)

    # S'assurer que le masque est bien en format CV_8UC1
    binary = binary.astype('uint8')

    # Appliquer un flou pour adoucir les bords et réduire les résidus
    blurred = cv2.GaussianBlur(binary, (5, 5), 0)

    # Réaffiner les bords avec un seuil
    _, refined_binary = cv2.threshold(blurred, 1, 255, cv2.THRESH_BINARY)

    # Trouver les contours des objets
    contours, _ = cv2.findContours(refined_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Créer un répertoire pour les sorties
    output_dir = os.path.splitext(image_path)[0]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Extraire et sauvegarder chaque objet détecté
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)

        # Ignorer les très petits objets
        if w < 50 or h < 50:
            continue

        # Extraire l'objet
        cropped_object = transparent_image[y:y+h, x:x+w]

        # Sauvegarder l'objet extrait
        object_output_path = os.path.join(output_dir, f"object_{i+1}.png")
        cv2.imwrite(object_output_path, cropped_object)

    # Supprimer le fichier temporaire
    os.remove(temp_output_path)

    print(f"Traitement terminé pour {image_path}. Objets sauvegardés dans : {output_dir}")

def process_directory(directory_path):
    print(f"Démarrage du traitement pour le répertoire : {directory_path}")
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(directory_path, filename)
            process_image(image_path)

if __name__ == "__main__":
    Tk().withdraw()  # Masquer la fenêtre Tkinter
    directory_path = askdirectory(title="Choisissez un répertoire contenant les planches d'images")

    if directory_path:
        process_directory(directory_path)
        print("\nTraitement terminé !")
        print("Les objets extraits ont été sauvegardés dans des sous-dossiers portant le nom des fichiers originaux.")
        print("Vérifiez le répertoire suivant :")
        print(directory_path)
    else:
        print("Aucun répertoire sélectionné. Fin du programme.")
