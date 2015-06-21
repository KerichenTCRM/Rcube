// This document is a translation from the french file README.md

# Rcube
Rubik's Cube solving algorithme, based on human solving methodes

## Welcome on the RCube project page
The RCube project aims at making an algorithm to solve a Rubik's Cube. It will accept a list of facets colors as argument and print a list of moves solving the cube.

## Some links
- Link 1 - Website proposing a 20 moves-or-less solution of the cube you descibe.

       http://rcombs.me/Cubes/?cube=clean

- Link 2 - Website where the algorithme used by the site of link 1 was found:

       http://kociemba.org/cube.htm

- Link 3 - YouTube video of an engine solving a 3x3 cube, very very quickly:

       https://www.youtube.com/watch?v=qTq2V1aPAp8

- Link 4 - YouTube video where I found link 1 and 2.

       https://www.youtube.com/watch?v=FJiDNkpGWXQ

## Lexique
* Cube (Rubik's Cube)
* Face (There are six of them on a cube)
* Facet (There are 9 of them by face)
* Bloc (Cubic mobile part of a cube)
* Centre (Bloc with one facet, located a the center of a face)
* Edge (Bloc with two facets, located on two faces. There are four of them by face, and 12 on a cube)
* Vertex (Bloc with three facets, located on three faces, in the corners. There are four of them by face, and 8 on a cube)

## Facets reading order
### Faces reading order
        1
        2 3 4 5
              6
### Faces' facets reading order
        1 2 3
        4 5 6
        7 8 9
        1 2 3 1 2 3 1 2 3 1 2 3
        4 5 6 4 5 6 4 5 6 4 5 6
        7 8 9 7 8 9 7 8 9 7 8 9
                          1 2 3
                          4 5 6
                          7 8 9
## Algorithm call
The algorithm, written in python 3, takes one argument: a string of 9*6+(6-1) = 59 characters: six groups of 9 characters, comma-separated (6-1 = 5 commas).
Remarks: We keep only the last 'word' of the command line.
For each color of the cube, the user will have to choose a letter (or whatever character he wants, provided he doesn't use twice a character for different colors).

#### Examples
Entierly undone:

        jjvvwojwr,vrjjbvbro,bwroobwbb,wovwvjoow,orrvrbbvo,rwwbjjjrv
With the two first rings done:

        wwwwwwwww,bbbbbbjbr,oooooojrr,vvvvvvboo,rrrrrrjvv,bjojjjjjv

## Algorithm's answer
The algorithm's answer will be a move list, a move consisting of two characters: the color of the face to be turned, and how many quart-turns to do, following this convention:
* + means a clockwise quarter turn.
* - means an anti-clockwise quarter turn.
* ² means half a turn (180°).

[The rest of the page wasn't translated, as it was mainly used by authors to organize the development of the project.]
