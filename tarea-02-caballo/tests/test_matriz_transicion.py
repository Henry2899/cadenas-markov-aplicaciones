import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from matriz_transicion import (
    construir_matriz_transicion, verificar_filas_suman_uno,
    verificar_ceros_fuera_de_N, verificar_dimension, es_simetrica,
    contraejemplo_simetria,
)

P = construir_matriz_transicion()
errores = []

def check(cond, msg):
    if not cond:
        errores.append(msg)

check(verificar_dimension(P), "P no es 64x64")
check(verificar_filas_suman_uno(P), "Alguna fila de P no suma 1")
check(verificar_ceros_fuera_de_N(P), "P tiene ceros/probabilidades incorrectas")
check(not es_simetrica(P), "P deberia NO ser simetrica")
check(contraejemplo_simetria(P) is not None, "No se encontro contraejemplo de simetria")

if errores:
    print("FALLOS:")
    for e in errores:
        print(" -", e)
    sys.exit(1)
else:
    print("Todas las pruebas de matriz_transicion pasaron.")
