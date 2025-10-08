# ✅ Installation Test Guide

Guía para verificar que todo está correctamente instalado y configurado.

## 🔍 Pre-Installation Checks

### 1. Verificar Python
```bash
python3 --version
# Debe mostrar: Python 3.8.x o superior
```

### 2. Verificar pip
```bash
pip3 --version
# Debe mostrar versión de pip
```

## 🚀 Installation Steps

### Opción A: Instalación Automática (Recomendado)

#### Linux/Mac
```bash
./setup.sh
```

#### Windows
```cmd
setup.bat
```

### Opción B: Instalación Manual

```bash
# 1. Crear virtual environment
python3 -m venv .venv

# 2. Activar virtual environment
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\activate.bat  # Windows

# 3. Actualizar pip
pip install --upgrade pip

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Crear archivo .env
cp .env.example .env

# 6. Editar .env con tus credenciales
nano .env  # o tu editor preferido
```

## ✅ Post-Installation Tests

### Test 1: Verificar Dependencias Instaladas

```bash
# Activar virtual environment si no está activo
source .venv/bin/activate

# Verificar instalación
pip list | grep -E "gitlab|genai|halo|dotenv"
```

**Salida esperada**:
```
google-genai          1.41.0
halo                  0.0.31
python-dotenv         1.0.0
python-gitlab         6.4.0
```

### Test 2: Verificar Estructura de Archivos

```bash
ls -la
```

**Debe mostrar**:
- ✅ `.env` (tu archivo de configuración)
- ✅ `.env.example` (template)
- ✅ `main.py`
- ✅ `requirements.txt`
- ✅ `src/` (directorio)
- ✅ `.venv/` (virtual environment)

### Test 3: Verificar Archivo .env

```bash
cat .env
```

**Debe contener** (con tus valores reales):
```env
GITLAB_ACCESS_TOKEN=glpat-xxxxxxxxxxxxx
GITLAB_PROJECT_ID=12345678
GEMINI_TOKEN=AIzaSyxxxxxxxxxxxxxxxxx
```

⚠️ **IMPORTANTE**: No debe tener espacios extra ni comillas.

### Test 4: Verificar Imports Python

```bash
python3 -c "
import gitlab
import google.genai as genai
from halo import Halo
from dotenv import load_dotenv
print('✅ Todos los imports funcionan correctamente')
"
```

**Salida esperada**:
```
✅ Todos los imports funcionan correctamente
```

### Test 5: Verificar Conexión GitLab (Opcional)

```bash
python3 << 'EOF'
import os
from dotenv import load_dotenv
import gitlab

load_dotenv()
token = os.getenv('GITLAB_ACCESS_TOKEN')
project_id = os.getenv('GITLAB_PROJECT_ID')

if not token or not project_id:
    print('❌ Credenciales no configuradas en .env')
    exit(1)

try:
    gl = gitlab.Gitlab(private_token=token)
    gl.auth()
    project = gl.projects.get(project_id)
    print(f'✅ Conectado a GitLab proyecto: {project.name}')
except Exception as e:
    print(f'❌ Error conectando a GitLab: {e}')
EOF
```

### Test 6: Verificar Conexión Gemini (Opcional)

```bash
python3 << 'EOF'
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
token = os.getenv('GEMINI_TOKEN')

if not token:
    print('❌ GEMINI_TOKEN no configurado en .env')
    exit(1)

try:
    client = genai.Client(api_key=token)
    print('✅ Conectado a Gemini AI correctamente')
except Exception as e:
    print(f'❌ Error conectando a Gemini: {e}')
EOF
```

### Test 7: Dry Run (Sin ejecutar completamente)

```bash
python3 -c "
from src.changelog_generator import ChangelogGenerator
print('✅ Módulo changelog_generator se importa correctamente')
"
```

## 🎯 Test Completo (Requiere Repositorio con Tags)

Si tu repositorio tiene al menos 2 tags:

```bash
python main.py
```

**Proceso esperado**:
1. 🔄 Connecting to GitLab...
2. ✅ Connected to GitLab project: [nombre]
3. 🔄 Connecting to Gemini AI...
4. ✅ Connected to Gemini AI
5. 🔄 Fetching repository tags...
6. ✅ Found tags: [latest] and [previous]
7. 🔄 Fetching commits...
8. ✅ Found X commits between tags
9. 🔄 Fetching commit details...
10. ✅ Fetched details for X commits
11. 🔄 Preparing context...
12. ✅ Context prepared
13. 🔄 Generating commercial changelog...
14. ✅ Commercial changelog generated
15. 🔄 Generating technical changelog...
16. ✅ Technical changelog generated
17. 🔄 Saving changelogs...
18. ✅ Changelogs saved to: results/[release]_[timestamp]

## 🐛 Troubleshooting Tests

### Si Test 1 falla (Dependencias)
```bash
pip install -r requirements.txt --force-reinstall
```

### Si Test 3 falla (.env no existe)
```bash
cp .env.example .env
nano .env  # Editar con tus credenciales
```

### Si Test 4 falla (Import errors)
```bash
# Verificar que virtual environment está activo
which python3
# Debe mostrar: /path/to/project/.venv/bin/python3

# Si no está activo:
source .venv/bin/activate
```

### Si Test 5 falla (GitLab)
- ✅ Verificar que GITLAB_ACCESS_TOKEN es correcto
- ✅ Verificar que GITLAB_PROJECT_ID es correcto
- ✅ Verificar permisos del token
- ✅ Verificar conectividad a internet

### Si Test 6 falla (Gemini)
- ✅ Verificar que GEMINI_TOKEN es correcto
- ✅ Verificar cuota disponible en Google AI Studio
- ✅ Verificar que Gemini está disponible en tu región

## 📋 Checklist Final

Antes de ejecutar `python main.py`, verificar:

- [ ] Python 3.8+ instalado
- [ ] Virtual environment creado y activado
- [ ] Todas las dependencias instaladas (Test 1 ✅)
- [ ] Archivo .env existe y está completo (Test 3 ✅)
- [ ] Imports funcionan (Test 4 ✅)
- [ ] Conexión GitLab funciona (Test 5 ✅)
- [ ] Conexión Gemini funciona (Test 6 ✅)
- [ ] Repositorio tiene al menos 2 tags
- [ ] Hay commits entre los tags

## 🎉 Si Todos los Tests Pasan

¡Felicitaciones! Tu instalación está completa y funcional.

**Siguiente paso**:
```bash
python main.py
```

Los changelogs se generarán en: `results/{release}_{timestamp}/`

## 📚 Documentación Adicional

- **Uso básico**: `QUICKSTART.md`
- **Documentación completa**: `README.md`
- **Solución de problemas**: `TROUBLESHOOTING.md`
- **Ejemplos de salida**: `SAMPLE_OUTPUT.md`
- **Visión general**: `PROJECT_OVERVIEW.md`

---

**¿Algún test falló?** Consulta `TROUBLESHOOTING.md` para soluciones detalladas.
