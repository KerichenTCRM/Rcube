#!/usr/bin/python3
# Résolveur de Rubik's Cube

# Génération de modèle, pour les testes de bon fonctionnement.
def genCouleurs ():
    return ['w', 'b', 'o', 'v', 'r', 'j']

def genModeleResolu (couleurs):
    """Génère une chaine de caractère décrivant un cube résolut."""
    (W,B,O,V,R,J) = couleurs
    return ",".join([9*W,9*B,9*O,9*V,9*R,9*J])

def genModeleA (couleurs):
    """Génère une chaine de caractère décrivant un cube dont les deux premières couronnes sont résolut"""
    (W,B,O,V,R,J) = couleurs
    return ",".join([9*W,\
    6*B+J+B+R, 6*O+J+R+R, 6*V+B+O+O, 6*R+J+V+V,\
    B+J+O+J+J+J+J+J+V])
    
def genModeleB (couleurs):
    """Génère une chaine de caractère décrivant un cube particulier, mais non-résolut."""
    (W,B,O,V,R,J) = couleurs
    return ",".join([O+W+W+W+W+W+W+W+R,\
                     B+B+V+B+B+J+B+R+B, J+O+O+B+O+O+W+O+O, V+V+B+V+V+J+V+O+V, J+R+R+V+R+R+W+R+R,\
                                                                              R+J+J+B+J+V+J+J+O])
    
def genModeleC (couleurs):
    """Génère une chaine de caractère décrivant un cube particulier, mais non-résolut."""
    (W,B,O,V,R,J) = couleurs
    return ",".join([R+J+W+J+W+J+W+J+O,\
                     V+B+B+B+B+W+V+R+V, J+O+R+B+O+O+W+O+R, B+V+V+V+V+W+B+O+B, J+R+O+V+R+R+W+R+O,\
                                                                              O+W+J+B+J+V+J+W+R])

class Cube:
    #W = "w" # 0 # Dessus [W-J Axe 0]
    #B = "b" # 1 # En face [B-V Axe 1]
    #O = "o" # 2 # A droite [O-R Axe 2]
    #V = "v" # 3 # Derrière
    #R = "r" # 4 # A gauche
    #J = "j" # 5 # Dessous
        
    def __init__ (s, chaineU):
        
        ## Initialisation (pré-création) de valeurs temporaires:
        s.viSommets = [None]*8 # Nous pré-créons ces huit valeur, pour pouvoir les affecter
        s.viAretes = [None]*12 # plus facilement ensuite, en utilisant les indices 'L[i]' uniquement.
        # vi-* : Ces listes contiendronts la version 'VIsuel' des sommets et des arrets. (deux ou trois facettes)
        
        s.sommetsBlocALaPos = [None]*8 # Numero du bloc, en fonction de sa posistion.
        s.sommetsRoALaPos = [None]*8   # Rotation du bloc trouvé à la position.
        s.aretesBlocALaPos = [None]*12 #
        s.aretesRoALaPos = [None]*12   #
        
        s.sommetsPosDuBloc = [None]*8 # Position en fonction du numero de bloc.
        s.sommetsRoDuBloc = [None]*8  # Rotation, en fonction du numero de bloc.
        s.aretesPosDuBloc = [None]*12 # 
        s.aretesRoDuBloc = [None]*12  # 
        # Fin de la pré-création #
        
        ## Définition de valeur propres au cube donné par l'utilisateur.
        s.faces = chaineU.split(',')
        # La facette n°4 (le centre) définit la couleur de la face :
        s.couleurs = [ face[4] for face in s.faces ] # Le quatrième caractère est le centre de la face.
        (s.W, s.B, s.O, s.V, s.R, s.J) = s.couleurs # Nous affectons des noms spécifique à chaque couleur.
        (s.Wf, s.Bf, s.Of, s.Vf, s.Rf, s.Jf) = s.faces # Nous affectons aussi des nom à chaque face.
        s.valeurParCouleurSommet = { s.W: 0,
                                   s.J: 1,
                                   s.B: 0,
                                   s.V: 2,
                                   s.O: 0,
                                   s.R: 4}
        # [W-J:Axe 0: 1], [B-V:Axe 1: 2], [O-R:Axe 2: 4]
        s.valeurParCouleurArete = { s.W: 0, # Anneau du haut
                                  s.J: 8, # Anneau du bas
                                  s.B: 0, # \
                                  s.O: 1, # . Parcours de l'anneau
                                  s.V: 2, # . du milieu.
                                  s.R: 3} # /
        
        s.couronneHaut = ''.join([ strg[0:3] for strg in s.faces[1:5]]) # On récupère les couronnes à différentes hauteurs
        s.couronneMil  = ''.join([ strg[3:6] for strg in s.faces[1:5]]) # Ceci facilitera l'identification ensuite.
        s.couronneBas  = ''.join([ strg[6:9] for strg in s.faces[1:5]])
        # Notion d'anneau (haut et bas) coresspond à une lecture particulière des faces :
        # 5 4 3
        # 6 . 2 - Face du haut, numérotation de l'anneau,    # 0 1 2
        # 7 0 1                 != Numérotation de la face : # 3 . 5
        # . . .                                              # 6 7 8
        # . . .
        # . . .                                                # 2 5 8
        # 7 0 1                 != Numérotation de la face :   # 1 . 7
        # 6 . 2 - Face du bas, numérotation de l'anneu (aussi) # 0 3 6
        # 5 4 3
        # Code correspondant:
        Wf,Jf = s.Wf, s.Jf
        s.anneauHaut   = ''.join([ Wf[7:9], Wf[5], Wf[0:3][::-1], Wf[3], Wf[6]])
        s.anneauBas    = ''.join([ Jf[5], Jf[8:5:-1], Jf[3], Jf[0:3]])
        s.modeleResolu = genModeleResolu(s.couleurs) # Nous intégrons trois modèles, pour les testes
        s.modeleA = genModeleA(s.couleurs) # ~
        s.modeleB = genModeleB(s.couleurs) # ~
        s.modeleC = genModeleC(s.couleurs) # ~
        
        s.quarterSommet = [[(0,4),(4,6),(6,2),(2,0)],
                           [(0,1),(1,5),(5,4),(4,0)],
                           [(0,2),(1,0),(3,1),(2,3)],
                           [(6,7),(7,3),(3,2),(2,6)],
                           [(4,5),(5,7),(7,6),(6,4)],
                           [(5,1),(1,3),(3,7),(7,5)]] # Les changements de position de type (oldPos,newPos) des Sommets
        s.quarterArete = [[(0,3),(3,2),(2,1),(1,0)],
                          [(0,4),(4,8),(8,7),(7,0)],
                          [(1,5),(4,1),(9,4),(5,9)],
                          [(2,6),(6,10),(10,5),(5,2)],
                          [(3,7),(7,11),(11,6),(6,3)],
                          [(11,8),(8,9),(9,10),(10,11)]] # Les changements de position de type (oldPos,newPos) des Aretes
    
    def identifieSommet (s,bloc3f):
        """ Caractérise un sommet du cube, à partir de trois couleurs d'un bloc.""" 
        # bloc3f contient trois couleurs: trois facettes
        # Identifions la rotation du sommet:
        rotation = 3
        for i,x in enumerate(bloc3f): 
            if x == s.W or x == s.J:
                rotation = i
        if rotation == 3:
            return "Erreur de sommet dans la description du cube"
        # Calculons le numero (entre 0 et 7) du sommet:
        num = sum([ s.valeurParCouleurSommet[x]  for x in bloc3f ])
        return (num,rotation)

# Numérotation arbitraire des arêtes:
# . 2 .                   
# 3 W 1                   
# . 0 .                   
# . 0 . . 1 . . 2 . . 3 . 
# 7 B 4 4 O 5 5 V 6 6 R 7 
# . 8 . . 9 . . A . . B . 
#                   . B . 
# [A = 10]          A J 8 
# [B = 11]          . 9 . 
    def identifieArete (s,bloc2f):
        """ Caractérise une arête du cube, à partir de deux couleurs d'un bloc."""
        # bloc2f contient deux couleurs: deux facettes
        # Identifions le numero du bloc:
        num = 12
        if s.W in bloc2f or s.J in bloc2f: # Cas simple: l'arrète contient du blanc ou du jaune.
            num = sum([ s.valeurParCouleurArete[x] for x in bloc2f ])
        elif s.B in bloc2f: # Sinon, cas complexe: on se trouve sur l'anneau du milieu
            if s.O in bloc2f:
                num = 4
            elif s.R in bloc2f:
                num = 7
        elif s.V in bloc2f:
            if s.O in bloc2f:
                num = 5
            elif s.R in bloc2f:
                num = 6
        if num == 12:
            return "Erreur d'arête dans la description du cube"
        # Identifions maintenant la rotation de l'arête:
        rotation = 2
        for i,x in enumerate(bloc2f):
            if x == s.W or x == s.J: # Verification de la couleur de la facette.
                rotation = i # Si une des deux facettes correspond, on le retient.
        if rotation == 2: # Si on a pas pu determiner la rotation, on utilise le bleu-vert:
            for i,x in enumerate(bloc2f):
                if x == s.B or x == s.V:
                    rotation = i
        if rotation == 2: # Si la rotation n'est toujours pas déterminée, c'est qu'il y a une erreur.
            return "Erreur d'arête dans la description du cube"
        return (num,rotation)


# Le regroupement des sommets et des aretes:
# Pour les SOMMETS :      # Pour les ARRETES :
#        CECI :           #        CECI :           
# 0 . 2                   # . 1 .                   
# . W .                   # 3 W 5                   
# 6 . 8                   # . 7 .                   
# 0 . 2 0 . 2 0 . 2 0 . 2 # . 1 . . 1 . . 1 . . 1 . 
# . B . . O . . V . . R . # 3 B 5 3 O 5 3 V 5 3 R 5 
# 6 . 8 6 . 8 6 . 8 6 . 8 # . 7 . . 7 . . 7 . . 7 . 
#                   0 . 2 #                   . 1 . 
#                   . J . #                   3 J 5 
#                   6 . 8 #                   . 7 . 
#      DOIT DEVENIR :     #      DOIT DEVENIR :     
# 6 . 2                   # . 2 .                   
# . W .                   # 3 W 1                   
# 4 . 0                   # . 0 .                   
# 4 . 0 0 . 2 2 . 6 6 . 4 # . 0 . . 1 . . 2 . . 3 . 
# . B . . O . . V . . R . # 7 B 4 4 O 5 5 V 6 6 R 7 
# 5 . 1 1 . 3 3 . 7 7 . 5 # . 8 . . 9 . . A . . B . 
#                   7 . 5 #                   . B . 
#                   . J . # [A = 10]          A J 8 
#                   3 . 1 # [B = 11]          . 9 . 
# [J:1, V:2, R:4]

    def groupSommets (s):
        """Regroupe les facettes des sommets par 2, selon leur numéro, en vue de leur identification"""
        # On va remplire le tableau viSommets, avec les valeurs voulus.
        # On s'occupe des couches Haut et Bas en même temps.
        for i,x in enumerate([0,1,3,2]): # Pour chaque sommet...
            s.viSommets[2*i]   = (s.anneauHaut[2*x+1],
                                 s.couronneHaut[(3*x+3)%12],
                                 s.couronneHaut[(3*x+2)%12])
            s.viSommets[2*i+1] = (s.anneauBas[2*x+1],
                                 s.couronneBas[(3*x+2)%12],
                                 s.couronneBas[(3*x+3)%12])

    def groupAretes (s):
        """Regroupe les facettes des arêtes par 2, selon leur numéro, en vue de leur identification"""
        # On va remplire le tableau viAretes, avec les valeurs voulus.
        # Les quatres premières et quatre dernières arêtes de la liste peuvent s'identifier ainsi :
        for x in range(4):
            s.viAretes[x]   = (s.anneauHaut[2*x],s.couronneHaut[3*x+1])
            s.viAretes[8+x] = (s.anneauBas[2*x],s.couronneBas[3*x+1])
        # Les arêtes suivantes sont identifiées manuellement :
        s.viAretes[4] = tuple(s.couronneMil[2:4])
        s.viAretes[5] = (s.couronneMil[6],s.couronneMil[5])
        s.viAretes[6] = tuple(s.couronneMil[8:10])
        s.viAretes[7] = (s.couronneMil[0],s.couronneMil[11])
    
    def mapSommets (s):
        """Utilise la liste s.viSommet et la methode s.identifieSommet pour générer la double indexation position-bloc des sommets du cube. (Génère les listes s.sommetsBloc et s.sommetsPos)"""
        # Remarque: s.viSommets indexe les BLOCS trouvés, pour chaque POSITION
        for pos,sommet in enumerate(s.viSommets):
            (bloc_lu, rot) = s.identifieSommet(sommet)
            s.sommetsBlocALaPos[pos] = bloc_lu # A chaque position, on associe l'sommet correspondante
            s.sommetsRoALaPos[pos] = rot
            s.sommetsPosDuBloc[bloc_lu] = pos # A chaque sommet, on associe la position corespondante
            s.sommetsRoDuBloc[bloc_lu] = rot
        
    def mapAretes (s):
        """Utilise la liste s.viArete et la methode s.identifieArete pour générer la double indexation position-bloc des aretes du cube. (Génère les listes s.aretesBloc et s.aretesPos)"""
        # Remarque: s.viAretes indexe les BLOCS trouvés, pour chaque POSITION
        for pos,arete in enumerate(s.viAretes):
            (bloc_lu, rot) = s.identifieArete(arete)
            s.aretesBlocALaPos[pos] = bloc_lu # A chaque position, on associe l'arête correspondante
            s.aretesRoALaPos[pos] = rot
            s.aretesPosDuBloc[bloc_lu] = pos # A chaque arête, on associe la position corespondante
            s.aretesRoDuBloc[bloc_lu] = rot
