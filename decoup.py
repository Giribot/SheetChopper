import os
import cv2
import numpy as np
from tkinter import Tk, filedialog

def select_directory():
    Tk().withdraw()
    folder = filedialog.askdirectory(title="Sélectionnez un répertoire contenant des images")
    return folder

def add_alpha_channel(image):
    if image.shape[2] == 3:
        b, g, r = cv2.split(image)
        alpha = np.ones(b.shape, dtype=b.dtype) * 255
        image = cv2.merge((b, g, r, alpha))
    return image

def detect_background_color(image):
    h, w, c = image.shape
    has_alpha = c == 4

    if has_alpha:
        border_pixels = np.concatenate([
            image[0, :, :],
            image[-1, :, :],
            image[:, 0, :],
            image[:, -1, :]
        ], axis=0)

        visible_pixels = border_pixels[border_pixels[:, 3] > 50]
        if len(visible_pixels) == 0:
            print("Tous les bords sont transparents, pas de couleur de fond à supprimer.")
            return None

        rgb_pixels = visible_pixels[:, :3]
    else:
        border_pixels = np.concatenate([
            image[0, :, :],
            image[-1, :, :],
            image[:, 0, :],
            image[:, -1, :]
        ], axis=0)
        rgb_pixels = border_pixels[:, :3]

    dominant_color = np.mean(rgb_pixels, axis=0).astype(int)
    return dominant_color

def save_background_color(color, output_dir, base_name):
    if color is None:
        return
    color_rgb = color[:3] if len(color) == 4 else color
    color_image = np.full((50, 50, 3), color_rgb, dtype=np.uint8)
    background_filename = os.path.join(output_dir, f"Background-{base_name}.png")
    cv2.imwrite(background_filename, color_image)
    print(f"Fichier de couleur de fond sauvegardé : {background_filename}")

def remove_background(image, dominant_color, tolerance=50):
    hsv = cv2.cvtColor(image[:, :, :3], cv2.COLOR_BGR2HSV)

    if np.all(dominant_color > 200):
        lower_bound = np.array([0, 0, 255 - tolerance])
        upper_bound = np.array([180, tolerance, 255])
    else:
        # Corriger conversion RGB -> BGR -> HSV
        dominant_color_bgr = np.array([[dominant_color]], dtype=np.uint8)
        dominant_color_hsv = cv2.cvtColor(dominant_color_bgr, cv2.COLOR_BGR2HSV)[0][0]
        lower_bound = np.array([max(0, dominant_color_hsv[0] - 10), 30, 30])
        upper_bound = np.array([min(180, dominant_color_hsv[0] + 10), 255, 255])

    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask_inv = cv2.bitwise_not(mask)

    b, g, r = cv2.split(image[:, :, :3])
    alpha = image[:, :, 3] if image.shape[2] == 4 else np.ones_like(b, dtype=np.uint8) * 255
    sum_rgb = cv2.add(cv2.add(b, g), r)
    new_alpha = np.where(mask == 255, 0, alpha)
    rgba = cv2.merge((b, g, r, new_alpha))

    debug_mask_path = os.path.join(os.getcwd(), "debug_mask.png")
    cv2.imwrite(debug_mask_path, mask)
    print(f"Masque de fond sauvegardé pour debug : {debug_mask_path}")

    return rgba, mask

def detect_objects(image, min_object_area=2000):
    alpha_channel = image[:, :, 3]
    _, thresh = cv2.threshold(alpha_channel, 1, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def filter_contours(contours, min_object_area=2000):
    return [c for c in contours if cv2.contourArea(c) >= min_object_area]

def extract_and_save_objects(image, contours, output_dir):
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        cropped_object = image[y:y+h, x:x+w]
        object_filename = os.path.join(output_dir, f"object_{i + 1}.png")
        cv2.imwrite(object_filename, cropped_object)
        print(f"Objet sauvegardé : {object_filename}")

def process_image(filepath, output_dir, min_object_area=2000):
    image = cv2.imread(filepath, cv2.IMREAD_UNCHANGED)

    if image is None:
        print(f"Erreur : Impossible de charger l'image {filepath}")
        return

    if len(image.shape) < 3:
        print(f"Image non supportée (niveaux de gris) : {filepath}")
        return

    image = add_alpha_channel(image)

    dominant_color = detect_background_color(image)
    base_name = os.path.splitext(os.path.basename(filepath))[0]
    output_subdir = os.path.join(output_dir, base_name)
    os.makedirs(output_subdir, exist_ok=True)

    if dominant_color is not None:
        print(f"Couleur dominante détectée : {dominant_color}")
        save_background_color(dominant_color, output_subdir, base_name)
        transparent_image, mask = remove_background(image, dominant_color)
    else:
        print("Image avec fond transparent déjà prête. Aucun traitement de fond.")
        transparent_image = image

    contours = detect_objects(transparent_image)
    filtered_contours = filter_contours(contours, min_object_area=min_object_area)
    print(f"{len(filtered_contours)} objets détectés dans {filepath}")

    extract_and_save_objects(transparent_image, filtered_contours, output_subdir)

def main():
    input_directory = select_directory()
    if not input_directory:
        print("Aucun répertoire sélectionné.")
        return

    min_object_area = 2000
    print(f"Taille minimale des objets : {min_object_area}")
    output_directory = os.path.join(input_directory, "extracted_objects")
    os.makedirs(output_directory, exist_ok=True)

    for filename in os.listdir(input_directory):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
            filepath = os.path.join(input_directory, filename)
            process_image(filepath, output_directory, min_object_area=min_object_area)

    print("\nTraitement terminé. Les objets extraits sont disponibles dans 'extracted_objects'.")

if __name__ == "__main__":
    main()
