# Tarea 1 — Método de Monte Carlo aplicado a la aproximación de π

Estimación de π mediante el método de Monte Carlo: se generan puntos
aleatorios uniformes en el cuadrado `Ω = [-2,2]×[-2,2]` y se estima la
probabilidad de que caigan dentro de un círculo `C_r = {(x,y): x²+y²≤r²}`
para los radios `r = 1, √2, 2`. A partir de `P(C_r) = πr²/16` se
despeja un estimador de π, evaluado con tamaños de muestra
`n = 10², 10³, 10⁴, 10⁵, 10⁶` y semilla `42`.

El desarrollo matemático completo, los resultados y el análisis de
varianza están en [`report/informe.pdf`](report/informe.pdf).

## Estructura

```text
tarea-01-monte-carlo/
├── src/
│   └── simulacion.py           # Simulación completa: genera resultados y gráficas
├── results/
│   ├── simulacion_resultados.csv   # n, radio, proporción, error, π estimado
│   ├── convergencia_pi.png         # Convergencia de la estimación de π
│   ├── error_pi.png                # Error absoluto vs. tamaño de muestra
│   ├── puntos_radio_1.png          # Puntos simulados, r = 1
│   ├── puntos_radio_1_4142.png     # Puntos simulados, r = √2
│   └── puntos_radio_2.png          # Puntos simulados, r = 2
└── report/
    ├── informe.tex
    └── informe.pdf
```

## Regenerar todos los resultados

**Importante:** el script guarda sus archivos con rutas relativas a la
raíz del repositorio, así que debe ejecutarse desde ahí (no desde
dentro de `tarea-01-monte-carlo/`):

```bash
cd ~/proyectos/cadenas-markov-aplicaciones   # raíz del repo
python tarea-01-monte-carlo/src/simulacion.py
```

Esto regenera el CSV y las 5 gráficas en `results/` a partir de la
semilla fija (`42`), por lo que los resultados son reproducibles.

## Compilar el informe

```bash
pdflatex -output-directory=report report/informe.tex
```

(el informe de esta tarea no usa referencias cruzadas con `\ref`, así
que una sola pasada es suficiente).

## Resultados principales

- Para `n = 1.000.000`, `r = 2` produjo la mejor aproximación de π
  (error absoluto ≈ 0.000759), consistente con que la varianza teórica
  del estimador disminuye al aumentar el radio.
- El error no disminuye de forma estrictamente monótona con `n`,
  comportamiento esperado dada la naturaleza aleatoria de la
  simulación (no implica un fallo del método).
