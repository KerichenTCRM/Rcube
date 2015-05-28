from numpy import *

## Pivot de Gauss : Inverser une matrice !

def matE(i,j,n):
    """Renvoie la matrice (i,j) de la base canonique des matrices carrées de taille n."""
    E = zeros((n,n))
    E[i,j]=1
    return E

def prodm(A,B):
    """Renvoie le produit A x B."""
    n,p,q = len(A),len(B[0]),len(B) # A est de taille (n,q) et B de taille (q,p) donc C de taille (n,p)
    C = zeros((n,p))
    for i in range(n):
        for j in range(p):
            for k in range(q): # On calcule le terme d'indice (i,j)
                C[i,j] += A[i,k]*B[k,j]
    return C

def multMat(l,k,n):
    """Renvoie la matrice d'ordre n de multiplication par l de la ligne/colonne k."""
    return eye(n)+(l-1)*matE(k,k,n)

def combMat(L,i):
    """Renvoie la matrice d'ordre len(L) de combinaison linéaire L, la liste des coefficients, de la ligne i."""
    n = len(L)
    P = eye(n)
    for k in range(n):
        P += L[k]*matE(i,k,n)
    return P

def transMat(r,s,n):
    """Renvoie la matrice d'ordre n de transposition (r,s)."""
    return eye(n)-matE(r,r,n)-matE(s,s,n)+matE(r,s,n)+matE(s,r,n)
    
def trouveInd(C):
    """Renvoie le plus petit indice de la liste C de coefficient non nul"""
    for k in range(len(C)):
        if C[k]!=0:
            return k
    print("Erreur : colonne nulle ou vide") # Si tous les coefficients sont nuls ou si la liste est vide ==> erreur
        
def etapeGauss(A,B,P):
    """Effectue les produits PxA et PxB correspond à une étape du pivot de Gauss"""
    return [prodm(P,A),prodm(P,B)]

def pivotGauss(M):
    """Renvoie la matrice inverse de A"""
    n = len(M)
    A,B = M,eye(n)
    for k in range(n):
        if A[k,k] == 0: # En cas de coefficient nul...
            (A,B) = etapeGauss(A,B,transMat(k,k+trouveInd(A[:,k][k:]),n)) # ... on échange la ligne k et une ligne où le coefficient est non nul qui existe si la matrice est inversible.
        (A,B) = etapeGauss(A,B,multMat(1/A[k,k],k,n)) # Donc, pas de division par 0.
        for i in range(n): # On annule tous les coefficients de la colonne k sur les lignes autres que k.
            if i != k:
                L = n*[0]
                L[k] = -A[i,k]
                (A,B) = etapeGauss(A,B,combMat(L,i))
    return B
