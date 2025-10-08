# 🎯 Getting Started - 3 Pasos Simples

## ⚡ Instalación Rápida

### Paso 1: Instalar
```bash
./setup.sh
```

### Paso 2: Configurar
Edita el archivo `.env` con tus credenciales:
```bash
nano .env
```

Completa:
```env
GITLAB_ACCESS_TOKEN=tu_token_aqui
GITLAB_PROJECT_ID=tu_project_id
GEMINI_TOKEN=tu_gemini_token
```

### Paso 3: Ejecutar
```bash
source .venv/bin/activate
python main.py
```

## ✅ ¡Listo!

Los changelogs se generarán en: `results/{release}_{timestamp}/`

---

## 📚 Más Información

- **[Guía Rápida](QUICKSTART.md)** - Instalación detallada
- **[Ejemplos](SAMPLE_OUTPUT.md)** - Ver cómo se ven los changelogs
- **[Documentación Completa](INDEX.md)** - Índice de toda la documentación
- **[Solución de Problemas](TROUBLESHOOTING.md)** - Si algo falla

## 🆘 ¿Necesitas Ayuda?

1. Revisa [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Ejecuta los tests: [INSTALLATION_TEST.md](INSTALLATION_TEST.md)
3. Abre un issue en el repositorio

---

**¡Feliz generación de changelogs! 🚀**
