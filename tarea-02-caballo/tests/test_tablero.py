import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from tablero import CASILLAS, vecinos, COLUMNAS

errores = []

def check(cond, msg):
    if not cond:
        errores.append(msg)

check(len(CASILLAS) == 64, "No hay exactamente 64 casillas")
check(len(set(CASILLAS)) == 64, "Hay casillas repetidas")
check(len(vecinos("a1")) == 2, "a1 no tiene 2 vecinos")
check(set(vecinos("a1")) == {"b3", "c2"}, "N(a1) no es {b3,c2}")
check(len(vecinos("h8")) == 2, "h8 no tiene 2 vecinos")

for esquina in ["a1", "a8", "h1", "h8"]:
    check(len(vecinos(esquina)) == 2, f"{esquina} no tiene 2 vecinos")
for centro in ["d4", "d5", "e4", "e5"]:
    check(len(vecinos(centro)) == 8, f"{centro} no tiene 8 vecinos")

for casilla in CASILLAS:
    for v in vecinos(casilla):
        col, fila = v[0], int(v[1:])
        check(col in COLUMNAS, f"Vecino {v} de {casilla} tiene columna invalida")
        check(1 <= fila <= 8, f"Vecino {v} de {casilla} tiene fila invalida")

conteo = {}
for c in CASILLAS:
    n = len(vecinos(c))
    conteo[n] = conteo.get(n, 0) + 1
esperado = {2: 4, 3: 8, 4: 20, 6: 16, 8: 16}
check(conteo == esperado, f"Distribucion de |N(x)| inesperada: {conteo} (esperado {esperado})")

if errores:
    print("FALLOS:")
    for e in errores:
        print(" -", e)
    sys.exit(1)
else:
    print("Todas las pruebas pasaron.")
    print("Distribucion de |N(x)|:", conteo)
