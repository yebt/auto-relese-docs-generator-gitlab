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
- **Formato compatible** con WhatsApp y Telegram
- **Emojis visuales** para identificar rápidamente el tipo de cambio
- **Análisis con IA** usando Gemini para comprender el contexto de los cambios
- **Spinners de progreso** con Halo para mejor UX

## 🎯 ¿Qué genera?

Cada ejecución crea una carpeta en `results/` con el formato: `{release}_{timestamp}/`

Dentro encontrarás:
- `Changelog_comercial_{release}.md` - Para comunicación con clientes
- `Changelog_tech_{release}.md` - Para el equipo técnico

### Estructura del Changelog Comercial

- ✨ Nuevas características (🟢)
- 🔧 Mejoras (🔵)
- 🐛 Correcciones (🟡)
- ⚠️ Cambios importantes (🔴)
- 💡 Valor aportado
- 🎯 Objetivos alcanzados

### Estructura del Changelog Técnico

- ✨ Nuevas funcionalidades (🟢)
- 🔧 Mejoras técnicas (🔵)
- 🐛 Bugs corregidos (🟡)
- ⚠️ Breaking changes (🔴)
- 🏗️ Cambios de arquitectura (🟣)
- 📦 Dependencias
- ⚡ Performance
- 🔒 Seguridad
- 🧪 Testing

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
GEMINI_TOKEN=tu_api_key_de_gemini
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

### Gemini API Key

1. Ve a Google AI Studio: https://aistudio.google.com/app/apikey
2. Crea una nueva API key
3. Copia la clave generada

## 🚀 Uso

### Ejecución básica

Genera changelogs entre los últimos dos tags del repositorio:

```bash
python main.py
```

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
```

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
│   └── changelog_generator.py   # Generador principal
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
├── INSTALLATION_TEST.md         # Pruebas de instalación
├── PROJECT_OVERVIEW.md          # Visión general del proyecto
├── SAMPLE_OUTPUT.md             # Ejemplos de salida
└── TROUBLESHOOTING.md           # Solución de problemas
```

## 📦 Dependencias Principales

- **python-gitlab**: Cliente para la API de GitLab
- **google-genai**: Cliente para Gemini AI
- **halo**: Spinners de progreso
- **python-dotenv**: Manejo de variables de entorno

## 🔄 Flujo de Trabajo

1. **Conexión**: Se conecta a GitLab y Gemini AI
2. **Tags**: Obtiene los últimos dos tags del repositorio
3. **Commits**: Extrae todos los commits entre esos tags
4. **Detalles**: Obtiene información detallada de cada commit (mensaje, diffs, stats)
5. **Análisis**: Envía el contexto a Gemini AI para análisis
6. **Generación**: Crea dos changelogs con diferentes enfoques
7. **Guardado**: Almacena los archivos en `results/`

## 🎨 Formato de Salida

Los changelogs están optimizados para compartir en mensajería:

- **Formato Markdown** compatible con WhatsApp/Telegram
- **Emojis** para identificación visual rápida
- **Negrita** para títulos y secciones importantes
- **Listas** organizadas por tipo de cambio
- **Colores** mediante emojis (🟢 verde, 🔵 azul, 🟡 amarillo, 🔴 rojo, 🟣 morado)

## ⚠️ Requisitos

- Python 3.8 o superior
- Acceso a un repositorio GitLab con al menos 2 tags
- Token de acceso de GitLab con permisos adecuados
- API Key de Gemini AI
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

### Error de Gemini AI
- Verifica que la API key es válida
- Confirma que tienes cuota disponible en tu cuenta de Google AI
- Revisa la conectividad a internet

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
