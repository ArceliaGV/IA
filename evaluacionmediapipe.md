# EVALUACION REDES NEURONALES MEDIAPIPE 

# Nombre: Arcelia González Vergara 

<Modelar una red neuronal que pueda identificar emociones a través de los valores obtenidos de landmarks que genera el mediapipe>

1. **Definir el tipo de red neuronal y describir cada una de sus partes** 
   
  Se utilizará una **Red Neuronal Artificial (ANN)** de tipo **feedforward** (perceptrón multicapa - MLP), ya que el modelo trabajará con vectores de características extraídas de los landmarks por cada frame de video o imagen.

### Capas:
**Capa de entrada (Input Layer):**
   - Recibe un vector numérico con las coordenadas `x`, `y`, `z` de los landmarks faciales (468 puntos).

**Capas ocultas (Hidden Layers):**
   - Dos o más capas densamente conectadas lo que quiere decir con `densamente conectadas`es que es una capa en la que cada neurona de la capa anterior está conectada con todas las neuronas de la capa actual lo que permitiría al modelo combinar toda la información de forma flexible y aprender otros patrones faciales aún más complejos 
  
   - Aplican funciones de activación para capturar relaciones no lineales, esto principalmente porque se necesita transformar su resultado antes de pasarlo a la siguiente capa, ya que por ejemplo si se quisiera detectar una expresión de sorpresa, es una combinación de patrones faciales, es decir, la combinación de apertura ocular + distancia de labios + cejas todas estas caracteristicas formarian en teoría la expresión de sorpresa 

 **Capa de salida (Output Layer):**
   - Produce una predicción probabilística sobre la emoción detectada.


1. **Definir los patrones a utilizar**
    
  ### Opción 1: **Todos los landmarks**
- 468 landmarks × 3 coordenadas (`x`, `y`, `z`) = **1,404 entradas**
- Mayor precisión

### Opción 2: **Landmarks seleccionados**
- Se eligen puntos clave (ojos, cejas, boca, mejillas, mandíbula)
- Por ejemplo: 50 landmarks → 150 entradas
- Más rápido de entrenar, más fácil de depurar

3. **Definir función de activación es necesaria para este problema**
  **Capas ocultas:** `ReLU` (Rectified Linear Unit) ya que permite aprender rápidamente, evitando que los gradientes desaparezcan, lo que permite que la red siga aprendiendo capa por capa, incluso si tiene muchas capas ocultas. Esto es fundamental cuando se usan muchos landmarks (como podrían ser los 468 de MediaPipe), ya que se tendrán redes más profundas y complejas.
  
4. **Definir el número máximo de entradas** 
  MediaPipe Face Mesh proporciona **468 landmarks por rostro**, cada landmark tiene: x, y, z → 3 coordenadas, entonces de entradas máximas = 468 × 3 = 1404 entradas máximas

5. **¿Qué valores a la salida de la red se podrían esperar?**
  Los valores a la salida de la red neuronal serán un vector de probabilidades generado mediante la función de activación softmax, donde cada posición representa una emoción específica (por ejemplo, felicidad, tristeza, enojo, sorpresa, miedo, neutral). Cada valor estará en el rango de 0 a 1 y la suma total del vector será igual a 1, lo que indica la probabilidad estimada de que la entrada corresponda a cada emoción

6. **¿Cuáles son los valores máximos que puede tener el bias?**
   En cuanto al bias, este es un parámetro adicional aprendido por cada neurona y, en teoría, no tiene un valor máximo definido. Sin embargo, en la práctica, se inicializa comúnmente en valores cercanos a cero (por ejemplo, entre -0.1 y 0.1) y se ajusta durante el entrenamiento