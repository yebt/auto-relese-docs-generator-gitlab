# 🚀 Quick Start Guide

## Configuración Rápida (5 minutos)

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar credenciales

Crea un archivo `.env` en la raíz del proyecto:

```bash
cp .env.example .env
```

Edita `.env` y completa:

```env
GITLAB_ACCESS_TOKEN=glpat-xxxxxxxxxxxxx
GITLAB_PROJECT_ID=12345678
GEMINI_TOKEN=AIzaSyxxxxxxxxxxxxxxxxx
```

### 3. Ejecutar

```bash
python main.py
```

## 📋 Checklist Pre-Ejecución

- [ ] Python 3.8+ instalado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Archivo `.env` creado con las 3 variables
- [ ] El repositorio GitLab tiene al menos 2 tags
- [ ] Token de GitLab tiene permisos: `api`, `read_api`, `read_repository`
- [ ] API Key de Gemini es válida

## 🎯 ¿Qué esperar?

El script:

1. ✅ Se conecta a GitLab
2. ✅ Se conecta a Gemini AI
3. ✅ Busca los últimos 2 tags
4. ✅ Obtiene commits entre esos tags
5. ✅ Analiza cada commit (mensaje + diffs)
6. ✅ Genera changelog comercial con IA
7. ✅ Genera changelog técnico con IA
8. ✅ Guarda ambos archivos en `results/{release}_{timestamp}/`

## 📁 Resultado

```
results/
└── v1.2.0_20251008_161430/
    ├── Changelog_comercial_v1.2.0.md
    └── Changelog_tech_v1.2.0.md
```

## 💡 Tips

- **Primera vez**: El proceso puede tardar 1-3 minutos dependiendo del número de commits
- **Formato**: Los archivos `.md` se pueden copiar directamente a WhatsApp/Telegram
- **Emojis**: Ayudan a identificar visualmente el tipo de cambio
- **Múltiples ejecuciones**: Cada ejecución crea una carpeta nueva con timestamp

## ⚠️ Errores Comunes

| Error | Solución |
|-------|----------|
| `Missing required environment variables` | Verifica que `.env` existe y tiene las 3 variables |
| `Not enough tags found` | El repo necesita al menos 2 tags |
| `Failed to connect to GitLab` | Verifica token y permisos |
| `Failed to connect to Gemini AI` | Verifica API key de Gemini |

## 🔗 Enlaces Útiles

- [Crear GitLab Token](https://gitlab.com/-/profile/personal_access_tokens)
- [Crear Gemini API Key](https://aistudio.google.com/app/apikey)
- [Documentación completa](README.md)

---

**¿Listo?** Ejecuta `python main.py` y deja que la IA haga el trabajo 🚀
