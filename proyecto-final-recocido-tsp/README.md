# Proyecto final — El recocido simulado como cadena de Markov (TSP)

Aplicación de cadenas de Markov al problema del agente viajero: la cadena
de Metropolis sobre rutas con vecindad 2-opt, su distribución de
Boltzmann, la brecha espectral, el recocido simulado como cadena no
homogénea (teorema de Hajek) y la variante sobre el modelo QUBO.

## Estructura

```text
proyecto-final-recocido-tsp/
├── notebook/     # Notebook de Google Colab (genera todas las figuras y tablas)
├── results/      # Figuras y CSV exportados por el notebook
└── report/
    ├── informe.tex
    ├── referencias.bib
    └── secciones/
```

## Compilar el informe

Desde `report/`:

```bash
pdflatex informe.tex
bibtex informe
pdflatex informe.tex
pdflatex informe.tex
```
