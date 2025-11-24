# 🚀 GitLab Changelog Generator with Gemini AI

Generador automático de changelogs para repositorios GitLab usando inteligencia artificial de Gemini. Crea dos tipos de documentos optimizados para diferentes audiencias.

> 📚 **[Ver Índice Completo de Documentación](INDEX.md)**

## 🚀 Inicio Rápido

```bash
# 1. Instalar
./setup.sh  # o setup.bat en Windows

# 2. Configurar credenciales en .env
nano .env

# 3. Activar entorno virtual
source .venv/bin/activate

# 4. Ejecutar
python main.py
```

> 💡 **Primera vez?** Lee la [Guía de Inicio](GETTING_STARTED.md) o el [Quickstart](QUICKSTART.md)

## 📋 Características

- **Análisis automático** de commits entre los últimos dos tags del repositorio
- **Dos tipos de changelog**:
  - 📊 **Comercial**: Para equipos de ventas y clientes (sin jerga técnica)
  - 🔧 **Técnico**: Para equipos de desarrollo (con detalles de implementación)
- **Sistema de caché** 💾: Guarda progreso y permite recuperación ante interrupciones
- **Formato compatible** con WhatsApp y Telegram
- **Emojis visuales** para identificar rápidamente el tipo de cambio
- **Análisis con IA** usando Gemini CLI (local) o Gemini API
- **Procesamiento por lotes** para manejar grandes volúmenes de commits
- **Spinners de progreso** con Halo para mejor UX

## 🎯 ¿Qué genera?

Cada ejecución crea una carpeta en `results/` con el formato: `{release}_{timestamp}/`

Dentro encontrarás:
- `Changelog_comercial_{release}.md` - Para comunicación con clientes
- `Changelog_tech_{release}.md` - Para el equipo técnico

### Estructura del Changelog Comercial

- Nuevas características (ítems marcados con 🟢)
- Mejoras (ítems marcados con 🔵)
- Correcciones (ítems marcados con 🟡)
- Cambios importantes (ítems marcados con 🔴)
- Valor aportado
- Objetivos alcanzados

> Las secciones sin ítems reales no se incluyen en el changelog generado.

### Estructura del Changelog Técnico

- Nuevas funcionalidades (ítems marcados con 🟢)
- Mejoras técnicas (ítems marcados con 🔵)
- Bugs corregidos (ítems marcados con 🟡)
- Breaking changes (ítems marcados con 🔴)
- Cambios de arquitectura (ítems marcados con 🟣)
- Dependencias
- Performance
- Seguridad
- Testing

> Al igual que en el changelog comercial, las secciones sin contenido no se generan.

## 🛠️ Instalación

### Opción 1: Instalación Automática (Recomendada)

Usa los scripts de instalación incluidos:

```bash
# En Linux/Mac
./setup.sh

# En Windows
setup.bat
```

Estos scripts automáticamente:
- Crean el entorno virtual
- Instalan las dependencias
- Copian el archivo `.env.example` a `.env`
- Verifican la instalación

### Opción 2: Instalación Manual

#### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd auto-relese-docs-generator-gitlab
```

#### 2. Crear entorno virtual

```bash
python3 -m venv .venv
source .venv/bin/activate  # En Linux/Mac
# o
.venv\Scripts\activate  # En Windows
```

#### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

#### 4. Configurar variables de entorno

Copia el archivo de ejemplo y completa tus credenciales:

```bash
cp .env.example .env
```

Edita `.env` con tus credenciales:

```env
GITLAB_ACCESS_TOKEN=tu_token_de_gitlab
GITLAB_PROJECT_ID=tu_project_id
GEMINI_TOKEN=tu_api_key_de_gemini  # Solo necesario si usas --api
```

## 🔑 Obtener Credenciales

### GitLab Access Token

1. Ve a GitLab: https://gitlab.com/-/profile/personal_access_tokens
2. Crea un nuevo token con los siguientes scopes:
   - `api`
   - `read_api`
   - `read_repository`
3. Copia el token generado

### GitLab Project ID

1. Ve a tu proyecto en GitLab
2. Settings > General
3. El Project ID aparece en la parte superior

### Gemini CLI (Recomendado)

**Por defecto, el generador usa Gemini CLI** que se ejecuta localmente y evita problemas con peticiones grandes.

1. Instala Gemini CLI siguiendo las instrucciones oficiales:
   - Visita: https://ai.google.dev/gemini-api/docs/cli
2. Verifica la instalación:
   ```bash
   gemini --version
   ```

### Gemini API Key (Opcional)

Solo necesario si prefieres usar `--api` en lugar de Gemini CLI:

1. Ve a Google AI Studio: https://aistudio.google.com/app/apikey
2. Crea una nueva API key
3. Copia la clave generada
4. Agrégala a tu archivo `.env`

## 🚀 Uso

### Ejecución básica

Genera changelogs entre los últimos dos tags del repositorio usando Gemini CLI (por defecto):

```bash
python main.py
```

### Usar Gemini API en lugar de CLI

Si prefieres usar la API de Gemini (requiere GEMINI_TOKEN en .env):

```bash
python main.py --api
```

> ⚠️ **Nota**: La API puede rechazar peticiones con muchos commits. Se recomienda usar Gemini CLI (modo por defecto).

### Especificar tags personalizados

Puedes especificar los tags entre los cuales generar el changelog:

```bash
# Especificar ambos tags (desde el más antiguo al más reciente)
python main.py --from-tag v1.0.0 --to-tag v1.2.0

# Especificar solo el tag final (usará el tag anterior automáticamente)
python main.py --to-tag v1.2.0

# Especificar solo el tag inicial (usará el siguiente tag automáticamente)
python main.py --from-tag v1.0.0
```

### Activar entorno virtual

Recuerda activar el entorno virtual antes de ejecutar:

```bash
# En Linux/Mac
source .venv/bin/activate

# En Windows
.venv\Scripts\activate
```

### Ejemplos de uso

```bash
# Caso 1: Changelog del último release
python main.py

# Caso 2: Changelog entre dos versiones específicas
python main.py --from-tag v2.0.0 --to-tag v2.5.0

# Caso 3: Changelog desde una versión hasta la más reciente
python main.py --from-tag v2.0.0

# Caso 4: Changelog de la versión específica
python main.py --to-tag v2.5.0

# Caso 5: Con caché para recuperación ante interrupciones
python main.py --cache

# Caso 6: Con caché y tags específicos
python main.py --from-tag v2.0.0 --to-tag v2.5.0 --cache

# Caso 7: Usar Gemini API en lugar de CLI
python main.py --api

# Caso 8: Combinar API con caché
python main.py --api --cache --from-tag v2.0.0 --to-tag v2.5.0
```

### Uso del Sistema de Caché

El flag `--cache` habilita el sistema de caché que:
- Guarda los commits obtenidos entre tags
- Guarda incrementalmente cada detalle de commit
- Permite recuperar el trabajo si hay interrupciones (Ctrl+C, errores de API, etc.)

```bash
# Primera ejecución (interrumpida en commit 100/254)
python main.py --cache --from-tag v3.92.4 --to-tag v3.94.15
# Ctrl+C para interrumpir

# Segunda ejecución (continúa desde commit 101)
python main.py --cache --from-tag v3.92.4 --to-tag v3.94.15
# Carga 100 commits desde caché, continúa con los restantes
```

> 📖 **Documentación completa del caché**: [CACHE_USAGE.md](CACHE_USAGE.md)

### Ver ayuda

```bash
python main.py --help
```

## 📁 Estructura del Proyecto

```
auto-relese-docs-generator-gitlab/
├── src/
│   ├── __init__.py              # Inicialización del paquete
│   ├── alert.py                 # Utilidades de alertas
│   ├── cache_manager.py         # Gestor de caché
│   ├── gemini_cli_analyzer.py   # Analizador con Gemini CLI
│   └── changelog_generator.py   # Generador principal
├── .cache/                      # Caché de commits (auto-creado)
├── results/                     # Changelogs generados (auto-creado)
│   └── {release}_{timestamp}/
│       ├── Changelog_comercial_{release}.md
│       └── Changelog_tech_{release}.md
├── .env                         # Credenciales (no versionado)
├── .env.example                 # Plantilla de credenciales
├── .gitignore                   # Archivos ignorados por Git
├── main.py                      # Punto de entrada principal
├── requirements.txt             # Dependencias Python
├── setup.sh                     # Script de instalación (Linux/Mac)
├── setup.bat                    # Script de instalación (Windows)
├── README.md                    # Este archivo
├── INDEX.md                     # Índice de documentación
├── GETTING_STARTED.md           # Guía de inicio rápido
├── QUICKSTART.md                # Inicio rápido
├── USAGE_GUIDE.md               # Guía detallada de uso
├── CACHE_USAGE.md               # Documentación del sistema de caché
├── INSTALLATION_TEST.md         # Pruebas de instalación
├── PROJECT_OVERVIEW.md          # Visión general del proyecto
├── SAMPLE_OUTPUT.md             # Ejemplos de salida
└── TROUBLESHOOTING.md           # Solución de problemas
```

## 📦 Dependencias Principales

- **python-gitlab**: Cliente para la API de GitLab
- **google-genai**: Cliente para Gemini AI (solo para modo --api)
- **halo**: Spinners de progreso
- **python-dotenv**: Manejo de variables de entorno
- **Gemini CLI**: Herramienta de línea de comandos de Google (modo por defecto)

## 🔄 Flujo de Trabajo

### Modo CLI (Por defecto)

1. **Conexión**: Se conecta a GitLab y verifica Gemini CLI
2. **Tags**: Obtiene los últimos dos tags del repositorio
3. **Commits**: Extrae todos los commits entre esos tags
4. **Detalles**: Obtiene información detallada de cada commit (mensaje, diffs, stats)
5. **Análisis por lotes**: Divide commits en lotes y los analiza con Gemini CLI
6. **Categorización**: Gemini CLI categoriza cada commit (features, fixes, improvements, etc.)
7. **Generación**: Crea dos changelogs usando los commits categorizados
8. **Guardado**: Almacena los archivos en `results/`

### Modo API (Con --api)

1. **Conexión**: Se conecta a GitLab y Gemini API
2. **Tags**: Obtiene los últimos dos tags del repositorio
3. **Commits**: Extrae todos los commits entre esos tags
4. **Detalles**: Obtiene información detallada de cada commit
5. **Contexto**: Prepara todo el contexto en un solo documento
6. **Análisis**: Envía el contexto completo a Gemini API
7. **Generación**: Crea dos changelogs
8. **Guardado**: Almacena los archivos en `results/`

## 🎨 Formato de Salida

Los changelogs están optimizados para compartir en mensajería:

- **Formato Markdown** compatible con WhatsApp/Telegram
- **Emojis de colores solo en los ítems**, no en los títulos de sección
- **Negrita** para títulos y secciones importantes
- **Listas** organizadas por tipo de cambio
- **Colores** mediante emojis (🟢 verde, 🔵 azul, 🟡 amarillo, 🔴 rojo, 🟣 morado)
- **Secciones vacías omitidas** para mantener el texto conciso y legible

## ⚠️ Requisitos

- Python 3.8 o superior
- Acceso a un repositorio GitLab con al menos 2 tags
- Token de acceso de GitLab con permisos adecuados
- **Gemini CLI** instalado (modo por defecto) O **API Key de Gemini AI** (modo --api)
- Conexión a internet

## 🐛 Troubleshooting

### Error: "Missing required environment variables"
- Verifica que el archivo `.env` existe y contiene todas las variables
- Asegúrate de que no hay espacios extra en las credenciales

### Error: "Not enough tags found"
- El repositorio debe tener al menos 2 tags
- Verifica que los tags existen: `git tag -l`

### Error de conexión a GitLab
- Verifica que el token tiene los permisos correctos
- Confirma que el Project ID es correcto
- Revisa que el token no ha expirado

### Error de Gemini CLI
- Verifica que Gemini CLI está instalado: `gemini --version`
- Instala Gemini CLI desde: https://ai.google.dev/gemini-api/docs/cli
- Verifica que tienes permisos de ejecución

### Error de Gemini API (modo --api)
- Verifica que la API key es válida en tu archivo `.env`
- Confirma que tienes cuota disponible en tu cuenta de Google AI
- Revisa la conectividad a internet
- Si tienes muchos commits, considera usar el modo CLI (sin --api)

## 📤 Salida del Programa

Después de ejecutar, encontrarás los changelogs en:

```
results/{release}_{timestamp}/
├── Changelog_comercial_{release}.md
└── Changelog_tech_{release}.md
```

**Ejemplo de salida en consola:**

```
============================================================
🚀 GitLab Changelog Generator with Gemini AI
============================================================

✔ Connected to GitLab project: my-project
✔ Connected to Gemini AI
✔ Found tags: v1.2.0 (latest) and v1.1.0 (previous)
✔ Found 15 commits between tags
✔ Fetched details for 15 commits
✔ Context prepared
✔ Commercial changelog generated
✔ Technical changelog generated
✔ Changelogs saved to: results/v1.2.0_20251106_163530

============================================================
✅ Changelog generation completed successfully!
============================================================

📁 Output directory: /path/to/results/v1.2.0_20251106_163530
📄 Files generated:
   - Changelog_comercial_v1.2.0.md
   - Changelog_tech_v1.2.0.md

💬 Files are formatted for WhatsApp/Telegram sharing
```

> 📖 **Ver ejemplos completos**: [SAMPLE_OUTPUT.md](SAMPLE_OUTPUT.md)

## 📝 Notas Importantes

- ✅ Los archivos `.env` están en `.gitignore` por seguridad
- ✅ La carpeta `results/` se crea automáticamente si no existe
- ✅ Cada ejecución crea una nueva carpeta con timestamp único
- ✅ Los diffs muy largos se truncan para evitar límites de tokens de la IA
- ✅ Los changelogs están optimizados para compartir en WhatsApp/Telegram
- ✅ Se requiere al menos 2 tags en el repositorio para funcionar
- ⚠️ Revisa y edita los changelogs antes de compartir con clientes

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT.

## 📚 Documentación Adicional

Este proyecto incluye documentación completa:

- **[INDEX.md](INDEX.md)** - Índice completo de toda la documentación
- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Guía paso a paso para comenzar
- **[QUICKSTART.md](QUICKSTART.md)** - Inicio rápido de 5 minutos
- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - Guía detallada de uso y casos prácticos
- **[CACHE_USAGE.md](CACHE_USAGE.md)** - Documentación completa del sistema de caché
- **[INSTALLATION_TEST.md](INSTALLATION_TEST.md)** - Cómo verificar tu instalación
- **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** - Visión general técnica del proyecto
- **[SAMPLE_OUTPUT.md](SAMPLE_OUTPUT.md)** - Ejemplos reales de changelogs generados
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Solución de problemas comunes

## 👥 Autor

Desarrollado para automatizar la generación de changelogs y mejorar la comunicación entre equipos técnicos y comerciales.

---

**¿Preguntas o problemas?** 
- Consulta la [documentación completa](INDEX.md)
- Revisa [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Abre un issue en el repositorio
