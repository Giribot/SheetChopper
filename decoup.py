import os
import cv2
import numpy as np
from tkinter import Tk, filedialog

def select_directory():
    """Ouvre une boîte de dialogue pour sélectionner un répertoire."""
    Tk().withdraw()
    folder = filedialog.askdirectory(title="Sélectionnez un répertoire contenant des images")
    return folder

def add_alpha_channel(image):
    """Ajoute un canal alpha à une image s'il n'existe pas."""
    if image.shape[2] == 3:  # Si l'image n'a pas de canal alpha
        b, g, r = cv2.split(image)
        alpha = np.ones(b.shape, dtype=b.dtype) * 255  # Canal alpha opaque
        image = cv2.merge((b, g, r, alpha))
    return image

def detect_background_color(image):
    """Détecte la couleur dominante sur les bords de l'image pour identifier le fond."""
    h, w, _ = image.shape

    # Extraire les pixels des bords (haut, bas, gauche, droite)
    border_pixels = np.concatenate([
        image[0, :, :],    # Haut
        image[-1, :, :],   # Bas
        image[:, 0, :],    # Gauche
        image[:, -1, :]    # Droite
    ], axis=0)

    # Calculer la couleur dominante comme moyenne des pixels des bords
    dominant_color = np.mean(border_pixels, axis=0).astype(int)
    return dominant_color

def save_background_color(color, output_dir, base_name):
    """Crée un PNG 50x50 de la couleur du fond détectée."""
    # Ne prendre que les trois premières valeurs (R, G, B)
    color_rgb = color[:3] if len(color) == 4 else color
    color_image = np.full((50, 50, 3), color_rgb, dtype=np.uint8)
    background_filename = os.path.join(output_dir, f"Background-{base_name}.png")
    cv2.imwrite(background_filename, color_image)
    print(f"Fichier de couleur de fond sauvegardé : {background_filename}")

def remove_background(image, dominant_color, tolerance=50):
    """Supprime le fond d'une image en fonction de la couleur dominante détectée."""
    # Conversion en HSV pour une gestion précise des variations de couleur
    hsv = cv2.cvtColor(image[:, :, :3], cv2.COLOR_BGR2HSV)

    # Vérifier si le fond est proche du blanc
    if np.all(dominant_color > 200):  # Si le fond est très clair
        lower_bound = np.array([0, 0, 255 - tolerance])
        upper_bound = np.array([180, tolerance, 255])
    else:
        # Conversion de la couleur dominante en HSV
        dominant_color_hsv = cv2.cvtColor(np.uint8([[dominant_color]]), cv2.COLOR_BGR2HSV)[0][0]

        # Créer les limites de tolérance autour de la couleur dominante
        lower_bound = np.array([max(0, dominant_color_hsv[0] - 10), 30, 30])
        upper_bound = np.array([min(180, dominant_color_hsv[0] + 10), 255, 255])

    # Création du masque pour isoler le fond
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # Appliquer des opérations morphologiques pour nettoyer le masque
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # Fermer les petits trous
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)   # Supprimer le bruit
    mask_inv = cv2.bitwise_not(mask)

    # Application du masque pour rendre le fond transparent
    b, g, r = cv2.split(image[:, :, :3])
    rgba = cv2.merge((b, g, r, mask_inv))
    return rgba, mask

def detect_objects(image, min_object_area=2000):
    """Détecte les contours des objets dans une image avec transparence."""
    alpha_channel = image[:, :, 3]
    _, thresh = cv2.threshold(alpha_channel, 1, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def filter_contours(contours, min_object_area=2000):
    """Filtre les contours trop petits pour éviter les artefacts."""
    return [c for c in contours if cv2.contourArea(c) >= min_object_area]

def extract_and_save_objects(image, contours, output_dir):
    """Extrait chaque objet détecté et le sauvegarde en fichiers PNG avec transparence."""
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        cropped_object = image[y:y+h, x:x+w]

        # Sauvegarde l'objet
        object_filename = os.path.join(output_dir, f"object_{i + 1}.png")
        cv2.imwrite(object_filename, cropped_object)
        print(f"Objet sauvegardé : {object_filename}")

def process_image(filepath, output_dir, min_object_area=2000):
    """Traite une image pour extraire les objets détectés."""
    image = cv2.imread(filepath, cv2.IMREAD_UNCHANGED)

    if image is None:
        print(f"Erreur : Impossible de charger l'image {filepath}")
        return

    # Ajouter le canal alpha si nécessaire
    image = add_alpha_channel(image)

    # Détecter la couleur dominante sur les bords
    dominant_color = detect_background_color(image)
    print(f"Couleur dominante détectée : {dominant_color}")

    # Créer le répertoire pour les objets extraits
    base_name = os.path.splitext(os.path.basename(filepath))[0]
    output_subdir = os.path.join(output_dir, base_name)
    os.makedirs(output_subdir, exist_ok=True)

    # Sauvegarder la couleur de fond en PNG dans le répertoire des objets extraits
    save_background_color(dominant_color, output_subdir, base_name)

    # Supprimer le fond
    transparent_image, mask = remove_background(image, dominant_color)

    # Détecter les contours
    contours = detect_objects(transparent_image)

    # Filtrer les contours
    filtered_contours = filter_contours(contours, min_object_area=min_object_area)

    # Sauvegarder les objets extraits
    extract_and_save_objects(transparent_image, filtered_contours, output_subdir)

def main():
    input_directory = select_directory()
    if not input_directory:
        print("Aucun répertoire sélectionné.")
        return

    # Paramètre : taille minimale des objets
    min_object_area = 2000  # Taille minimale par défaut

    print(f"Taille minimale des objets : {min_object_area}")
    output_directory = os.path.join(input_directory, "extracted_objects")
    os.makedirs(output_directory, exist_ok=True)

    for filename in os.listdir(input_directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            filepath = os.path.join(input_directory, filename)
            process_image(filepath, output_directory, min_object_area=min_object_area)

    print("Traitement terminé. Les objets extraits sont disponibles dans 'extracted_objects'.")

if __name__ == "__main__":
    main()
