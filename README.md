# Rcube
Algorithme de résolution du rubiks cube, basé sur les méthodes de résolution humaines.

## Bienvenue sur la page du projet RCube
Le projet RCube, réalisé par quatre étudiants de première année de classe préparatoire, vise à créer un algorithme, qui à partir de l'énumération des couleurs des faces d'un Rubik's Cube, propose une suite de mouvements solution du cube.

## Lexique
* Cube (Rubik's Cube)
* Face (Il y en a six sur le cube)
* Facette (Il y en a 9 par face)
* Bloc (Unité cubique mobile composants le cube)
* Centre (Bloc a une facette, située au centre d'une face)
* Arrete (Bloc doté de deux facettes, situé sur deux faces, sur le bord. Il y en a quatre par face et 12 sur le cube.)
* Sommet (Bloc doté de trois facettes, situé sur trois faces, dans les coins. Il y en a quatre par face et 8 sur le cube.)

## Ordre de lecture des facettes du cube
### Ordre de lecture des faces
        1
        2 3 4 5
              6
### Ordre de lecture des facettes des faces
        1 2 3
        4 5 6
        7 8 9
## Appelle de l'algorithme
L'algorithme, codé en python, recevra un argument: une chaine de caractères de 59 caractères: six groupes de 9 caractères, séparés par des virgules. A chaque couleur de facette, l'utilisateur associera une lettre (ou un nombre). Chaque groupe de neuf caractères correspondra aux couleurs des facettes d'une face.

#### Exemples
Entièrement défait:

        jjvvwojwr,vrjjbvbro,bwroobwbb,wovwvjoow,orrvrbbvo,rwwbjjjrv
Avec les deux premières couronnes de faites:

        wwwwwwwww,bbbbbbjbr,oooooojrr,vvvvvvboo,rrrrrrjvv,bjojjjjjv

## Caractérisation pratique du cube
Propositions de caratérisation du cube:
* Par les facettes de chaque face

        Avantage: pas de conversion des données utilisateurs nécéssaire
        Inconvénient: observation du cube difficile; manipulation difficile

* Par identification des blocs (par un nom ou un indice):

    +En associant à chaque position un bloc

        -Inconvénient: observation du cube difficile

    +En associant à chaque bloc sa position

        Inconvénient: manipulation du cube difficile

    +En associant un bloc à chaque position, et une position à chaque bloc

        Avantage: observation et manipulation facile
        Inconvenient: maintient de deux descriptions du cube necessaire
