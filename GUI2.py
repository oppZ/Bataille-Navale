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

#Taille en pixel de la grille
SIZE_X = 460
SIZE_Y = 460

LINES = 0 #Taille de la grille (verticalement)
COLUMNS = 0 #Taille de la grille (horizontalement)

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

NUMBER_DEFAULT_SHIPS_PER_LENGTH = {1:0, 2:1, 3:2, 4:1, 5:1} 
NUMBER_SHIPS_PER_LENGTH = {}
MAX_SHIPS_PER_LENGTH = 8

MODE = 0 #0 pour SOLO / 1 pour MULTI

IMGS_TAB = [] #Tableau des images

#g
shipPos = []
shipLen = 1

#Event clic pour placement
def xyPos(event):
    global placeJoueur, passage
    if playerPlace:
        global shipPos,UneCase, nbBoats, shipLeng
        UneCase = False
        reponse = 0
        
        #Si on a placé tous les bateaux d'une même taille, alors on récupère le nombre de bateaux à placer
        while nbBoats == 0:
            shipLen = shipLen + 1
            try:
                nbBoats = NUMBER_SHIPS_PER_LENGTH[shipLen]
            except:
                #Le joueur ne doit plus placer ses bateaux
                playerPlace = False
                
        #On récupère les positions de x y sur le canvas, puis on calcul la case correspondante
        eventX = event.x
        eventY = event.y
        shipPos.append(ceil(eventX/TAILLE_CASE_X)-1)
        shipPos.append(ceil(eventY/TAILLE_CASE_Y)-1)
        #Si un bateau a une seule case, alors dès le début on place le bateau si possible
        if shipLen == 1:
            UneCase = True
            if placement(shipLeng,shipIdPlayer, 1) != -1:
                nbBoats = nbBoats -1
        #Lorsque l'utilisateur aura cliquer 2 fois, alors on essaye de placer le bateaux dans les cases correspondantes (case 1, pour la case
        #de début, case 2 en guise de direction du bateau)
        elif len(shipPos)==4 and shipLeng <= 5:
            reponse  = placement(shipLeng,shipIdPlayer, 1)
            shipPos = []
            if reponse != -1:
                tmp = tmp -1
        if shipLeng == 5 and tmp == 0:
            placeJoueur = False
    else:
        if passage == False:
            computerGrid.bind("<Button-1>", jeu)
            messagebox.showinfo("Bataille navale", "Vous avez terminé de placer vos bateaux. Vous pouvez commencer ŕ jouer !")
            computerGrid.config(cursor = "target")
            passage = True
            #shipIdPlayer = 1
            shipLeng = 1
    return

'''
Création des grilles du joueur
et de l'ordinateur
TODO : DONE
'''
def create_grids():
    global computerGrid, playerGrid
    global IMGS_TAB
    
    #Rangement des images dans le tableau
    imgTab.append(PhotoImage(file ="unknown.png"))
    imgTab.append(PhotoImage(file = "sea.png"))
    imgTab.append(PhotoImage(file = "ship.png"))
    imgTab.append(PhotoImage(file = "destroyedShip.png"))
    
    #Titres
    cTitle = Label(window, text = "Grille de l'ordinateur")
    pTitle = Label(window, text = "Grille du joueur")
    
    #Taille du titre
    cTitle.configure(font='Helvetica 18 bold')
    tTitle.configure(font='Helvetica 18 bold')
    
    #Création de canvas
    computerGrid = Canvas(window, bg = "white", width = SIZE_X, height = SIZE_Y)
    playerGrid = Canvas(window, bg = "white", width = SIZE_X, height = SIZE_Y)

    gridToPlace = playerGrid.bind( "<Button-1>", xyPos)

    #Positionnement des titres et des canvas
    computerGrid.grid(row = 1, column = 0, padx = 60, pady = 25)
    playerGrid.grid(row = 1, column = 1, padx = 150)
    cTitle.grid(row = 0, column = 0)
    pTitle.grid(row = 0, column = 1, padx = 80)

    #Contour des canvas
    computerGrid.create_line(3,3,SIZE_X,3, width=2)
    computerGrid.create_line(SIZE_X,3,SIZE_X,SIZE_Y, width=2)
    computerGrid.create_line(SIZE_X,SIZE_Y,3,SIZE_Y, width=2)
    computerGrid.create_line(3,SIZE_Y,3,3, width=2)

    playerGrid.create_line(3,3,SIZE_X,3, width=2)
    playerGrid.create_line(SIZE_X,2,SIZE_X,SIZE_Y, width=2)
    playerGrid.create_line(SIZE_X,SIZE_Y,2,SIZE_Y, width=2)
    playerGrid.create_line(3,SIZE_Y,3,3, width=2)

    #Création de lignes sur les canvas de l'ordinateur et de l'utilisateur
    for y in range(LINES):
        for x in range(COLUMNS):
            divC = SIZE_X/COLUMNS
            divL = SIZE_Y/LINES
            X = int(divC*x) 
            Y = int(divL*y)
            
            #Création du quadrillage
            computerGrid.create_line(X, 0, X, SIZE_X, width=1)
            computerGrid.create_line(0, Y, SIZE_Y, Y, width=1)
            playerGrid.create_line(X, 0, X, SIZE_X, width=1)
            playerGrid.create_line(0, Y, SIZE_Y, Y, width=1)
  
            caseX = TAILLE_CASE_X*x + TAILLE_CASE_X/2
            caseY = TAILLE_CASE_Y*y + TAILLE_CASE_Y/2
            
            #Ajout d'images "case inconnue" sur la grille de l'ordinateur
            computerGrid.create_image(caseX, caseY, image = IMGS_TAB[0])
            #Ajout d'images "mer" sur la grille du joueur
            playerGrid.create_image(caseX, caseY, image = IMGS_TAB[1])
    return
        
'''
Placement d'un bateau
instance :
  0 : Ordinateur
  1 : Joueur 1
'''
def placement(shipLength, shipId, instance):
    ship = []
    tab = [] #Tableau de l'instance

    if instance == 0:
        #Ordinateur               
        tab = computerTab
        
        x = randint(0, COLUMNS-1)
        y = randint(0, LINES-1)       
        direction = randint(1,4)
        
    else:
        #Joueur
        tab = player1Tab
        print("Le joueur 1 remplit sa grille")
        #On récupère les coordonnées récupèrées par xyPos()
        x = shipPos[0]
        y = shipPos[1]
        '''
        g
        '''
        if UneCase == False:
            x2 = shipPos[2]
            y2 = shipPos[3]
            #On cherche la direction
            if y2 == y - 1 and x2 == x:
                direction = 1
            elif y2 == y + 1 and x2 == x:
                direction = 2
            elif y2 == y and x2 == x - 1:
                direction = 3
            elif y2 == y and x2 == x + 1:
                direction = 4
            else:
                return -1
        else:
            direction = 5

    ship.append(str(x) + " " + str(y))

    #Pour chaque case, on calcul les x y suivants en fonction de la direction
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
        elif direction == 5:
            print()
        else:
            return -1
        
        #Test si la position existe
        try:
            #Case occupée => on sort de la fonction
            if tab[x][y] != 0:
                return -1
        except:
            return -1

    #Toutes les positions sont OK
    for case in range(len(ship)):
        xy = ship[case].split(" ")
        print(xy, COLUMNS,LINES, direction) #DEV
        #Si le joueur place ses bateaux, alors on place l'image imageCaseShip
        if instance == 1:
            playerGrid.create_image(int(xy[0])*TAILLE_CASE_X + TAILLE_CASE_X / 2, int(xy[1])*TAILLE_CASE_Y + TAILLE_CASE_Y / 2, image = IMGS_TAB[2])
        
        tab[int(xy[0])][int(xy[1])] = shipId
    return 0

'''
Création d'une nouvelle partie
'''
def new_game():
    global LINES, COLUMNS, NUMBER_SHIPS_PER_LENGTH
    global player1Tab, computerTab #Tableaux des grilles du joueur et de l'ordinateur
    global TAILLE_CASE_X, TAILLE_CASE_Y, placeJoueur, passage, shipIdPlayer
    global nbBoats #Nombre de bateaux d'une taille donnée
    global playerPlace #Le joueur place t-il ses bateaux ?
    
    #Tableaux pour les grilles du joueur 1 et de l'ordinateur
    player1Tab = []
    computerTab = []

    playerPlace = True
    passage = False

    shipIdPlayer = 1

    #Paramètres non modifiés => On prend ceux par défaut
    if LINES == 0:
        LINES = deepcopy(NUMBER_DEFAULT_LINES)
    if COLUMNS == 0:
        COLUMNS = deepcopy(NUMBER_DEFAULT_COLUMNS)
    if len(NUMBER_SHIPS_PER_LENGTH) == 0:
        NUMBER_SHIPS_PER_LENGTH = deepcopy(NUMBER_DEFAULT_SHIPS_PER_LENGTH)

    nbBoats = deepcopy(NUMBER_SHIPS_PER_LENGTH[shipLen])

    #Taille d'une case horizontalement et verticalement
    TAILLE_CASE_X = SIZE_X / COLUMNS
    TAILLE_CASE_Y = SIZE_Y / LINES
    
    #Création et initialisation de la grille du joueur 1
    player1Tab = [0]*COLUMNS
    for _ in range(COLUMNS):
        player1Tab[_] = [0]*LINES
        
    #Création et initialisation de la grille de l'ordinateur      
    computerTab = [0]*COLUMNS
    for _ in range(COLUMNS):
        computerTab[_] = [0]*LINES

    shipId = 1
    #Pour chaque longueur de bateau
    for shipLength in NUMBER_SHIPS_PER_LENGTH:
        #Pour chaque bateau de longueur shipLength
        for ship in range(NUMBER_SHIPS_PER_LENGTH[shipLength]):
            result = -1
            #Tant que la fonction retourne une erreur
            while result == -1 and NUMBER_SHIPS_PER_LENGTH[shipLength] != 0:                
                result = placement(shipLength, shipId, 0)
                #S'il n'y a pas eu d'erreur, on incrémente l'id du bateau
                if result != -1:
                    shipId = shipId + 1

    #Création des grilles du joueur et de l'ordinateur
    create_grids()

'''
def jeu(event):
    #Récupération des x y de la sourie dans la grille de l'orinateur  
    caseX = floor(event.x / TAILLE_CASE_X)
    caseY = floor(event.y / TAILLE_CASE_Y)
    #Calcul des x y correspondant pour pouvoir afficher l'image centré dans une case
    x = caseX * TAILLE_CASE_X + TAILLE_CASE_X /2
    y = caseY * TAILLE_CASE_Y + TAILLE_CASE_Y / 2
    if (computerTab[caseX][caseY] > 0):
        drawingComputer.create_image(x, y, image=imageCaseShip)
    elif (computerTab[caseX][caseY] == 0):
        drawingComputer.create_image(x, y, image=imageCaseMer)
'''

'''
Application des paramètres
TODO : -Prendre en compte la modification des tailles de bateaux
'''
def change_settings():
    global LINES, COLUMNS
    LINES = int(lignesE.get())
    COLUMNS = int(colonesE.get())
    
'''
Menu "Paramètres"
TODO : -Changer les noms des variables
       -Depop la fenêtre quand on clique sur confirmer
'''
def settings():
    settings = Tk()
    settings.title("Paramètres")
    settings.geometry("370x350+300+200")
    settings.resizable(False, False)

    global colonesE,lignesE

    #Création d'élèments
    bienvenue = Label(settings, text='Paramètres du jeu\n')
    colones = Label(settings, text='Nombre de colonnes :')
    lignes = Label(settings, text='Nombre de lignes :')
    colonesE = Spinbox(settings, from_=NUMBER_MIN_COLUMNS, to=NUMBER_MAX_COLUMNS, width=3)
    lignesE = Spinbox(settings, from_=NUMBER_MIN_LINES, to=NUMBER_MAX_LINES, width=3)
    #width, height

    taille = Label(settings, text='\nLe nombre de bateaux par taille\n')
    case1 = Label(settings, text='1 case(s) :')
    case2 = Label(settings, text='2 case(s) :')
    case3 = Label(settings, text='3 case(s) :')
    case4 = Label(settings, text='4 case(s) :')
    case5 = Label(settings, text='5 case(s) :')
    case6 = Label(settings, text=' ')
    act = Label(settings, text = 'Actuellement :')
    
    case1E = Spinbox(settings, from_=0, to=MAX_SHIPS_PER_LENGTH, width=3)
    case2E = Spinbox(settings, from_=0, to=MAX_SHIPS_PER_LENGTH, width=3)
    case3E = Spinbox(settings, from_=0, to=MAX_SHIPS_PER_LENGTH, width=3)
    case4E = Spinbox(settings, from_=0, to=MAX_SHIPS_PER_LENGTH, width=3)
    case5E = Spinbox(settings, from_=0, to=MAX_SHIPS_PER_LENGTH, width=3)
    appliquer = ttk.Button(settings, text= 'Appliquer', command = change_settings)
    confirmer = ttk.Button(settings, text = 'Confirmer', command = main_menu)
    
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
  
    settings.mainloop()

'''
Menu "A propos"
TODO : ALL
'''
def informations():
    print()

'''
Confirmation lors du clic du boutton "Quitter"
TODO : DONE
'''
def callback():
    if messagebox.askokcancel("Quit", "Voulez-vous vraiment quitter ?"):
        window.destroy()
'''
Menu principal
TODO : DONE
'''
def main_menu():
    global window
    
    window = Tk()
    window.title("Bataille Navale")
    window.geometry("1280x700")
    window.resizable(False, False)

    menu = Menu(window)

    menu1 = Menu(menu, tearoff=0)
    menu.add_cascade(label="Partie", menu=menu1)

    sub_menu1 = Menu(menu1, tearoff=0)
    menu1.add_cascade(label="Nouvelle Partie", menu=sub_menu1)
    sub_menu1.add_command(label="1 joueur", command=new_game)
    sub_menu1.add_command(label="2 joueurs", command=new_game)
    #menu1.add_command(label="Continuer Partie", command=continue_game)

    menu2 = Menu(menu, tearoff=0)
    menu.add_cascade(label="Options", menu=menu2)
    menu2.add_command(label="Configurer le jeu", command=settings)
    menu2.add_command(label="A propos", command=informations)
    menu2.add_separator()
    menu2.add_command(label="Quitter", command=callback)

    window.config(menu=menu)
    window.protocol("WM_DELETE_WINDOW", callback) 
    window.mainloop()

main_menu()