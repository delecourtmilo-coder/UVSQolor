# Import de toutes les choses nécessaires

import numpy as np
import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk

from filtres import (
    filtre_negatif,
    filtre_luminosite,
    filtre_contraste,
    filtre_sepia,
    filtre_flou,
    filtre_nettete,
    filtre_fusion,
    filtre_flou_gaussien,
    filtre_nettete_gaussienne
)


# Initialisation des variables globales

image = None
photo = None
matrice_image = None

historique = []
indice_historique = -1

menu_edition = None


# Afficher l'image

def afficher_image():
    global photo, image, canvas

    if image is None:
        return

    photo = ImageTk.PhotoImage(image)

    canvas.config(width=image.width, height=image.height)
    canvas.delete("all")
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)


# Gestion de l'historique

def mettre_a_jour_menu_historique():
    """Active ou désactive Annuler / Rétablir selon la position dans l'historique."""
    global menu_edition, historique, indice_historique

    if menu_edition is not None:
        if indice_historique > 0:
            menu_edition.entryconfig("Annuler", state="normal")
        else:
            menu_edition.entryconfig("Annuler", state="disabled")

        if indice_historique < len(historique) - 1:
            menu_edition.entryconfig("Rétablir", state="normal")
        else:
            menu_edition.entryconfig("Rétablir", state="disabled")


def initialiser_historique():
    """Remet l'historique à zéro quand on ouvre une nouvelle image."""
    global historique, indice_historique, matrice_image

    historique = []
    historique.append(matrice_image.copy())
    indice_historique = 0

    mettre_a_jour_menu_historique()


def appliquer_nouvelle_image(nouvelle_matrice):
    """
    Applique une nouvelle matrice comme image actuelle,
    l'ajoute à l'historique,
    puis affiche l'image.
    """
    global image, matrice_image, historique, indice_historique

    if indice_historique < len(historique) - 1:
        historique = historique[:indice_historique + 1]

    historique.append(nouvelle_matrice.copy())
    indice_historique = indice_historique + 1

    matrice_image = nouvelle_matrice.copy()
    image = Image.fromarray(matrice_image.astype("uint8"))

    afficher_image()
    mettre_a_jour_menu_historique()


def annuler():
    """Revient à l'image précédente dans l'historique."""
    global image, matrice_image, historique, indice_historique

    if indice_historique > 0:
        indice_historique = indice_historique - 1

        matrice_image = historique[indice_historique].copy()
        image = Image.fromarray(matrice_image.astype("uint8"))

        afficher_image()
        mettre_a_jour_menu_historique()


def retablir():
    """Revient à l'image suivante après une annulation."""
    global image, matrice_image, historique, indice_historique

    if indice_historique < len(historique) - 1:
        indice_historique = indice_historique + 1

        matrice_image = historique[indice_historique].copy()
        image = Image.fromarray(matrice_image.astype("uint8"))

        afficher_image()
        mettre_a_jour_menu_historique()


# Ouvrir une image

def ouvrir_image():
    global image, matrice_image

    nom_fichier = filedialog.askopenfilename(
        title="Choisis ton image",
        filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")]
    )

    if nom_fichier != "":
        image = Image.open(nom_fichier).convert("RGB")
        matrice_image = np.array(image)

        afficher_image()
        initialiser_historique()

        print("Image ouverte :", nom_fichier)
        print("Taille de l'image :", image.size)
        print("Forme de la matrice :", matrice_image.shape)


# Fonctions appelées par le menu

def negatif():
    global matrice_image

    if matrice_image is not None:
        nouvelle_matrice = filtre_negatif(matrice_image)
        appliquer_nouvelle_image(nouvelle_matrice)


def luminosite():
    global matrice_image

    if matrice_image is not None:
        nouvelle_matrice = filtre_luminosite(matrice_image)
        appliquer_nouvelle_image(nouvelle_matrice)


def contraste():
    global matrice_image

    if matrice_image is not None:
        nouvelle_matrice = filtre_contraste(matrice_image)
        appliquer_nouvelle_image(nouvelle_matrice)


def sepia():
    global matrice_image

    if matrice_image is not None:
        nouvelle_matrice = filtre_sepia(matrice_image)
        appliquer_nouvelle_image(nouvelle_matrice)


def flou():
    global matrice_image

    if matrice_image is not None:
        nouvelle_matrice = filtre_flou(matrice_image)
        appliquer_nouvelle_image(nouvelle_matrice)


def nettete():
    global matrice_image

    if matrice_image is not None:
        nouvelle_matrice = filtre_nettete(matrice_image)
        appliquer_nouvelle_image(nouvelle_matrice)


def fusion():
    global matrice_image

    if matrice_image is not None:
        nom_fichier = filedialog.askopenfilename(
            title="Choisis la deuxième image",
            filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")]
        )

        if nom_fichier != "":
            deuxieme_image = Image.open(nom_fichier).convert("RGB")
            deuxieme_matrice = np.array(deuxieme_image)

            if deuxieme_matrice.shape == matrice_image.shape:
                nouvelle_matrice = filtre_fusion(matrice_image, deuxieme_matrice)
                appliquer_nouvelle_image(nouvelle_matrice)
            else:
                print("Erreur : les deux images doivent avoir la même taille.")


def flou_gaussien():
    global matrice_image

    if matrice_image is not None:
        rayon = simpledialog.askfloat(
            "Flou gaussien",
            "Choisis le rayon du flou :\n1 = léger\n3 = moyen\n6 = fort",
            minvalue=0.1,
            maxvalue=20
        )

        if rayon is not None:
            nouvelle_matrice = filtre_flou_gaussien(matrice_image, rayon)
            appliquer_nouvelle_image(nouvelle_matrice)


def nettete_gaussienne():
    global matrice_image

    if matrice_image is not None:
        rayon = simpledialog.askfloat(
            "Netteté gaussienne",
            "Choisis le rayon du flou gaussien :\n1 = léger\n3 = moyen\n6 = fort",
            minvalue=0.1,
            maxvalue=20
        )

        if rayon is not None:
            nouvelle_matrice = filtre_nettete_gaussienne(matrice_image, rayon)
            appliquer_nouvelle_image(nouvelle_matrice)


# Création de la fenêtre

fenetre = tk.Tk()
fenetre.title("UVSQolor")
fenetre.geometry("800x600")

canvas = tk.Canvas(fenetre, bg="white")
canvas.grid(row=1, column=0)


# Menu principal

menu = tk.Menu(fenetre)
fenetre.config(menu=menu)


# Menu Fichier

menu_fichier = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Fichier", menu=menu_fichier)

menu_fichier.add_command(label="Ouvrir", command=ouvrir_image)


# Menu Édition

menu_edition = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Édition", menu=menu_edition)

menu_edition.add_command(label="Annuler", command=annuler, state="disabled")
menu_edition.add_command(label="Rétablir", command=retablir, state="disabled")


# Menu Effets

menu_effets = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Effets", menu=menu_effets)

menu_effets.add_command(label="Négatif", command=negatif)
menu_effets.add_command(label="Luminosité", command=luminosite)
menu_effets.add_command(label="Contraste", command=contraste)
menu_effets.add_command(label="Sepia", command=sepia)
menu_effets.add_command(label="Flou", command=flou)
menu_effets.add_command(label="Netteté", command=nettete)
menu_effets.add_command(label="Fusion", command=fusion)
menu_effets.add_command(label="Flou gaussien", command=flou_gaussien)
menu_effets.add_command(label="Netteté gaussienne", command=nettete_gaussienne)


# Mainloop

fenetre.mainloop()
