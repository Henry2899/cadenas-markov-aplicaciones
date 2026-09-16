# Tarea 2 — Cadena de Markov de un caballo en un tablero de ajedrez 8×8

Cadena de Markov cuyo espacio de estados son las 64 casillas de un
tablero de ajedrez. Desde cada casilla, el caballo elige uniformemente
al azar uno de sus movimientos legales. Se construye el espacio de
estados, los conjuntos de vecindad `N(x)`, la matriz de transición
`P`, se calculan probabilidades sobre trayectorias específicas y se
estudia la alcanzabilidad (irreducibilidad y periodicidad de la
cadena).

El enunciado completo está en el repositorio del curso; el desarrollo
matemático y la discusión de resultados están en
[`report/informe.pdf`](report/informe.pdf).

## Estructura

```text
tarea-02-caballo/
├── src/
│   ├── tablero.py              # Casillas, movimientos y N(x)
│   ├── matriz_transicion.py    # Construcción y verificación de P
│   ├── ejercicio2.py           # Probabilidades sobre trayectorias (X0=a1)
│   ├── alcanzabilidad.py       # BFS por niveles desde una casilla inicial
│   ├── visualizacion.py        # Tablero coloreado por nivel de alcanzabilidad
│   └── exportar_resultados.py  # Genera todos los CSV en results/
├── tests/
│   ├── test_tablero.py             # 64 estados, N(a1)={b3,c2}, distribución de |N(x)|
│   ├── test_matriz_transicion.py   # Dimensión, filas suman 1, no simetría
│   └── test_alcanzabilidad.py      # 64 casillas alcanzadas desde a1 y d5
├── results/
│   ├── tabla_vecindades.csv        # N(x) y |N(x)| para las 64 casillas
│   ├── matriz_transicion.csv       # Matriz P completa (64×64)
│   ├── alcanzabilidad_a1.csv       # Nivel de cada casilla desde a1
│   ├── alcanzabilidad_d5.csv       # Nivel de cada casilla desde d5
│   ├── alcanzabilidad_a1.png       # Visualización del tablero desde a1
│   └── alcanzabilidad_d5.png       # Visualización del tablero desde d5
└── report/
    ├── informe.tex
    └── informe.pdf
```

## Regenerar todos los resultados

Desde esta carpeta (`tarea-02-caballo/`), con el entorno virtual del
repositorio activado:

```bash
python src/exportar_resultados.py   # genera los 4 CSV en results/
python src/visualizacion.py         # genera los 2 PNG en results/
python src/ejercicio2.py            # imprime las 4 probabilidades del ejercicio 2
```

Ningún resultado en `results/` se edita a mano: todo se regenera desde
el código.

## Pruebas

```bash
python tests/test_tablero.py
python tests/test_matriz_transicion.py
python tests/test_alcanzabilidad.py
```

## Compilar el informe

```bash
pdflatex -output-directory=report report/informe.tex
pdflatex -output-directory=report report/informe.tex
```

(dos veces, para resolver el índice y las referencias cruzadas).

## Resultados principales

- Distribución de `|N(x)|` sobre las 64 casillas: `{2: 4, 3: 8, 4: 20, 6: 16, 8: 16}`.
- `P` no es simétrica (contraejemplo: `P_{a1,b3}=1/2 ≠ P_{b3,a1}=1/6`).
- La cadena es irreducible: desde `a1` y desde `d5` se alcanzan las 64 casillas.
- La cadena es periódica con período 2 (grafo de movimientos bipartito
  según el color de la casilla).
