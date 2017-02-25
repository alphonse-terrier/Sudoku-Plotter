#!/usr/bin/env python

import numpy as np
from tkinter import *
from tkinter.messagebox import *


class Display(Tk):
    """
    Hérite de la classe Tk() qui permet l'affichage d'une fenêtre sous tkinter
    Permet d'exploiter une interface graphique pour afficher et éditer une
    grille de sudoku de manière plus interactive avec l'utilisateur.
    """

    def __init__(self, boss):
        Tk.__init__(self)

        self.boss = boss
        self.taille = self.boss.taille
        self.nb_cases = self.boss.nb_cases
        self.color = 'black'
        self.liste_position = []
        self.title("Sudoku")
        self.edition = False
        self.rectangle = None
        self.x, self.y = 0, 0
        self.sudoku = np.zeros((self.nb_cases, self.nb_cases), int)
        self.affichage_sudoku = [[0 for i in range(self.nb_cases)] for i in range(self.nb_cases)]

        # Creation des variables tkinter et widgets
        self.Can = Canvas(width=455, height=455)
        self.BarreMenu = self.BarreMenu(self)

        # Placement des widgets
        self.Can.grid(padx=10, pady=10)
        self.configure(menu=self.BarreMenu)

        self.createMatrix()
        self.bind_all('<Key>', self.tryToEdit)

        self.update()
        self.setInTheMiddle()

        if not self.boss.beta_version:
            # Affiche les erreurs survenues au démarrage
            for error in self.boss.getError():
                self.showError(error)

    def choixMethode(self, methode):
        self.boss.setMethodeResolution(methode)

    def choixVitesse(self, vitesse):
        self.boss.setVitesse(vitesse)

    def startResolution(self):
        self.startManualEdition(False)
        self.boss.setError("sudoku_insoluble", False)
        self.boss.startResolution(self.sudoku)

    def beforeUsingCamera(self):
        if "module_camera" in self.boss.getError():
            self.showError("module_camera")
        elif "disponibilite_camera" in self.boss.getError():
            self.showError("disponibilite_camera")
        else:
            self.boss.Camera.takePhoto()

    def beforeUsingOpenCv(self):
        if "module_cv2" in self.boss.getError():
            self.showError("module_cv2")

    def startManualEdition(self, edition=None):
        if edition is not None:
            self.edition = edition
        else:
            self.edition = not self.edition
        if self.edition:
            self.Can.itemconfigure(self.rectangle, width=5)
            self.x, self.y = 0, 0
        else:
            self.Can.itemconfigure(self.rectangle, width=0)
        self.update()

    def createMatrix(self):
        """
        Permet d'afficher une grille de sudoku vide ainsi que le curseur qui est à l'origine masqué
        :return: None
        """
        self.Can.delete(ALL)
        for i in range(self.nb_cases + 1):
            column = self.Can.create_line(50 * i + 5, 5, 50 * i + 5, 455, width=2)
            line = self.Can.create_line(3, 50 * i + 5, 457, 50 * i + 5, width=2)
            if i % self.taille[0] == 0:
                self.Can.itemconfigure(column, width=5)
            if i % self.taille[1] == 0:
                self.Can.itemconfigure(line, width=5)
            if i != self.nb_cases:
                for j in range(self.nb_cases):
                    self.affichage_sudoku[i][j] = self.Can.create_text(50 * j + 30, 50 * i + 30,
                                                                       font=('Times', 24, 'bold'), text="")
        self.rectangle = self.Can.create_rectangle(5 + 50 * self.x, 5 + 50 * self.y, 55 + 50 * self.x,
                                                   55 + 50 * self.y, outline='red', width=0)

    def tryToEdit(self, evt):
        key = evt.keysym

        if key == 'F5':
            self.startResolution()

        if key == "x" or key == "X":
            self.effacerSudoku()

        if key == "b" or key == "B":
            self.color = "black"
            print("black")

        if key == "r" or key == "R":
            self.color = "red"
            print("red")

        if key == "v" or key == "V":
            try:
                sleep = float(input("sleep = "))
                self.boss.setSpeed(sleep)
            except ValueError:
                print("a doit etre un nombre")

        if key == 'Return':
            self.startManualEdition()

        if key == "BackSpace":
            for x in range(self.nb_cases):
                for y in range(self.nb_cases):
                    if (x, y) in self.liste_position:
                        self.sudoku[x][y] = 0
            self.updateSudoku(self.sudoku, self.liste_position)

        if key == 'c' or key == 'C':
            self.boss.stopResolution()

        if self.edition:
            if key == 'Right':
                self.y += 1
                if self.y == self.nb_cases:
                    self.y = 0

            if key == 'Left':
                self.y -= 1
                if self.y == -1:
                    self.y = self.nb_cases - 1

            if key == 'Down':
                self.x += 1
                if self.x == self.nb_cases:
                    self.x = 0

            if key == 'Up':
                self.x -= 1
                if self.x == -1:
                    self.x = self.nb_cases - 1

            try:
                if 0 < int(key) < self.nb_cases + 1:
                    self.Can.itemconfigure(self.affichage_sudoku[self.x][self.y], text=key, fill=self.color)
                if int(key) == 0:
                    self.Can.itemconfigure(self.affichage_sudoku[self.x][self.y], text="")
                self.sudoku[self.x, self.y] = int(key)
            except ValueError:
                pass

            self.Can.coords(self.rectangle, 5 + 50 * self.y, 5 + 50 * self.x, 55 + 50 * self.y, 55 + 50 * self.x)

    def updateSudoku(self, sudoku, liste_position=[]):
        self.liste_position = liste_position
        self.startManualEdition(False)
        if "sudoku_insoluble" in self.boss.getError():
            self.showError("sudoku_insoluble")
        else:
            for x in range(self.nb_cases):
                for y in range(self.nb_cases):
                    if (x, y) in self.liste_position:
                        self.Can.itemconfigure(self.affichage_sudoku[x][y], text=sudoku[x][y], fill='red')
                    else:
                        self.Can.itemconfigure(self.affichage_sudoku[x][y], text=sudoku[x][y], fill='black')
                    if sudoku[x][y] == 0:
                        self.Can.itemconfigure(self.affichage_sudoku[x][y], text="", fill='black')
            self.sudoku = np.copy(sudoku)

    def effacerSudoku(self):
        for x in range(self.nb_cases):
            for y in range(self.nb_cases):
                self.Can.itemconfigure(self.affichage_sudoku[x][y], text="", fill='black')
        self.sudoku = np.zeros((self.nb_cases, self.nb_cases), int)

    def showError(self, error):
        if error == "module_camera":
            showerror("Caméra", "Désolé, le module picamera n'a pas été installé correctement !")
        elif error == "disponibilite_camera":
            showerror("Caméra", "Désolé, la caméra n'est pas disponible !")
        elif error == "module_cv2":
            showerror("OpenCV", "Désolé, le module cv2 n'a pas été installé correctement !")
        elif error == "camera_error":
            showerror("Caméra", "Une erreur inattendue avec la camera est survenue !\n"
                                "Veuillez réessayer ou redémarrer votre raspberry pi")
        elif error == "sudoku_insoluble":
            showwarning("Sudoku", "Le sudoku n'est pas résoluble")
        else:
            showerror("Erreur", "Une erreur inattendue est survenue !")

    def showAide(self):
        showinfo("Aide", "Le menu 'Aide' n'est pas encore disponible !")

    def showAPropos(self):
        showinfo("Aide", "Le menu 'A Propos' n'est pas encore disponible !")

    def setInTheMiddle(self):
        geo = []
        s = ''
        for i in self.geometry():
            if i.isdigit():
                s += i
            else:
                geo.append(s)
                s = ''
        geo.append(s)
        new_geo = geo[0] + "x" + geo[1] + "+" + str(int(0.5 * (self.winfo_screenwidth() - int(geo[0])))) \
                  + "+" + str(int(0.5 * (self.winfo_screenheight() - int(geo[1]))))
        self.geometry(new_geo)

    class BarreMenu(Menu):
        """
        Hérite de la classe Menu() qui permet à l'utilisateur de définir
        ses préférences et les opérations qui doivent être efféctuées
        """

        def __init__(self, boss):
            Menu.__init__(self)
            self.boss = boss
            self.mode_resolution = IntVar()
            self.vitesse = IntVar()

            # Sélection par défaut des items
            self.mode_resolution.set(3)
            self.vitesse.set(0)

            # Création des menus
            self.menu_edition = Menu(self, tearoff=0)
            self.menu_resolution = Menu(self, tearoff=0)
            self.menu_methode = Menu(self, tearoff=0)
            self.menu_aide = Menu(self, tearoff=0)

            # Ajout des menus
            self.add_cascade(label="Edition", menu=self.menu_edition)
            self.add_cascade(label="Résolution", menu=self.menu_resolution)
            self.add_cascade(label="Méthode", menu=self.menu_methode)
            self.add_cascade(label="Aide", menu=self.menu_aide)

            # Ajout des items du menu 'Edition'
            self.menu_edition.add_command(label="Caméra", command=self.boss.beforeUsingCamera)
            self.menu_edition.add_command(label="Automatique", command=self.boss.beforeUsingOpenCv)
            self.menu_edition.add_command(label="Manuelle", command=self.boss.startManualEdition)
            self.menu_edition.add_command(label="Effacer", command=self.boss.effacerSudoku)

            # Ajout des items du menu 'Résolution'
            self.menu_resolution.add_radiobutton(label="Directe", value=0, variable=self.vitesse,
                                                 command=lambda: self.boss.choixVitesse("Directe"))
            self.menu_resolution.add_radiobutton(label="Pas à pas", value=1, variable=self.vitesse,
                                                 command=lambda: self.boss.choixVitesse("Pas à pas"))

            self.menu_resolution.add_separator()
            self.menu_resolution.add_command(label="Lancer", command=self.boss.startResolution)

            # Ajout des items du menu "Méthode"
            self.menu_methode.add_radiobutton(label="Globale", value=0, variable=self.mode_resolution,
                                              command=lambda: self.boss.choixMethode("Globale"))
            self.menu_methode.add_radiobutton(label="Inclusion", value=1, variable=self.mode_resolution,
                                              command=lambda: self.boss.choixMethode("Inclusion"))
            self.menu_methode.add_radiobutton(label="Exclusion", value=2, variable=self.mode_resolution,
                                              command=lambda: self.boss.choixMethode("Exclusion"))
            self.menu_methode.add_radiobutton(label="Backtracking", value=3, variable=self.mode_resolution,
                                              command=lambda: self.boss.choixMethode("Backtracking"))

            # Ajout des items du menu "Aide
            self.menu_aide.add_command(label="Fonctionnement", command=self.boss.showAide)
            self.menu_aide.add_command(label="A Propos", command=self.boss.showAPropos)
