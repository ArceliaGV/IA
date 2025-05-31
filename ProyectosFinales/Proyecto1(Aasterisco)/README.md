# Proyecto 1 – Evaluación Final de Inteligencia Artificial  
**Alumna:** González Vergara Arcelia – Matrícula: 21120211

---

##  Descripción general

Este proyecto consiste en la implementación visual del algoritmo **A\*** utilizando la biblioteca **Pygame**, como parte de la evaluación final del curso de Inteligencia Artificial.

Se desarrolla sobre un cascarón base que permite:
- Interacción gráfica para definir el **punto de inicio**, **final** y **obstáculos**.
- Visualización del proceso de búsqueda óptima con:
  - Colores para nodos abiertos, cerrados, camino final, etc.
  - Panel lateral mostrando la **lista cerrada** y **lista abierta**.
  - Visualización en tiempo real del cálculo de `g`, `h` y `f` para cada nodo.

---

##  Requisitos del proyecto

- La solución implementa el algoritmo A\* garantizando **optimalidad**.
- Se muestran al usuario:
  - Lista abierta
  - Lista cerrada
  - Camino óptimo final
- Se emplea una **heurística Manhattan** y se consideran costos:
  - 10 unidades para movimientos ortogonales
  - 14 unidades para movimientos diagonales

---

##  ¿Cómo se usa?

1. Activar un entorno en la consola y posterior ejecutar el script con `python Aasterisco.py`:
  
   Dentro de la interfaz:

2. Clic izquierdo: seleccionar nodo de inicio, fin y obstáculos.

3. Clic derecho: borrar nodo.

4. Presionar barra espaciadora para ejecutar el algoritmo A*.

5. Se mostrará el camino más corto encontrado y las listas abierta/cerrada.

## Requisitos del entorno

Instalar dependencias usando pip:

# pip install -r requeriments.txt

## Archivos Incluidos

| Archivo            | Descripción                                                    |
| ------------------ | -------------------------------------------------------------- |
| `Aasterisco.py`    | Código completo del algoritmo A\* con visualización en Pygame. |
| `aAsterisco.md`    | Documentación detallada del código, clases y funciones.        |
| `requeriments.txt` | Requisitos de entorno (solo Pygame 2.6.1).                     |
| `/entorno/`        | Archivos adicionales si se usan recursos o configuraciones.    |

## Objetivo académico
Evaluar la capacidad de aplicar inteligencia artificial para la resolución de caminos óptimos en entornos dinámicos, utilizando estructuras de datos, heurísticas y visualización eficiente del proceso de búsqueda.
