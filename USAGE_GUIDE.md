# 📖 Usage Guide

Guía completa de uso del generador de changelogs.

## 🚀 Uso Básico

### Ejecución Simple

```bash
# Activar virtual environment
source .venv/bin/activate

# Ejecutar
python main.py
```

Esto generará automáticamente changelogs para los últimos 2 tags del repositorio.

## 📊 Salida Esperada

### Durante la Ejecución

```
============================================================
🚀 GitLab Changelog Generator with Gemini AI
============================================================

⠋ Connecting to GitLab...
✔ Connected to GitLab project: my-awesome-project

⠋ Connecting to Gemini AI...
✔ Connected to Gemini AI

⠋ Fetching repository tags...
✔ Found tags: v1.2.0 (latest) and v1.1.0 (previous)

⠋ Fetching commits between v1.1.0 and v1.2.0...
✔ Found 15 commits between tags

⠋ Fetching commit details 1/15...
⠋ Fetching commit details 2/15...
...
✔ Fetched details for 15 commits

⠋ Preparing context for AI analysis...
✔ Context prepared

⠋ Generating commercial changelog with Gemini AI...
✔ Commercial changelog generated

⠋ Generating technical changelog with Gemini AI...
✔ Technical changelog generated

⠋ Saving changelogs...
✔ Changelogs saved to: results/v1.2.0_20251008_163530

============================================================
✅ Changelog generation completed successfully!
============================================================

📁 Output directory: /path/to/results/v1.2.0_20251008_163530
📄 Files generated:
   - Changelog_comercial_v1.2.0.md
   - Changelog_tech_v1.2.0.md

💬 Files are formatted for WhatsApp/Telegram sharing
```

### Archivos Generados

```
results/
└── v1.2.0_20251008_163530/
    ├── Changelog_comercial_v1.2.0.md
    └── Changelog_tech_v1.2.0.md
```

## 📱 Compartir en Mensajería

### WhatsApp

1. Abrir el archivo `.md` en un editor de texto
2. Copiar todo el contenido (Ctrl+A, Ctrl+C)
3. Pegar en WhatsApp
4. El formato se preservará automáticamente

**Ejemplo**:
```
*📋 CHANGELOG COMERCIAL - Release v1.2.0*

*🎯 RESUMEN EJECUTIVO*
Esta versión introduce...

*✨ NUEVAS CARACTERÍSTICAS*
🟢 Característica 1: Descripción...
```

### Telegram

**Opción 1: Copiar y pegar** (igual que WhatsApp)

**Opción 2: Enviar como archivo**
1. En Telegram, usar el botón de adjuntar
2. Seleccionar el archivo `.md`
3. Enviar como documento
4. Telegram mostrará el formato correctamente

### Email

```bash
# Convertir a HTML para email
pip install markdown

python3 << 'EOF'
import markdown
with open('results/v1.2.0_xxx/Changelog_comercial_v1.2.0.md', 'r') as f:
    md_content = f.read()
    html = markdown.markdown(md_content)
    with open('changelog.html', 'w') as out:
        out.write(html)
print('✅ Convertido a HTML: changelog.html')
EOF
```

## 🎯 Casos de Uso Específicos

### 1. Release Notes para Clientes

```bash
# 1. Generar changelogs
python main.py

# 2. Abrir changelog comercial
cd results/v1.2.0_*/
cat Changelog_comercial_v1.2.0.md

# 3. Copiar y enviar a clientes por WhatsApp/Email
```

### 2. Documentación Técnica

```bash
# 1. Generar changelogs
python main.py

# 2. Copiar changelog técnico a wiki/docs
cp results/v1.2.0_*/Changelog_tech_v1.2.0.md docs/releases/

# 3. Commit a repositorio
git add docs/releases/Changelog_tech_v1.2.0.md
git commit -m "docs: Add technical changelog for v1.2.0"
git push
```

### 3. Retrospectiva de Sprint

```bash
# 1. Generar changelogs después del sprint
python main.py

# 2. Usar ambos changelogs en reunión
# - Comercial: Para discutir valor entregado
# - Técnico: Para discutir deuda técnica y mejoras
```

### 4. Comunicación con Stakeholders

```bash
# 1. Generar changelog comercial
python main.py

# 2. Extraer secciones relevantes
# - Nuevas características → Para product managers
# - Correcciones → Para QA/Support
# - Cambios importantes → Para todos
```

## 🔧 Configuración Avanzada

### Modificar Prompts de IA

Editar `src/changelog_generator.py`:

```python
# Línea ~220 - Prompt comercial
prompt = f"""Eres un experto en comunicación comercial...
[Modificar según necesidades]
"""

# Línea ~280 - Prompt técnico
prompt = f"""Eres un experto en desarrollo de software...
[Modificar según necesidades]
"""
```

### Cambiar Límites de Contexto

```python
# Línea ~150 - Limitar archivos por commit
for diff_item in commit['diff'][:5]:  # Cambiar número

# Línea ~160 - Limitar líneas de diff
diff_lines = diff_item['diff'].split('\n')[:20]  # Cambiar número
```

### Usar GitLab Self-Hosted

```python
# Línea ~40 en src/changelog_generator.py
self.gl = gitlab.Gitlab(
    url='https://gitlab.tu-empresa.com',  # Tu URL
    private_token=self.gitlab_token
)
```

### Cambiar Modelo de Gemini

```python
# Línea ~230 y ~290
response = self.gemini_client.models.generate_content(
    model='gemini-2.0-flash-exp',  # Cambiar modelo
    contents=prompt
)
```

Modelos disponibles:
- `gemini-2.0-flash-exp` (rápido, recomendado)
- `gemini-pro` (balanceado)
- `gemini-pro-vision` (con imágenes)

## 📊 Interpretando los Resultados

### Changelog Comercial

**Para quién**: Clientes, ventas, product managers

**Qué buscar**:
- 🟢 **Nuevas características**: Qué valor aportan
- 🔵 **Mejoras**: Cómo mejora la experiencia
- 🟡 **Correcciones**: Qué problemas se resolvieron
- 🔴 **Cambios importantes**: Qué debe comunicarse

**Cómo usar**:
- Copiar secciones relevantes para comunicados
- Adaptar lenguaje según audiencia
- Destacar valor de negocio

### Changelog Técnico

**Para quién**: Developers, DevOps, arquitectos

**Qué buscar**:
- 🟢 **Funcionalidades**: Implementación técnica
- 🔵 **Mejoras técnicas**: Refactoring, optimizaciones
- 🟡 **Bugs**: Causa raíz y solución
- 🔴 **Breaking changes**: Qué requiere migración
- 🟣 **Arquitectura**: Cambios estructurales

**Cómo usar**:
- Referencia para code reviews
- Documentación de decisiones técnicas
- Guía para onboarding de nuevos developers

## 🎨 Personalización de Formato

### Añadir Secciones Personalizadas

Editar prompts en `src/changelog_generator.py`:

```python
# Ejemplo: Añadir sección de "Impacto en Performance"
prompt = f"""...

*⚡ IMPACTO EN PERFORMANCE*
[Métricas de performance antes y después]

..."""
```

### Cambiar Emojis

```python
# En los prompts, reemplazar:
🟢 → ✅  # Para features
🔵 → 🔧  # Para mejoras
🟡 → 🐛  # Para bugs
🔴 → ⚠️  # Para breaking changes
🟣 → 🏗️  # Para arquitectura
```

### Formato Alternativo (Sin Emojis)

Para entornos que no soportan emojis bien:

```python
# Modificar prompts para usar:
[NEW] en lugar de 🟢
[IMP] en lugar de 🔵
[FIX] en lugar de 🟡
[BRK] en lugar de 🔴
[ARC] en lugar de 🟣
```

## 🔄 Workflow Recomendado

### Para Cada Release

```bash
# 1. Crear tag del release
git tag -a v1.2.0 -m "Release v1.2.0"
git push --tags

# 2. Generar changelogs
python main.py

# 3. Revisar y editar si necesario
nano results/v1.2.0_*/Changelog_comercial_v1.2.0.md
nano results/v1.2.0_*/Changelog_tech_v1.2.0.md

# 4. Distribuir
# - Comercial → WhatsApp a clientes
# - Técnico → Wiki/Confluence del equipo

# 5. Archivar
git add results/v1.2.0_*
git commit -m "docs: Add changelogs for v1.2.0"
git push
```

### Automatización con CI/CD

**GitLab CI** (`.gitlab-ci.yml`):
```yaml
generate_changelog:
  stage: deploy
  only:
    - tags
  script:
    - pip install -r requirements.txt
    - python main.py
  artifacts:
    paths:
      - results/
    expire_in: 1 week
```

## 📈 Tips y Best Practices

### 1. Commits Descriptivos
```bash
# ❌ Mal
git commit -m "fix"

# ✅ Bien
git commit -m "fix: Resolve memory leak in user session handler"
```

### 2. Tags Semánticos
```bash
# Usar Semantic Versioning
v1.2.0  # Major.Minor.Patch
v2.0.0  # Breaking changes
v1.2.1  # Bug fixes
```

### 3. Revisar Antes de Compartir
- IA puede cometer errores
- Verificar información sensible
- Adaptar lenguaje según audiencia

### 4. Mantener Historial
```bash
# No borrar carpeta results/
# Mantener historial de todos los releases
results/
├── v1.0.0_20251001_120000/
├── v1.1.0_20251015_140000/
└── v1.2.0_20251008_163530/
```

### 5. Feedback Loop
- Recopilar feedback sobre changelogs
- Ajustar prompts según necesidades
- Iterar y mejorar

## 🆘 Comandos Útiles

```bash
# Ver últimos tags
git tag -l | tail -5

# Ver commits entre tags
git log v1.1.0..v1.2.0 --oneline

# Contar commits entre tags
git log v1.1.0..v1.2.0 --oneline | wc -l

# Ver archivos modificados entre tags
git diff v1.1.0..v1.2.0 --name-only

# Buscar changelog específico
find results/ -name "Changelog_comercial_v1.2.0.md"

# Ver todos los changelogs generados
ls -lR results/
```

## 📚 Recursos Adicionales

- **Markdown Guide**: https://www.markdownguide.org/
- **Semantic Versioning**: https://semver.org/
- **Conventional Commits**: https://www.conventionalcommits.org/
- **GitLab API Docs**: https://docs.gitlab.com/ee/api/
- **Gemini AI Docs**: https://ai.google.dev/docs

---

**¿Preguntas?** Consulta `TROUBLESHOOTING.md` o abre un issue en el repositorio.
