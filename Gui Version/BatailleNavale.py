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

player1Tab = []
computerTab, player2Tab = [], []

#Fonction qui demande la longueur du bateau et l'id pour pouvoir le placer sur le terrain de jeu de l'ordinateur
def computerPlacement(shipLength, shipId):
    x = randint(0, COLUMNS-1)
    y = randint(0, LINES-1)
    global computerTab
    ship = []
    #On regarde si la case d'origine est ocupé ou non. Si oui, on sort de la fonction
    if computerTab[x][y] != 0:
        return -1
    else:
        ship.append(str(x)+" "+str(y)) 
    direction = randint(1, 4)
    for case in range(shipLength -1):
        #UP
        if direction == 1 and y > 0:
            y = y - 1
            ship.append(str(x)+" "+str(y))
        #DOWN
        elif direction == 2 and y < LINES - 1:
            y = y + 1
            ship.append(str(x)+" "+str(y))
        #LEFT
        elif direction == 3 and x > 0:
            x = x - 1
            ship.append(str(x)+" "+str(y))
        #RIGHT
        elif direction == 4 and x < COLUMNS -1:
            x = x + 1
            ship.append(str(x)+" "+str(y))
        #Si on sort des limites du tableau de jeu, alors on sort de cette fonction en retournant erreur
        else:
            return -1
        #Si cettte case est occupé, alors on sort de cette fonction en retournant erreur
        if computerTab[x][y] != 0:
            return -1
    #Si on arrive ici, alors toutes les positions sont libres et elles existent
    print(ship,shipId)
    for case in range(len(ship)):
        xy = ship[case]
        tab = xy.split(" ")
        computerTab[int(tab[0])][int(tab[1])] = shipId
    return 0

def new_game(isMulti):
    print("Création d'une nouvelle partie...")
    global LINES, COLUMNS, NUMBER_SHIPS_PER_LENGTH
    #Si les lignes, colones et le nombre de bateaux n'ont pas été changés dans les paramčtres, alors on récupčre les valeurs par défault
    if LINES == 0:
        LINES = deepcopy(NUMBER_DEFAULT_LINES)
    if COLUMNS == 0:
        COLUMNS = deepcopy(NUMBER_DEFAULT_COLUMNS)
    if len(NUMBER_SHIPS_PER_LENGTH) == 0:
        NUMBER_SHIPS_PER_LENGTH = deepcopy(NUMBER_DEFAULT_SHIPS_PER_LENGTH)

    #Si on veut jouer contre l'ordinateur
    if not(isMulti):
        print("[1/3] Initialisation de la grille de l'ordinateur")

        global computerTab
        #Création du tableau de l'ordinateur
        computerTab = [0]*LINES
        for _ in range(LINES):
            computerTab[_] = [0]*COLUMNS

        shipId = 1
        #Ajout de bateaux sur le terrain de l'ordinateur
        for shipLength in NUMBER_SHIPS_PER_LENGTH:
            #Pour chaque bateau d'un taille NUMBER_SHIPS_PER_LENGTH[shipLength]
            for ship in range(NUMBER_SHIPS_PER_LENGTH[shipLength]):
                result = -1
                #Tant qu'on ne ressoit pas le succčs de la fonction computerPlacement(), continuer
                while result == -1 and NUMBER_SHIPS_PER_LENGTH[shipLength] != 0:                
                    result = int(computerPlacement(shipLength, shipId))
                    if result != -1:
                        shipId = shipId + 1
        
        print("[1/3] TERMINÉ !")
        for y in range(LINES):
            for x in range(COLUMNS):
                print(computerTab[x][y], end="")
            print("")
                    
def continue_game():
    #TODO
    print()

def parameters():
    #TODO
    print()

def informations():
    #TODO
    print()

def solo():
    new_game(False)

def multi():
    new_game(True)

def main_menu():
    window = Tk()
    window.title("Bataille Navale")

    menu = Menu(window)

    menu1 = Menu(menu, tearoff=0)
    menu.add_cascade(label="Partie", menu=menu1)

    menu1bis = Menu(menu1, tearoff=0)
    menu1.add_cascade(label="Nouvelle Partie", menu=menu1bis)
    menu1bis.add_command(label="1 joueur", command=solo)
    menu1bis.add_command(label="2 joueurs", command=multi)   
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
