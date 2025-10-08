# 🔧 Troubleshooting Guide

Guía completa para resolver problemas comunes.

## 📋 Tabla de Contenidos

- [Problemas de Instalación](#problemas-de-instalación)
- [Problemas de Configuración](#problemas-de-configuración)
- [Problemas de Conexión](#problemas-de-conexión)
- [Problemas de Ejecución](#problemas-de-ejecución)
- [Problemas con la Salida](#problemas-con-la-salida)

---

## Problemas de Instalación

### Error: `python3: command not found`

**Causa**: Python no está instalado o no está en el PATH.

**Solución**:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# macOS
brew install python3

# Windows
# Descargar desde https://www.python.org/downloads/
```

### Error: `pip install` falla con permisos

**Causa**: Intentando instalar sin virtual environment.

**Solución**:
```bash
# Crear y activar virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\activate.bat  # Windows

# Luego instalar
pip install -r requirements.txt
```

### Error: Dependencias no se instalan correctamente

**Causa**: pip desactualizado o caché corrupto.

**Solución**:
```bash
# Actualizar pip
pip install --upgrade pip

# Limpiar caché e instalar
pip cache purge
pip install -r requirements.txt --no-cache-dir
```

---

## Problemas de Configuración

### Error: `Missing required environment variables`

**Causa**: Archivo `.env` no existe o está incompleto.

**Solución**:
```bash
# Verificar que existe
ls -la .env

# Si no existe, crear desde template
cp .env.example .env

# Editar y completar todas las variables
nano .env  # o tu editor preferido
```

**Verificar formato correcto**:
```env
# ✅ CORRECTO
GITLAB_ACCESS_TOKEN=glpat-xxxxxxxxxxxx
GITLAB_PROJECT_ID=12345678
GEMINI_TOKEN=AIzaSyxxxxxxxxxx

# ❌ INCORRECTO (con espacios o comillas)
GITLAB_ACCESS_TOKEN = "glpat-xxxxxxxxxxxx"
GITLAB_PROJECT_ID = 12345678
```

### Error: Variables de entorno no se cargan

**Causa**: Archivo `.env` en ubicación incorrecta.

**Solución**:
```bash
# El .env debe estar en la raíz del proyecto
/home/user/auto-relese-docs-generator-gitlab/
├── .env  ← Aquí
├── main.py
└── src/
```

---

## Problemas de Conexión

### Error: `Failed to connect to GitLab`

**Posibles causas y soluciones**:

#### 1. Token inválido o expirado

```bash
# Verificar token en GitLab
# https://gitlab.com/-/profile/personal_access_tokens

# Crear nuevo token con scopes:
# - api
# - read_api
# - read_repository
```

#### 2. Project ID incorrecto

```bash
# Encontrar Project ID:
# 1. Ir a tu proyecto en GitLab
# 2. Settings > General
# 3. Copiar el número que aparece arriba
```

#### 3. Problemas de red/firewall

```bash
# Verificar conectividad
curl -H "PRIVATE-TOKEN: tu_token" https://gitlab.com/api/v4/user

# Si falla, verificar:
# - Firewall
# - Proxy
# - VPN
```

#### 4. GitLab self-hosted

Si usas GitLab self-hosted, modifica `src/changelog_generator.py`:

```python
# Línea ~40, cambiar:
self.gl = gitlab.Gitlab(
    url='https://tu-gitlab.com',  # Añadir tu URL
    private_token=self.gitlab_token
)
```

### Error: `Failed to connect to Gemini AI`

**Posibles causas y soluciones**:

#### 1. API Key inválida

```bash
# Verificar/crear nueva key:
# https://aistudio.google.com/app/apikey

# Probar key:
curl -H "Content-Type: application/json" \
     -d '{"contents":[{"parts":[{"text":"Hello"}]}]}' \
     "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=TU_API_KEY"
```

#### 2. Cuota excedida

- Verificar límites en Google AI Studio
- Esperar reset de cuota (diario/mensual)
- Considerar upgrade de plan

#### 3. Región bloqueada

- Gemini AI no está disponible en todos los países
- Usar VPN si es necesario
- Verificar disponibilidad: https://ai.google.dev/available_regions

---

## Problemas de Ejecución

### Error: `Not enough tags found`

**Causa**: El repositorio tiene menos de 2 tags.

**Solución**:
```bash
# Verificar tags existentes
git tag -l

# Si hay menos de 2, crear tags:
git tag v1.0.0
git tag v1.1.0
git push --tags
```

### Error: `No commits found between tags`

**Causa**: Los tags apuntan al mismo commit o están en orden inverso.

**Solución**:
```bash
# Verificar orden de tags
git log --oneline --decorate --graph

# Asegurarse que hay commits entre tags
git log v1.0.0..v1.1.0
```

### Error: `Failed to fetch commit details`

**Causa**: Permisos insuficientes o commits muy grandes.

**Solución**:
1. Verificar permisos del token (debe tener `read_repository`)
2. Si hay commits muy grandes, modificar límites en el código:
   ```python
   # En src/changelog_generator.py, línea ~150
   diff_lines = diff_item['diff'].split('\n')[:50]  # Aumentar límite
   ```

### Error: Token limit exceeded en Gemini

**Causa**: Demasiados commits o diffs muy grandes.

**Solución**:
```python
# Opción 1: Reducir commits procesados
# En src/changelog_generator.py, línea ~140
for diff_item in commit['diff'][:3]:  # Reducir de 5 a 3

# Opción 2: Reducir líneas de diff
diff_lines = diff_item['diff'].split('\n')[:10]  # Reducir de 20 a 10
```

### Script se cuelga en "Fetching commits..."

**Causa**: Repositorio muy grande o conexión lenta.

**Solución**:
- Esperar (puede tardar varios minutos)
- Verificar conexión a internet
- Considerar limitar número de commits:
  ```python
  # En src/changelog_generator.py, método get_commits_between_tags
  commits = self.project.commits.list(
      ref_name=tag1,
      all=True,
      per_page=50  # Añadir límite
  )
  ```

---

## Problemas con la Salida

### Los archivos no se generan

**Verificar**:
```bash
# 1. Permisos de escritura
ls -ld results/

# 2. Espacio en disco
df -h

# 3. Logs de error
python main.py 2>&1 | tee output.log
```

### Formato incorrecto en WhatsApp/Telegram

**Causa**: Algunos clientes no soportan todo el formato Markdown.

**Solución**:
- WhatsApp: Copiar y pegar directamente funciona
- Telegram: Usar "Enviar como archivo" para mejor formato
- Alternativa: Convertir a HTML:
  ```bash
  pip install markdown
  python -c "import markdown; print(markdown.markdown(open('results/xxx/Changelog_comercial_xxx.md').read()))" > output.html
  ```

### Contenido generado es genérico o incorrecto

**Causa**: Gemini AI no tiene suficiente contexto.

**Solución**:
1. Asegurarse que los commit messages sean descriptivos
2. Aumentar contexto en los prompts (editar `src/changelog_generator.py`)
3. Revisar y editar manualmente los changelogs generados

### Emojis no se ven correctamente

**Causa**: Terminal o editor no soporta emojis.

**Solución**:
- Usar terminal moderno (iTerm2, Windows Terminal, etc.)
- Abrir archivos en editor con soporte UTF-8
- Los emojis se verán correctamente en WhatsApp/Telegram

---

## 🆘 Obtener Ayuda Adicional

### Logs Detallados

```bash
# Ejecutar con más información
python -v main.py

# Guardar logs
python main.py 2>&1 | tee debug.log
```

### Verificar Instalación

```bash
# Verificar Python
python3 --version

# Verificar dependencias
pip list | grep -E "gitlab|genai|halo"

# Verificar .env
cat .env | grep -v "^#"
```

### Modo Debug

Añadir al inicio de `src/changelog_generator.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Reportar Issues

Si ninguna solución funciona:

1. Recopilar información:
   ```bash
   python3 --version
   pip list
   cat .env.example  # NO compartas tu .env real
   ```

2. Crear issue con:
   - Descripción del problema
   - Pasos para reproducir
   - Mensaje de error completo
   - Información del sistema

---

## ✅ Checklist de Diagnóstico

Antes de reportar un problema, verificar:

- [ ] Python 3.8+ instalado
- [ ] Virtual environment activado
- [ ] Todas las dependencias instaladas
- [ ] Archivo `.env` existe y está completo
- [ ] Tokens/API keys son válidos
- [ ] Repositorio tiene al menos 2 tags
- [ ] Hay commits entre los tags
- [ ] Conexión a internet funciona
- [ ] Permisos de escritura en directorio `results/`

---

**¿Aún tienes problemas?** Revisa los logs, busca el error específico en este documento, o crea un issue con toda la información relevante.
