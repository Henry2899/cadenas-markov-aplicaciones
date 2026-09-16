"""
matriz_transicion.py

Construccion de la matriz de transicion P de la cadena de Markov del
caballo, a partir de N(x):

    P[x, y] = 1 / |N(x)|   si y in N(x)
    P[x, y] = 0            en otro caso

La matriz se indexa segun el orden fijo definido en tablero.CASILLAS.
"""

import numpy as np
import pandas as pd

from tablero import CASILLAS, INDICE, vecinos


def construir_matriz_transicion() -> np.ndarray:
    """
    Construye la matriz P (64x64) de transicion del caballo.

    P[i, j] = probabilidad de pasar de CASILLAS[i] a CASILLAS[j]
            = 1/|N(CASILLAS[i])| si CASILLAS[j] in N(CASILLAS[i]), 0 si no.
    """
    n = len(CASILLAS)
    P = np.zeros((n, n), dtype=float)

    for x in CASILLAS:
        i = INDICE[x]
        n_x = vecinos(x)
        prob = 1.0 / len(n_x)
        for y in n_x:
            j = INDICE[y]
            P[i, j] = prob

    return P


def matriz_a_dataframe(P: np.ndarray) -> pd.DataFrame:
    """Envuelve P en un DataFrame con etiquetas de casillas en filas/columnas."""
    return pd.DataFrame(P, index=CASILLAS, columns=CASILLAS)


def fila_transicion(P: np.ndarray, casilla: str) -> pd.Series:
    """
    Devuelve P_{x,y} para todo y, dado x = casilla, como una Serie de
    pandas indexada por casilla destino, incluyendo solo las entradas
    no nulas (y en N(x)).
    """
    i = INDICE[casilla]
    fila = pd.Series(P[i, :], index=CASILLAS)
    return fila[fila > 0]


# ---------------------------------------------------------------------
# Verificaciones (secciones 12 y 25 del contexto del proyecto)
# ---------------------------------------------------------------------

def verificar_filas_suman_uno(P: np.ndarray, tol: float = 1e-10) -> bool:
    """Comprueba que cada fila de P suma 1 (dentro de una tolerancia)."""
    sumas = P.sum(axis=1)
    return bool(np.all(np.abs(sumas - 1.0) < tol))


def verificar_ceros_fuera_de_N(P: np.ndarray) -> bool:
    """
    Comprueba que P[i, j] == 0 siempre que CASILLAS[j] no este en
    N(CASILLAS[i]), y que P[i, j] == 1/|N(x)| cuando si lo esta.
    """
    for x in CASILLAS:
        i = INDICE[x]
        n_x = set(vecinos(x))
        prob_esperada = 1.0 / len(n_x)
        for y in CASILLAS:
            j = INDICE[y]
            if y in n_x:
                if abs(P[i, j] - prob_esperada) > 1e-12:
                    return False
            else:
                if P[i, j] != 0.0:
                    return False
    return True


def verificar_dimension(P: np.ndarray) -> bool:
    """Comprueba que P sea 64x64."""
    return P.shape == (64, 64)


def es_simetrica(P: np.ndarray, tol: float = 1e-12) -> bool:
    """Comprueba si P == P^T."""
    return bool(np.allclose(P, P.T, atol=tol))


def contraejemplo_simetria(P: np.ndarray):
    """
    Busca un par (x, y) tal que P[x,y] != P[y,x] y lo devuelve como
    (x, y, P_xy, P_yx). Devuelve None si P es simetrica.
    """
    for x in CASILLAS:
        i = INDICE[x]
        for y in CASILLAS:
            j = INDICE[y]
            if abs(P[i, j] - P[j, i]) > 1e-12:
                return (x, y, P[i, j], P[j, i])
    return None


if __name__ == "__main__":
    P = construir_matriz_transicion()

    print(f"Dimension de P: {P.shape}")
    print(f"Dimension correcta (64x64): {verificar_dimension(P)}")
    print(f"Todas las filas suman 1: {verificar_filas_suman_uno(P)}")
    print(f"Ceros fuera de N(x) y probabilidades correctas: {verificar_ceros_fuera_de_N(P)}")
    print(f"P es simetrica: {es_simetrica(P)}")

    contraejemplo = contraejemplo_simetria(P)
    if contraejemplo:
        x, y, pxy, pyx = contraejemplo
        print(f"Contraejemplo de simetria: P[{x},{y}]={pxy:.4f} != P[{y},{x}]={pyx:.4f}")

    print()
    print("Fila g1:")
    print(fila_transicion(P, "g1"))
    print()
    print("Fila h6:")
    print(fila_transicion(P, "h6"))

    print()
    for casilla in ["h8", "g1", "b7", "f7", "e5"]:
        print(f"P_{{{casilla},y}}:")
        print(fila_transicion(P, casilla))
        print()
