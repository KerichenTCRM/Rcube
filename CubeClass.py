#!/usr/bin/python3
# Cube solver

# Génération de modèle
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

class Cube:
    # Valeurs de la classe Cube (inutiles)
    W = "w" # 0 # Dessus [W-J Axe 0]
    B = "b" # 1 # En face [B-V Axe 1]
    O = "o" # 2 # A droite [O-R Axe 2]
    V = "v" # 3 # Derrière
    R = "r" # 4 # A gauche
    J = "j" # 5 # Dessous
    
    modeleResolu = genModeleResolu([W,B,O,V,R,J])
    modeleA = genModeleA([W,B,O,V,R,J])
    
    def __init__ (s, chaineU):
        s.faces = chaineU.split(',')
        # La facette n°4 (le centre) définit la couleur de la face :
        s.couleurs = [ face[4] for face in s.faces ]
        (s.W, s.B, s.O, s.V, s.R, s.J) = s.couleurs
        (s.Wf, s.Bf, s.Of, s.Vf, s.Rf, s.Jf) = s.faces
        s.sommets = [() for huit in range(8)]
        s.aretes = [() for douze in range(12)]
        s.couronneHaut = ''.join([ strg[0:3] for strg in s.faces[1:5]])
        s.couronneMil  = ''.join([ strg[3:6] for strg in s.faces[1:5]])
        s.couronneBas  = ''.join([ strg[6:9] for strg in s.faces[1:5]])
        Wf,Jf = s.Wf, s.Jf
        s.anneauHaut   = ''.join([Wf[7:9],Wf[5],Wf[3:0:-1],Wf[3],Wf[6]])
        s.anneauBas    = ''.join([Jf[5],Jf[9:6:-1],Jf[3],Jf[0:3]])
        s.modeleResolu = genModeleResolu(s.couleurs)
        s.modeleA = genModeleA(s.couleurs)

    
    valeurParCouleur = {W:0, B:0, O:0, J:1, V:2, R:4}
    # [W-J:Axe 0: 1], [B-V:Axe 1: 2], [O-R:Axe 2: 4]
    
    def identifieSommet (s,bloc3f):
        """ Caractérise un sommet du cube, à partir de trois couleurs d'un bloc."""
        # bloc3f contient trois couleurs: trois facettes
        # Identifions la rotation du sommet:
        rotation = 3
        for (i,x) in enumerate(bloc3f): 
            if x == s.W or x == s.J:
                rotation = i
        if rotation == 3:
            return "Erreur de sommet dans la description du cube"
        # Calculons le numero (entre 0 et 7) du sommet:
        num = sum([ valeurParCouleur[x]  for x in bloc3f ])
            

    def identifieArete (s,bloc2f):
        """ Caractérise une arête du cube, à partir de deux couleurs d'un bloc."""
        # bloc2f contient deux couleurs: deux facettes
        # Identifions la rotation de l'arête:
        rotation == 2
        
        for (i,x) in enumerate(bloc2f):
            if x == s.W or x == s.J: # Verification de la couleur de la facette.
                rotation = i # Si une des deux facettes correspond, on le retient.
                
        if rotation == 2: # Si on a pas pu determiner la rotation, on utilise le bleu-vert:
            for (i,x) in enumerate(bloc2f):
                if x == s.B or x == s.V:
                    rotation = i
                    
        if rotation == 2:
            return "Erreur d'arête dans la description du cube"



# Le regroupement des sommets et des aretes:
#        THIS :           #        THIS :           
# 0 . 2                   # . 1 .                   
# . W .                   # 3 W 5                   
# 6 . 8                   # . 7 .                   
# 0 . 2 0 . 2 0 . 2 0 . 2 # . 1 . . 1 . . 1 . . 1 . 
# . B . . O . . V . . R . # 3 B 5 3 O 5 3 V 5 3 R 5 
# 6 . 8 6 . 8 6 . 8 6 . 8 # . 7 . . 7 . . 7 . . 7 . 
#                   0 . 2 #                   . 1 . 
#                   . J . #                   3 J 5 
#                   6 . 8 #                   . 7 . 
#      SHALL BECOME :     #      SHALL BECOME :     
# 6 . 2                   # . 2 .                   
# . W .                   # 3 W 1                   
# 4 . 0                   # . 0 .                   
# 4 . 0 0 . 2 2 . 6 6 . 4 # . 0 . . 1 . . 2 . . 3 . 
# . B . . O . . V . . R . # 7 B 4 4 O 5 5 V 6 6 R 7 
# 5 . 1 1 . 3 3 . 7 7 . 5 # . 8 . . 9 . . A . . B . 
#                   7 . 5 #                   . B . 
#                   . J . #                   A J 8 
#                   3 . 1 #                   . 9 . 
# [J:1, V:2, R:4]

    def groupSommets (s):        
        # On s'occupe des couches Haut et Bat en même temps. 
        for i,x in enumerate([0,1,3,2]): # Pour chaque sommet...
            s.sommets[2*i]   = (s.anneauHaut[2*x],
                                 s.couronneHaut[(3*x+2)%12],
                                 s.couronneHaut[3*(x+1)%12])
            s.sommets[2*i+1] = (s.anneauBas[2*x],
                                 s.couronneBas[3*(x+1)%12],
                                 s.couronneBas[(3*x+2)%12])

    def groupAretes (s):
        for x in range(4):
            s.aretes[x]   = (s.anneauHaut[2*x],s.couronneHaut[3*x+1])
            s.aretes[8+x] = (s.anneauBas[2*x],s.couronneBas[3*x+1])
        s.aretes[4] = tuple(s.couronneMil[2:4])
        s.aretes[5] = (s.couronneMil[6],s.couronneMil[5])
        s.aretes[6] = tuple(s.couronneMil[8:10])
        s.aretes[7] = (s.couronneMil[0],s.couronneMil[11])
        
