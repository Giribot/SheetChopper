import os
import cv2
from PIL import Image
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askdirectory

def detect_background_color(image):
    # Convertir en RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Extraire les coins de l'image pour analyser la couleur du fond
    corners = [
        image_rgb[0, 0],  # Coin supérieur gauche
        image_rgb[0, -1],  # Coin supérieur droit
        image_rgb[-1, 0],  # Coin inférieur gauche
        image_rgb[-1, -1]  # Coin inférieur droit
    ]

    # Calculer la couleur moyenne des coins
    background_color = np.mean(corners, axis=0).astype(int)
    return background_color

def process_image(image_path):
    print(f"Traitement de l'image : {image_path}")
    
    # Charger l'image
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if image is None:
        print(f"Impossible de charger l'image : {image_path}")
        return

    # Détecter la couleur du fond
    background_color = detect_background_color(image)
    lower_bound = np.array(background_color - 20, dtype=np.uint8)  # Plage minimale
    upper_bound = np.array(background_color + 20, dtype=np.uint8)  # Plage maximale

    # Convertir en RGB pour la manipulation
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Créer un masque pour les zones de fond
    mask = cv2.inRange(image_rgb, lower_bound, upper_bound)

    # Supprimer les petites zones de fond à l'intérieur de l'objet
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask_cleaned = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Inverser le masque pour garder l'objet
    mask_inv = cv2.bitwise_not(mask_cleaned)

    # Ajouter un canal alpha à l'image
    b, g, r = cv2.split(image_rgb)
    rgba = cv2.merge((b, g, r, mask_inv))

    # Créer un répertoire pour les sorties
    output_dir = os.path.splitext(image_path)[0]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Sauvegarder l'image avec fond transparent
    output_path = os.path.join(output_dir, f"{os.path.basename(image_path).split('.')[0]}_transparent.png")
    cv2.imwrite(output_path, rgba)

    print(f"Traitement terminé pour {image_path}. Image sauvegardée dans : {output_path}")

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
