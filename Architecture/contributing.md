# 🤝 Guía de Contribución - LLM Premier League

## ¡Bienvenido!

Gracias por tu interés en contribuir al proyecto LLM Premier League. Esta guía te ayudará a realizar contribuciones efectivas al proyecto.

---

## 🎯 Tipos de Contribuciones

### 🐛 **Bug Reports**
- Errores en predicciones
- Problemas de rendimiento
- Fallos en la API
- Issues del frontend

### ✨ **Feature Requests**
- Nuevas funcionalidades
- Mejoras en la UI/UX
- Nuevas métricas estadísticas
- Integraciones adicionales

### 📖 **Documentación**
- Mejorar guías existentes
- Añadir ejemplos
- Traducir contenido
- Crear tutoriales

### 🔧 **Código**
- Correción de bugs
- Implementación de features
- Optimizaciones de rendimiento
- Refactoring

---

## 🚀 Proceso de Contribución

### 1. **Setup Inicial**
```bash
# Fork el repositorio en GitHub
# Clonar tu fork
git clone https://github.com/TU-USERNAME/LLM-PremierLeague.git
cd LLM-PremierLeague

# Añadir remote upstream
git remote add upstream https://github.com/ArthurzKV/LLM-PremierLeague.git

# Crear rama para tu feature
git checkout -b feature/tu-nueva-funcionalidad
```

### 2. **Configurar Entorno de Desarrollo**
```bash
# Crear entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependencias de desarrollo
pip install -r requirements.txt
pip install pytest black flake8 coverage

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones
```

### 3. **Desarrollo**
```bash
# Hacer tus cambios
# Seguir las convenciones de código (ver abajo)

# Ejecutar tests
pytest tests/

# Verificar formato de código
black --check .
flake8 .

# Verificar que todo funciona
python LLM/api_server_optimized.py
```

### 4. **Commit y Push**
```bash
# Añadir cambios
git add .

# Commit con mensaje descriptivo (ver convenciones)
git commit -m "feat: añadir predicción por jugador específico"

# Push a tu fork
git push origin feature/tu-nueva-funcionalidad
```

### 5. **Pull Request**
- Crear PR desde tu fork al repositorio principal
- Usar el template de PR (ver abajo)
- Esperar review y responder comentarios
- Hacer cambios solicitados si es necesario

---

## 📝 Convenciones de Código

### **Python Style Guide**
Seguimos PEP 8 con algunas modificaciones:

```python
# ✅ Nombres de clases: PascalCase
class ClaudePremierLeagueLLM:
    pass

# ✅ Nombres de funciones y variables: snake_case
def predict_match(home_team, away_team):
    prediction_result = calculate_odds()

# ✅ Constantes: UPPER_SNAKE_CASE
MAX_RETRIES = 3
API_BASE_URL = "https://api.anthropic.com"

# ✅ Docstrings: Google style
def analyze_team(self, team_name: str) -> TeamAnalysis:
    """
    Analiza un equipo específico.
    
    Args:
        team_name: Nombre del equipo a analizar
        
    Returns:
        TeamAnalysis: Objeto con el análisis completo
        
    Raises:
        ValueError: Si el equipo no existe en los datos
    """
```

### **JavaScript Style Guide**
```javascript
// ✅ Usar camelCase
const updateAIModeIndicator = () => {
    const indicator = document.getElementById('aiModeIndicator');
};

// ✅ Usar const/let, no var
const API_BASE_URL = 'http://localhost:8080';
let currentPrediction = null;

// ✅ Funciones arrow para callbacks
teams.forEach(team => {
    console.log(team);
});

// ✅ Async/await en lugar de promises
const fetchPrediction = async (homeTeam, awayTeam) => {
    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            body: JSON.stringify({ home_team: homeTeam, away_team: awayTeam })
        });
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
    }
};
```

---

## 📋 Convenciones de Commits

Usamos **Conventional Commits**:

```
<type>(<scope>): <description>

<body>

<footer>
```

### **Types**
- `feat`: Nueva funcionalidad
- `fix`: Correción de bug  
- `docs`: Cambios en documentación
- `style`: Formato, punto y coma faltante, etc
- `refactor`: Refactoring de código
- `perf`: Mejora de rendimiento
- `test`: Añadir tests
- `chore`: Mantenimiento

### **Ejemplos**
```bash
feat(api): añadir endpoint para análisis de jugadores
fix(frontend): corregir cálculo de probabilidades en UI
docs(readme): actualizar instrucciones de instalación
style(llm): formatear código con black
refactor(data): simplificar procesamiento de estadísticas
perf(api): optimizar consultas de datos históricos
test(predictions): añadir tests para casos edge
chore(deps): actualizar dependencias de seguridad
```

---

## 🧪 Testing Guidelines

### **Estructura de Tests**
```
tests/
├── conftest.py              # Configuración pytest
├── test_llm.py              # Tests del motor principal
├── test_api.py              # Tests de endpoints
├── test_data_processing.py  # Tests de procesamiento
└── fixtures/                # Datos de prueba
    └── test_matches.csv
```

### **Escribir Tests**
```python
import pytest
from LLM.premier_league_llm import ClaudePremierLeagueLLM

def test_predict_match_valid_teams():
    """Test predicción con equipos válidos."""
    llm = ClaudePremierLeagueLLM()
    llm.load_data()
    
    prediction = llm.predict_match("Liverpool", "Chelsea")
    
    assert prediction.home_team == "Liverpool"
    assert prediction.away_team == "Chelsea"
    assert 0 <= prediction.win_probability_home <= 1
    assert prediction.confidence_score > 0

def test_predict_match_invalid_team():
    """Test predicción con equipo inválido."""
    llm = ClaudePremierLeagueLLM()
    llm.load_data()
    
    with pytest.raises(ValueError):
        llm.predict_match("Fake Team", "Chelsea")
```

### **Ejecutar Tests**
```bash
# Todos los tests
pytest

# Con coverage
pytest --cov=LLM

# Tests específicos
pytest tests/test_llm.py::test_predict_match_valid_teams

# Verbose output
pytest -v
```

---

## 📁 Estructura del Proyecto

### **Añadir Nuevos Archivos**
```
LLM-PremierLeague/
├── LLM/                    # Core del sistema
│   ├── premier_league_llm.py      # Motor principal ⚠️ CRÍTICO
│   ├── api_server_optimized.py    # Servidor API ⚠️ CRÍTICO
│   └── utils/              # Utilidades (nuevo)
│       ├── data_helpers.py
│       └── validation.py
├── front/                  # Frontend
│   ├── app.js             # ⚠️ CRÍTICO
│   ├── styles.css
│   └── components/        # Componentes (nuevo)
├── tests/                 # Tests (expandir)
├── docs/                  # Documentación (expandir)
└── scripts/               # Scripts de utilidad (nuevo)
    ├── setup.py
    └── deploy.py
```

### **Archivos Críticos (No Modificar Sin Coordinar)**
- `LLM/premier_league_llm.py` - Motor principal
- `LLM/api_server_optimized.py` - API server
- `front/app.js` - Frontend principal
- `.env` - Configuración
- `datasets/processed/dataset_2014-2024_clean.csv` - Datos

---

## 🎨 Template de Pull Request

```markdown
## 📋 Descripción

Breve descripción de los cambios realizados.

## 🎯 Tipo de Cambio

- [ ] Bug fix (cambio que corrige un problema)
- [ ] Nueva funcionalidad (cambio que añade funcionalidad)
- [ ] Breaking change (cambio que rompe funcionalidad existente)
- [ ] Documentación (cambio que solo afecta documentación)

## 🧪 Testing

- [ ] He añadido tests que prueban mi funcionalidad
- [ ] Todos los tests nuevos y existentes pasan
- [ ] He probado manualmente la funcionalidad

## 📝 Checklist

- [ ] Mi código sigue las convenciones del proyecto
- [ ] He revisado mi propio código
- [ ] He añadido comentarios, especialmente en áreas complejas
- [ ] He actualizado la documentación correspondiente
- [ ] Mis cambios no generan nuevos warnings

## 🖼️ Screenshots (si aplica)

Añadir screenshots de cambios en la UI.

## 📎 Información Adicional

Cualquier información adicional relevante para la review.
```

---

## 🐛 Template de Bug Report

```markdown
## 🐛 Descripción del Bug

Descripción clara y concisa del bug.

## 🔄 Pasos para Reproducir

1. Ir a '...'
2. Hacer click en '...'
3. Scroll hasta '...'
4. Ver error

## 📱 Comportamiento Esperado

Descripción clara de lo que esperabas que pasara.

## 📱 Comportamiento Actual

Descripción de lo que realmente pasa.

## 🖼️ Screenshots

Si aplica, añadir screenshots para explicar el problema.

## 🖥️ Información del Entorno

- OS: [e.g. macOS 14.0]
- Browser: [e.g. Chrome 119, Safari]
- Python Version: [e.g. 3.11.5]
- Claude AI Mode: [ON/OFF]

## 📎 Información Adicional

Cualquier otro contexto sobre el problema.
```

---

## ✨ Template de Feature Request

```markdown
## 🎯 ¿Tu feature request está relacionado con un problema?

Descripción clara del problema. Ej: "Me frustra cuando [...]"

## 💡 Describe la solución que te gustaría

Descripción clara y concisa de lo que quieres que pase.

## 🔄 Describe alternativas que has considerado

Descripción de soluciones alternativas o funcionalidades consideradas.

## 📋 Casos de Uso

¿Quién usaría esta funcionalidad y cómo?

## 🎨 Mockups/Ejemplos (opcional)

Cualquier imagen, wireframe o ejemplo que ayude a visualizar la funcionalidad.

## 📎 Información Adicional

Cualquier otro contexto o screenshots sobre la feature request.
```

---

## 🏷️ Labels del Proyecto

### **Priority**
- `priority:high` - Crítico, bloquea funcionalidad
- `priority:medium` - Importante pero no bloquea
- `priority:low` - Nice to have

### **Type**
- `bug` - Algo está roto
- `enhancement` - Nueva funcionalidad
- `documentation` - Mejoras en docs
- `question` - Pregunta o discusión

### **Area**
- `area:frontend` - Relacionado con UI/UX
- `area:backend` - Relacionado con API/LLM
- `area:data` - Relacionado con datasets
- `area:deployment` - Relacionado con deploy

### **Status**
- `status:in-progress` - En desarrollo
- `status:review-needed` - Listo para review
- `status:blocked` - Bloqueado por dependencia

---

## 🎉 Reconocimiento

Los contribuidores serán reconocidos en:
- README.md del proyecto
- Release notes
- Contributors page (cuando esté disponible)

### **Contribuidores Actuales**
- [@ArthurzKV](https://github.com/ArthurzKV) - Creator & Maintainer

---

## 💬 Comunicación

### **Canales**
- **GitHub Issues**: Para bugs y feature requests
- **GitHub Discussions**: Para preguntas generales
- **Pull Requests**: Para review de código

### **Response Time**
- Issues: 24-48 horas
- Pull Requests: 48-72 horas
- Questions: 24 horas

---

## ⚖️ Code of Conduct

### **Nuestro Compromiso**
Mantener un ambiente abierto, welcoming, diverso, inclusivo y saludable.

### **Comportamientos Esperados**
- ✅ Usar lenguaje welcoming e inclusivo
- ✅ Respetar puntos de vista diferentes
- ✅ Aceptar crítica constructiva
- ✅ Foco en lo que es mejor para la comunidad

### **Comportamientos Inaceptables**
- ❌ Lenguaje sexualizado o imagery
- ❌ Trolling, comentarios insultantes
- ❌ Harassment público o privado
- ❌ Publicar información privada de otros

---

**¡Gracias por contribuir a LLM Premier League! 🚀⚽**

*Si tienes preguntas, no dudes en abrir un issue o contactar a los maintainers.*
