from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from random import *
from copy import *

NUMBER_DEFAULT_LINES = 10
NUMBER_MIN_LINES = 5
NUMBER_MAX_LINES = 20

NUMBER_DEFAULT_COLUMNS = 10
NUMBER_MIN_COLUMNS = 5
NUMBER_MAX_COLUMNS = 20

RESOLUTION_X = 460
RESOLUTION_Y = 460

LINES = 0 #Taille de la grille (verticalement)
COLUMNS = 0 #Taille de la grille (horizontalement)

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

NUMBER_DEFAULT_SHIPS_PER_LENGTH = {1:0, 2:1, 3:2, 4:1, 5:1} 
NUMBER_SHIPS_PER_LENGTH = {}
MAX_SHIPS_PER_LENGTH = 8

MODE = 0 #0 pour SOLO / 1 pour MULTI

player1Tab = []
computerTab, player2Tab = [], []


def draw_grid(instance):
    
    ordinateur = Label(window, text = "Grille de l'ordinateur")
    joueur = Label(window, text = "Grille du joueur")
    ordinateur.configure(font='Helvetica 18 bold')
    joueur.configure(font='Helvetica 18 bold')


    drawing = Canvas(window, bg = "white", width = RESOLUTION_X, height = RESOLUTION_Y)
    drawing2 = Canvas(window, bg = "white", width = RESOLUTION_X, height = RESOLUTION_Y)
    
    drawing.grid(row = 1, column = 0, padx = 60, pady = 25)
    drawing2.grid(row = 1, column = 1, padx = 150)
    ordinateur.grid(row = 0, column = 0)
    joueur.grid(row = 0, column = 1, padx = 80)

    for y in range(LINES):
        for x in range(COLUMNS):
            divC = RESOLUTION_X/COLUMNS
            divL = RESOLUTION_Y/LINES
            X = int(divC*x) 
            Y = int(divL*y) 
            
            drawing.create_line(X, 0, X, RESOLUTION_X, width=2)
            drawing.create_line(0, Y, RESOLUTION_Y, Y, width=2)
            drawing2.create_line(X, 0, X, RESOLUTION_X, width=2)
            drawing2.create_line(0, Y, RESOLUTION_Y, Y, width=2)

'''
Placement d'un bateau
instance :
  0 : Ordinateur
  1 : Joueur 1
  2 : Joueur 2
'''
def placement(shipLength, shipId, instance):

    ship = []
    tab = []

    if instance == 0:
        #Ordinateur               
        tab = computerTab
        
        x = randint(0, COLUMNS-1)
        y = randint(0, LINES-1)       
        direction = randint(1,4)
        
    else:
        #Joueur
        if instance == 1:
            tab = player1Tab
            print("Le joueur 1 remplit sa grille")
        else:
            tab = player2Tab
            print("Le joueur 2 remplit sa grille")
        draw_grid(instance)

        #TODO : Choisir ses coordonnées
        x = -1
        y = -1
        direction = -1

    ship.append(str(x) + " " + str(y))
    
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
        
        #Case occupée => on sort de la fonction
        try:
            if tab[x][y] != 0:
                return -1
        except:
            return -1

    print(ship, shipId, shipLength)
    #Toutes les positions sont OK
    for case in range(len(ship)):
        t = ship[case].split(" ")
        print(t, COLUMNS,LINES, direction)
        tab[int(t[0])][int(t[1])] = shipId
    return 0
                        
'''
#Initialisation d'une grille
instance :
  0 : Ordinateur
  1 : Joueur 1
  2 : Joueur 2
'''
def init_grid(instance):
    shipId = 1
    
    for shipLength in NUMBER_SHIPS_PER_LENGTH:

        for ship in range(NUMBER_SHIPS_PER_LENGTH[shipLength]):
            result = -1
            
            while result == -1 and NUMBER_SHIPS_PER_LENGTH[shipLength] != 0:                
                result = placement(shipLength, shipId, instance)
                
                if result != -1:
                    shipId = shipId + 1

'''
Création de la nouvelle partie
isSolo :
 True : SOLO
 False : MULTI
'''
def new_game(isSolo):
    print("Création d'une nouvelle partie...")

    global MODE
    MODE = isSolo
    
    global LINES, COLUMNS, NUMBER_SHIPS_PER_LENGTH

    #Paramètres non modifiés => On prend ceux par défaut
    if LINES == 0:
        LINES = deepcopy(NUMBER_DEFAULT_LINES)
    if COLUMNS == 0:
        COLUMNS = deepcopy(NUMBER_DEFAULT_COLUMNS)
    if len(NUMBER_SHIPS_PER_LENGTH) == 0:
        NUMBER_SHIPS_PER_LENGTH = deepcopy(NUMBER_DEFAULT_SHIPS_PER_LENGTH)
    
    print("[1/3] Initialisation de la grille du joueur 1")
    
    #Création et initialisation de la grille du joueur 1
    global player1Tab   
    player1Tab = [0]*COLUMNS
    print(player1Tab)
    for _ in range(COLUMNS):
        player1Tab[_] = [0]*LINES
        print(player1Tab)
    #init_grid(1)

    if MODE == 0:
        #====Solo====#
        print("[2/3] Initialisation de la grille de l'ordinateur")
        
        #Création et initialisation de la grille de l'ordinateur      
        global computerTab
        computerTab = [0]*COLUMNS
        for _ in range(COLUMNS):
            computerTab[_] = [0]*LINES
        init_grid(0)

        draw_grid(0)
            
    else:
        #====Multi====#    
        print("[2/3] Initialisation de la grille du joueur 2")
        
        #Création et initialisation de la grille du joueur 2
        global player2Tab
        player2Tab = [0]*COLUMNS
        for _ in range(COLUMNS):
            player2Tab[_] = [0]*LINES        
        init_grid(2)
                    
def continue_game():
    #TODO
    print()

def changeParametres():
    global LINES, COLUMNS
    LINES = int(lignesE.get())
    COLUMNS = int(colonesE.get())

def confir():
    print()

def parameters():
    para = Tk()
    para.title("Paramètres")
    para.geometry("370x350+300+200")
    para.resizable(False, False)

    global colonesE,lignesE

    #Création d'élčments
    bienvenue = Label(para, text='Paramètres du jeu\n')
    colones = Label(para, text='Nombre de colonnes :')
    lignes = Label(para, text='Nombre de lignes :')
    colonesE = Spinbox(para, from_=NUMBER_MIN_COLUMNS, to=NUMBER_MAX_COLUMNS, width=3)
    lignesE = Spinbox(para, from_=NUMBER_MIN_LINES, to=NUMBER_MAX_LINES, width=3)
    #width, height

    taille = Label(para, text='\nLe nombre de bateaux par taille\n')
    case1 = Label(para, text='1 case(s) :')
    case2 = Label(para, text='2 case(s) :')
    case3 = Label(para, text='3 case(s) :')
    case4 = Label(para, text='4 case(s) :')
    case5 = Label(para, text='5 case(s) :')
    case6 = Label(para, text=' ')
    act = Label(para, text = 'Actuellement :')
    
    case1E = Spinbox(para, from_=0, to=MAX_SHIPS_PER_LENGTH, width=3)
    case2E = Spinbox(para, from_=0, to=MAX_SHIPS_PER_LENGTH, width=3)
    case3E = Spinbox(para, from_=0, to=MAX_SHIPS_PER_LENGTH, width=3)
    case4E = Spinbox(para, from_=0, to=MAX_SHIPS_PER_LENGTH, width=3)
    case5E = Spinbox(para, from_=0, to=MAX_SHIPS_PER_LENGTH, width=3)
    appliquer = ttk.Button(para, text= 'Appliquer', command = changeParametres)
    confirmer = ttk.Button(para, text = 'Confirmer', command = confir)
    
    #Agrandissement du texte
    bienvenue.configure(font = "-size 12")
    colones.configure(font = "-size 11")
    lignes.configure(font = "-size 11")

    taille.configure(font = "-size 11")
    case1.configure(font = "-size 11")
    case2.configure(font = "-size 11")
    case3.configure(font = "-size 11")
    case4.configure(font = "-size 11")
    case5.configure(font = "-size 11")
    case6.configure(font = "-size 11")
    act.configure(font = "-size 11")
    
    #Répartition des différents élements
    bienvenue.grid(row = 0, column = 0, padx = 120, pady = 10, sticky = W, columnspan = 1)
    colones.grid(row = 2, column = 0, sticky = W, padx = 20)
    lignes.grid(row = 3, column = 0, sticky = W, padx = 20)
    colonesE.grid(row = 2, column = 0, padx = 180, sticky = W)
    lignesE.grid(row = 3, column = 0, padx = 180, sticky = W)

    taille.grid(row = 5, column = 0, sticky = W, padx = 20, columnspan = 1)
    case1.grid(row = 7, column = 0, sticky = W, padx = 20)
    case2.grid(row = 8, column = 0, sticky = W, padx = 20)
    case3.grid(row = 9, column = 0, sticky = W, padx = 20)
    case4.grid(row = 10, column = 0, sticky = W, padx = 20)
    case5.grid(row = 11, column = 0, sticky = W, padx = 20)
    case6.grid(row = 12, column = 0, sticky = W, padx = 20)
    act.grid(row = 5, column = 0, padx = 20)

    case1E.grid(row=7, column = 0, padx = 100, sticky = W)
    case2E.grid(row=8, column = 0, padx = 100, sticky = W)
    case3E.grid(row=9, column = 0, padx = 100, sticky = W)
    case4E.grid(row=10, column = 0, padx = 100, sticky = W)
    case5E.grid(row=11, column = 0, padx = 100, sticky = W)
    appliquer.grid(row = 13, column = 0, padx = 150, sticky = W)
    confirmer.grid(row = 13, column = 0, padx = 250)

    #TODO : Bouton de validation / fermeture fenêtre
    
    para.mainloop()

def informations():
    #TODO
    print()

def callback():
    if messagebox.askokcancel("Quit", "Voulez-vous vraiment quitter?"):
        window.destroy()

def xyPos(event):
    print(event.x,event.y)

def main_menu():
    global window
    window = Tk()
    window.title("Bataille Navale")
    window.geometry("1280x700+200+100")

    window.bind( "<Button-1>", xyPos )


    menu = Menu(window)

    menu1 = Menu(menu, tearoff=0)
    menu.add_cascade(label="Partie", menu=menu1)

    menu1bis = Menu(menu1, tearoff=0)
    menu1.add_cascade(label="Nouvelle Partie", menu=menu1bis)
    menu1bis.add_command(label="1 joueur", command=lambda: new_game(0))
    menu1bis.add_command(label="2 joueurs", command=lambda: new_game(1))   
    menu1.add_command(label="Continuer Partie", command=continue_game)

    menu2 = Menu(menu, tearoff=0)
    menu.add_cascade(label="Options", menu=menu2)
    menu2.add_command(label="Configurer le jeu", command=parameters)
    menu2.add_command(label="A propos", command=informations)
    menu2.add_separator()
    menu2.add_command(label="Quitter", command=callback)

    window.config(menu=menu)

    window.protocol("WM_DELETE_WINDOW", callback)
    window.resizable(False, False)
    
    window.mainloop()

main_menu()
