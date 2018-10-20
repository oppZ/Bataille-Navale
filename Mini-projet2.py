import os
import time

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

def traduction(demande,coor):
    if demande == True:
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
        tableau = Coordonnes[coor]
        valeur = tableau.split(" ")
        return valeur[0], valeur[1]

def verificationEmplacements(direction,emplacement1,emplacement2,Joueur):
    global emplacements, complets
    emplacements = []
    def existe(emplacement1,emplacement2,Joueur):
        if Joueur == True:
            try:
                emplacements.append(emplacement1)
                emplacements.append(emplacement2)
                return JeuJoueur[emplacement1][emplacement2]
            except:
                return -1
        else:
            try:
                return JeuOrdinateur[emplacement1][emplacement2]
            except:
                return -1
    def changement(direction,emplacement1,emplacement2,Joueur):
        var = cases -1
        global tout
        tout=emplacement1+" "+emplacement2+";"
        if direction == "N":
            while var != 0:
                var = var -1
                emplacement2 = int(emplacement2) 
                emplacement2 = emplacement2 - 1
                ValeurTableau = existe(int(emplacement1),emplacement2,Joueur)
                if ValeurTableau == -1 or emplacement2 < 0:
                    return -1
                else:
                    tout = tout + str(emplacement1) +" "+ str(emplacement2)+";"
            return tout
        elif direction == "W":
            while var != 0:
                var = var -1
                emplacement1 = int(emplacement1) 
                emplacement1 = emplacement1 - 1
                ValeurTableau = existe(emplacement1,int(emplacement2),Joueur)
                if ValeurTableau == -1 or emplacement1 < 0:
                    return -1
                else:
                    tout = tout + str(emplacement1) + " "+ str(emplacement2)+";"
            return tout
        elif direction == "E":
            while var != 0:
                var = var -1
                emplacement1 = int(emplacement1) 
                emplacement1 = emplacement1 + 1
                ValeurTableau = existe(emplacement1,int(emplacement2),Joueur)
                if ValeurTableau == -1:
                    return -1
                else:
                    tout = tout + str(emplacement1) + " " + str(emplacement2)+";"
            return tout
        elif direction == "S":
            while var != 0:
                var = var -1
                emplacement2 = int(emplacement2) 
                emplacement2 = emplacement2 + 1
                ValeurTableau = existe(int(emplacement1),emplacement2,Joueur)
                if ValeurTableau == -1:
                    return -1
                else:
                    tout = tout + str(emplacement1) + " " + str(emplacement2)+";"
            return tout
    if Joueur == True:
        complets = changement(direction,emplacement1,emplacement2,Joueur)
        global BateauxJoueur
        bateaux=""
        if complets == -1:
            return complets
        else:
            coor = complets.split(";")
            for i in range(len(coor)-1):
                for t in Coordonnes:
                    if Coordonnes[t]==coor[i]:
                        bateaux = bateaux + str(t) + " "
            BateauxJoueur.append(bateaux)
            print(BateauxJoueur)
            os.system("pause")
                

def ecriture(joueur,loop):
    global JeuJoueur,JeuOrdinateur,coor1,coor2,cas,valeurs,val
    if joueur == True:
        resultat=-1
        while resultat == -1:
            emplacement1,emplacement2 = traduction(True,"")
            if JeuJoueur[int(emplacement1)][int(emplacement2)] == 1:
                print("Sur cet emplacement il y a déjŕ un bateau, vous ne pouvez pas placer un bateau ici. Veuillez réessayer...")
                ecriture(joueur,loop)
            else:
                choix =""
                print("Dans quelle direction voulez-vous placer votre bateau?")
                print("  N\nW   E\n  S")
                while choix != "N" and choix != "W" and choix != "E" and choix != "S":
                    choix = input("")
                    if choix != "N" and choix != "W" and choix != "E" and choix != "S":
                        print("Direction non correcte. Il est attendu une seule lettre (N/W/E/S)")
                resultat = verificationEmplacements(choix,emplacement1,emplacement2,True)
                if resultat == -1:
                    print("Impossible de placer le bateau de",cases,"cases en direction",choix,". Veuillez trouvez un autre endroit ou une autre direction pour votre bateau...\n")
                    ecriture(joueur,loop)
            cas = BateauxJoueur[loop]
            valeurs = cas.split(" ")
            for i in range(len(valeurs)-1):
                val = valeurs[i]
                coor1,coor2 = traduction(False,val)
                JeuJoueur[int(coor1)][int(coor2)] = 1

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
            print("Emplacement oů vous voulez placer votre bateau de ",str(cases)," case(s) : ",sep='',end='')
            ecriture(True,loop)
            loop = loop + 1
            Constente = Constente - 1
        cases = cases+1
            
        

def afficherJeu(preparation):
    #global JeuJoueur,JeuOrdinateur
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
            print(alfabet[t])
            for h in range(Lignes):
                print("  ",sep='',end='')
                if (JeuOrdinateur[h][t]==0):
                    print(" ",sep='',end='')
                elif JeuJoueur[h][t]==1:
                    print("B",sep='',end='')
                elif JeuOrdinateur[h][t]==2:
                    print("X",sep='',end='')
                elif JeuOrdinateur[h][t]==3:
                    print("C",sep='',end='')
    
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
