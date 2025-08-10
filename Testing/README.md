# 🧪 LLM Premier League - Testing Suite

Sistema completo de testing para evaluar y comparar el rendimiento entre **Claude AI mode** y **Local mode**.

## 📋 Descripción General

Esta suite de testing evalúa:
- **Rendimiento**: Tiempos de respuesta, throughput, confiabilidad
- **Calidad**: Precisión de predicciones, calidad de análisis, conversaciones
- **Carga**: Capacidad bajo múltiples usuarios concurrentes
- **Stress**: Límites del sistema y puntos de quiebre

## 🗂️ Estructura de Archivos

```
testing/
├── performance_test.py      # Tests de rendimiento básico
├── quality_test.py          # Tests de calidad de respuestas  
├── load_stress_test.py      # Tests de carga y stress
├── run_all_tests.py         # Master runner - ejecuta todo
├── results/                 # Directorio de resultados
└── README.md               # Esta documentación
```

## 🚀 Ejecución Rápida

### Prerequisitos
1. **Servidor API corriendo**:
   ```bash
   cd /Users/rios/Desktop/LLM-PREMIER
   python LLM/api_server_optimized.py
   ```

2. **Dependencias instaladas**:
   ```bash
   pip install requests statistics concurrent.futures
   ```

### Ejecutar Todo (Recomendado)
```bash
cd testing
python run_all_tests.py
```
**Duración**: 30-45 minutos  
**Output**: Reporte completo + archivos JSON con resultados

### 💸 Ejecutar Tests Económicos (Budget-Friendly)
```bash
cd testing
python budget_test.py
```
**Duración**: ~7 minutos  
**Output**: Insights básicos con <10 requests vs 200+ de la suite completa
**Ideal para**: Desarrollo iterativo, pruebas rápidas, wallets limitados

### Ejecutar Tests Individuales

#### 💸 Tests Económicos (Recomendado para desarrollo)

##### Quick Test (3-5 min)
```bash
python quick_test.py
```
- Solo 6 requests totales
- Compara velocidad LOCAL vs CLAUDE AI
- Resultados básicos pero útiles

##### Mini Quality Test (2 min)
```bash
python mini_quality_test.py
```
- Solo 4 requests totales
- Evaluación básica de calidad
- Perfecto para iteración rápida

#### 🚀 Tests Completos (Para análisis profundo)

#### 1. Test de Rendimiento (10-15 min)
```bash
python performance_test.py
```
- Compara velocidad LOCAL vs CLAUDE AI
- Mide todas las endpoints
- Estadísticas detalladas

#### 2. Test de Calidad (5-8 min)
```bash
python quality_test.py
```
- Evalúa precisión de predicciones
- Calidad de análisis de equipos
- Naturalidad de conversaciones

#### 3. Test de Carga y Stress (15-20 min)
```bash
python load_stress_test.py
```
- Tests con múltiples usuarios concurrentes
- Escalamiento progresivo hasta punto de quiebre
- Capacidad del servidor

## 📊 Interpretación de Resultados

### Performance Test Results
```json
{
  "claude_ai_off": {
    "summary": {
      "avg_response_time": 0.15,    // Segundos promedio
      "success_rate": 0.98,         // % de requests exitosos
      "requests_per_second": 12.5   // Throughput
    }
  },
  "claude_ai_on": {
    "summary": {
      "avg_response_time": 2.3,     // Más lento pero más inteligente
      "success_rate": 0.95,
      "requests_per_second": 3.2
    }
  }
}
```

### Quality Test Results
```json
{
  "claude_ai_off": {
    "summary": {
      "overall_quality_score": 0.65,  // Score 0-1
      "category_scores": {
        "predictions": 0.7,           // Bueno en predicciones
        "analysis": 0.6,              // Básico en análisis
        "chat": 0.65                  // Conversacional limitado
      }
    }
  }
}
```

### Load Test Results
```json
{
  "stress_escalation": {
    "20": {
      "success_rate": 0.95,
      "avg_response_time": 1.2
    },
    "40": {
      "success_rate": 0.78,          // Punto de degradación
      "avg_response_time": 3.5
    }
  }
}
```

## 🎯 Casos de Uso

### Desarrollo y Optimización
```bash
# Test rápido después de cambios
python performance_test.py

# Verificar calidad después de ajustes
python quality_test.py
```

### Pre-Producción
```bash
# Suite completa antes de deploy
python run_all_tests.py
```

### Monitoreo Continuo
```bash
# Script automatizable para CI/CD
python performance_test.py --quick-mode
```

## 📈 Métricas Clave

### Rendimiento
- **Response Time**: < 1s LOCAL, < 5s CLAUDE AI
- **Success Rate**: > 95% ambos modos
- **Throughput**: 10+ RPS LOCAL, 3+ RPS CLAUDE AI

### Calidad
- **Predictions**: Score > 0.7 LOCAL, > 0.8 CLAUDE AI
- **Analysis**: Score > 0.6 LOCAL, > 0.9 CLAUDE AI
- **Chat**: Score > 0.6 LOCAL, > 0.8 CLAUDE AI

### Carga
- **Concurrent Users**: 20+ LOCAL, 15+ CLAUDE AI
- **Breaking Point**: 50+ usuarios LOCAL, 30+ CLAUDE AI
- **Resource Usage**: CPU/Memory monitoring

## 🔧 Personalización

### Agregar Nuevos Tests

1. **Crear test personalizado**:
```python
def my_custom_test():
    # Test específico para tu caso de uso
    pass
```

2. **Agregar al master runner**:
```python
self.test_suite['custom'] = {
    'script': 'my_test.py',
    'description': 'Mi Test Personalizado',
    'duration_estimate': '5 minutos'
}
```

### Configurar Endpoints de Test
```python
# En cualquier script, modifica:
self.test_endpoints = [
    {'name': 'mi_endpoint', 'method': 'POST', 'path': '/mi-api', 
     'payload': {'param': 'value'}}
]
```

### Ajustar Parámetros de Carga
```python
self.test_scenarios = {
    'light_load': {'users': 3, 'requests_per_user': 5, 'delay': 1.0},
    'custom_load': {'users': 15, 'requests_per_user': 10, 'delay': 0.3}
}
```

## 🚨 Troubleshooting

### Error: "Servidor API no disponible"
```bash
# Verificar servidor
curl http://localhost:8080/api/health

# Reiniciar servidor
python LLM/api_server_optimized.py
```

### Error: "Timeout exceeded"
- Aumentar timeouts en scripts
- Verificar recursos del sistema
- Reducir carga de test

### Error: "Toggle AI mode failed"
- Verificar archivo `.env` 
- Confirmar API keys válidas
- Revisar logs del servidor

### Resultados Inconsistentes
- Ejecutar múltiples veces
- Verificar carga del sistema
- Cerrar aplicaciones pesadas

## 📋 Checklist Pre-Testing

- [ ] Servidor API corriendo en puerto 8080
- [ ] Archivo `.env` configurado correctamente
- [ ] Claude API key válida (si testeas AI mode)
- [ ] Sistema con recursos suficientes
- [ ] Directorio `testing/results/` creado
- [ ] Sin otras cargas pesadas en el sistema

## 📊 Archivos de Resultados

Todos los resultados se guardan automáticamente:

```
testing/results/
├── performance_results_YYYYMMDD_HHMMSS.json
├── quality_results_YYYYMMDD_HHMMSS.json  
├── load_stress_results_YYYYMMDD_HHMMSS.json
└── master_test_results_YYYYMMDD_HHMMSS.json
```

Cada archivo incluye:
- Timestamp de ejecución
- Resultados detallados por modo
- Estadísticas calculadas
- Datos raw para análisis posterior

## 🎯 Recomendaciones

### Para Desarrollo
1. Ejecutar `performance_test.py` después de cada cambio significativo
2. Usar `quality_test.py` para validar mejoras en respuestas
3. Ejecutar suite completa antes de commits importantes

### Para Producción
1. Ejecutar suite completa mensualmente
2. Monitorear degradación de rendimiento
3. Establecer alertas basadas en métricas clave
4. Usar resultados para planificar scaling

### Para Análisis
1. Comparar resultados históricos
2. Identificar patrones de degradación
3. Optimizar basado en bottlenecks encontrados
4. Ajustar configuraciones según uso real

---

**💡 Tip**: Ejecuta `python run_all_tests.py` para obtener un reporte completo que te ayudará a tomar decisiones informadas sobre qué modo usar en qué situaciones.
