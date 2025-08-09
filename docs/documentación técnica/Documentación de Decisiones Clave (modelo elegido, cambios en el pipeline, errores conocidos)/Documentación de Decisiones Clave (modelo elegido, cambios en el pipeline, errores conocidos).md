**Documentación de Decisiones Clave (modelo elegido, cambios en el pipeline, errores conocidos)**

Decisión sobre el Modelo de Lenguaje

Para el desarrollo del sistema conversacional del proyecto LLM Deportivo, se optó por siguiente:

- Capacidad de comprensión contextual amplia.
- Flexibilidad para adaptación con datos propios del dominio deportivo.
- Rendimiento sólido en generación de texto, respuestas explicativas y razonamiento estructurado.

La elección del modelo se basó en pruebas de generación, documentación técnica disponible, capacidad de integración con otros módulos (como búsqueda semántica y visualización), así como en criterios de escalabilidad, privacidad y eficiencia.

Cambios Realizados en el Pipeline del Proyecto

- Se incorporó una etapa intermedia de verificación semántica para asegurar que las respuestas generadas fueran coherentes y específicas al dominio deportivo.
- Se amplió la limpieza y normalización de datos debido a errores de codificación, ruido textual y formatos inconsistentes.
- Se agregó una fase de validación cruzada entre respuestas para evaluar la estabilidad del modelo ante preguntas similares en distintos contextos.
- Se incluyó una etapa de pruebas con usuarios simulados para identificar errores frecuentes, ambigüedades y oportunidades de mejora en el diseño de los prompts.

Errores Conocidos 

- Respuestas poco específicas ante preguntas amplias: el modelo tiende a generalizar cuando la pregunta carece de contexto temporal o nombres concretos.
- Inestabilidad en preguntas comparativas: ante consultas como “¿Quién es mejor entre X e Y?”, el modelo ofrece respuestas variables con justificaciones inconsistentes.
- Problemas con unidades o métricas no normalizadas: algunas respuestas mezclaban formatos (por ejemplo, minutos vs. horas), afectando la claridad.
- Sobrecarga semántica al exceder el límite de tokens: cuando el prompt incluye demasiada información, disminuye la coherencia de la respuesta.
- Sensibilidad a errores de redacción en el prompt**:** si la pregunta está mal escrita, el modelo presenta dificultades para interpretar la intención del usuario.

