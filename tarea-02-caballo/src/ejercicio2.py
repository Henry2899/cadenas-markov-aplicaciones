"""
ejercicio2.py

Calculo de las probabilidades pedidas en el ejercicio 2, para la cadena
del caballo con X_0 = a1.

Cada calculo se documenta explicitamente con la formula matematica
utilizada (no solo el resultado numerico), tal como exige el enunciado.
"""

import numpy as np

from tablero import INDICE
from matriz_transicion import construir_matriz_transicion


def prob_transicion(P: np.ndarray, x: str, y: str) -> float:
    """P_{x,y}, la probabilidad de transicion de x a y en un paso."""
    return P[INDICE[x], INDICE[y]]


def p_x1_igual_c2(P: np.ndarray) -> float:
    """
    P(X1 = c2 | X0 = a1) = P_{a1,c2}
    (lectura directa de la matriz de transicion).
    """
    return prob_transicion(P, "a1", "c2")


def p_trayectoria_c2_d4_e6_c7(P: np.ndarray) -> float:
    """
    P(X1=c2, X2=d4, X3=e6, X4=c7 | X0=a1)
        = P_{a1,c2} * P_{c2,d4} * P_{d4,e6} * P_{e6,c7}

    Se usa la propiedad de Markov: la probabilidad conjunta de una
    trayectoria es el producto de las probabilidades de transicion de
    cada paso, condicionadas cada una solo al estado inmediatamente
    anterior.
    """
    pasos = [("a1", "c2"), ("c2", "d4"), ("d4", "e6"), ("e6", "c7")]
    probs = [prob_transicion(P, x, y) for x, y in pasos]
    return float(np.prod(probs)), probs


def p_condicional_x3_e2_x2_d4_dado_x1_b3(P: np.ndarray):
    """
    P(X3=e2, X2=d4 | X1=b3) = P_{b3,d4} * P_{d4,e2}

    Por la propiedad de Markov, condicionar en X1=b3 hace que el futuro
    (X2, X3) dependa solo de b3, no de X0. Por eso el calculo es
    identico en forma al de una trayectoria de 2 pasos que comienza
    en b3.
    """
    p1 = prob_transicion(P, "b3", "d4")
    p2 = prob_transicion(P, "d4", "e2")
    return p1 * p2, (p1, p2)


def p_dos_pasos_a3_a_e3(P: np.ndarray):
    """
    P(X_{n+2} = e3 | X_n = a3) = (P^2)_{a3,e3}

    Se calcula de dos formas independientes para verificar consistencia:

    Metodo 1: multiplicacion matricial P @ P, leyendo la entrada (a3, e3).
    Metodo 2: suma sobre el estado intermedio z,
              sum_z P_{a3,z} * P_{z,e3}.
    """
    i, k = INDICE["a3"], INDICE["e3"]

    P2 = P @ P
    metodo1 = P2[i, k]

    metodo2 = sum(P[i, j] * P[j, k] for j in range(P.shape[0]))

    return metodo1, metodo2


if __name__ == "__main__":
    P = construir_matriz_transicion()

    print("1) P(X1 = c2 | X0 = a1)")
    r1 = p_x1_igual_c2(P)
    print(f"   = P_{{a1,c2}} = {r1}")
    print()

    print("2) P(X1=c2, X2=d4, X3=e6, X4=c7 | X0=a1)")
    r2, probs2 = p_trayectoria_c2_d4_e6_c7(P)
    print(f"   = P_a1,c2 * P_c2,d4 * P_d4,e6 * P_e6,c7")
    print(f"   = {probs2[0]:.6f} * {probs2[1]:.6f} * {probs2[2]:.6f} * {probs2[3]:.6f}")
    print(f"   = {r2:.10f}")
    print()

    print("3) P(X3=e2, X2=d4 | X1=b3)")
    r3, probs3 = p_condicional_x3_e2_x2_d4_dado_x1_b3(P)
    print(f"   = P_b3,d4 * P_d4,e2 = {probs3[0]:.6f} * {probs3[1]:.6f} = {r3:.10f}")
    print()

    print("4) P(X_{n+2} = e3 | X_n = a3)")
    m1, m2 = p_dos_pasos_a3_a_e3(P)
    print(f"   Metodo 1 (P@P)[a3,e3]        = {m1:.10f}")
    print(f"   Metodo 2 (suma intermedios z) = {m2:.10f}")
    print(f"   Coinciden: {abs(m1 - m2) < 1e-12}")
