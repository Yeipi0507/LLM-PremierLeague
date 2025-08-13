# 📄 Documentación de Posibles Mejoras de Prompt o Dataset

## Objetivo
Identificar y registrar mejoras potenciales en los **prompts** y en el **dataset** utilizados para el entrenamiento y validación del LLM, con el fin de optimizar la calidad, precisión y consistencia de las respuestas relacionadas con **promedios de goles y predicción de resultados** en la Premier League.

---

## 1. Mejoras en Prompts

### 1.1 Claridad y Contexto
- Asegurar que cada prompt sea **claro, específico y sin ambigüedades**.
- Incluir **temporada, equipos y tipo de predicción** para reducir respuestas imprecisas.  
  **Ejemplo:**
  - ❌ "¿Cuántos goles en promedio se anotan?"
  - ✅ "¿Cuál fue el promedio de goles por partido en la temporada 2023/24?"

### 1.2 Formato de Respuesta Esperada
- Definir una **estructura uniforme** para las respuestas (ej. `[Promedio de goles] - [Temporada] - [Contexto del cálculo]`).
- Usar etiquetas o delimitadores si el resultado será procesado por otra herramienta.

### 1.3 Evitar Hallucinations
- Incluir instrucciones que **limiten el contenido** a la información confirmada en el dataset.
- **Ejemplo de instrucción preventiva:**  
  `"Si no tienes datos exactos para la temporada, responde 'No dispongo de esa información' en lugar de inventar un resultado."`

### 1.4 Pruebas A/B de Prompts
- Probar variantes de la misma pregunta para medir consistencia.
- Documentar cuál versión produce respuestas más precisas y coherentes.

---

## 2. Mejoras en el Dataset

### 2.1 Cobertura Completa
- Incluir todas las temporadas relevantes de la Premier League que el modelo debe manejar para cálculos de promedio y predicción.
- Mantener datos actualizados de goles anotados y recibidos antes de cada nueva etapa de entrenamiento.

### 2.2 Estructura y Normalización
- Homogeneizar formatos de:
  - Fechas (`YYYY-MM-DD`)
  - Nombres de equipos (usar nombre oficial)
  - Campos numéricos (goles, partidos jugados).
- Eliminar duplicados y registros inconsistentes.

### 2.3 Etiquetado y Metadatos
- Añadir metadatos útiles como:
  - Fuente del dato.
  - Fecha de actualización.
  - Contexto del cálculo (ej. liga, temporada, fase del torneo).

### 2.4 Datos para Predicción de Resultados
- Incluir:
  - Historial de goles anotados y recibidos por equipo.
  - Resultados previos entre rivales (head-to-head).
  - Promedios por condición (local / visitante).

---

## Plantilla de Registro de Mejoras

| Tipo de Mejora | Descripción | Ejemplo Actual | Propuesta de Mejora | Estado |
|----------------|-------------|---------------|---------------------|--------|
| Prompt | Hacer más específica la pregunta sobre promedios | "¿Cuál es el promedio de goles?" | "¿Cuál fue el promedio de goles por partido en la temporada 2023/24?" | Pendiente |
| Dataset | Normalizar nombres de equipos | "Man City" y "Manchester City" | Usar siempre "Manchester City" | En progreso |
| Prompt | Evitar hallucinations | Modelo inventa datos para temporadas sin información | Incluir instrucción de no responder sin datos confirmados | Pendiente |

---

## Beneficios Esperados
- Mayor **consistencia** en los cálculos de promedio de goles.
- Respuestas más precisas en la **predicción de resultados**.
- Reducción de errores y datos inventados.
- Documentación clara para futuras iteraciones del proyecto.

---
