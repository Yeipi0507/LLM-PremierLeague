# LLM Deportivo

**LLM Deportivo** es un proyecto colaborativo que busca aprovechar modelos de lenguaje (LLM) para analizar, consultar y generar información relevante sobre la **Premier League de Inglaterra** (temporadas entre **2014 y 2024**). El objetivo principal es desarrollar una herramienta capaz de responder preguntas, generar estadísticas útiles y presentar datos de forma clara, usando un modelo de lenguaje entrenado con datos reales del fútbol inglés.

## Objetivo del Proyecto

Desarrollar un modelo LLM enfocado en datos deportivos de la Premier League, capaz de interactuar con usuarios a través de lenguaje natural para ofrecer:
- Estadísticas de jugadores y equipos.
- Historiales de partidos.
- Datos comparativos y análisis.
- Respuestas a preguntas futboleras complejas.

## Estructura inicial del proyecto

- `data/` → Conjuntos de datos recopilados (.csv, .json).
- `scripts/` → Limpieza, normalización y carga de datos.
- `model/` → Entrenamiento y fine-tuning del modelo LLM.
- `interface/` → Interfaz gráfica o prototipo de uso.
- `docs/` → Documentación, wireframes y manuales.
- `README.md` → Este archivo.

## Tecnologías (por definir o propuestas)

- Python + Pandas para procesamiento de datos.
- HuggingFace Transformers para el modelo LLM.
- PEFT o LoRA para fine-tuning eficiente.
- LLaMA y Claude para arquitectura base del modelo, usando la API de Anthropic.
- AWS (Amazon Web Services) para almacenamiento, despliegue y cómputo en la nube.
- Streamlit o Gradio (prototipo de interfaz).
- Google Sheets o Docs (coordinación del equipo).

## Equipo de trabajo

- Diego Díaz - Planificador de proyecto y gestor de tareas
- Gerardo Palmieri - Ingeniero de limpieza y preparación de datos
- Ángel Ramírez - Responsable de adquisición y validación de datos
- Goethe Ramírez - Coordinador de documentación y pruebas de modelo
- Arturo Ríos - Desarrollador backend e integrador de modelo
- Daniel Ávila - Documentación técnica y estrategia de prompts
- Darynka Morales - Diseño de experiencia y documentación técnica
- Juan Pablo Silva - Experiencia de usuario y QA funcional

**Cada integrante del equipo participa con responsabilidades específicas dentro del proyecto**, que abarcan desde la investigación y limpieza de datos, hasta el diseño de la interfaz, documentación técnica, y pruebas del modelo. Esta distribución de tareas permite un desarrollo colaborativo y estructurado del LLM Deportivo.

## Estado actual

> Proyecto en fase inicial. Recolección de datasets, diseño del enfoque y documentación básica en curso.

## Licencia

Este proyecto está licenciado bajo la **GNU General Public License v3.0 (GPL-3.0)**.  
Está destinado exclusivamente a fines académicos y sin fines de lucro.  
El uso de los datos, el código y las interfaces desarrolladas es libre, siempre y cuando se respete esta licencia, que garantiza la libertad de uso, modificación y distribución del software, siempre compartiendo las mejoras bajo las mismas condiciones.
