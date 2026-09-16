"""
alcanzabilidad.py

Exploracion por niveles (BFS) del grafo de movimientos del caballo,
a partir de una casilla inicial.

Nivel 0 = casilla inicial.
Nivel k = casillas alcanzadas por primera vez en k movimientos.

Esto corresponde al ejercicio 3 del enunciado (pintar sucesivamente
las casillas alcanzables).
"""

from collections import deque

from tablero import CASILLAS, vecinos


def alcanzabilidad(casilla_inicial: str) -> dict:
    """
    Realiza BFS desde 'casilla_inicial' sobre el grafo de movimientos
    del caballo.

    Devuelve un diccionario con:
        "niveles": dict  casilla -> nivel (distancia minima, en numero
                   de movimientos, desde casilla_inicial)
        "orden_por_nivel": list de listas; orden_por_nivel[k] son las
                   casillas nuevas alcanzadas en el nivel k
        "alcanzadas": set de todas las casillas alcanzadas
        "no_alcanzadas": set de casillas nunca alcanzadas
        "num_niveles": int, el nivel maximo alcanzado (profundidad del BFS)
    """
    nivel = {casilla_inicial: 0}
    orden_por_nivel = [[casilla_inicial]]

    cola = deque([casilla_inicial])
    while cola:
        actual = cola.popleft()
        nivel_actual = nivel[actual]
        for vecino in vecinos(actual):
            if vecino not in nivel:
                nivel[vecino] = nivel_actual + 1
                if len(orden_por_nivel) <= nivel_actual + 1:
                    orden_por_nivel.append([])
                orden_por_nivel[nivel_actual + 1].append(vecino)
                cola.append(vecino)

    alcanzadas = set(nivel.keys())
    no_alcanzadas = set(CASILLAS) - alcanzadas

    return {
        "niveles": nivel,
        "orden_por_nivel": orden_por_nivel,
        "alcanzadas": alcanzadas,
        "no_alcanzadas": no_alcanzadas,
        "num_niveles": len(orden_por_nivel) - 1,
    }


def resumen_alcanzabilidad(resultado: dict, casilla_inicial: str) -> str:
    """Genera un resumen textual legible del resultado del BFS."""
    n_alcanzadas = len(resultado["alcanzadas"])
    n_no_alcanzadas = len(resultado["no_alcanzadas"])
    lineas = [
        f"Casilla inicial: {casilla_inicial}",
        f"Casillas alcanzadas: {n_alcanzadas} de 64",
        f"Casillas NO alcanzadas: {n_no_alcanzadas}",
        f"Numero de niveles (profundidad del BFS): {resultado['num_niveles']}",
    ]
    if resultado["no_alcanzadas"]:
        lineas.append(f"No alcanzadas: {sorted(resultado['no_alcanzadas'])}")
    for k, casillas_nivel in enumerate(resultado["orden_por_nivel"]):
        lineas.append(f"  Nivel {k}: {len(casillas_nivel)} casillas nuevas -> {sorted(casillas_nivel)}")
    return "\n".join(lineas)


if __name__ == "__main__":
    for inicio in ["a1", "d5"]:
        resultado = alcanzabilidad(inicio)
        print(resumen_alcanzabilidad(resultado, inicio))
        print()
