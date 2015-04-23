#!/usr/bin/python3
# Résolveur de Rubik's Cube

# Génération de modèle, pour les tests de bon fonctionnement.
def genCouleurs ():
    return ['w', 'b', 'o', 'v', 'r', 'j']

def genModeleResolu (couleurs):
    """Génère une chaîne de caractère décrivant un cube résolu."""
    (W,B,O,V,R,J) = couleurs
    return ",".join([9*W,9*B,9*O,9*V,9*R,9*J])

def genModeleA (couleurs):
    """Génère une chaîne de caractères décrivant un cube dont les deux premières couronnes sont résolues"""
    (W,B,O,V,R,J) = couleurs
    return ",".join([9*W,\
    6*B+J+B+R, 6*O+J+R+R, 6*V+B+O+O, 6*R+J+V+V,\
    B+J+O+J+J+J+J+J+V])
    
def genModeleB (couleurs):
    """Génère une chaîne de caractères décrivant un cube particulier, mais non résolu."""
    (W,B,O,V,R,J) = couleurs
    return ",".join([O+W+W+W+W+W+W+W+R,\
                     B+B+V+B+B+J+B+R+B, J+O+O+B+O+O+W+O+O, V+V+B+V+V+J+V+O+V, J+R+R+V+R+R+W+R+R,\
                                                                              R+J+J+B+J+V+J+J+O])
    
def genModeleC (couleurs):
    """Génère une chaîne de caractères décrivant un cube particulier, mais non résolu."""
    (W,B,O,V,R,J) = couleurs
    return ",".join([R+J+W+J+W+J+W+J+O,\
                     V+B+B+B+B+W+V+R+V, J+O+R+B+O+O+W+O+R, B+V+V+V+V+W+B+O+B, J+R+O+V+R+R+W+R+O,\
                                                                              O+W+J+B+J+V+J+W+R])

def genModeleEtape1 (couleurs): # Complètement mélangé
    """Génère une chaîne de caractères décrivant un cube juste avant l'étape 1"""
    (W,B,O,V,R,J) = couleurs
    return ",".join([J+R+V+W+W+O+W+B+J,\
                     O+W+B+J+B+W+R+V+W, R+B+J+R+O+V+V+R+V, R+B+O+J+V+J+J+V+W, B+O+B+O+R+B+R+O+B,\
                                                                              V+V+W+W+J+R+O+J+O])

def genModeleEtape7 (couleurs):
    """Génère une chaîne de caractères décrivant un cube juste avant l'étape 7"""
    (W,B,O,V,R,J) = couleurs
    return ",".join([W+W+W+W+W+W+W+W+W,\
                     B+B+B+B+B+B+R+B+O, O+O+O+O+O+O+J+O+O, V+V+V+V+V+V+V+V+V, R+R+R+R+R+R+R+R+J,\
                                                                              J+J+B+J+J+J+J+J+B])

class Cube:
    #W = "w" # 0 # Dessus [W-J Axe 0]
    #B = "b" # 1 # En face [B-V Axe 1]
    #O = "o" # 2 # A droite [O-R Axe 2]
    #V = "v" # 3 # Derrière
    #R = "r" # 4 # A gauche
    #J = "j" # 5 # Dessous
        
    def __init__ (s, chaineU):
        
        ### Initialisation (pré-création) de valeurs temporaires:
        s.viSommets = [None]*8 # Nous pré-créons ces huit valeur, pour pouvoir les affecter
        s.viAretes = [None]*12 # plus facilement ensuite, en utilisant les indices 'L[i]' uniquement.
        # vi-* : Ces listes contiendronts la version 'VIsuel' des sommets et des arêtes. (deux ou trois facettes)
        
        s.sommetsBlocALaPos = [None]*8 # Numéro du bloc, en fonction de sa position.
        s.sommetsRoALaPos = [None]*8   # Rotation du bloc trouvé à la position.
        s.aretesBlocALaPos = [None]*12 #
        s.aretesRoALaPos = [None]*12   #
        
        s.sommetsPosDuBloc = [None]*8 # Position en fonction du numéro de bloc.
        s.sommetsRoDuBloc = [None]*8  # Rotation, en fonction du numéro de bloc.
        s.aretesPosDuBloc = [None]*12 # 
        s.aretesRoDuBloc = [None]*12  # 
        # Fin de la pré-création #

        ### Initialilisation de la liste des mouvements : celle que renverra l'algorithme:
        s.listeDesMouvements = ""

        ### Données figées, éguales pour toutes les instances:
        s.sommetsPosParitee = [0,1,0,1,1,0,1,0]
        s.BOVR = [1,2,3,4]
        s.OVRB = [2,3,4,1]
        s.inf = float('inf')
        
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
        W = 0 ; B = 1 ; O = 2 ; V = 3 ; R = 4 ; J = 5
        s.v = (lambda a,b : 2**a+2**b) # v comme valeur
        v = s.v
        s.retrouverNumeroArete = {
        v(W,W): -1, v(W,B):  0, v(W,O):  1, v(W,V):  2, v(W,R):  3, v(W,J): -2, # Cas Blancs
        v(J,J): -1, v(J,B):  8, v(J,O):  9, v(J,V): 10, v(J,R): 11, # Cas Jaunes non-blancs
        v(B,O):  4, v(O,V):  5, v(V,R):  6, v(R,B):  7, # Cas de la `couronne_milieu`
        v(B,B): -1, v(O,O): -1, v(V,V): -1, v(R,R): -1, v(B,V): -2, v(O,R): -2 # Autres cas, les erreurs
        } # -1 est une erreur: deux fois la même couleur 
          # -2 est une erreur: couleurs de faces opposées
          # Remarque: nous sommes sur d'avoir énuméré toutes les possibilités, car
          # C(6;2) + C(6;1) = 6!/(2!*4!) + 6!/5! = (6*5/2) + 6 = 3*5 + 6 = 15 + 6 = 21
          # et nous avons bien 21 cas traités.


# Numérotation arbitraire des sommets et des arêtes:
# 2 . 1                    #  . 2 .                   
# . W .                    #  3 W 1                   
# 3 . 0                    #  . 0 .                   
# 3 . 0 0 . 1 1 . 2 2 . 3  #  . 0 . . 1 . . 2 . . 3 . 
# . B . . O . . V . . R .  #  7 B 4 4 O 5 5 V 6 6 R 7 
# 7 . 4 4 . 5 5 . 6 6 . 7  #  . 8 . . 9 . . A . . B . 
#                   6 . 7  #                    . B . 
#                   . J .  #   [A = 10]         A J 8 
#                   5 . 4  #   [B = 11]         . 9 . 
       # Tables de correspondance indiquant les positions dont les blocs vont bouger, ainsi que la nouvelle position associée.
        s.cyclesSommet = [[0,3,2,1], # Rotation de la face 0 : W : Blanche
                         [0,4,7,3], # 1: B : Bleu
                         [0,1,5,4], # 2: O
                         [1,2,6,5], # 3: V
                         [2,3,7,6], # 4: R
                         [4,5,6,7]] # 5: J
                         
        s.cyclesArete = [[0,3,2,1], # Rotation de la face 0 : W : Blanche
                        [0,4,8,7], # 1: B
                        [1,5,9,4], # 2: O
                        [2,6,10,5], # 3: V
                        [3,7,11,6], # 4: R
                        [11,8,9,10]] # 5: J
        
        
        ### Analyse de base des données de génération du cube (chaineU)
        s.faces = chaineU.split(',')
        
        # La facette n°4 (le centre) définit la couleur de la face :
        s.couleurs = [ face[4] for face in s.faces ]      # Le quatrième caractère est le centre de la face.
        (s.W, s.B, s.O, s.V, s.R, s.J) = s.couleurs       # Nous affectons des noms spécifique à chaque couleur.
        (s.Wf, s.Bf, s.Of, s.Vf, s.Rf, s.Jf) = s.faces    # Nous affectons aussi des noms à chaque face.
        s.numeroDeCouleur = { s.W: 0, s.B: 1, s.O: 2, s.V: 3, s.R: 4, s.J: 5} # Correspondance inverse couleur-nombre.
        ## Définition des tableaux anneauHaut, anneauBas, couronneHaut, couronneMil et couronneBas
        # Notion d'anneau (haut et bas) correspond à une lecture particulière des faces :
        # 5 4 3
        # 6 . 2 - Face du haut, numérotation de l'anneau,    # 0 1 2
        # 7 0 1                 != Numérotation de la face : # 3 . 5
        # . . .                                              # 6 7 8
        # . . .
        # . . .                                                 # 2 5 8
        # 7 0 1                  != Numérotation de la face :   # 1 . 7
        # 6 . 2 - Face du bas, numérotation de l'anneau (aussi) # 0 3 6
        # 5 4 3
        # Code correspondant:
        Wf,Jf = s.Wf, s.Jf
        s.anneauHaut   = ''.join([ Wf[7:9], Wf[5], Wf[0:3][::-1], Wf[3], Wf[6]])
        s.anneauBas    = ''.join([ Jf[5], Jf[8:5:-1], Jf[3], Jf[0:3]])
        s.couronneHaut = ''.join([ strg[0:3] for strg in s.faces[1:5]]) # On récupère les couronnes à différentes hauteurs.
        s.couronneMil  = ''.join([ strg[3:6] for strg in s.faces[1:5]]) # Ceci facilitera l'identification ensuite.
        s.couronneBas  = ''.join([ strg[6:9] for strg in s.faces[1:5]])
        
        s.groupSommets()
        s.groupAretes()
        s.mapSommets()
        s.mapAretes()
        
        # Fin de __init__
        #(FIN DE __init__!)
        
    def decrireCube (s):
        """Renvoie l'état du cube"""
        return "\n".join([
        "s.sommetsBlocALaPos = {}".format(s.sommetsBlocALaPos),
        "s.sommetsRoALaPos = {}".format(s.sommetsRoALaPos),
        "s.aretesBlocALaPos = {}".format(s.aretesBlocALaPos),
        "s.aretesRoALaPos = {}".format(s.aretesRoALaPos),
        
        #"s.sommetsPosDuBloc = {}".format(s.sommetsPosDuBloc),
        #"s.sommetsRoDuBloc = {}".format(s.sommetsRoDuBloc),
        #"s.aretesPosDuBloc = {}".format(s.aretesPosDuBloc),
        #"s.aretesRoDuBloc = {}".format(s.aretesRoDuBloc),
        ""
        ])
    
    def printCube (s):
        """Affiche l'état du cube"""
        print( s.decrireCube() )
    
    
# Numérotation arbitraire des sommets:
# 2 . 1                   
# . W .                   
# 3 . 0                   
# 3 . 0 0 . 1 1 . 2 2 . 3 
# . B . . O . . V . . R . 
# 7 . 4 4 . 5 5 . 6 6 . 7 
#                   6 . 7 
#                   . J . 
#                   5 . 4 
    def identifieSommet (s,bloc3f):
        """ Caractérise un sommet du cube, à partir de trois couleurs d'un bloc.""" 
        # bloc3f contient trois couleurs: trois facettes
        # Identifions la rotation du sommet:
        orientation = s.inf
        for i,x in enumerate(bloc3f): 
            if x == s.W or x == s.J:
                orientation = i
        # Calculons le numero (entre 0 et 7) du sommet:
        if s.O in bloc3f:
            if s.B in bloc3f:
                num = 0
            elif s.V in bloc3f:
                num = 1
            else:
                num = s.inf
        elif s.R in bloc3f:
            if s.B in bloc3f:
                num = 3
            elif s.V in bloc3f:
                num = 2
            else:
                num = s.inf
        else:
            num = s.inf

        num += 4*(s.J in bloc3f)
        # Ainsi:
        # Si bloc3f contient du blanc: 0 <= num < 4
        # Si bloc3f contient du jaune: 4 <= num < 8 
        return (num,orientation)

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
        valeur0 = s.numeroDeCouleur[ bloc2f[0] ]
        valeur1 = s.numeroDeCouleur[ bloc2f[1] ]
        num = s.retrouverNumeroArete[ s.v(valeur0,valeur1) ]
        # Identifions maintenant l'orientation de l'arête:
        orientation = 2
        for i,x in enumerate(bloc2f):
            if x == s.W or x == s.J: # Verification de la couleur de la facette.
                orientation = i # Si une des deux facettes correspond, on le retient.
        if orientation == 2: # Si on a pas pu determiner l'orientation, on utilise le bleu-vert:
            for i,x in enumerate(bloc2f):
                if x == s.B or x == s.V:
                    orientation = i
        if orientation == 2: # Si l'orientation n'est toujours pas déterminée, c'est qu'il y a une erreur.
            return "Erreur (d'orientation) d'arête dans la description du cube"
        return (num,orientation)


# Le regroupement des sommets et des arêtes:
# Pour les SOMMETS :      # Pour les ARÊTES :
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
# 2 . 1                   # . 2 .                   
# . W .                   # 3 W 1                   
# 3 . 0                   # . 0 .                   
# 3 . 0 0 . 1 1 . 2 2 . 3 # . 0 . . 1 . . 2 . . 3 . 
# . B . . O . . V . . R . # 7 B 4 4 O 5 5 V 6 6 R 7 
# 7 . 4 4 . 5 5 . 6 6 . 7 # . 8 . . 9 . . A . . B . 
#                   6 . 7 #                   . B . 
#                   . J . # [A = 10]          A J 8 
#                   5 . 4 # [B = 11]          . 9 . 

    def groupSommets (s):
        """Regroupe les facettes des sommets par 2, selon leur numéro, en vue de leur identification"""
        # On va remplir le tableau viSommets, avec les valeurs voulues.
        # On s'occupe des couches Haut et Bas en même temps.
        for i in range(0,4): # Pour chaque sommet...
            s.viSommets[i]   = (s.anneauHaut[2*i+1],
                                 s.couronneHaut[(3*i+3)%12],
                                 s.couronneHaut[(3*i+2)%12])
            s.viSommets[i+4] = (s.anneauBas[2*i+1],
                                 s.couronneBas[(3*i+2)%12],
                                 s.couronneBas[(3*i+3)%12])

    def groupAretes (s):
        """Regroupe les facettes des arêtes par 2, selon leur numéro, en vue de leur identification"""
        # On va remplir le tableau viArêtes, avec les valeurs voulues.
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
            s.sommetsBlocALaPos[pos] = bloc_lu # A chaque position, on associe le sommet correspondant
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
     
    def diffRoSommets (s,fNum,nbQuarts,oldPos):
        """Calcule l'écart de degrée d'un sommet à la position old_Pos entre avant et après une rotation de la face de numéro fNum, de nbQuarts quarts de tours. """
        if fNum != 0 and fNum != 5 and (nbQuarts % 2 != 0) :
            return 1 + ( fNum + s.sommetsPosParitee[oldPos] ) % 2
        else:
            return 0
        
    def rotationSommets (s,fNum,nbQuarts):
        """Applique aux sommets du cube les changements que causent une rotation de la face de numéro fNum, de nbQuarts quarts de tours. """
        # On gère en même temps la position et la rotation
        # On établit d'abord une liste temporaire, indiquant un bloc, sa nouvelle position, et sa nouvelle rotation.
        nbQuarts %= 4 # donc nbQuarts = 1,2 ou 3
        cycle = s.cyclesSommet[fNum]
        bloc_pos_ro_list = []
        for i in range(-4,0):
            oldPos = cycle[i]
            newPos = cycle[i+nbQuarts]
            bloc = s.sommetsBlocALaPos[oldPos]
            oldRo = s.sommetsRoALaPos[oldPos]
            newRo = (oldRo + s.diffRoSommets(fNum,nbQuarts,oldPos) ) % 3
            bloc_pos_ro_list.append( (bloc,newPos,newRo) )
        # Puis on applique ces valeurs:
        for bloc,pos,ro in bloc_pos_ro_list:
            s.sommetsPosDuBloc[bloc] = pos
            s.sommetsBlocALaPos[pos] = bloc
            s.sommetsRoDuBloc[bloc] = ro
            s.sommetsRoALaPos[pos] = ro
        
    def diffRoAretes (s,fNum,nbQuarts):
        """ Indique, pour la rotation d'une face, si les arêtes subissent un changement de degré. """
        return (nbQuarts % 2) * (fNum == 1 or fNum == 3)
        
    def rotationAretes (s,fNum,nbQuarts):
        """Applique aux arêtes du cube les changements que causent une rotation de la face de numéro fNum, de nbQuarts quarts de tours. """
        # On gère en même temps la position et la rotation
        # On établit d'abord une liste temporaire, indiquant un bloc, sa nouvelle position, et sa nouvelle rotation.
        nbQuarts %= 4 # donc nbQuarts = 1,2 ou 3
        cycle = s.cyclesArete[fNum]
        addRo = s.diffRoAretes(fNum,nbQuarts)
        bloc_pos_ro_list = []
        for i in range(-4,0):
            oldPos = cycle[i]
            newPos = cycle[i+nbQuarts]
            bloc = s.aretesBlocALaPos[oldPos]
            oldRo = s.aretesRoALaPos[oldPos]
            newRo = (oldRo + addRo) % 2
            bloc_pos_ro_list.append( (bloc,newPos,newRo) )
        # Puis on applique ces valeurs:
        for bloc,pos,ro in bloc_pos_ro_list:
            s.aretesPosDuBloc[bloc] = pos
            s.aretesBlocALaPos[pos] = bloc
            s.aretesRoDuBloc[bloc] = ro
            s.aretesRoALaPos[pos] = ro
     
    def rotationFace (s,fNum,nbQuarts):
        """ Applique aux blocs du cube les changements que causent une rotation de la face de numéro fNum, de nbQuarts quarts de tours. """
        s.rotationSommets(fNum,nbQuarts)
        s.rotationAretes(fNum,nbQuarts)
        
    def move (s,fNum,nbQuarts): # Finalement, il semble plus simple de n'utiliser que le numero des faces.
        """ Opère la rotation d'une des face du cube """
        couleurFace = s.couleurs[fNum]
        if nbQuarts % 4 == 1:
            action = "+"
        elif nbQuarts % 4 == 3:
            action = "-"
        elif nbQuarts % 4 == 2:
            action = "²"
        else: # nbQuarts % 4 == 0
            action = ''
            couleurFace = ''
        s.listeDesMouvements += couleurFace + action
        s.rotationFace(fNum,nbQuarts)
        
    def act (s,action):
        """ Tourne une face, spécifiée selon le code convention-utilisateur """
        fNum = s.numeroDeCouleur[action[0]]
        symbol = action[1]
        if symbol == "+":
            nbQuarts = 1
        elif symbol == "-":
            nbQuarts = 3
        elif symbol == "²":
            nbQuarts = 2
        else:
            nbQuarts = 0
        s.move(fNum,nbQuarts)

    def appliquer (s,instruction):
        """Applique la série de mouvements donnée (selon la convention utilisateur)"""
        for i in range(0, len(instruction), 2):
            s.act(instruction[i:i+2])
    
    
    ## Réalisation du cube, étape par étape ##
        
    def croixW(s):
        """ Effectue une succession de mouvements établissant une croix de blocs bien placés sur la face s.W (Etape 1) """
        W,J = 0,5 # Les numéros correspondant aux faces
        for k in range(4):
            arete = [0,1,2,3][k] # Les 4 blocs à déplacer.
            
            (currentPos,currentDeg) = (s.aretesPosDuBloc[arete],s.aretesRoDuBloc[arete])
            
            if not(currentPos == arete and currentDeg == 0): # Est-il mal placé ?
            
                if currentPos in (0,1,2,3): # Cas face supérieure
                    s.move(s.BOVR[currentPos],2)
                elif currentPos in (4,5,6,7): # Cas 2ème couronne
                    c = (k+4-currentPos)
                    s.move(W,c)
                    s.move(s.BOVR[arete-c%4],1)
                    s.move(W,-c) # Toujours réorienter la face supérieure !
                
                # On se ramène au cas inférieur :
                (currentPos,currentDeg) = (s.aretesPosDuBloc[arete],s.aretesRoDuBloc[arete])
                
                s.move(J,(k-currentPos)%4)
                
                # 2 cas sont possibles:
                if currentDeg == 0:
                    s.move(s.BOVR[arete],2)   # -> combinaison
                else:
                    s.move(s.BOVR[arete],1)   # -> combinaison
                    s.move(W,1)               # -> -----------
                    s.move(s.BOVR[arete-1],3) # -> -----------
                    s.move(W,3)               # -> ----------- # Toujours réorienter la face supérieure !
    
    def belge(s):
        """ Effectue une succession de mouvements établissant la deuxième couronne (Etape 3) """
        
        J = 5 # 5 est le numéro de la face jaune
        
        for k in range(4):
            arete = [4,5,6,7][k] # Les 4 blocs à déplacer.
            
            (currentPos,currentDeg) = (s.aretesPosDuBloc[arete],s.aretesRoDuBloc[arete])
            
            if not(currentPos == arete and currentDeg == 0):# Est-il mal placé ?
                if currentPos in (4,5,6,7):
                    s.move(s.BOVR[currentPos%4],1)
                    s.move(J,3)
                    s.move(s.BOVR[currentPos%4],3)
                    s.move(J,3)
                    s.move(s.OVRB[currentPos%4],3)
                    s.move(J,1)
                    s.move(s.OVRB[currentPos%4],1)
                    #L'arête est désormais sur la face jaune
                    (currentPos,currentDeg) = (s.aretesPosDuBloc[arete],s.aretesRoDuBloc[arete])
                    
                if k%2==0:
                    a=k-currentPos+1-currentDeg
                else:
                    a=k-currentPos+currentDeg
                s.move(J,a)
                currentPos=s.aretesPosDuBloc[arete]
                #On place le bloc sous la bonne face pour commencer le belge
                        
                #Doit-on faire le belge à droite ou à gauche?
                if (currentPos-arete)%2==1:     #à gauche
                    s.move(J,1)
                    s.move(s.BOVR[currentPos%4-1],1)
                    s.move(J,3)
                    s.move(s.BOVR[currentPos%4-1],3)
                    s.move(J,3)
                    s.move(s.BOVR[currentPos%4],3)
                    s.move(J,1)
                    s.move(s.BOVR[currentPos%4],1)
                else:                           # à droite
                    s.move(J,3)
                    s.move(s.OVRB[currentPos%4],3)
                    s.move(J,1)
                    s.move(s.OVRB[currentPos%4],1)
                    s.move(J,1)
                    s.move(s.BOVR[currentPos%4],1)
                    s.move(J,3)
                    s.move(s.BOVR[currentPos%4],3)
    
    
    
    
    def mvtligne(s,fNum3):
        """fait les mouvements correspondant à une configuration de type ligne horizontale avec la face d'indice fNum3 à droite de la ligne horizontale et fNum4 en face de soi"""
        if fNum3!=4:
            fNum4=fNum3+1
        else:
            fNum4=1
        
        J=5
        s.move(fNum4,1)
        s.move(fNum3,1)
        s.move(J,1)
        s.move(fNum3,3)    
        s.move(J,3)
        s.move(fNum4,3)
    def mvttypeJ(s,fNum1,fNum2):
        """fait les mouvements correspondant à une configuration de type J avec la face d'indice fNum1 à gauche du J et la face d'indice fNum2 au dessus du J"""
        if fNum2!=4:    #on créée l'indice du bloc à droite du J
            fNum3=fNum2+1
        else:
            fNum3=1
        if fNum1!=1:    #on créée l'indice du bloc en dessous du J
            fNum4=fNum1-1
        else:
            fNum4=4
        J=5
        s.move(fNum3,3)
        s.move(J,3)
        s.move(fNum4,3)
        s.move(J,1)
        s.move(fNum4,1)
        s.move(fNum3,1)
    def lienarretefacepourfaceJ(bloc2f):
        """à partir de l'indice d'une arrête de la face jaune, associe l'indice de l'autre face de contact"""
        if bloc2f=8:
            return 1
        elif bloc2f=9:
            return 2
        elif bloc2f=10:
            return 3
        else:
            return 4
        
    def petitecroixJ(s):
        """réalise la petite croix jaune du cube"""
        J=5
        if s.aretesRoDuBloc[8]!=0 and s.aretesRoDuBloc[9]!=0 and s.aretesRoDuBloc[10]!=0 and s.aretesRoDuBloc[11]!=0: #on traite le cas où le centre jaune est la seule facette jaune sur sa face
            s.mvtligne()
            for k in range(8,12):
                if k!=11 and s.aretesRoDuBloc[k]=0 and s.aretesRoDuBloc[k+1]=0: #on cherche les config de type J
                    s.mvttypeJ(lienarretefacepourfaceJ(k),lienarretefacepourfaceJ(k+1))
                elif k=11 and s.aretesRoDuBloc[11]=0 and s.aretesRoDuBloc[8]=0:
                    s.mvttypeJ(lienarretefacepourfaceJ(11),lienarretefacepourfaceJ(8))
                elif k!=10 and k!=11 and s.aretesRoDuBloc[k]=0 and s.aretesRoDuBloc[k+2]=0:     #on cherche les config de type ligne horyzontale
                    s.mvtligne(lienarretefacepourfaceJ(k))
                elif k=10 and s.aretesRoDuBloc[k]=0 and  s.aretesRoDuBloc[8]=0:
                    s.mvtligne(lienarretefacepourfaceJ(8))
                else:
                    s.mvtligne(lienarretefacepourfaceJ(9))
        else:
            for k in range(8,12):
                if k!=11 and s.aretesRoDuBloc[k]=0 and s.aretesRoDuBloc[k+1]=0: #on cherche les config de type J
                    s.mvttypeJ(lienarretefacepourfaceJ(k),lienarretefacepourfaceJ(k+1))
                elif k=11 and s.aretesRoDuBloc[11]=0 and s.aretesRoDuBloc[8]=0:
                    s.mvttypeJ(lienarretefacepourfaceJ(11),lienarretefacepourfaceJ(8))
                elif k!=10 and k!=11 and s.aretesRoDuBloc[k]=0 and s.aretesRoDuBloc[k+2]=0:     #on cherche les config de type ligne horyzontale
                    s.mvtligne(lienarretefacepourfaceJ(k))
                elif k=10 and s.aretesRoDuBloc[k]=0 and  s.aretesRoDuBloc[8]=0:
                    s.mvtligne(lienarretefacepourfaceJ(8))
                else:
                    s.mvtligne(lienarretefacepourfaceJ(9))
                    
    
    
    
    
    def petitechaise(s,fNum,coté):              #à renommer si vous voulez
        """effectue les 8 mouvements de la chaise sur une face et dans un sens donné"""
        [B,O,V,R,J]=[1,2,3,4,5]
        s.move(fNum,1+2*coté)   #coté=0 =>droite
        s.move(J,2)             #coté=1 =>gauche
        s.move(fNum,3-2*coté)
        s.move(J,3-2*coté)
        s.move(fNum,1+2*coté)
        s.move(J,3-2*coté)
        s.move(fNum,3-2*coté)
    
    def chaise(s):
        """établit la grande croix/positionne les 4 dernières arêtes (étape 5)"""
        PosB=s.aretesPosDuBloc[8]
        [B,O,V,R,J]=[1,2,3,4,5]
        a=8-PosB
        c=0
        s.move(J,a)  #le bloc 8 est correctement placé      
        
        PosB=s.aretesPosDuBloc[8]
        PosO=s.aretesPosDuBloc[9]
        PosV=s.aretesPosDuBloc[10]
        PosR=s.aretesPosDuBloc[11]
        if not([PosO,PosV,PosR]==[9,10,11]): #sont-ils bien placé?
            
            if PosV==10:                            #   .o.
                #Chaise                             #   xox
                s.petitechaise(R,0)                 #   .o.
                PosO=s.aretesPosDuBloc[9]
                PosR=s.aretesPosDuBloc[11]
                    
            if PosO==9:                             #   .x.
                #Chaise Verte                       #   oox
                s.move(J,3)                         #   .o.
                b=O
                    
            elif PosR==11:                          #   .x.
                #Chaise Orange                      #   xoo
                s.move(J,3)                         #   .o.
                b=B
                    
            elif PosO==11:
                #Chaise droite
                b=R
            else:
                #Chaise gauche
                b=O
                c=1
            s.petitechaise(b,c)
            
    def coinsDegJ(s):
        """ Effectue une succession de mouvements établissant une rotation des derniers blocs mal orientés sur la face s.J (Etape 7) """
        J = 5 # 5 est le numéro de la face jaune
        for k in range(3):
            sommet = [1,3,5][k]
            
            currentDeg = s.sommetsRoDuBloc[sommet]
            
            while not(currentDeg == 0):
                for i in range(2): # Partie 1 face de gauche (k+1), Partie 2 face de droite (k-1)
                    s.move(s.BOVR[[k+1,k-1][i]],[3,1][i]) # -> combinaison partie (i+1)/2
                    s.move(J,2)                           # -> ----------- ------ -------
                    s.move(s.BOVR[[k+1,k-1][i]],[1,3][i]) # -> ----------- ------ -------
                    s.move(J,[1,3][i])                    # -> ----------- ------ -------
                    s.move(s.BOVR[[k+1,k-1][i]],[3,1][i]) # -> ----------- ------ -------
                    s.move(J,[1,3][i])                    # -> ----------- ------ -------
                    s.move(s.BOVR[[k+1,k-1][i]],[1,3][i]) # -> ----------- ------ -------
                
                currentDeg = s.sommetsRoDuBloc[sommet]
