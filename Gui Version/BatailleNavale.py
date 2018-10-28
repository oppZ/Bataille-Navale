from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from random import *
from copy import *
from math import *
import time

NUMBER_DEFAULT_LINES = 10
NUMBER_MIN_LINES = 5
NUMBER_MAX_LINES = 16

NUMBER_DEFAULT_COLUMNS = 10
NUMBER_MIN_COLUMNS = 5
NUMBER_MAX_COLUMNS = 16

#Taille en pixel du terrain du jeu sur la fenêtre (canvas)
SIZE_X = 460
SIZE_Y = 460

LINES = 0 #Taille de la grille (verticalement)
COLUMNS = 0 #Taille de la grille (horizontalement)

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

NUMBER_DEFAULT_SHIPS_PER_LENGTH = {1:0, 2:1, 3:2, 4:1, 5:1} 
NUMBER_SHIPS_PER_LENGTH = {}
MAX_SHIPS_PER_LENGTH = 8

MODE = 0 #0 pour SOLO / 1 pour MULTI


player1Tab = []
computerTab = []


def draw_grid():
    global drawingComputer, drawingPlayer, tabPosImages
    global imageCaseInconnue, imageCaseBombe, imageCaseShip, imageCaseShipDestroyed, imageCaseMer
    #Ouvreture des images
    imageCaseInconnue = PhotoImage(file ="unknown.png")
    imageCaseBombe = PhotoImage(file = "bomb45.png")
    imageCaseShip = PhotoImage(file = "ship.png")
    imageCaseShipDestroyed = PhotoImage(file = "destroy45.png")
    imageCaseMer = PhotoImage(file = "wave45.png")
    
    #Titre
    ordinateur = Label(window, text = "Grille de l'ordinateur")
    joueur = Label(window, text = "Grille du joueur")
    #Taille du titre
    ordinateur.configure(font='Helvetica 18 bold')
    joueur.configure(font='Helvetica 18 bold')
    #Création de canvas
    drawingComputer = Canvas(window, bg = "white", width = SIZE_X, height = SIZE_Y)
    drawingPlayer = Canvas(window, bg = "white", width = SIZE_X, height = SIZE_Y)

    drawingToPlace = drawingPlayer.bind( "<Button-1>", xyPos)

    #Positionnement des titres et des canvas
    drawingComputer.grid(row = 1, column = 0, padx = 60, pady = 25)
    drawingPlayer.grid(row = 1, column = 1, padx = 150)
    ordinateur.grid(row = 0, column = 0)
    joueur.grid(row = 0, column = 1, padx = 80)

    #Contour des canvas
    drawingComputer.create_line(3,3,SIZE_X,3, width=2)
    drawingComputer.create_line(SIZE_X,3,SIZE_X,SIZE_Y, width=2)
    drawingComputer.create_line(SIZE_X,SIZE_Y,3,SIZE_Y, width=2)
    drawingComputer.create_line(3,SIZE_Y,3,3, width=2)

    drawingPlayer.create_line(3,3,SIZE_X,3, width=2)
    drawingPlayer.create_line(SIZE_X,2,SIZE_X,SIZE_Y, width=2)
    drawingPlayer.create_line(SIZE_X,SIZE_Y,2,SIZE_Y, width=2)
    drawingPlayer.create_line(3,SIZE_Y,3,3, width=2)

    tabPosImages = []
    #Création de lignes sur les canvas de l'ordinateur et de l'utilisateur
    for y in range(LINES):
        for x in range(COLUMNS):
            divC = SIZE_X/COLUMNS
            divL = SIZE_Y/LINES
            X = int(divC*x) 
            Y = int(divL*y)
            
            x2 = TAILLE_CASE_X*x + TAILLE_CASE_X/2
            y2 = TAILLE_CASE_Y*y + TAILLE_CASE_Y/2
            tabPosImages.append(drawingComputer.create_image(x2, y2, image = imageCaseInconnue))
            
            drawingComputer.create_line(X, 0, X, SIZE_X, width=1)
            drawingComputer.create_line(0, Y, SIZE_Y, Y, width=1)
            drawingPlayer.create_line(X, 0, X, SIZE_X, width=1)
            drawingPlayer.create_line(0, Y, SIZE_Y, Y, width=1)
    

'''
Placement d'un bateau
instance :
  0 : Ordinateur
  1 : Joueur 1
  2 : Joueur 2
'''
shipPos = []
shipIdPlayer = 1
shipLeng = 1
placeJoueur = True


#Appel de la fonction lorsque le clic droit a été actionné ainsi 
def xyPos(event):
    global placeJoueur
    print(placeJoueur)
    if placeJoueur == True:
        global shipPos,UneCase, tmp, shipLeng
        UneCase = False
        res = 0
        #Si on a placé tous les bateaux d'une même taille, alors on récupère le nombre de bateaux à placer
        while tmp == 0:
            shipLeng = shipLeng + 1
            try:
                tmp = deepcopy(NUMBER_SHIPS_PER_LENGTH[shipLeng])
            except:
                #On fait en sorte que la fonction ne soit plus utilisable
                placeJoueur = False
        #On récupère les positions de x y sur le canvas, puis on calcul la case correspondante
        eventX = event.x
        eventY = event.y
        shipPos.append(ceil(eventX/TAILLE_CASE_X)-1)
        shipPos.append(ceil(eventY/TAILLE_CASE_Y)-1)
        #Si un bateau a une seule case, alors dès le début on place le bateau si possible
        if shipLeng == 1:
            UneCase = True
            res = placement(shipLeng,shipIdPlayer, 1)
            shipPos = []
            if res != -1:
                tmp = tmp -1
        #Lorsque l'utilisateur aura cliquer 2 fois, alors on essaye de placer le bateaux dans les cases correspondantes (case 1, pour la case
        #de début, case 2 en guise de direction du bateau)
        elif len(shipPos)==4 and shipLeng <= 5:
            res  = placement(shipLeng,shipIdPlayer, 1)
            shipPos = []
            if res != -1:
                tmp = tmp -1
        

def placement(shipLength, shipId, instance):

    ship = []
    tab = []
    error = []

    if instance == 0:
        #Ordinateur               
        tab = computerTab
        
        x = randint(0, COLUMNS-1)
        y = randint(0, LINES-1)       
        direction = randint(1,4)
        
    else:
        tab = player1Tab
        print("Le joueur 1 remplit sa grille")
        x = shipPos[0]
        y = shipPos[1]
        if UneCase == False:
            x2 = shipPos[2]
            y2 = shipPos[3]
            if y2 == y - 1 and x2 == x:
                direction = 1
            elif y2 == y + 1 and x2 == x:
                direction = 2
            elif y2 == y and x2 == x - 1:
                direction = 3
            elif y2 == y and x2 == x + 1:
                direction = 4
            else:
                direction = -1
        else:
            direction = 5

    ship.append(str(x) + " " + str(y))
    if instance == 1:
            if tab[x][y] != 0:
                error.append(-1)
    
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
        elif direction == 5:
            print()
        else:
            return -1
        
        #Case occupée => on sort de la fonction
        try:
            if tab[x][y] != 0:
                return -1
        except:
            return -1
        if instance == 1:
            if tab[x][y] != 0:
                error.append(-1)

    if len(error)==0:
        print(ship, shipId, shipLength)
        #Toutes les positions sont OK
        for case in range(len(ship)):
            t = ship[case].split(" ")
            print(t, COLUMNS,LINES, direction)
            tab[int(t[0])][int(t[1])] = shipId
        return 0
    else:
        return -1
                        
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


def new_game(isSolo):
    print("Création d'une nouvelle partie...")
    
    global LINES, COLUMNS, NUMBER_SHIPS_PER_LENGTH, player1Tab, computerTab, tmp, MODE
    global TAILLE_CASE_X, TAILLE_CASE_Y

    MODE = isSolo

    #Paramètres non modifiés => On prend ceux par défaut
    if LINES == 0:
        LINES = deepcopy(NUMBER_DEFAULT_LINES)
    if COLUMNS == 0:
        COLUMNS = deepcopy(NUMBER_DEFAULT_COLUMNS)
    if len(NUMBER_SHIPS_PER_LENGTH) == 0:
        NUMBER_SHIPS_PER_LENGTH = deepcopy(NUMBER_DEFAULT_SHIPS_PER_LENGTH)

    tmp = deepcopy(NUMBER_SHIPS_PER_LENGTH[shipLeng]) #nombre de bateaux utilisé dans la fonction qui est activée lorsqu'on clic droit sur le canvas de l'utilisateur lors du placement des bateaux (dans xyPos)

    #Taille d'une case à l'horizontal et vertical
    TAILLE_CASE_X = SIZE_X / COLUMNS
    TAILLE_CASE_Y = SIZE_Y / LINES
    
    draw_grid()
    
    print("[1/3] Initialisation de la grille du joueur 1")
    
    #Création et initialisation de la grille du joueur 1
    player1Tab = [0]*COLUMNS
    for _ in range(COLUMNS):
        player1Tab[_] = [0]*LINES

    print("[2/3] Initialisation de la grille de l'ordinateur")
        
    #Création et initialisation de la grille de l'ordinateur      
    computerTab = [0]*COLUMNS
    for _ in range(COLUMNS):
        computerTab[_] = [0]*LINES
    init_grid(0)


def changeParametres():
    global LINES, COLUMNS
    LINES = int(lignesE.get())
    COLUMNS = int(colonesE.get())

def parameters():
    para = Tk()
    para.title("Paramètres")
    para.geometry("370x350+300+200")
    para.resizable(False, False)

    global colonesE,lignesE

    #Création d'élèments
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
    #Bouton de validation / confirmation
    appliquer.grid(row = 13, column = 0, padx = 150, sticky = W)
    confirmer.grid(row = 13, column = 0, padx = 250)

    
    
    para.mainloop()

def informations():
    #TODO
    print()

def callback():
    if messagebox.askokcancel("Quit", "Voulez-vous vraiment quitter?"):
        window.destroy()

def main_menu():
    global window
    window = Tk()
    window.title("Bataille Navale")
    window.geometry("1280x700")

    menu = Menu(window)

    menu1 = Menu(menu, tearoff=0)
    menu.add_cascade(label="Partie", menu=menu1)

    menu1bis = Menu(menu1, tearoff=0)
    menu1.add_cascade(label="Nouvelle Partie", menu=menu1bis)
    menu1bis.add_command(label="1 joueur", command=lambda: new_game(0))
    menu1bis.add_command(label="2 joueurs", command=lambda: new_game(1))   
    #menu1.add_command(label="Continuer Partie", command=continue_game)

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
