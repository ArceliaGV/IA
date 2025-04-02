1. Distinguir si tiene signos de vida (detección de "liveness").

2. Diferenciar entre imagen estática y video.

# Sistema de Reconocimiento Facial con MediaPipe y OpenCV

Este proyecto permite la detección y análisis facial en tiempo real utilizando MediaPipe y OpenCV. Actualmente, dibuja landmarks faciales clave (ojos y boca) y calcula distancias entre ellos, como entre los ojos. Esta base podría extenderse para identificar signos de vida y diferenciar entre imágenes y video.

# Funcionalidades actuales

- Detección de rostros en tiempo real con cámara web.
- Identificación de landmarks faciales específicos (ojos y boca).
- Cálculo de distancia euclidiana entre landmarks (ej. entre ambos ojos).
- Visualización en tiempo real con puntos y líneas superpuestos.

# Objetivo: Detección de Vida de lo que se está intentando identificar 

# ¿Cómo detectar si tiene vida en reconocimiento facial?

**Idea clave:** Un rostro real presenta microexpresiones y movimientos naturales (parpadeo, movimientos de cabeza, etc.) que no ocurren en una imagen o foto impresa.

# Estrategias posibles:
1. Detección de parpadeo:
   - Monitorear la distancia entre los párpados superiores e inferiores con los landmarks de los ojos.
   - Si esta distancia se reduce periódicamente, es un signo de parpadeo → señal de vida.

2. Seguimiento de movimiento natural:
   - Analizar si hay pequeños movimientos de cabeza o cambios en la geometría del rostro entre frames.

3. Variación temporal:
   - Si los landmarks permanecen idénticos por muchos frames, probablemente se trata de una imagen estática.
  
# ¿Cómo diferenciar imagen de video?
MediaPipe tiene un parámetro llamado static_image_mode que cambia la forma en que procesa las entradas.

# Método:
1. # En modo imagen (`static_image_mode=True`):
   - El sistema procesa una sola imagen sin usar la temporalidad.

2. # En modo video (`static_image_mode=False`)**:
   - MediaPipe realiza *tracking* de los landmarks a través del tiempo.
   - Se podría medir movimiento entre frames para detectar si la fuente es video.

