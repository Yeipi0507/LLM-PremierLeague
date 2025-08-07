# 🔌 API Documentation - LLM Premier League

## Introducción
API RESTful para predicciones y análisis de la Premier League usando Claude AI y análisis estadístico.

**Base URL**: `http://localhost:8080`  
**Versión**: 1.0  
**Modo actual**: Claude AI + Datos Locales

---

## 🚀 Endpoints Disponibles

### 1. **Health Check**
```http
GET /api/health
```

**Respuesta:**
```json
{
  "status": "healthy",
  "llm_ready": true,
  "teams_loaded": 34,
  "ai_mode": "Claude AI Activo",
  "use_claude_ai": true,
  "model_version": "claude-opus-4-20250514",
  "data_range": "2014-2024",
  "timestamp": "2025-08-06T10:30:00Z"
}
```

### 2. **Lista de Equipos**
```http
GET /api/teams
```

**Respuesta:**
```json
{
  "success": true,
  "teams": [
    "Arsenal", "Chelsea", "Liverpool", "Man City", 
    "Man United", "Tottenham", "..."
  ],
  "total_teams": 34
}
```

### 3. **Predicción de Partido**
```http
POST /api/predict
```

**Request Body:**
```json
{
  "home_team": "Liverpool",
  "away_team": "Chelsea"
}
```

**Respuesta:**
```json
{
  "success": true,
  "prediction": {
    "home_team": "Liverpool",
    "away_team": "Chelsea",
    "predicted_home_goals": 2.1,
    "predicted_away_goals": 1.3,
    "win_probability_home": 0.52,
    "win_probability_draw": 0.23,
    "win_probability_away": 0.25,
    "confidence_score": 0.78,
    "expected_result": "Victoria Local",
    "key_insights": [
      "Liverpool tiene ventaja estadística en Anfield",
      "Chelsea ha mejorado defensivamente bajo Maresca",
      "Historial equilibrado en enfrentamientos directos"
    ],
    "reasoning": "Análisis completo considerando forma actual y estadísticas..."
  }
}
```

### 4. **Análisis de Equipo**
```http
POST /api/analyze
```

**Request Body:**
```json
{
  "team_name": "Arsenal"
}
```

### 5. **Chat con LLM**
```http
POST /api/chat
```

**Request Body:**
```json
{
  "question": "¿Quién será el máximo anotador esta temporada?"
}
```

---

## 🛠️ Feature Toggle

El sistema incluye un toggle para alternar entre:
- **Claude AI Mode**: Análisis avanzado con IA
- **Local Data Mode**: Solo estadísticas históricas

**Configuración**: Variable `USE_CLAUDE_AI` en `.env`

---

## 📊 Códigos de Respuesta

- `200` - Operación exitosa
- `400` - Error en parámetros
- `404` - Equipo no encontrado
- `500` - Error interno del servidor

---

## 🧪 Ejemplos de Uso

### JavaScript (Frontend)
```javascript
// Predicción de partido
const prediction = await fetch('http://localhost:8080/api/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    home_team: 'Liverpool',
    away_team: 'Chelsea'
  })
});
```

### Python
```python
import requests

response = requests.post('http://localhost:8080/api/predict', 
  json={'home_team': 'Liverpool', 'away_team': 'Chelsea'})
prediction = response.json()
```

### cURL
```bash
curl -X POST "http://localhost:8080/api/predict" \
  -H "Content-Type: application/json" \
  -d '{"home_team": "Liverpool", "away_team": "Chelsea"}'
```
