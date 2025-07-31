# Testing del Modelo LLM - Premier League

El proceso de pruebas estará enfocado principalmente en **tests unitarios basados en prompts**, diseñados para evaluar el comportamiento del modelo LLM entrenado con datos de la Premier League.  
Las pruebas buscarán verificar aspectos clave como:

- **Consistencia de respuestas**: el modelo debe entregar resultados coherentes ante preguntas similares o equivalentes.  
- **Velocidad de respuesta**: se medirá el tiempo que tarda el modelo en generar una respuesta para distintos tipos de consultas.  
- **Precisión y relevancia**: se validará si el contenido generado corresponde correctamente a los datos reales de la Premier League (jugadores, estadísticas, temporadas, etc.).

---

## Metodología

Cada prueba consistirá en un prompt controlado, y se evaluarán los resultados mediante:

- Comparaciones con respuestas esperadas.
- Repetición del mismo prompt en diferentes sesiones para analizar estabilidad.
- Evaluación manual o automática según sea necesario.

---

Este enfoque permitirá asegurar que el modelo responde correctamente y de forma predecible ante diferentes tipos de inputs relacionados con la liga.
