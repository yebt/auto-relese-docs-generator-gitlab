# 📊 Project Overview

## 🎯 Objetivo del Proyecto

Automatizar la generación de changelogs profesionales para releases de software, creando dos documentos diferenciados:
1. **Changelog Comercial**: Para equipos de ventas y clientes
2. **Changelog Técnico**: Para equipos de desarrollo

## 🏗️ Arquitectura

```
┌─────────────────┐
│   main.py       │  ← Punto de entrada
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  changelog_generator.py             │
│  ┌───────────────────────────────┐  │
│  │ 1. GitLab API Integration     │  │
│  │    - Fetch tags               │  │
│  │    - Get commits              │  │
│  │    - Extract diffs            │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │ 2. Context Preparation        │  │
│  │    - Format commit data       │  │
│  │    - Prepare for AI           │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │ 3. Gemini AI Analysis         │  │
│  │    - Generate commercial doc  │  │
│  │    - Generate technical doc   │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │ 4. File Generation            │  │
│  │    - Save to results/         │  │
│  │    - Format for messaging     │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  results/{release}_{timestamp}/     │
│  ├── Changelog_comercial_xxx.md     │
│  └── Changelog_tech_xxx.md          │
└─────────────────────────────────────┘
```

## 📁 Estructura de Archivos

```
auto-relese-docs-generator-gitlab/
│
├── 📄 main.py                      # Punto de entrada principal
├── 📄 requirements.txt             # Dependencias Python
├── 📄 .env.example                 # Template de configuración
├── 📄 .gitignore                   # Archivos ignorados por Git
│
├── 🔧 setup.sh                     # Script de instalación (Linux/Mac)
├── 🔧 setup.bat                    # Script de instalación (Windows)
│
├── 📚 README.md                    # Documentación principal
├── 📚 QUICKSTART.md                # Guía rápida de inicio
├── 📚 TROUBLESHOOTING.md           # Solución de problemas
├── 📚 SAMPLE_OUTPUT.md             # Ejemplos de salida
├── 📚 PROJECT_OVERVIEW.md          # Este archivo
│
├── 📂 src/                         # Código fuente
│   ├── __init__.py                 # Inicialización del paquete
│   ├── changelog_generator.py     # Generador principal
│   └── alert.py                    # Utilidades de alertas
│
└── 📂 results/                     # Changelogs generados (auto-creado)
    └── {release}_{timestamp}/
        ├── Changelog_comercial_{release}.md
        └── Changelog_tech_{release}.md
```

## 🔄 Flujo de Trabajo Detallado

### 1. Inicialización
```python
generator = ChangelogGenerator()
# - Carga variables de entorno desde .env
# - Valida credenciales
# - Inicializa clientes (GitLab, Gemini)
```

### 2. Conexión a Servicios
```python
generator.connect_gitlab()
# - Autentica con GitLab API
# - Obtiene referencia al proyecto

generator.connect_gemini()
# - Inicializa cliente de Gemini AI
# - Valida API key
```

### 3. Obtención de Tags
```python
latest_tag, previous_tag = generator.get_last_two_tags()
# - Lista todos los tags del repositorio
# - Ordena por fecha de actualización
# - Retorna los 2 más recientes
```

### 4. Extracción de Commits
```python
commits = generator.get_commits_between_tags(latest_tag, previous_tag)
# - Obtiene SHA de ambos tags
# - Lista commits en el rango
# - Filtra commits relevantes
```

### 5. Análisis Detallado
```python
commit_details = generator.get_commit_details(commits)
# Para cada commit:
# - Mensaje completo
# - Autor y fecha
# - Estadísticas (additions/deletions)
# - Diffs de archivos modificados
```

### 6. Preparación de Contexto
```python
context = generator.prepare_context_for_gemini(commit_details, latest_tag)
# - Formatea información de commits
# - Estructura datos para IA
# - Limita tamaño para evitar límites de tokens
```

### 7. Generación con IA
```python
commercial = generator.generate_commercial_changelog(context, latest_tag)
# - Envía contexto a Gemini
# - Usa prompt especializado para audiencia comercial
# - Retorna changelog formateado

technical = generator.generate_technical_changelog(context, latest_tag)
# - Envía contexto a Gemini
# - Usa prompt especializado para audiencia técnica
# - Retorna changelog formateado
```

### 8. Guardado de Archivos
```python
output_dir = generator.save_changelogs(commercial, technical, latest_tag)
# - Crea directorio results/ si no existe
# - Crea subdirectorio con release y timestamp
# - Guarda ambos archivos .md
# - Retorna path del directorio
```

## 🔌 Integraciones

### GitLab API
- **Librería**: `python-gitlab`
- **Endpoints usados**:
  - `/api/v4/projects/{id}/tags` - Listar tags
  - `/api/v4/projects/{id}/repository/commits` - Listar commits
  - `/api/v4/projects/{id}/repository/commits/{sha}` - Detalles de commit
  - `/api/v4/projects/{id}/repository/commits/{sha}/diff` - Diffs

### Gemini AI
- **Librería**: `google-genai`
- **Modelo**: `gemini-2.0-flash-exp`
- **Uso**: Análisis de contexto y generación de texto estructurado

### Otros
- **halo**: Spinners de progreso
- **python-dotenv**: Gestión de variables de entorno

## 🎨 Características Clave

### 1. Formato Compatible con Mensajería
- ✅ WhatsApp
- ✅ Telegram
- ✅ Slack
- ✅ Discord
- Usa formato Markdown con emojis

### 2. Código de Colores con Emojis
| Emoji | Color | Significado |
|-------|-------|-------------|
| 🟢 | Verde | Nueva característica |
| 🔵 | Azul | Mejora/Optimización |
| 🟡 | Amarillo | Bug fix |
| 🔴 | Rojo | Breaking change |
| 🟣 | Morado | Cambio arquitectónico |

### 3. Dos Perspectivas
**Comercial**:
- Sin jerga técnica
- Enfoque en valor para el cliente
- Lenguaje claro y profesional

**Técnico**:
- Detalles de implementación
- Archivos y funciones modificadas
- Impacto en arquitectura

### 4. Análisis Inteligente
Gemini AI analiza:
- Mensajes de commit
- Diffs de código
- Estadísticas de cambios
- Patrones en modificaciones

## 🔒 Seguridad

### Variables de Entorno
```bash
# Credenciales NUNCA en código
# Siempre en .env (ignorado por Git)
GITLAB_ACCESS_TOKEN=secret
GITLAB_PROJECT_ID=12345
GEMINI_TOKEN=secret
```

### Tokens de GitLab
- Usar tokens con permisos mínimos necesarios
- Scopes requeridos: `api`, `read_api`, `read_repository`
- Rotar tokens periódicamente

### API Keys de Gemini
- No compartir keys
- Monitorear uso y cuotas
- Usar límites de rate

## 📊 Métricas y Limitaciones

### Límites de GitLab API
- Rate limit: 600 requests/minuto (autenticado)
- Paginación: 100 items por página (default)

### Límites de Gemini AI
- Tokens por request: ~30,000 (input)
- Tokens por minuto: Depende del plan
- Requests por día: Depende del plan

### Optimizaciones Implementadas
- Limitar diffs a primeros 5 archivos por commit
- Truncar diffs a primeras 20 líneas
- Procesar commits en batch

## 🧪 Testing

### Manual Testing
```bash
# 1. Verificar conexión GitLab
python -c "from src.changelog_generator import ChangelogGenerator; g = ChangelogGenerator(); g.connect_gitlab()"

# 2. Verificar conexión Gemini
python -c "from src.changelog_generator import ChangelogGenerator; g = ChangelogGenerator(); g.connect_gemini()"

# 3. Ejecución completa
python main.py
```

### Validación de Salida
- ✅ Archivos .md creados
- ✅ Formato Markdown válido
- ✅ Emojis presentes
- ✅ Secciones estructuradas
- ✅ Contenido coherente

## 🚀 Mejoras Futuras

### Corto Plazo
- [ ] Soporte para más de 2 tags (comparar cualquier par)
- [ ] Modo interactivo para seleccionar tags
- [ ] Preview antes de guardar
- [ ] Exportar a PDF/HTML

### Mediano Plazo
- [ ] Soporte para GitHub/Bitbucket
- [ ] Plantillas personalizables
- [ ] Múltiples idiomas
- [ ] Integración con Jira/Linear

### Largo Plazo
- [ ] Web UI
- [ ] API REST
- [ ] Webhooks automáticos
- [ ] Machine learning para categorización

## 📈 Casos de Uso

### 1. Release Notes Automáticas
Generar changelogs al crear un nuevo tag:
```bash
git tag v1.2.0
git push --tags
python main.py
```

### 2. Comunicación con Clientes
- Copiar changelog comercial
- Enviar por WhatsApp/Email
- Cliente entiende cambios sin tecnicismos

### 3. Documentación Técnica
- Changelog técnico para wiki
- Referencia para developers
- Historial de cambios detallado

### 4. Retrospectivas
- Analizar trabajo realizado
- Identificar patrones
- Mejorar procesos

## 🤝 Contribuciones

### Cómo Contribuir
1. Fork el repositorio
2. Crear branch: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -m 'Add: nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request

### Estándares de Código
- Python 3.8+ compatible
- PEP 8 style guide
- Type hints donde sea posible
- Docstrings en funciones públicas

## 📞 Soporte

### Documentación
- **Inicio Rápido**: `QUICKSTART.md`
- **Guía Completa**: `README.md`
- **Problemas**: `TROUBLESHOOTING.md`
- **Ejemplos**: `SAMPLE_OUTPUT.md`

### Recursos
- GitLab API: https://docs.gitlab.com/ee/api/
- Gemini AI: https://ai.google.dev/docs
- Python-GitLab: https://python-gitlab.readthedocs.io/

---

**Versión**: 1.0.0  
**Última actualización**: 2025-10-08  
**Licencia**: MIT
