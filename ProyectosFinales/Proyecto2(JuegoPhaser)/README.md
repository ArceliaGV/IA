## PROYECTO 2 - Evaluación Final IA
**Alumna:** González Vergara Arcelia

Este proyecto consiste en el desarrollo de un **juego tipo "Phaser" en Python con Pygame**, donde el personaje debe esquivar obstáculos utilizando decisiones automatizadas por tres modelos de inteligencia artificial:

- 1.  Árboles de Decisión (`decision_trees.py`)
- 2. Redes Neuronales (`redes_neuronales.py`)
- 3. K-Nearest Neighbor (`k_nearest_neighbor.py`)

Cada script está acompañado de su respectivo archivo `.md` con la explicación detallada del código, estructura y comportamiento de cada modelo.

---

##  ¿Cómo se usa?

1. Activar el entorno virtual:
   ```bash
   conda activate proyectophaser
o si usas venv:
 ```bash
source proyectophaser/bin/activate

2. Ejecutar cualquiera de los scripts según el modelo que se desea probar:
- python decision_trees.py
- python redes_neuronales.py
- python k_nearest_neighbor.py

3. Uso dentro del juego:

**Modo manual: el jugador controla las acciones (salto y movimiento).**

**Modo automático: el modelo IA decide cuándo saltar o avanzar, es decir adapta el modo de entramiento que se le da en modo manual**

**Se recolectan datos en modo manual para luego entrenar el modelo.**

 Estructura del directorio

| Archivo                 | Descripción                                       |
| ----------------------- | ------------------------------------------------- |
| `decision_trees.py`     | Juego controlado por modelo de árbol de decisión. |
| `redes_neuronales.py`   | Juego controlado por red neuronal artificial.     |
| `k_nearest_neighbor.py` | Juego controlado por algoritmo KNN.               |
| `*.md`                  | Documentación individual por cada modelo.         |
| `pygamesc/assets/`      | Recursos gráficos y de audio usados en el juego.  |

Objetivo académico
Evaluar y comparar el desempeño de modelos de IA supervisados dentro de un entorno interactivo simulado, 
enfocándose en la toma de decisiones autónoma ante estímulos dinámicos.

# Requisitos
1. Python 3.12+
2. pygame==2.6.1
3. numpy
4. scikit-learn

Instalación rápida:
pip install pygame numpy scikit-learn
