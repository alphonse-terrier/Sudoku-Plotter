#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from tkinter.filedialog import *
import save


class Display(Tk):
    """
    Hérite de la classe Tk() qui permet l'affichage d'une fenêtre sous tkinter
    Permet d'exploiter une interface graphique pour afficher et éditer une
    grille de sudoku de manière plus interactive avec l'utilisateur.
    """

    def __init__(self, boss):
        Tk.__init__(self)

        self.boss = boss
        self.color = 'black'
        self.title("Sudoku")
        self.resizable(width=False, height=False)
        self.edition = False
        self.rectangle = None
        self.x, self.y = 0, 0
        self.liste_position = []
        self.taille = self.boss.taille
        self.nb_cases = self.boss.nb_cases
        self.sudoku = np.zeros((self.nb_cases, self.nb_cases), int)
        self.affichage_sudoku = [[0 for i in range(self.nb_cases)] for i in range(self.nb_cases)]

        os.chdir("../pictures/tkinter/")
        self.raspberry = PhotoImage(file="raspi_icone.png").subsample(2)
        os.chdir("../../script/")

        # Creation des variables tkinter et widgets
        self.Can = Canvas(width=455, height=455)
        self.raspi = self.Can.create_image(227, 227, image=self.raspberry)
        self.BarreMenu = self.BarreMenu(self)

        # Placement des widgets
        self.Can.grid(padx=10, pady=10)

        self.configure(menu=self.BarreMenu)

        self.createMatrix()
        self.bindAll()

        self.update()
        self.setInTheMiddle()

        if not self.boss.beta_version:
            # Affiche les erreurs survenues au démarrage
            for error in self.boss.getError():
                self.showError(error)

        self.protocol("WM_DELETE_WINDOW", self.boss.closeAll)

    def bindAll(self):
        self.bind_all('<Control-e>', self.boss.sendSudoku)
        self.bind_all('<Control-E>', self.boss.sendSudoku)
        self.bind_all('<Control-h>', self.showAide)
        self.bind_all('<Control-H>', self.showAide)
        self.bind_all('<Control-o>', self.openSudoku)
        self.bind_all('<Control-O>', self.openSudoku)
        self.bind_all('<Control-s>', self.saveSudoku)
        self.bind_all('<Control-S>', self.saveSudoku)
        self.bind_all('<Key>', self.tryToEdit)

    def choixMethode(self, methode):
        self.boss.setMethodeResolution(methode)

    def choixMode(self, mode):
        self.boss.setMode(mode)

    def choixVitesse(self, vitesse):
        self.boss.setVitesse(vitesse)

    def startResolution(self):
        self.startManualEdition(False)
        # self.boss.setError("sudoku_insoluble", False)
        self.boss.startResolution(self.sudoku)

    def backUp(self):
        save.saveSudoku(self.sudoku)
        self.showInfo("sudoku_save")

    def openSudoku(self, evt=None):
        self.showRaspi(False)
        filepath = None
        filepath = askopenfilename(title="Ouvrir une grille", initialdir="/Sudoku-Plotter/sudoku",
                                   filetypes=[('Text files', '.txt')])
        if filepath:
            self.sudoku = save.readSudoku(filepath)
        self.boss.setSudoku(self.sudoku)
        self.updateSudoku()

    def saveSudoku(self, evt=None):
        filepath = asksaveasfilename(title="Enregistrer une grille", initialdir="/Sudoku-Plotter/sudoku",
                                     initialfile="Sudoku", filetypes=[('Text files', '.txt')])
        save.saveSudoku(self.sudoku, filepath)

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

    def showRaspi(self, show=True):
        if show:
            self.raspi = self.Can.create_image(227, 227, image=self.raspberry)
            self.Can.tag_lower(self.raspi)
        else:
            self.Can.delete(self.raspi)

    def createMatrix(self):
        """
        Permet d'afficher une grille de sudoku vide ainsi que le curseur qui est à l'origine masqué
        :return: None
        """
        for i in range(self.nb_cases + 1):
            column = self.Can.create_line(50 * i + 4, 5, 50 * i + 4, 455, width=2)
            line = self.Can.create_line(2, 50 * i + 4, 457, 50 * i + 4, width=2)
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

    def eraseResolution(self):
        for x in range(self.nb_cases):
            for y in range(self.nb_cases):
                if (x, y) in self.liste_position:
                    self.sudoku[x][y] = 0
        self.updateSudoku(self.sudoku, self.liste_position)

    def tryToEdit(self, evt):
        key = evt.keysym

        self.showRaspi(False)
        if key == 'F5':
            self.startResolution()

        elif key.lower() == "b":
            self.color = "black"
            print("black")

        elif key == 'space':
            self.boss.stopResolution()

        elif key.lower() == "o":
            self.sudoku = save.readSudoku()
            self.updateSudoku(self.sudoku)

        elif key.lower() == "r":
            self.color = "red"
            print("red")

        elif key.lower() == "s":
            self.backUp()

        elif key.lower() == "x":
            self.effacerSudoku()

        elif key == 'Return':
            self.startManualEdition()

        elif key == "BackSpace":
            self.eraseResolution()

        elif self.edition:
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

        else:
            self.showRaspi()

    def updateSudoku(self, sudoku=None, liste_position=[]):
        if sudoku is None:
            sudoku = self.boss.sudoku
        self.liste_position = liste_position
        self.startManualEdition(False)
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
        self.startManualEdition(False)
        self.showRaspi()

    def showError(self, error):
        if error == "sudoku_insoluble":
            showerror("Sudoku", "Le sudoku n'est pas résoluble !")
        elif error == "raspi_connection":
            showerror("Connexion impossible", "Assurez-vous d'être connécté à la Rapsberry Pi !")
        else:
            showerror("Erreur", "Une erreur inattendue est survenue !")

    def showInfo(self, info):
        if info == "sudoku_received":
            showinfo("Sudoku", "La grille a été transmis à la Raspberry Pi avec succès !")
        elif info == "sudoku_save":
            showinfo("Sudoku", "La grille a été enregistrée avec succès !")
        elif info == "photo_taken":
            showinfo("Raspberry", "La Raspberry a pris une photo avec succès ! !")
        elif info == "raspi_shutdown":
            showinfo("Raspberry", "La Raspberry a été arrétée avec succès !")
        elif info == "raspi_reboot":
            showinfo("Raspberry", "La Raspberry a été redémarrée avec succès !")
        elif info == "raspi_stop":
            showinfo("Raspberry", "L'écriture de la grille a été arrétée avec succès !")

    def showAide(self, evt=None):
        self.HelpMenu()

    def showAPropos(self):
        self.AboutMenu()

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

    class HelpMenu(Toplevel):
        def __init__(self):
            Toplevel.__init__(self)
            self.title("Aide")
            self.text = []
            self.url = None
            self.label = None
            self.focus_set()
            self.notebook = ttk.Notebook(self)
            self.general = Frame(self)
            self.raccourci = Frame(self)
            self.notebook.add(self.general, text="Général")
            self.notebook.add(self.raccourci, text="Raccourci")
            self.notebook.grid(padx=10, pady=10)
            self.showGeneral()
            self.showRaccourci()

        def showGeneral(self):
            self.text = ["Cette application OpenSource permet la résolution de grilles de sudoku. \n",
                         "La résolution des grilles de sudoku peut se faire à l'aide des méthodes :\n",
                         "     - inclusion ; \n     - exclusion ; \n     - backtracking ; \n     - globale.\n",
                         "Il est également possible de choisir la vitesse de résolution. Il est ainsi \n",
                         "possible d'opter pour une résolution en temps réel, la plus rapide possible.\n",
                         "Il existe également une résolution en pas à pas montrant le fonctionnement\n",
                         "de la méthode de résolution utilisée.\n",
                         "Les grilles peuvent être enregistrées afin de pouvoir y accéder plus simple-\n",
                         "ment, sans avoir à réécrire chacun des chiffres.\n",
                         "La grille peut aussi être envoyée à la Raspberry Pi, qui pourra, si elle est\n",
                         "connectée, écrire physiquement celle-ci à l'aide du bras mécanique."]
            self.showLabel(self.general)

        def showRaccourci(self):
            self.text = ["De nombreux raccourcis claviers sont disponibles afin de faciliter\n l'utilisation",
                         "de l'application.\n\n",
                         " Ctrl + O \t\tOuvrir une grille existante (en format .txt)\n",
                         " Ctrl + S \t\tSauvegarder une nouvelle grille (en format .txt)\n",
                         " Ctrl + E \t\tEnvoyer la grille courante à la Raspberry Pi\n",
                         " Ctrl + H \t\tOuverture du menu d'aide\n",
                         " Entrée \t\tEditer la grille manuellement\n",
                         " Espace \t\tSuspendre la résolution\n",
                         " Retour \t\tAffihcer la grille avant sa résolution\n",
                         " F5 \t\tLancer la résolution\n",
                         " O \t\tOuverture de la dernière grille créée\n",
                         " S \t\tSauvegarde rapide\n",
                         " X \t\tEffacer la grille courante"]
            self.showLabel(self.raccourci)

        def showLabel(self, Frame):
            self.label = Label(Frame)
            self.url = Label(Frame)
            url = "Plus d'informations disponibles sur www.github.com/alphter/Sudoku-Plotter"
            self.label.configure(text=''.join(self.text), font=('Times', 12), borderwidth=3,
                                 anchor=N, justify=LEFT, height=15)
            self.url.configure(text=url, font=('Times', 12), borderwidth=3, anchor=N, justify=LEFT)
            self.label.grid(padx=15, pady=15, sticky='w')
            self.url.grid(padx=15, pady=5)

    class AboutMenu(Toplevel):
        def __init__(self):
            Toplevel.__init__(self)
            self.title("A propos")
            self.label = Label(self)
            self.focus_set()
            self.text = ["\nCette application a été\n développée par Laurent Tainturier\n et Alphonse Terrier\n",
                         "dans le cadre de leur TIPE\n intitulé 'Sudoku Plotter'\n supervisé par Patrick Couvez.\n\n\n",
                         "Plus d'informations disponibles sur :\n www.github.com/alphter/Sudoku-Plotter"]
            self.label.configure(text=''.join(self.text), font=('Times', 12), borderwidth=3)
            self.label.grid(padx=5, pady=10)

    class BarreMenu(Menu):
        """
        Hérite de la classe Menu() qui permet à l'utilisateur de définir
        ses préférences et les opérations qui doivent être efféctuées
        """

        def __init__(self, boss):
            Menu.__init__(self)
            self.boss = boss
            self.mode = IntVar()
            self.vitesse = IntVar()
            self.mode_resolution = IntVar()
            os.chdir("../pictures/tkinter/")
            self.save_icon = PhotoImage(file="save_icone.png").subsample(24)
            self.open_icon = PhotoImage(file="open_icone.png").subsample(16)
            self.edit_icon = PhotoImage(file="edit_icone.png").subsample(2)
            self.delete_icon = PhotoImage(file="delete_icone.png").subsample(16)
            self.send_icon = PhotoImage(file="send_icon.png").subsample(43)
            self.run_icon = PhotoImage(file="run_icone.png").subsample(13)
            self.pause_icon = PhotoImage(file="pause_icone.png").subsample(22)
            self.restart_icone = PhotoImage(file="restart_icone.png").subsample(27)
            self.shutdown_icon = PhotoImage(file="shutdown_icone.png").subsample(17)
            self.photo_icon = PhotoImage(file="photo_icone.png").subsample(6)
            self.stop_icon = PhotoImage(file="stop_icone.png").subsample(10)
            self.help_icon = PhotoImage(file="help_icone.png").subsample(19)
            self.about_icon = PhotoImage(file="about_icon.png").subsample(37)
            os.chdir("../../script/")

            # Sélection par défaut des items
            self.mode_resolution.set(0)
            self.mode.set(0)
            self.vitesse.set(0)

            # Création des menus
            self.menu_edition = Menu(self, tearoff=0)
            self.menu_resolution = Menu(self, tearoff=0)
            self.menu_methode = Menu(self, tearoff=0)
            self.menu_raspberry = Menu(self, tearoff=0)
            self.menu_aide = Menu(self, tearoff=0)

            # Ajout des menus
            self.add_cascade(label="Edition", menu=self.menu_edition)
            self.add_cascade(label="Résolution", menu=self.menu_resolution)
            self.add_cascade(label="Méthode", menu=self.menu_methode)
            self.add_cascade(label="Raspberry", menu=self.menu_raspberry)
            self.add_cascade(label="Aide", menu=self.menu_aide)

            # Ajout des items du menu 'Edition'
            self.menu_edition.add_command(label="Ouvrir", command=self.boss.openSudoku, accelerator="Ctrl+O",
                                          image=self.open_icon, compound=LEFT)
            self.menu_edition.add_command(label="Sauvegarder", command=self.boss.saveSudoku, accelerator="Ctrl+S",
                                          image=self.save_icon, compound=LEFT)
            self.menu_edition.add_command(label="Manuelle", command=self.boss.startManualEdition,
                                          image=self.edit_icon, compound=LEFT)
            self.menu_edition.add_command(label="Effacer", command=self.boss.effacerSudoku,
                                          image=self.delete_icon, compound=LEFT)

            # Ajout des items du menu 'Résolution'
            self.menu_resolution.add_radiobutton(label="Directe", value=0, variable=self.mode,
                                                 command=lambda: self.boss.choixMode("Directe"))
            vitesse = Menu(tearoff=0)
            self.menu_resolution.add_cascade(label="Pas à pas", menu=vitesse)
            vitesse.add_radiobutton(label="Rapide", value=1, variable=self.mode,
                                    command=lambda: self.boss.choixMode("Rapide"))
            vitesse.add_radiobutton(label="Lente", value=2, variable=self.mode,
                                    command=lambda: self.boss.choixMode("Lente"))

            self.menu_resolution.add_separator()
            self.menu_resolution.add_command(label="Lancer", command=self.boss.startResolution, accelerator="F5",
                                             image=self.run_icon, compound=LEFT)
            self.menu_resolution.add_command(label="Pause", command=self.boss.boss.pauseResolution,
                                             image=self.pause_icon, compound=LEFT)
            self.menu_resolution.add_command(label="Stop", command=self.boss.boss.stopResolution,
                                             image=self.stop_icon, compound=LEFT)

            # Ajout des items du menu 'Méthode'
            self.menu_methode.add_radiobutton(label="Globale", value=0, variable=self.mode_resolution,
                                              command=lambda: self.boss.choixMethode("Globale"))
            self.menu_methode.add_radiobutton(label="Inclusion", value=1, variable=self.mode_resolution,
                                              command=lambda: self.boss.choixMethode("Inclusion"))
            self.menu_methode.add_radiobutton(label="Exclusion", value=2, variable=self.mode_resolution,
                                              command=lambda: self.boss.choixMethode("Exclusion"))
            self.menu_methode.add_radiobutton(label="Backtracking", value=3, variable=self.mode_resolution,
                                              command=lambda: self.boss.choixMethode("Backtracking"))

            # Ajout des items du menu 'Raspberry'
            self.menu_raspberry.add_command(label="Envoyer", command=self.boss.boss.sendSudoku,
                                            image=self.send_icon, compound=LEFT, accelerator="Ctrl+E")
            self.menu_raspberry.add_command(label="Photo", image=self.photo_icon, compound=LEFT,
                                            command=lambda: self.boss.boss.sendInfo("photo"))
            self.menu_raspberry.add_command(label="Stop", image=self.delete_icon, compound=LEFT,
                                            command=lambda: self.boss.boss.sendInfo("stop"))
            self.menu_raspberry.add_separator()
            self.menu_raspberry.add_command(label="Redémarrer", image=self.restart_icone, compound=LEFT,
                                            command=lambda: self.boss.boss.sendInfo("reboot"))
            self.menu_raspberry.add_command(label="Arréter", image=self.shutdown_icon, compound=LEFT,
                                            command=lambda: self.boss.boss.sendInfo("shutdown"))

            # Ajout des items du menu 'Aide'
            self.menu_aide.add_command(label="A propos", command=self.boss.showAPropos,
                                       image=self.about_icon, compound=LEFT)
            self.menu_aide.add_command(label="Aide", command=self.boss.showAide, image=self.help_icon,
                                       compound=LEFT)
