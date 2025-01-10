import os
import cv2
from PIL import Image
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askdirectory

def process_image(image_path):
    print(f"Traitement de l'image : {image_path}")
    
    # Charger l'image
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if image is None:
        print(f"Impossible de charger l'image : {image_path}")
        return

    # Convertir en niveaux de gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Appliquer un seuil pour créer un masque binaire
    _, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

    # Trouver les contours des objets
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Créer un répertoire pour les sorties
    output_dir = os.path.splitext(image_path)[0]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Extraire et sauvegarder chaque objet détecté
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)

        # Ignorer les très petits contours
        if w < 50 or h < 50:
            continue

        # Extraire l'objet
        extracted = image[y:y+h, x:x+w]

        # Créer un masque pour la transparence
        mask = binary[y:y+h, x:x+w]

        # Ajouter un canal alpha à l'image
        b, g, r = cv2.split(extracted)
        rgba = cv2.merge((b, g, r, mask))

        # Sauvegarder l'objet extrait
        output_path = os.path.join(output_dir, f"object_{i+1}.png")
        cv2.imwrite(output_path, rgba)

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
        print("Les images extraites ont été sauvegardées avec des fonds transparents dans des sous-dossiers portant le nom des fichiers originaux.")
        print("Vérifiez le répertoire suivant :")
        print(directory_path)
    else:
        print("Aucun répertoire sélectionné. Fin du programme.")
