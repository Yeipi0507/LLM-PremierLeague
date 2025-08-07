# Toggleable Feature: External API Query vs. Local Context

Este archivo describe la funcionalidad de un toggle (interruptor) que controla el comportamiento del modelo LLM en cuanto a la obtención de información, dependiendo de si se desea usar únicamente contexto local o también realizar consultas a una API externa.

## Descripción

El sistema incluirá un toggle que permite elegir entre dos rutas distintas de funcionamiento del modelo LLM:

### 1. Toggle **ON** (Activado)

Cuando el toggle está activado:

- El modelo intentará responder a las consultas del usuario utilizando primero los datasets locales disponibles.
- **Si no se encuentra información suficiente en los datos locales**, se realizará una **consulta directa a la API de Anthropic** para obtener una respuesta más completa.

### 2. Toggle **OFF** (Desactivado)

Cuando el toggle está desactivado:

- El modelo se limitará a responder exclusivamente con la información que se encuentra en los datasets locales y el contexto proporcionado.
- **Si no hay datos suficientes**, el modelo devolverá un mensaje indicando que no se tiene información disponible en ese momento.

## Propósito

Este toggle permite:

- Mayor control sobre el flujo de información y costos asociados al uso de APIs externas.
- Un modo seguro y local cuando se desee trabajar sin dependencia de servicios externos o sin acceso a red.
- Flexibilidad en entornos donde se requieren distintas políticas de acceso a datos.

---

Este archivo puede ser movido o referenciado desde cualquier subcarpeta de `docs`, según la organización del proyecto.
