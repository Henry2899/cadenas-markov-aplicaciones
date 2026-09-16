"""
tablero.py

Representacion del tablero de ajedrez 8x8 y movimientos del caballo.

Orden fijo de las 64 casillas (definido por el enunciado):
    a1, a2, ..., a8, b1, ..., b8, ..., h1, ..., h8
"""

COLUMNAS = "abcdefgh"
FILAS = range(1, 9)

# Orden fijo de estados: columna por columna, fila 1 -> 8
CASILLAS = [f"{col}{fila}" for col in COLUMNAS for fila in FILAS]

assert len(CASILLAS) == 64, "Debe haber exactamente 64 casillas"
assert len(set(CASILLAS)) == 64, "Las 64 casillas deben ser unicas"

# Indice de cada casilla dentro del orden fijo (para construir la matriz luego)
INDICE = {casilla: i for i, casilla in enumerate(CASILLAS)}

# Los 8 desplazamientos relativos de un caballo (columna, fila)
MOVIMIENTOS_CABALLO = [
    (1, 2), (1, -2), (-1, 2), (-1, -2),
    (2, 1), (2, -1), (-2, 1), (-2, -1),
]


def _col_a_indice(col: str) -> int:
    """Convierte una letra de columna ('a'..'h') a un indice 0..7."""
    return COLUMNAS.index(col)


def _indice_a_col(idx: int) -> str:
    """Convierte un indice 0..7 a letra de columna."""
    return COLUMNAS[idx]


def _parsear_casilla(casilla: str) -> tuple[int, int]:
    """Convierte 'a1' -> (col_idx=0, fila=1)."""
    col = casilla[0]
    fila = int(casilla[1:])
    return _col_a_indice(col), fila


def _formar_casilla(col_idx: int, fila: int) -> str:
    """Convierte (col_idx, fila) -> 'a1'."""
    return f"{_indice_a_col(col_idx)}{fila}"


def vecinos(casilla: str) -> list[str]:
    """
    Calcula N(x): las casillas alcanzables desde 'casilla' en un movimiento
    legal de caballo.

    Devuelve la lista en un orden determinista (el orden de
    MOVIMIENTOS_CABALLO, filtrando los que caen fuera del tablero).
    """
    col_idx, fila = _parsear_casilla(casilla)
    resultado = []
    for dc, df in MOVIMIENTOS_CABALLO:
        nueva_col = col_idx + dc
        nueva_fila = fila + df
        if 0 <= nueva_col <= 7 and 1 <= nueva_fila <= 8:
            resultado.append(_formar_casilla(nueva_col, nueva_fila))
    return resultado


def tabla_vecindades() -> list[dict]:
    """
    Genera la tabla completa x, N(x), |N(x)| para las 64 casillas,
    en el orden fijo de CASILLAS.
    """
    filas = []
    for casilla in CASILLAS:
        n_x = vecinos(casilla)
        filas.append({
            "casilla": casilla,
            "N(x)": ", ".join(n_x),
            "|N(x)|": len(n_x),
        })
    return filas


if __name__ == "__main__":
    print(f"Numero de casillas: {len(CASILLAS)}")
    print(f"Primeras 5 casillas: {CASILLAS[:5]}")
    print(f"Ultimas 5 casillas: {CASILLAS[-5:]}")
    print()
    print(f"N(a1) = {vecinos('a1')}  (|N(a1)| = {len(vecinos('a1'))})")
    print(f"N(h8) = {vecinos('h8')}  (|N(h8)| = {len(vecinos('h8'))})")
    print(f"N(d5) = {vecinos('d5')}  (|N(d5)| = {len(vecinos('d5'))})")
