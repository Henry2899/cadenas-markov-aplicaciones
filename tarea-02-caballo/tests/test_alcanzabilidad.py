import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from alcanzabilidad import alcanzabilidad
from tablero import CASILLAS

errores = []
def check(cond, msg):
    if not cond:
        errores.append(msg)

for inicio in ["a1", "d5"]:
    r = alcanzabilidad(inicio)
    check(len(r["alcanzadas"]) == 64, f"Desde {inicio} no se alcanzan las 64 casillas")
    check(len(r["no_alcanzadas"]) == 0, f"Desde {inicio} hay casillas no alcanzadas")
    check(set(r["niveles"].keys()) == set(CASILLAS), f"Niveles de {inicio} no cubren las 64 casillas")
    check(r["niveles"][inicio] == 0, f"Nivel de la casilla inicial {inicio} no es 0")
    total = sum(len(nivel) for nivel in r["orden_por_nivel"])
    check(total == 64, f"Suma de casillas por nivel desde {inicio} no da 64 (da {total})")
    for k, casillas_nivel in enumerate(r["orden_por_nivel"]):
        for c in casillas_nivel:
            check(r["niveles"][c] == k, f"Casilla {c} en nivel {k} no coincide con niveles[{c}]={r['niveles'][c]}")

r_a1 = alcanzabilidad("a1")
check(r_a1["niveles"]["h8"] == 6, "Distancia a1->h8 deberia ser 6")

if errores:
    print("FALLOS:")
    for e in errores: print(" -", e)
    sys.exit(1)
else:
    print("Todas las pruebas de alcanzabilidad pasaron.")
