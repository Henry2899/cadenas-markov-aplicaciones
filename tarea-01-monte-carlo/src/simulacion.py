# ============================================================
# TAREA 01 - SIMULACIÓN DE MONTE CARLO
# Curso: Cadenas de Markov y Aplicaciones
# ============================================================
#
# Objetivo:
# Aproximar probabilidades mediante simulación de Monte Carlo
# y utilizar estos resultados para estimar el valor de pi.
#
# Dominio:
# Ω = [-2,2] × [-2,2]
#
# Conjuntos:
# C_r = {(x,y) : x² + y² <= r²}
#
# Radios estudiados:
# r = 1, sqrt(2), 2
# ============================================================


# ------------------------------------------------------------
# 1. Importación de librerías
# ------------------------------------------------------------

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# 2. Parámetros de la simulación
# ------------------------------------------------------------

# Tamaños de muestra solicitados en la tarea
TAMANOS_MUESTRA = [10**2, 10**3, 10**4, 10**5, 10**6]

# Intervalos que definen el cuadrado Ω
LIMITE_INFERIOR = -2
LIMITE_SUPERIOR = 2

# Radios de los círculos que vamos a estudiar
RADIOS = [1, np.sqrt(2), 2]

# Semilla para garantizar reproducibilidad
SEMILLA = 42

# Generador de números aleatorios
rng = np.random.default_rng(SEMILLA)


# ------------------------------------------------------------
# 3. Generación de puntos aleatorios
# ------------------------------------------------------------

def generar_puntos(n, rng):
    """
    Genera n puntos aleatorios uniformemente distribuidos
    en el cuadrado [-2,2] × [-2,2].
    """

    x = rng.uniform(
        LIMITE_INFERIOR,
        LIMITE_SUPERIOR,
        n
    )

    y = rng.uniform(
        LIMITE_INFERIOR,
        LIMITE_SUPERIOR,
        n
    )

    return x, y


# ------------------------------------------------------------
# 4. Determinar qué puntos pertenecen al círculo
# ------------------------------------------------------------

def puntos_dentro_circulo(x, y, radio):
    """
    Determina qué puntos pertenecen al círculo de radio dado.

    Un punto (x,y) pertenece al círculo si:

        x² + y² <= r²
    """

    distancia_cuadrada = x**2 + y**2

    dentro = distancia_cuadrada <= radio**2

    return dentro


# ------------------------------------------------------------
# 5. Calcular la probabilidad estimada
# ------------------------------------------------------------

def calcular_proporcion(dentro):
    """
    Calcula la frecuencia relativa de puntos que
    pertenecen al círculo.
    """

    return np.mean(dentro)


# ------------------------------------------------------------
# 6. Calcular la probabilidad teórica
# ------------------------------------------------------------

def probabilidad_teorica(radio):
    """
    Calcula la probabilidad teórica de que un punto
    uniforme en Ω pertenezca al círculo de radio r.

    Área del cuadrado:
        4 × 4 = 16

    Área del círculo:
        πr²

    Por tanto:

        P(C_r) = πr² / 16
    """

    return np.pi * radio**2 / 16


# ------------------------------------------------------------
# 7. Estimar pi
# ------------------------------------------------------------

def estimar_pi(proporcion, radio):
    """
    Estima pi a partir de la proporción observada.

    Como:

        P(C_r) = πr² / 16

    entonces:

        π = 16 P(C_r) / r²

    Por tanto:

        π_hat = 16 P_hat / r²
    """

    return 16 * proporcion / radio**2


# ------------------------------------------------------------
# 8. Calcular error absoluto
# ------------------------------------------------------------

def calcular_error(valor_estimado, valor_real):
    """
    Calcula el error absoluto entre un valor estimado
    y su valor teórico.
    """

    return abs(valor_estimado - valor_real)


# ------------------------------------------------------------
# 9. Ejecutar una simulación
# ------------------------------------------------------------

def simular_montecarlo(n, radio, rng):
    """
    Ejecuta una simulación completa para un tamaño de muestra
    n y un radio determinado.
    """

    # Generar puntos aleatorios
    x, y = generar_puntos(n, rng)

    # Determinar cuáles están dentro del círculo
    dentro = puntos_dentro_circulo(x, y, radio)

    # Número de puntos dentro
    puntos_dentro = np.sum(dentro)

    # Probabilidad estimada mediante frecuencia relativa
    proporcion = calcular_proporcion(dentro)

    # Probabilidad teórica
    prob_teorica = probabilidad_teorica(radio)

    # Error de la probabilidad
    error_probabilidad = calcular_error(
        proporcion,
        prob_teorica
    )

    # Estimación de pi
    pi_estimado = estimar_pi(
        proporcion,
        radio
    )

    # Error absoluto de la estimación de pi
    error_pi = calcular_error(
        pi_estimado,
        np.pi
    )

    return {
        "n": n,
        "radio": radio,
        "puntos_dentro": int(puntos_dentro),
        "proporcion": proporcion,
        "probabilidad_teorica": prob_teorica,
        "error_probabilidad": error_probabilidad,
        "pi_estimado": pi_estimado,
        "error_pi": error_pi
    }


# ============================================================
# 10. PROGRAMA PRINCIPAL
# ============================================================

print("\n" + "=" * 60)
print("SIMULACIÓN DE MONTE CARLO")
print("=" * 60)

print(f"\nSemilla utilizada: {SEMILLA}")
print(f"Tamaños de muestra: {TAMANOS_MUESTRA}")
print(f"Dominio: [{LIMITE_INFERIOR}, {LIMITE_SUPERIOR}]²")

print("\nRadios estudiados:")

for radio in RADIOS:
    print(f"  r = {radio:.6f}")


# ------------------------------------------------------------
# 11. Ejecutar todas las simulaciones
# ------------------------------------------------------------

resultados = []

for radio in RADIOS:

    print("\n" + "-" * 60)
    print(f"RADIO r = {radio:.6f}")
    print("-" * 60)

    for n in TAMANOS_MUESTRA:

        resultado = simular_montecarlo(
            n,
            radio,
            rng
        )

        resultados.append(resultado)

        print(
            f"n = {n:>7,} | "
            f"dentro = {resultado['puntos_dentro']:>7,} | "
            f"P̂ = {resultado['proporcion']:.8f} | "
            f"π̂ = {resultado['pi_estimado']:.8f} | "
            f"error = {resultado['error_pi']:.8f}"
        )


# ------------------------------------------------------------
# 12. Construcción del DataFrame
# ------------------------------------------------------------

df_resultados = pd.DataFrame(resultados)


# ------------------------------------------------------------
# 13. Guardar resultados numéricos
# ------------------------------------------------------------

ruta_csv = (
    "tarea-01-monte-carlo/"
    "results/simulacion_resultados.csv"
)

df_resultados.to_csv(
    ruta_csv,
    index=False
)

print("\nResultados guardados en:")
print(ruta_csv)


# ------------------------------------------------------------
# 14. Mostrar tablas por radio
# ------------------------------------------------------------

for radio in RADIOS:

    tabla = df_resultados[
        df_resultados["radio"] == radio
    ].copy()

    print("\n" + "=" * 60)
    print(f"TABLA PARA r = {radio:.6f}")
    print("=" * 60)

    print(
        tabla[
            [
                "n",
                "puntos_dentro",
                "proporcion",
                "error_probabilidad",
                "pi_estimado",
                "error_pi"
            ]
        ].to_string(index=False)
    )


# ============================================================
# 15. VISUALIZACIÓN
# ============================================================

print("\n" + "=" * 60)
print("GENERANDO GRÁFICAS")
print("=" * 60)


# ------------------------------------------------------------
# 15.1 Convergencia de π
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

for radio in RADIOS:

    datos = df_resultados[
        df_resultados["radio"] == radio
    ]

    plt.plot(
        datos["n"],
        datos["pi_estimado"],
        marker="o",
        label=f"r = {radio:.4f}"
    )

plt.axhline(
    np.pi,
    linestyle="--",
    label=f"π = {np.pi:.6f}"
)

plt.xscale("log")

plt.xlabel("Tamaño de muestra n")
plt.ylabel("Estimación de π")

plt.title(
    "Convergencia de la estimación de π"
)

plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()

ruta_grafica_pi = (
    "tarea-01-monte-carlo/"
    "results/convergencia_pi.png"
)

plt.savefig(
    ruta_grafica_pi,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ------------------------------------------------------------
# 15.2 Error absoluto de π
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

for radio in RADIOS:

    datos = df_resultados[
        df_resultados["radio"] == radio
    ]

    plt.plot(
        datos["n"],
        datos["error_pi"],
        marker="o",
        label=f"r = {radio:.4f}"
    )

plt.xscale("log")
plt.yscale("log")

plt.xlabel("Tamaño de muestra n")
plt.ylabel("Error absoluto")

plt.title(
    "Error absoluto de la estimación de π"
)

plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()

ruta_grafica_error = (
    "tarea-01-monte-carlo/"
    "results/error_pi.png"
)

plt.savefig(
    ruta_grafica_error,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 16. Visualización de los puntos
# ============================================================

# Utilizamos una muestra de 1000 puntos únicamente
# para facilitar la visualización.

N_VISUALIZACION = 1000

rng_vis = np.random.default_rng(SEMILLA)

x_vis, y_vis = generar_puntos(
    N_VISUALIZACION,
    rng_vis
)


for radio in RADIOS:

    dentro_vis = puntos_dentro_circulo(
        x_vis,
        y_vis,
        radio
    )

    plt.figure(figsize=(7, 7))

    plt.scatter(
        x_vis[dentro_vis],
        y_vis[dentro_vis],
        s=10,
        alpha=0.6,
        label="Dentro del círculo"
    )

    plt.scatter(
        x_vis[~dentro_vis],
        y_vis[~dentro_vis],
        s=10,
        alpha=0.4,
        label="Fuera del círculo"
    )

    theta = np.linspace(
        0,
        2 * np.pi,
        300
    )

    circle_x = radio * np.cos(theta)
    circle_y = radio * np.sin(theta)

    plt.plot(
        circle_x,
        circle_y,
        linewidth=2,
        label=f"Círculo r = {radio:.4f}"
    )

    # Límites del cuadrado Ω
    plt.plot(
        [-2, -2, 2, 2, -2],
        [-2, 2, 2, -2, -2],
        linestyle="--",
        linewidth=1.5,
        label="Cuadrado Ω"
    )

    plt.xlabel("x")
    plt.ylabel("y")

    plt.title(
        f"Simulación de Monte Carlo - r = {radio:.4f}"
    )

    plt.axis("equal")
    plt.xlim(-2.2, 2.2)
    plt.ylim(-2.2, 2.2)

    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.tight_layout()

    nombre_radio = str(round(radio, 4)).replace(".", "_")

    ruta_grafica = (
        "tarea-01-monte-carlo/"
        f"results/puntos_radio_{nombre_radio}.png"
    )

    plt.savefig(
        ruta_grafica,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


# ============================================================
# 17. Finalización
# ============================================================

print("\n" + "=" * 60)
print("SIMULACIÓN COMPLETADA")
print("=" * 60)

print("\nArchivos generados:")

print(
    "  - results/simulacion_resultados.csv"
)

print(
    "  - results/convergencia_pi.png"
)

print(
    "  - results/error_pi.png"
)

for radio in RADIOS:

    nombre_radio = str(round(radio, 4)).replace(".", "_")

    print(
        f"  - results/puntos_radio_{nombre_radio}.png"
    )

print("\nValor teórico de π:")
print(f"  π = {np.pi:.10f}")