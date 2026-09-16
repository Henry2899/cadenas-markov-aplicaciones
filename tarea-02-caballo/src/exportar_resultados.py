"""
exportar_resultados.py

Genera los archivos CSV de resultados del ejercicio 1 (tabla de
vecindades y matriz de transicion) y del ejercicio 3 (alcanzabilidad
desde a1 y d5), a partir del codigo, para mantener la reproducibilidad:
nunca se escriben estos CSV a mano.

Uso:
    python src/exportar_resultados.py
"""

import os
import pandas as pd

from tablero import tabla_vecindades
from matriz_transicion import construir_matriz_transicion, matriz_a_dataframe
from alcanzabilidad import alcanzabilidad

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")


def exportar_tabla_vecindades():
    df = pd.DataFrame(tabla_vecindades())
    ruta = os.path.join(RESULTS_DIR, "tabla_vecindades.csv")
    df.to_csv(ruta, index=False, encoding="utf-8")
    print(f"Guardado: {ruta}  ({len(df)} filas)")
    return df


def exportar_matriz_transicion():
    P = construir_matriz_transicion()
    df = matriz_a_dataframe(P)
    ruta = os.path.join(RESULTS_DIR, "matriz_transicion.csv")
    df.to_csv(ruta, encoding="utf-8")
    print(f"Guardado: {ruta}  (dimension {df.shape})")
    return df


def exportar_alcanzabilidad(casilla_inicial: str):
    resultado = alcanzabilidad(casilla_inicial)
    filas = [
        {"casilla": c, "nivel": nivel}
        for c, nivel in sorted(resultado["niveles"].items(), key=lambda t: (t[1], t[0]))
    ]
    df = pd.DataFrame(filas)
    ruta = os.path.join(RESULTS_DIR, f"alcanzabilidad_{casilla_inicial}.csv")
    df.to_csv(ruta, index=False, encoding="utf-8")
    print(f"Guardado: {ruta}  ({len(df)} filas, {resultado['num_niveles']} niveles)")
    return df


if __name__ == "__main__":
    os.makedirs(RESULTS_DIR, exist_ok=True)
    exportar_tabla_vecindades()
    exportar_matriz_transicion()
    exportar_alcanzabilidad("a1")
    exportar_alcanzabilidad("d5")
