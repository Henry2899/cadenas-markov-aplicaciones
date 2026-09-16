"""
visualizacion.py

Dibuja el tablero de ajedrez 8x8 coloreando cada casilla segun el
nivel (numero minimo de movimientos de caballo) al que fue alcanzada
desde una casilla inicial, obtenido mediante alcanzabilidad().

Esto corresponde a la parte grafica del ejercicio 3 (3a-3f).
"""

import os

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import cm
from matplotlib.colors import Normalize

from tablero import COLUMNAS
from alcanzabilidad import alcanzabilidad

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")


def graficar_alcanzabilidad(casilla_inicial: str, ruta_salida: str = None):
    """
    Dibuja el tablero 8x8 con cada casilla coloreada segun su nivel de
    alcanzabilidad desde 'casilla_inicial'. Guarda la figura en
    'ruta_salida' (por defecto, results/alcanzabilidad_<casilla>.png).
    """
    resultado = alcanzabilidad(casilla_inicial)
    niveles = resultado["niveles"]
    nivel_max = resultado["num_niveles"]

    fig, ax = plt.subplots(figsize=(7, 7))

    cmap = matplotlib.colormaps["viridis"].resampled(nivel_max + 1)
    norm = Normalize(vmin=0, vmax=nivel_max)

    for col_idx, col in enumerate(COLUMNAS):
        for fila in range(1, 9):
            casilla = f"{col}{fila}"
            nivel = niveles[casilla]
            color = cmap(norm(nivel))
            rect = patches.Rectangle(
                (col_idx, fila - 1), 1, 1,
                facecolor=color, edgecolor="black", linewidth=0.5,
            )
            ax.add_patch(rect)

            # Color de texto legible segun el brillo del fondo
            brillo = 0.299 * color[0] + 0.587 * color[1] + 0.114 * color[2]
            color_texto = "white" if brillo < 0.5 else "black"

            ax.text(
                col_idx + 0.5, fila - 0.5, str(nivel),
                ha="center", va="center", fontsize=10, color=color_texto,
            )

    ax.set_xlim(0, 8)
    ax.set_ylim(0, 8)
    ax.set_xticks([i + 0.5 for i in range(8)])
    ax.set_xticklabels(list(COLUMNAS))
    ax.set_yticks([i + 0.5 for i in range(8)])
    ax.set_yticklabels([str(i) for i in range(1, 9)])
    ax.set_aspect("equal")
    ax.set_title(
        f"Alcanzabilidad del caballo desde {casilla_inicial}\n"
        f"(numero = nivel minimo de movimientos; maximo = {nivel_max})"
    )

    sm = cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, ticks=range(nivel_max + 1), fraction=0.046, pad=0.04)
    cbar.set_label("Nivel (movimientos desde la casilla inicial)")

    plt.tight_layout()

    if ruta_salida is None:
        ruta_salida = os.path.join(RESULTS_DIR, f"alcanzabilidad_{casilla_inicial}.png")
    fig.savefig(ruta_salida, dpi=150)
    plt.close(fig)
    print(f"Guardado: {ruta_salida}")
    return ruta_salida


if __name__ == "__main__":
    os.makedirs(RESULTS_DIR, exist_ok=True)
    graficar_alcanzabilidad("a1")
    graficar_alcanzabilidad("d5")
