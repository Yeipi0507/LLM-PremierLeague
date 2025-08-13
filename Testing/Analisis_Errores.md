# 🛠 Detección de Errores Repetitivos del Modelo

## Objetivo
Identificar, clasificar y documentar patrones de error que el LLM comete de forma recurrente al responder sobre **estadísticas de fútbol de la Premier League**, con el fin de implementar estrategias de mitigación y optimización.

---

## Aspectos Clave

### 1. Respuestas Unificadas
- Mantener un **formato consistente** en todas las respuestas (estructura, unidades, estilo de redacción).
- Evitar variaciones innecesarias como:
  - `Haaland marcó 28 goles`
  - `28 goles fueron anotados por Erling Haaland`
- Aplicar **normalización de respuestas** para asegurar coherencia en cifras, nombres y fechas.

---

### 2. Happy Path Definido
- Cada **prompt** debe tener un **flujo de respuesta esperado** que cubra la consulta sin desviaciones.
- Ejemplo:  
  **Prompt:** `¿Quién fue el máximo goleador en la temporada 2023/24?`  
  **Respuesta esperada:** `Erling Haaland fue el máximo goleador con 28 goles en la temporada 2023/24.`
- Evitar información irrelevante como estadísticas de temporadas no solicitadas.

---

### 3. Fallback para Prevenir Inconsistencias o Duplicidades
- Si no existe información exacta, el modelo debe usar un **fallback**:
  - Reconocer la falta de datos:  
    `"No dispongo de información exacta para esa temporada, pero el último registro indica…"`
  - Evitar **hallucinations** (respuestas inventadas).
- Prevenir que el mismo prompt devuelva datos distintos sin cambios en el contexto.

---

### 4. Registro y Análisis de Patrones de Error
Documentar los errores más frecuentes:
- Datos desactualizados.
- Confusión con otras ligas (ej. incluir datos de LaLiga).
- Diferencias en cifras ante el mismo prompt.
- Respuestas incompletas o demasiado generales.

**Acciones recomendadas:**
- Ajustes en prompts.
- Mejora de datasets.
- Postprocesamiento de salidas.

---
