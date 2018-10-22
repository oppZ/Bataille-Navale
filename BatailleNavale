from tkinter import *
from random import *

LINES = 10 #Taille de la grille (verticalement)
COLUMNS = 10 #Taille de la grille (horizontalement)

ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" #Alphabet

CONFIG = [1,1,2,1,1] #Configuration (par taille)

plTab = []
comTab, pl2Tab = [], []
subTab = []

def rand_binary():
    return randint(0, 1) == 0

def verify(comTab):
    for x in range(0, COLUMNS):
        for y in range(0, LINES):
            i = subTab[x][y]
            if (not (i == 0) and comTab[x][y] != 0):
                return False
    return True

def new_game(isMulti):
    print("Création d'une nouvelle partie...")

    if not(isMulti):
        print("[1/3] Initialisation de la grille de l'ordinateur")
        global compTab
        comTab = [0]*LINES
        for _ in range(LINES):
            comTab[_] = [0]*COLUMNS

        for i in range(2, 7):

            for k in range(0, CONFIG[i-2]):
                global subTab
                validated = False
                
                while not validated:
                    subTab = [0]*LINES
                    for _ in range(LINES):
                        subTab[_] = [0]*COLUMNS
                    
                    if rand_binary():
                        #VERTICAL
                        x = randint(0, LINES-1)
                        if rand_binary():
                            #HAUT
                            y = randint(i, COLUMNS-1)
                            for _ in range(y, (y-i), -1):
                                subTab[x][_] = i
                        else:
                            #BAS
                            y = randint(0, COLUMNS-i-1)
                            for _ in range(y, (y+i)):
                                subTab[x][_] = i
                            
                    else:
                        #HORINZONTAL
                        y = randint(0, COLUMNS-1)
                        if rand_binary():
                            #DROITE
                            x = randint(0, LINES-i-1)
                            for _ in range(x, (x+i)):
                                subTab[x][_] = i
                        else:
                            #GAUCHE
                            x = randint(k, LINES-1)
                            for _ in range(x, (x-i), -1):
                                subTab[x][_] = i

                    validated = verify(comTab)

                for x in range(COLUMNS):
                    for y in range(LINES):
                        z = subTab[x][y]
                        if z != 0:
                            comTab[x][y] = z
                        
        print("[1/3] TERMINÉ !")
        for i in range(10):
            for k in range(10):
                print(comTab[i][k], end="")
            print("\n")
                    
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
