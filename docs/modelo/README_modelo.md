# README - Uso del Modelo LLM Deportivo

Este documento describe cómo utilizar el modelo LLM Deportivo una vez entrenado, con instrucciones claras sobre su instalación, carga, uso e integración. El modelo está enfocado en responder preguntas relacionadas con estadísticas y datos de la Premier League inglesa (2014-2024).

---

## Requisitos Previos

- Python 3.10+
- GPU (opcional pero recomendado)
- Instalar las dependencias necesarias:

```bash
pip install torch transformers peft accelerate langchain chromadb sentence-transformers
```

---

## Carga del Modelo

```python
from transformers import AutoTokenizer, AutoModelForCausalLM

model_path = "ruta/del/modelo"  # Puede ser local o repositorio HuggingFace
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)
```

---

## Inferencia: Hacer una pregunta

```python
prompt = "¿Quién fue el máximo goleador del Manchester City en 2021?"
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=100)
respuesta = tokenizer.decode(outputs[0], skip_special_tokens=True)

print(respuesta)
```

---

## Parámetros útiles

- `max_new_tokens`: Límite de tokens a generar.
- `temperature`: Controla la creatividad (0.2 para precisión, 1.0 para creatividad).
- `top_k`, `top_p`: Filtrado de tokens para respuestas más coherentes.

---

## Ejemplos de uso esperados

| Prompt | Resultado esperado |
|--------|--------------------|
| ¿Cuántos títulos ganó el Chelsea desde 2010? | 2 Premier League, 1 Champions, etc. |
| ¿Qué delantero tuvo más asistencias en la temporada 2022-2023? | Kevin De Bruyne (según datos) |

---

## Posibles errores y soluciones

- **Out of memory**: reducir `max_new_tokens` o usar `model.to("cuda")` si se tiene GPU.
- **Error de tokenizer**: asegúrarse de que `tokenizer` y `model` coincidan.
- **Respuestas imprecisas**: verificar contexto, embeddings o formato de prompt.

---

## Integración con interfaz

Para conectar el modelo con una interfaz:

1. Desarrollar frontend con Streamlit, Gradio o Flask, etc.
2. Importar el modelo como backend.
3. Usar LangChain si se requiere orquestación más avanzada (RAG, filtros).

---

## Herramientas complementarias

- **LangChain**: para conectar búsqueda semántica + generación.
- **ChromaDB o Pinecone**: para embeddings y búsqueda vectorial.
- **Scikit-learn**: para filtros numéricos y clasificación.
- **Plotly/Matplotlib**: para visualizaciones estadísticas.

---

## Notas finales

Este modelo está en fase de desarrollo y evaluación. Las respuestas generadas están sujetas a los datos con los que fue entrenado, por lo que se hara validación continua y mejoras iterativas.
