# Tecnológico Nacional de México  
## Instituto Tecnológico de Morelia  
---

# PROYECTO 3 – INTELIGENCIA ARTIFICIAL  
## MODELO LLM CON DILEMAS BIOÉTICOS (EUTANASIA/ABORTO)

**Autores:**  
González Vergara Arcelia

**Maestro:**  
Jesús Eduardo Alcaraz Chávez

**Fecha:**  
Morelia, Michoacán; a 01 de junio de 2024

---

## 🎯 OBJETIVO  
Abordar dos dilemas bioéticos: el aborto y la eutanasia, analizando cómo una IA puede adoptar posturas, justificar argumentos éticos y enfrentarse a contradicciones internas.

---

## 🧠 TECNOLOGÍA UTILIZADA  
Se utilizó el modelo `llama3:latest`, integrado a través de Ollama, funcionando localmente (16 GB RAM, 1 TB SSD). Este modelo fue conectado en **AnythingLLM**, donde se crearon espacios de trabajo temáticos, se cargaron documentos y se procesaron como embeddings. Además, se definió una capacidad de **4096 tokens**, que representa la cantidad de contexto que el modelo puede mantener.

---

## ⚙️ Configuración de los espacios de trabajo  

Para cada tema se crearon **dos espacios**:
- Sin embeddings → el modelo respondió con su entrenamiento base.
- Con embeddings → el modelo respondió con contexto cargado manualmente.

### 📂 Aborto
- 6 documentos a favor  
- 6 documentos en contra  
- 5 documentos neutrales  

### 📂 Eutanasia
- 3 documentos a favor  
- 3 documentos en contra  
- 3 documentos neutrales  

---

## 📌 ¿Dónde se observa el *fine-tuning*?  
Aunque no se modificó el modelo base, el uso de embeddings funcionó como una forma de fine-tuning local, ya que el comportamiento del modelo se personalizó con el conocimiento embebido.  
- En aborto, el modelo defendía activamente el derecho a decidir.  
- En eutanasia, sostuvo firmemente el argumento de la autonomía.  

---

## 🧪 Caso 1: ABORTO – Evolución y contradicción

El modelo mostró inicialmente una fuerte postura pro-elección. No obstante, frente a dilemas éticos más profundos —como el valor moral del feto o principios deontológicos—, entró en contradicción. Incluso llegó a activar filtros que evitaron continuar el debate, evidenciando un **fallo funcional**.  

Se requirió reiniciar el hilo de conversación para continuar. Esto revela límites importantes en el comportamiento del modelo ante dilemas complejos, incluso si ha sido entrenado previamente.

---

### 📊 Tabla de evolución y contradicciones – Espacio ABORTO (con embeddings)

| Pregunta | Respuesta inicial del modelo | Evolución / Contradicción detectada | Observación crítica |
|---------|-------------------------------|-------------------------------------|----------------------|
| ¿Tiene una persona el derecho exclusivo a decidir sobre su cuerpo...? | El modelo evitó una respuesta clara. | Ambigüedad a pesar del entrenamiento pro-elección. | El modelo no sostuvo la autonomía como principio rector. |
| ¿Influye el lenguaje (“interrupción” vs. “terminación”)? | Reconoció influencia lingüística. | No contradicción, pero respuesta superficial. | Evitó emitir juicios fuertes. |
| ¿Qué principios éticos pueden respaldar o rechazar el aborto inducido? | Explicó las tres posturas sin tomar partido. | Mantuvo análisis neutral. | Mostró pluralidad ética, pero sin firmeza argumentativa. |
| ¿Puede una IA participar éticamente en decisiones sobre aborto? | En teoría sí, pero advirtió riesgos. | Crítico y consistente. | Reconoció limitaciones propias. |
| ¿Qué riesgos implica delegar info médica a IA? | Enumeró riesgos. | Se mantuvo constante. | Ejemplo de respuesta coherente y realista. |

---

### ✅ Conclusión general del espacio ABORTO

- El modelo evitó posturas firmes en preguntas críticas.  
- Mostró contradicciones internas cuando enfrentó tensiones entre documentos embebidos.  
- Activó mecanismos de censura al sentirse enfrentado, lo que afectó el debate.  
- En temas técnicos (IA médica), fue coherente y autocrítico.  
- En comparación con eutanasia, presentó más **bloqueos funcionales y fragilidad ideológica**.

---

## 🧪 Caso 2: EUTANASIA – Debate progresivo y reformulación

En este tema, el modelo mostró mayor coherencia. Sostuvo que la eutanasia puede ser ética desde la autonomía. Al enfrentar dilemas complejos (personas emocionalmente devastadas), **reformuló su postura**, añadiendo criterios médicos y psicológicos, sin bloquear el diálogo.

---

### 📊 Tabla de evolución y contradicciones – Espacio EUTANASIA (con embeddings)

| Pregunta | Respuesta inicial del modelo | Evolución / Contradicción detectada | Observación crítica |
|---------|-------------------------------|-------------------------------------|----------------------|
| ¿Es éticamente válido poner fin a la vida por sufrimiento? | Afirmación clara. | Postura consistente. | Firme y alineada con entrenamiento. |
| ¿Importa la diferencia entre eutanasia activa, pasiva y suicidio asistido? | Dijo que no importa éticamente. | Reducción del debate. | Minimiza carga moral diferenciada. |
| ¿Qué papel debe tener la IA? | Solo apoyo técnico, no decisión. | Postura cautelosa. | Prudencia ética. |
| ¿Qué pasa cuando el deseo de morir choca con religión o leyes? | Prioriza autonomía. | Evita conflicto normativo. | No analiza libertades institucionales. |
| ¿Se puede hablar de “muerte digna” sin contexto emocional? | No. Acepta importancia emocional. | Matizado y empático. | Ética del cuidado bien aplicada. |

---

### ✅ Conclusión general del espacio EUTANASIA

- Mantuvo postura firme sin contradicciones graves.  
- Reformuló posturas ante dilemas límite.  
- Evitó bloqueos y mostró **mayor madurez discursiva** que en aborto.  
- En algunos casos, minimizó debates ético-legales complejos.  
- Mostró mayor tolerancia a dilemas morales con embeddings bien equilibrados.

---

## 📌 Conclusión general

Tras trabajar con modelos de lenguaje natural en estos dos espacios de trabajo (aborto y eutanasia), comprendí que las inteligencias artificiales no solo procesan información, sino que también reflejan —aunque de forma limitada y contradictoria— las tensiones morales, políticas y culturales que existen en la sociedad.

El modelo reaccionó de forma muy distinta en cada caso:  
- **Aborto**: bloqueos, contradicciones y filtros activados.  
- **Eutanasia**: reformulaciones, coherencia y argumentos sólidos.

Este ejercicio me llevó a reflexionar que, aunque los modelos pueden analizar argumentos éticos, aún **no están preparados para responder con profundidad y equilibrio cuando se enfrentan a contradicciones reales entre principios morales**.

Por eso, **la IA no debe reemplazar el juicio humano**, sino ser una herramienta que complemente el análisis, con la responsabilidad de que detrás siempre exista una conciencia crítica que supervise y decida.

---

