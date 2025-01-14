import tkinter as tk
import random

# Classe Navire (chaque navire a une taille, des positions, et un suivi des touches)
class Navire:
    def __init__(self, taille):
        self.taille = taille
        self.positions = []   # Liste des cases (x,y) occupées par le navire
        self.touchees = []    # Liste des cases (x,y) déjà touchées

    def est_coule(self):
        # Vérifie si toutes les positions du navire sont dans la liste touchees
        for pos in self.positions:
            if pos not in self.touchees:
                return False
        return True

# Classe Plateau (chaque plateau possède une grille et des navires)
class Plateau:
    def __init__(self):
        self.grille = []
        for _ in range(10):
            ligne = []
            for _ in range(10):
                ligne.append(".")
            self.grille.append(ligne)
        self.navires = []

    # Ajoute un navire dans la grille si possible
    def ajouter_navire(self, navire, positions):
        for (x, y) in positions:
            if x < 0 or x > 9 or y < 0 or y > 9:
                return False
            if self.grille[x][y] != ".":
                return False
        navire.positions = positions
        for (x, y) in positions:
            self.grille[x][y] = "N"
        self.navires.append(navire)
        return True

    # Vérifie un tir sur la case (x,y)
    def verifier_tir(self, x, y):
        if self.grille[x][y] == "N":
            self.grille[x][y] = "X"
            # On marque la touche pour le navire concerné
            for navire in self.navires:
                if (x, y) in navire.positions:
                    navire.touchees.append((x, y))
                    if navire.est_coule():
                        print("Un navire vient d’être coulé !")
                    break
            return "touché"
        elif self.grille[x][y] == ".":
            self.grille[x][y] = "O"
            return "manqué"
        else:
            return "déjà tiré"

    # Vérifie si tous les navires du plateau sont coulés
    def tous_navires_coules(self):
        for navire in self.navires:
            if not navire.est_coule():
                return False
        return True

    # Place automatiquement des navires de différentes tailles
    def generer_placement_aleatoire(self, tailles_navires):
        for taille in tailles_navires:
            while True:
                orientation = random.choice(["horizontal", "vertical"])
                if orientation == "horizontal":
                    x = random.randint(0, 9)
                    y = random.randint(0, 9 - taille)
                    positions = []
                    for i in range(taille):
                        positions.append((x, y + i))
                else:
                    x = random.randint(0, 9 - taille)
                    y = random.randint(0, 9)
                    positions = []
                    for i in range(taille):
                        positions.append((x + i, y))
                libre = True
                for (px, py) in positions:
                    if self.grille[px][py] != ".":
                        libre = False
                        break
                if libre:
                    navire = Navire(taille)
                    self.ajouter_navire(navire, positions)
                    break

# Classe Joueur (chaque joueur a un nom et un plateau)
class Joueur:
    def __init__(self, nom):
        self.nom = nom
        self.plateau = Plateau()

# Fonction pour placer un navire manuellement
def placer_navire(bouton, x, y, joueur, grille, tailles_navires, bouton_jouer, orientation):
    if not tailles_navires:
        print("Tous les navires ont été placés.")
        return

    taille = tailles_navires[0]

    if orientation.get() == "H":
        positions = []
        for i in range(taille):
            positions.append((x, y + i))
    else:
        positions = []
        for i in range(taille):
            positions.append((x + i, y))

    ok = joueur.plateau.ajouter_navire(Navire(taille), positions)
    if ok:
        for (px, py) in positions:
            grille[px][py].config(text="N", bg="blue")
        tailles_navires.pop(0)
        if not tailles_navires:
            bouton_jouer.config(state=tk.NORMAL)
            print("Placement terminé !")
    else:
        print("Impossible de placer le navire ici.")

# Fonction quand le joueur tire sur la grille adverse
def tirer(bouton, x, y, joueur, adversaire, grille_adversaire, bouton_tour):
    resultat = adversaire.plateau.verifier_tir(x, y)
    if resultat == "touché":
        print(joueur.nom, "a touché un navire en (", x, ",", y, ") !")
        bouton.config(text="X", bg="blue")
    elif resultat == "manqué":
        print(joueur.nom, "a manqué en (", x, ",", y, ").")
        bouton.config(text="O", bg="white")
    else:
        print(joueur.nom, "a déjà tiré sur cette case (", x, ",", y, ").")
        return

    if adversaire.plateau.tous_navires_coules():
        print(joueur.nom, "a gagné la partie !")
        bouton_tour.config(state=tk.DISABLED)
        return

    bouton_tour.config(state=tk.NORMAL)
    for ligne in grille_adversaire:
        for b in ligne:
            b.config(state=tk.DISABLED)

# Fonction pour le tir aléatoire de l'ordinateur
def tir_ordinateur(joueur, grille_joueur, bouton_tour):
    while True:
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        resultat = joueur.plateau.verifier_tir(x, y)
        if resultat == "touché":
            print("L'ordinateur a touché un navire en (", x, ",", y, ") !")
            grille_joueur[x][y].config(text="X", bg="red")
            break
        elif resultat == "manqué":
            print("L'ordinateur a manqué en (", x, ",", y, ").")
            grille_joueur[x][y].config(text="O", bg="white")
            break

    if joueur.plateau.tous_navires_coules():
        print("L'ordinateur a gagné la partie !")
        bouton_tour.config(state=tk.DISABLED)
        return

    bouton_tour.config(state=tk.DISABLED)
    for ligne in grille_joueur:
        for b in ligne:
            b.config(state=tk.NORMAL)

# Crée la grille visuelle
def creer_grille(frame, grille, label, action=None, joueur=None, tailles_navires=None, bouton_jouer=None, orientation=None, adversaire=None, bouton_tour=None):
    tk.Label(frame, text="Grille " + label, bg=frame["bg"], font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=10, pady=10)
    for x in range(10):
        ligne_boutons = []
        for y in range(10):
            b = tk.Button(frame, text=" ", width=3, height=1)
            b.grid(row=x + 1, column=y, padx=2, pady=2)
            if action is not None:
                b.config(command=lambda btn=b, i=x, j=y: action(btn, i, j, joueur, grille, tailles_navires, bouton_jouer, orientation))
            elif adversaire is not None and bouton_tour is not None and joueur is not None:
                b.config(command=lambda btn=b, i=x, j=y: tirer(btn, i, j, joueur, adversaire, grille, bouton_tour))
                b.config(state=tk.DISABLED)
            ligne_boutons.append(b)
        grille.append(ligne_boutons)

# Active la grille de l'ordinateur quand tout est prêt
def commencer_jeu(grille_ordinateur, bouton_tour):
    print("La partie commence !")
    for ligne in grille_ordinateur:
        for b in ligne:
            b.config(state=tk.NORMAL)
    bouton_tour.config(state=tk.DISABLED)

# Fenêtre principale du jeu
def interface_principale():
    root = tk.Tk()
    root.title("Bataille Navale")
    root.geometry("1000x700")

    frame_joueur = tk.Frame(root, bg="lightblue")
    frame_ordinateur = tk.Frame(root, bg="lightgreen")
    frame_joueur.grid(row=0, column=0, padx=20, pady=20)
    frame_ordinateur.grid(row=0, column=1, padx=20, pady=20)

    joueur = Joueur("Joueur")
    ordinateur = Joueur("Ordinateur")

    ordinateur.plateau.generer_placement_aleatoire([5, 4, 3, 3, 2])

    grille_joueur = []
    grille_ordinateur = []

    tailles_navires_joueur = [5, 4, 3, 3, 2]
    orientation = tk.StringVar(value="H")

    bouton_tour = tk.Button(root, text="Tour de l'ordinateur", state=tk.DISABLED, command=lambda: tir_ordinateur(joueur, grille_joueur, bouton_tour))
    bouton_tour.grid(row=1, column=0, columnspan=2, pady=20)

    bouton_jouer = tk.Button(root, text="Commencer la Partie", state=tk.DISABLED, command=lambda: commencer_jeu(grille_ordinateur, bouton_tour))
    bouton_jouer.grid(row=2, column=0, columnspan=2, pady=20)

    creer_grille(frame_joueur, grille_joueur, "Joueur", action=placer_navire, joueur=joueur, tailles_navires=tailles_navires_joueur, bouton_jouer=bouton_jouer, orientation=orientation)
    creer_grille(frame_ordinateur, grille_ordinateur, "Ordinateur", adversaire=ordinateur, bouton_tour=bouton_tour, joueur=joueur)

    root.mainloop()

if __name__ == "__main__":
    interface_principale()
