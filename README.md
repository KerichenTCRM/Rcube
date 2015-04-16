# Rcube
Algorithme de résolution du rubiks cube, basé sur les méthodes de résolution humaines.

## Bienvenue sur la page du projet RCube
Le projet RCube, réalisé par quatre étudiants de première année de classe préparatoire, vise à créer un algorithme, qui à partir de l'énumération des couleurs des faces d'un Rubik's Cube, propose une suite de mouvements solution du cube.

## Quelque liens
- Lien 1 - Site web proposant une résolution en 20 coups ou moins du Rubiks Cube 3x3 :

       http://rcombs.me/Cubes/?cube=clean

- Lien 2 - Site web d'où provient l'algorithme utilisé par le site du lien 1 (je ne l'ai pas lu @Mathieu) :

       http://kociemba.org/cube.htm

- Lien 3 - Vidéo YouTube d'une machine qui résoud le Rubik's cube très très vite :

       https://www.youtube.com/watch?v=qTq2V1aPAp8

- Lien 4 - Vidéo Youtube d'ou proviennent les liens 1 et 2 :

       https://www.youtube.com/watch?v=FJiDNkpGWXQ

- Lien 5 - Pour comprendre les déclaration de classes que j'utilise en Python (@Mathieu):

       http://fr.wikibooks.org/wiki/Apprendre_%C3%A0_programmer_avec_Python/Classes,_m%C3%A9thodes,_h%C3%A9ritage


## Lexique
* Cube (Rubik's Cube)
* Face (Il y en a six sur le cube)
* Facette (Il y en a 9 par face)
* Bloc (Unité cubique mobile composant le cube)
* Centre (Bloc à une facette, situé au centre d'une face)
* Arête (Bloc doté de deux facettes, situé sur deux faces, sur le bord. Il y en a quatre par face et 12 sur le cube.)
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
## Appel de l'algorithme
L'algorithme, codé en python, recevra un argument: une chaine de caractères de 59 caractères: six groupes de 9 caractères, séparés par des virgules. A chaque couleur de facette, l'utilisateur associera une lettre (ou un nombre). Chaque groupe de neuf caractères correspondra aux couleurs des facettes d'une face.

#### Exemples
Entièrement défait:

        jjvvwojwr,vrjjbvbro,bwroobwbb,wovwvjoow,orrvrbbvo,rwwbjjjrv
Avec les deux premières couronnes de faites:

        wwwwwwwww,bbbbbbjbr,oooooojrr,vvvvvvboo,rrrrrrjvv,bjojjjjjv

## Sortie de l'algorithme
La réponse, en sortie de l'algorithme, sera une liste de mouvements.

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

    +En associant un bloc à chaque position, et une position à chaque bloc [ Proposition retenue ]

        Avantage: observation et manipulation facile
        Inconvenient: maintient de deux descriptions du cube necessaire
        
## Caractérisation pratique des mouvements

Propositions de caratérisation des mouvements:
* Par le centre de la face et le sens de rotation(horaire/anti-horaire): [ Utilisé dans la réponse de l'algorithme à l'utilisateur ]

        Avantage: manipulation facile pour l'utilisateur

* Par un des 12 mouvements et une référence (face devant et dessus): [ Utilisé dans le code ]
        
        Avantage: similaire au langage utilisé lors de l'apprentissage de la résolution
        Inconvénient: nécessite une référence

