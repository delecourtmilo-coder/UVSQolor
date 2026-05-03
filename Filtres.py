import numpy as np
from PIL import Image, ImageFilter


def limiter_pixels(matrice):
    """Garde les valeurs des pixels entre 0 et 255."""
    matrice = np.clip(matrice, 0, 255)
    matrice = matrice.astype("uint8")
    return matrice


def filtre_negatif(matrice_image):
    """Inverse les couleurs de l'image."""
    resultat = 255 - matrice_image
    return limiter_pixels(resultat)


def filtre_luminosite(matrice_image):
    """Augmente la luminosité de l'image."""
    resultat = matrice_image.astype(float) + 10
    return limiter_pixels(resultat)


def filtre_contraste(matrice_image):
    """Augmente le contraste autour du gris moyen 0.5."""
    matrice = matrice_image.astype(float) / 255

    pivot = 0.5
    facteur = 1.75

    resultat = pivot + facteur * (matrice - pivot)
    resultat = resultat * 255

    return limiter_pixels(resultat)


def filtre_sepia(matrice_image):
    """Applique un filtre sépia."""
    matrice = matrice_image.astype(float)

    rouge = matrice[:, :, 0]
    vert = matrice[:, :, 1]
    bleu = matrice[:, :, 2]

    nouveau_rouge = 0.393 * rouge + 0.769 * vert + 0.189 * bleu
    nouveau_vert = 0.349 * rouge + 0.686 * vert + 0.168 * bleu
    nouveau_bleu = 0.272 * rouge + 0.534 * vert + 0.131 * bleu

    resultat = np.zeros(matrice.shape)
    resultat[:, :, 0] = nouveau_rouge
    resultat[:, :, 1] = nouveau_vert
    resultat[:, :, 2] = nouveau_bleu

    return limiter_pixels(resultat)


def filtre_flou(matrice_image):
    """Applique un flou moyen 3x3."""
    matrice = matrice_image.astype(float)

    matrice_bord = np.pad(matrice, ((1, 1), (1, 1), (0, 0)), mode="edge")
    resultat = np.zeros(matrice.shape)

    for ligne in range(3):
        for colonne in range(3):
            morceau = matrice_bord[
                ligne:ligne + matrice.shape[0],
                colonne:colonne + matrice.shape[1],
                :
            ]
            resultat = resultat + morceau / 9

    return limiter_pixels(resultat)


def filtre_nettete(matrice_image):
    """Renforce la netteté de l'image."""
    image_originale = matrice_image.astype(float)
    image_floue = filtre_flou(matrice_image).astype(float)

    details = image_originale - image_floue
    resultat = image_originale + details

    return limiter_pixels(resultat)


def filtre_fusion(matrice1, matrice2):
    """Fusionne deux images avec une proportion moitié-moitié."""
    image1 = matrice1.astype(float)
    image2 = matrice2.astype(float)

    resultat = 0.5 * image1 + 0.5 * image2

    return limiter_pixels(resultat)


def filtre_flou_gaussien(matrice_image, rayon):
    """Applique un flou gaussien avec un rayon choisi."""
    image_pil = Image.fromarray(matrice_image.astype("uint8"))
    image_pil = image_pil.filter(ImageFilter.GaussianBlur(radius=rayon))

    resultat = np.array(image_pil)

    return resultat


def filtre_nettete_gaussienne(matrice_image, rayon):
    """Renforce la netteté en utilisant un flou gaussien."""
    image_originale = matrice_image.astype(float)

    image_floue = filtre_flou_gaussien(matrice_image, rayon).astype(float)

    details = image_originale - image_floue
    resultat = image_originale + details

    return limiter_pixels(resultat)
