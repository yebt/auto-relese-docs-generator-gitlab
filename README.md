# 🚀 GitLab Changelog Generator with Gemini AI

Generador automático de changelogs para repositorios GitLab usando inteligencia artificial de Gemini. Crea dos tipos de documentos optimizados para diferentes audiencias.

> 📚 **[Ver Índice Completo de Documentación](INDEX.md)**

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

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd auto-relese-docs-generator-gitlab
```

### 2. Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate  # En Linux/Mac
# o
venv\Scripts\activate  # En Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

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

```bash
python main.py
```

### Ejecución del módulo directamente

```bash
python -m src.changelog_generator
```

## 📁 Estructura del Proyecto

```
auto-relese-docs-generator-gitlab/
├── src/
│   ├── alert.py                 # Utilidades de alertas
│   └── changelog_generator.py   # Generador principal
├── results/                     # Changelogs generados (auto-creado)
│   └── {release}_{timestamp}/
│       ├── Changelog_comercial_{release}.md
│       └── Changelog_tech_{release}.md
├── .env                         # Credenciales (no versionado)
├── .env.example                 # Plantilla de credenciales
├── .gitignore
├── main.py                      # Punto de entrada
├── requirements.txt             # Dependencias
└── README.md                    # Este archivo
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

## 📝 Notas

- Los archivos `.env` están en `.gitignore` por seguridad
- La carpeta `results/` se crea automáticamente si no existe
- Cada ejecución crea una nueva carpeta con timestamp
- Los diffs muy largos se truncan para evitar límites de tokens

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT.

## 👥 Autor

Desarrollado para automatizar la generación de changelogs y mejorar la comunicación entre equipos técnicos y comerciales.

---

**¿Preguntas o problemas?** Abre un issue en el repositorio.
