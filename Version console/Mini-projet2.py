import os
import time
import random

NombreMaxLignes = 26
NombreMinLignes = 5
NombreLignesDefaut = 10
NombreMaxColones = 26
NombreMinColones = 5
NombreColonesDefaut = 10
Lignes = 0
Colones = 0
BatauxAutorisésParTaille = 8
TailleBateaux = {1:0, 2:1, 3:2, 4:1, 5:1}
Coordonnes = {}
JeuJoueur=[]
JeuOrdinateur=[]
BateauxJoueur = []
BateauxOrdinateur = []
alfabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

#On regarde si ce que l'utilisateur nous donne est bien un nombre entier. Sinon, on lui redemande la valeur
def demandeNombre(message, DoitEtrePositif, MaxBateaux):
    nombre=0
    while True:
        nombre = input(message)
        try:
            int(nombre)
            break
        except ValueError:
            print("Erreur : Ceci n'est pas un nombre entier. Veuiller réessayer...\n")
    if DoitEtrePositif == True and int(nombre)<0:
        print("Le nombre doit ętre positif. Veuillez réessayer...\n")
        demandeNombre(message, DoitEtrePositif, MaxBateaux)
    if MaxBateaux == True and int(nombre) > BatauxAutorisésParTaille:
        print("Le nombre de bateaux entré est au nombre de bateaux autorisés. Veuillez réessayer...\n")
        demandeNombre(message, DoitEtrePositif, MaxBateaux)
    return int(nombre)

#L'utilisateur choisi de changer la taille du jeu, le nombre de bateaux par chaque taille et si l'odinateur doit avoir une plus grande intélligence
def paramètre():
    print("La taille du tableau que vous voullez qui soit entre",NombreMinLignes,"et",NombreMaxLignes,"pour les lignes et",NombreMinColones,"et",NombreMaxColones,"pour les colones.")
    print("Ces valeurs sont compris dans l'interval que vous pouvez choisir.")
    global Lignes,Colones
    #Demande le nombre de lignes du jeu dans l'interval [NombreMinLignes;NombreMaxLignes]
    while Lignes < NombreMinLignes or Lignes > NombreMaxLignes:
        Lignes = demandeNombre("Donnez le nombre de lignes dans votre tableau : ",True,False)
        if Lignes < NombreMinLignes or Lignes > NombreMaxLignes:
            print("Le nombre de lignes imposés n'est pas dans l'interval",NombreMinLignes,"et",NombreMaxLignes)
            print("Veuillez réessayer\n")      
    #Demande le nombre de colones du jeu dans l'interval [NombreMinColones;NombreMaxColones]
    while Colones < NombreMinColones or Colones > NombreMaxColones:
        Colones = demandeNombre("Donnez le nombre de Colones dans votre tableau : ",True,False)
        if Colones < NombreMinColones or Colones > NombreMaxColones:
            print("Le nombre de Colones imposés n'est pas dans l'interval",NombreMinColones,"et",NombreMaxColones)
            print("Veuillez réessayer\n")
    #Demande le nombre de bateaux par taille
    TailleJeu=Lignes*Colones
    def demandeBateaux():
        global TailleBateaux
        total=0
        print("Attention, les bateaux ne peuvent pas prendre plus de place que la taille du jeu divisée par 4 et il faut un minimum 1 bateau de 1 case. ",end='')
        print("De plus, il ne faut pas que le nombre de bateaux par taille dépasse",BatauxAutorisésParTaille,".\n")
        for i in TailleBateaux:
            message = "Veuillez choisir le nombre de bateaux de taille " + str(i)+ " : "
            TailleBateaux[i] = demandeNombre(message,True,True)
        for t in TailleBateaux:
            total=total+TailleBateaux[t]*t
        if total > TailleJeu/4 or total < 1:
            print("Les rčgles n'ont pas été respectés, rappel des rčgles :")
            demandeBateaux()
    demandeBateaux()
    print("\nRetour au menu principale...\n")
    time.sleep(2)

#Conversion d'une position (ex. A2) en localisation dans le tableau de jeu (ex. 1 0)
def traduction(demande,coor):
    if demande == True:
        #Si on demande la position de l'utilisateur
        while True:
            emplacement = input("")
            try:
                a = Coordonnes[emplacement]
                break
            except:
                print("Cette case n'existe pas, veuillez réessayer...")
        tableau = Coordonnes[emplacement]
        valeur = tableau.split(" ")
        return valeur[0], valeur[1]
    else:
        #Conversion simple
        tableau = Coordonnes[coor]
        valeur = tableau.split(" ")
        return valeur[0], valeur[1]

def verificationEmplacements(direction,emplacement1,emplacement2,Joueur):
    #Vérifie l'existance d'une case dans le tableau du jeu
    def existe(emplacement1,emplacement2,Joueur):
        if Joueur == True:
            try:
                return JeuJoueur[emplacement1][emplacement2]
            except:
                return -1
        else:
            try:
                return JeuOrdinateur[emplacement1][emplacement2]
            except:
                return -1
    #Vérifie s'il n'y a pas de bateau
    def caseBateau(emplacement1,emplacement2,Joueur):
        if Joueur == True:
            if JeuJoueur[emplacement1][emplacement2] == 1:
                return True
            else:
                return False
        else:
            if JeuOrdinateur[emplacement1][emplacement2] == 1:
                return True
            else:
                return False
    #On essaye d'ajouter le bateau case par case
    def changement(direction,emplacement1,emplacement2,Joueur):
        var = cases - 1
        tout=emplacement1+" "+emplacement2+";"
        emplacement1 = int(emplacement1)
        emplacement2 = int(emplacement2)
        #Test si les cases vers le North sont libres et existantes (vers le haut)
        if direction == "N":
            while var != 0:
                var = var - 1
                emplacement2 = emplacement2 - 1
                ValeurTableau = existe(emplacement1,emplacement2,Joueur)
                if ValeurTableau == -1 or emplacement2 < 0 or caseBateau(emplacement1,emplacement2,Joueur):
                    return -1
                else:
                    tout = tout + str(emplacement1) +" "+ str(emplacement2)+";"
            return tout
        #Test si les cases vers le West sont libres et existantes (vers la droite)
        elif direction == "W":
            while var != 0:
                var = var - 1
                emplacement1 = emplacement1 - 1
                ValeurTableau = existe(emplacement1,emplacement2,Joueur)
                if ValeurTableau == -1 or emplacement1 < 0 or caseBateau(emplacement1,emplacement2,Joueur):
                    return -1
                else:
                    tout = tout + str(emplacement1) + " "+ str(emplacement2)+";"
            return tout
        #Test si les cases vers le Est sont libres et existantes (vers la gauche)
        elif direction == "E":
            while var != 0:
                var = var - 1
                emplacement1 = emplacement1 + 1
                ValeurTableau = existe(emplacement1,emplacement2,Joueur)
                if ValeurTableau == -1 or caseBateau(emplacement1,emplacement2,Joueur):
                    return -1
                else:
                    tout = tout + str(emplacement1) + " " + str(emplacement2)+";"
            return tout
        #Test si les cases vers le South sont libres et existantes (vers le bas)
        elif direction == "S":
            while var != 0:
                var = var - 1
                emplacement2 = emplacement2 + 1
                ValeurTableau = existe(emplacement1,emplacement2,Joueur)
                if ValeurTableau == -1 or caseBateau(emplacement1,emplacement2,Joueur):
                    return -1
                else:
                    tout = tout + str(emplacement1) + " " + str(emplacement2)+";"
            return tout
    def recupereCoordonneesBateau(direction,emplacement1,emplacement2,Joueur):
        #On récupčre toutes les coordonnées du bateau
        complets = changement(direction,emplacement1,emplacement2,Joueur)
        global BateauxJoueur, BateauxOrdinateur
        bateaux = ""
        if complets == -1:
            return complets
        else:
            #Ajout les coordonnees des bateaux de l'utilisateur dans un tableau en 1D
            coor = complets.split(";")
            for i in range(len(coor)-1):
                for t in Coordonnes:
                    if Coordonnes[t] == coor[i]:
                        bateaux = bateaux + str(t) + " "
            if Joueur==True:
                BateauxJoueur.append(bateaux)
            else:
                BateauxOrdinateur.append(bateaux)
            return 0
    return recupereCoordonneesBateau(direction,emplacement1,emplacement2,Joueur)                

def ecriture(joueur,loop):
    global JeuJoueur,JeuOrdinateur
    if joueur == True:
        #Demande l'emplacement initial du bateau a ajouter
        emplacement1,emplacement2 = traduction(True,"")
        if JeuJoueur[int(emplacement1)][int(emplacement2)] == 1:
            print("Sur cet emplacement il y a déjŕ un bateau, vous ne pouvez pas placer un bateau ici. Veuillez réessayer...")
            return -1
        else:
            choix = ""
            #Si le bateau fait une case, on ne demande pas la direction
            if cases == 1:
                choix == "N"
            else:
                #Demande la direction du positionnement du bateau
                print("Dans quelle direction voulez-vous placer votre bateau?")
                print("  N\nW   E\n  S")
                while choix != "N" and choix != "W" and choix != "E" and choix != "S":
                    choix = input("")
                    if choix != "N" and choix != "W" and choix != "E" and choix != "S":
                        print("Direction non correcte. Il est attendu une seule lettre (N/W/E/S)")
                        return -1
            resultat = verificationEmplacements(choix,emplacement1,emplacement2,True)
            if resultat == -1:
                print("Impossible de placer le bateau de",cases,"cases en direction",choix,". Veuillez trouvez un autre endroit ou une autre direction pour votre bateau...\n")
                return -1
        cas = BateauxJoueur[loop]
        valeurs = cas.split(" ")
        #Conversion puis placement des bateaux dans le tableau du jeu du joueur
        for i in range(len(valeurs)-1):
            val = valeurs[i]
            coor1,coor2 = traduction(False,val)
            JeuJoueur[int(coor1)][int(coor2)] = 1
        return 0
    else:
        x = random.randrange(1, Lignes + 1)
        y = random.randrange(1, Colones + 1)
        chou = random.randrange (1,4+1)
        coor = str(x)+" "+str(y)
        if chou==1:
            choix="N"
        elif chou==2:
            choix="W"
        elif chou==3:
            choix="E"
        elif chou== 4:
            choix="S"
        resultat = verificationEmplacements(choix,str(x),str(y),False)
        if resultat == -1:
            return -1
        else:
            cas = BateauxOrdinateur[loop]
            valeurs = cas.split(" ")
            #Conversion puis placement des bateaux dans le tableau du jeu du joueur
            for i in range(len(valeurs)-1):
                val = valeurs[i]
                coor1,coor2 = traduction(False,val)
                JeuOrdinateur[int(coor1)][int(coor2)] = 1
            return 0
        

def preparations():
    global JeuJoueur,JeuOrdinateur,Lignes,Colones,Coordonnes,cases,loop
    JeuJoueur=[]
    JeuOrdinateur=[]
    BateauxJoueur = []
    BateauxOrdinateur = []
    if Lignes == 0:
        Lignes = NombreLignesDefaut
    if Colones == 0:
        Colones = NombreColonesDefaut
    #Création des tableaux de jeux de l'utilisateur et de l'ordinateur
    JeuJoueur = [0]*Lignes
    for i in range(len(JeuJoueur)):
        JeuJoueur[i]=[0]*Colones
    JeuOrdinateur = [0]*Lignes
    for n in range(len(JeuOrdinateur)):
        JeuOrdinateur[n] = [0]*Colones
    #Création du dictionnaire de position
    for y in range(Lignes):
        for x in range(Colones):
            Coordonnes[alfabet[y]+str(x+1)] = str(x)+" "+str(y)
    #Demande d'insérer les bateaux dans les cases que l'utilisateur aura choisi
    cases=1
    loop=0
    for r in TailleBateaux:
        Constente = TailleBateaux[r]
        while Constente!=0:
            afficherJeu(True)
            test=-1
            while test == -1:
                print("Emplacement oů vous voulez placer votre bateau de ",str(cases)," case(s) : ",sep='',end='')
                test = ecriture(True,loop)
            loop = loop + 1
            Constente = Constente - 1
        cases = cases+1
    #Insertion des bateaux de l'ordinateur sur son jeu
    cases=1
    loop=0
    for r in TailleBateaux:
        Constente = TailleBateaux[r]
        while Constente!=0:
            test=-1
            while test == -1:
                test = ecriture(False,loop)
            loop = loop + 1
            Constente = Constente - 1
        cases = cases+1
        

def afficherJeu(preparation):
    os.system("cls")
    print("Joueur : \n")
    print("   ",sep='',end='')
    for i in range(Lignes):
        if i+1 < 10:
            print(i+1, "  ",sep='',end='')
        else:
            print(i+1, " ",sep='',end='')
    print(" ")
    for t in range(Colones):
        print(alfabet[t],sep='',end='')
        for h in range(Lignes):
            print("  ",sep='',end='')
            if JeuJoueur[h][t]==0:
                print(" ",sep='',end='')
            elif JeuJoueur[h][t]==1:
                print("B",sep='',end='')
            elif JeuJoueur[h][t]==2:
                print("X",sep='',end='')
            elif JeuJoueur[h][t]==3:
                print("C",sep='',end='')
        print("")
    if preparation != True:
        #Les nombres pour les colones de l'ordinateur
        print("\nOrdinateur : \n  ")
        print("   ",sep='',end='')
        for i in range(Lignes):
            if i+1 < 10:
                print(i+1, "  ",sep='',end='')
            else:
                print(i+1, " ",sep='',end='')
        print(" ")
        #Affiche les lettres pour les lignes de l'ordinateur
        for t in range(Colones):
            print(alfabet[t],sep='',end='')
            for h in range(Lignes):
                print("  ",sep='',end='')
                if JeuOrdinateur[h][t]==0:
                    print(" ",sep='',end='')
                elif JeuOrdinateur[h][t]==1: #Le temps du développement
                    print("B",sep='',end='')
                elif JeuOrdinateur[h][t]==2:
                    print("X",sep='',end='')
                elif JeuOrdinateur[h][t]==3:
                    print("C",sep='',end='')
            print("")

def commencerPartie():
    preparations()
    afficherJeu(False)
    os.system("Pause")
    
def main():
    os.system("cls")
    print("Bienvenue dans le menu principale de la bataille navale!")
    print("Tapez 1 pour commencer une partie")
    print("Tapez 2 pour changer les paramčtres du jeu")
    print("Tapez 3 pour quitter")
    choix = demandeNombre("",False,False)
    if choix >=1 and choix <=3:
        if choix == 1:
            commencerPartie()
        elif choix == 2:
            paramètre()
    if choix !=3:
        main()

main()
