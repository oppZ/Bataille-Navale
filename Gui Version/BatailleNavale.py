from tkinter import *
from random import *
from copy import *

NUMBER_DEFAULT_LINES = 10
NUMBER_MIN_LINES = 5
NUMBER_MAX_LINES = 26

NUMBER_DEFAULT_COLUMNS = 10
NUMBER_MIN_COLUMNS = 5
NUMBER_MAX_COLUMNS = 26

LINES = 0 #Taille de la grille (verticalement)
COLUMNS = 0 #Taille de la grille (horizontalement)

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

NUMBER_DEFAULT_SHIPS_PER_LENGTH = {1:0, 2:1, 3:2, 4:1, 5:1} 
NUMBER_SHIPS_PER_LENGTH = {}

MODE = 0 #Par défaut, mode SOLO

player1Tab = []
computerTab, player2Tab = [], []

#Fonction qui demande la longueur du bateau et l'id pour pouvoir le placer sur le terrain de jeu de l'ordinateur

def placement(shipLength, shipId, x, y, playerTab):
    global ship

    tab = computerTab if MODE == 0 else playerTab 
    
    for case in range(shipLength -1):
        if direction == 1 and y > 0:
            #HAUT
            y = y - 1
            ship.append(str(x) + " " + str(y))

        elif direction == 2 and y < LINES - 1:
            #BAS
            y = y + 1
            ship.append(str(x) + " " + str(y))

        elif direction == 3 and x > 0:
            #GAUCHE
            x = x - 1
            ship.append(str(x) + " " + str(y))

        elif direction == 4 and x < COLUMNS -1:
            #DROITE
            x = x + 1
            ship.append(str(x) + " " + str(y))
        else:
            return -1
        '''
        Si on sort des limites du jeu, on sort de la fonction
        et on retourne 'erreur'
        '''
        
        '''
        Si la case est occupée, on sort de la fonction
        et on retourne 'erreur'
        '''
        if tab[x][y] != 0:
            return -1

    '''
    Si on arrive ici, c'est que toutes les positions
    existent et ne sont pas déjà prises
    '''
    for case in range(len(ship)):
        t = ship[case].split(" ")
        tab[int(t[0])][int(t[1])] = shipId
    return 0
                        
#Initialisation de la grille de l'ordinateur
def computerPlacement(shipLength, shipId):
    x = randint(0, COLUMNS-1)
    y = randint(0, LINES-1)

    global ship
    ship = []
	
    if computerTab[x][y] != 0:
        return -1
    else:
        ship.append(str(x) + " " + str(y))

    global direction
    direction = randint(1, 4)

    return placement(shipLength, shipId, x, y, -1)

#Initialisation de la grille d'un joueur
def playerPlacement(shipLength, shipId, playerTab):
    x = randint(0, COLUMNS-1)
    y = randint(0, LINES-1)
    #TODO : Demander les coordonnées à l'utilisateur
    
    global ship
    ship = []
    if playerTab[x][y] != 0:
        return -1
    else:
        ship.append(str(x) + "  " + str(y))

    global direction
    #TODO : Demander la direction à l'utilisateur
    
    
    return placement(shipLength, shipId, x, y, playerTab)

#Initialisation d'une grille
def init_grid(isPlayer, playerTab):
    shipId = 1
    
    #Ajout de bateaux sur le terrain de l'ordinateur
    for shipLength in NUMBER_SHIPS_PER_LENGTH:
        #Pour chaque bateau d'un taille NUMBER_SHIPS_PER_LENGTH[shipLength]
        for ship in range(NUMBER_SHIPS_PER_LENGTH[shipLength]):
            result = -1
            #Tant qu'on ne ressoit pas le succčs de la fonction computerPlacement(), continuer
            while result == -1 and NUMBER_SHIPS_PER_LENGTH[shipLength] != 0:                
                if isPlayer == True:
                    result = int(playerPlacement(shipLength, shipId, playerTab))
                else:
                    result = int(computerPlacement(shipLength, shipId))
                if (result != -1):
                    shipId = shipId + 1

def new_game(isMulti):
    print("Création d'une nouvelle partie...")

    global MODE
    MODE = isMulti
    
    global LINES, COLUMNS, NUMBER_SHIPS_PER_LENGTH
    
    '''
    Si les paramètres n'ont pas été modifié,
    alors on utilise ceux par défauts
    '''
    if LINES == 0:
        LINES = deepcopy(NUMBER_DEFAULT_LINES)
    if COLUMNS == 0:
        COLUMNS = deepcopy(NUMBER_DEFAULT_COLUMNS)
    if len(NUMBER_SHIPS_PER_LENGTH) == 0:
        NUMBER_SHIPS_PER_LENGTH = deepcopy(NUMBER_DEFAULT_SHIPS_PER_LENGTH)
    
    print("[1/3] Initialisation de la grille du joueur 1")

    global player1Tab
    
    #Création de la grille du joueur 1
    player1Tab = [0]*LINES
    for _ in range(LINES):
        player1Tab[_] = [0]*COLUMNS
        
    init_grid(True, player1Tab)

    if not(isMulti):
        #====Solo====#
        
        print("[2/3] Initialisation de la grille de l'ordinateur")

        global computerTab
        
        #Création du tableau de l'ordinateur
        computerTab = [0]*LINES
        for _ in range(LINES):
            computerTab[_] = [0]*COLUMNS

        init_grid(False, -1)
            
    else:
        #====Multi====#
        
        print("[2/3] Initialisation de la grille du joueur 2")

        global player2Tab

        #Création du tableau du joueur 2
        player2Tab = [0]*LINES
        for _ in range(LINES):
            player2Tab[_] = [0]*COLUMNS
            
        init_grid(True, player2Tab)
                    
def continue_game():
    #TODO
    print()

def parameters():
    para = Tk()
    para.title("Parametres")
    para.geometry("500x200")

    
    #Création d'élčments
    bienvenue = Label(para, text='Changer les parametres du jeu\n')
    colones = Label(para, text='Le nombre de colones du jeu')
    lignes = Label(para, text='Le nombre de lignes du jeu')
    colonesE = Spinbox(para, from_=NUMBER_MIN_COLUMNS, to=NUMBER_MAX_COLUMNS)
    lignesE = Spinbox(para, from_=NUMBER_MIN_LINES, to=NUMBER_MAX_LINES)

    #Agrandissement du text
    bienvenue.configure(font = "-size 12")
    colones.configure(font = "-size 11")
    lignes.configure(font = "-size 11")

    #Répartition des différents élements
    bienvenue.grid(row = 0, column = 0, padx = 100,  sticky = W)
    colones.grid(row = 2, column = 0, sticky = W)
    lignes.grid(row = 3, column = 0, sticky = W)
    colonesE.grid(row = 2, column = 0, padx = 220)
    lignesE.grid(row = 3, column = 0, padx = 220)
    
    para.mainloop()
    
    
    print()

def informations():
    #TODO
    print()

def main_menu():
    window = Tk()
    window.title("Bataille Navale")

    menu = Menu(window)

    menu1 = Menu(menu, tearoff=0)
    menu.add_cascade(label="Partie", menu=menu1)

    menu1bis = Menu(menu1, tearoff=0)
    menu1.add_cascade(label="Nouvelle Partie", menu=menu1bis)
    menu1bis.add_command(label="1 joueur", command=lambda: new_game(1))
    menu1bis.add_command(label="2 joueurs", command=lambda: new_game(0))   
    menu1.add_command(label="Continuer Partie", command=continue_game)

    menu2 = Menu(menu, tearoff=0)
    menu.add_cascade(label="Options", menu=menu2)
    menu2.add_command(label="Configurer le jeu", command=parameters)
    menu2.add_command(label="A propos", command=informations)
    menu2.add_separator()
    menu2.add_command(label="Quitter", command=window.quit)

    window.config(menu=menu)

    window.mainloop()

main_menu()
