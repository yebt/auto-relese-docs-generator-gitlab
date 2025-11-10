# 🤖 Guía de Gemini CLI

## ¿Por qué Gemini CLI?

El generador de changelogs ahora usa **Gemini CLI por defecto** en lugar de la API de Gemini. Esto resuelve el problema de rechazo de peticiones cuando hay muchos commits o diffs grandes.

### Ventajas de Gemini CLI

✅ **Procesamiento local**: Evita límites de tamaño de petición de la API  
✅ **Análisis por lotes**: Divide commits en grupos manejables  
✅ **Mayor confiabilidad**: No depende de cuotas de API  
✅ **Mejor manejo de contexto grande**: Puede procesar repositorios con muchos commits  

## 🚀 Instalación de Gemini CLI

### Requisitos previos

- Sistema operativo: Linux, macOS o Windows
- Acceso a internet para la instalación

### Pasos de instalación

1. **Visita la documentación oficial**:
   ```
   https://ai.google.dev/gemini-api/docs/cli
   ```

2. **Sigue las instrucciones de instalación** según tu sistema operativo

3. **Verifica la instalación**:
   ```bash
   gemini --version
   ```

   Deberías ver la versión instalada de Gemini CLI.

## 🎯 Uso

### Modo por defecto (Gemini CLI)

Simplemente ejecuta el generador sin flags adicionales:

```bash
python main.py
```

El generador automáticamente:
1. Verifica que Gemini CLI está instalado
2. Divide los commits en lotes de 5
3. Analiza cada lote con Gemini CLI
4. Categoriza los commits (features, fixes, improvements, etc.)
5. Genera los changelogs basándose en el análisis

### Modo API (alternativo)

Si prefieres usar la API de Gemini (requiere GEMINI_TOKEN en .env):

```bash
python main.py --api
```

⚠️ **Advertencia**: La API puede rechazar peticiones si hay muchos commits o diffs grandes.

## 🔄 Flujo de trabajo con Gemini CLI

### 1. Análisis por lotes

Los commits se dividen en lotes de 5 para evitar sobrecargar Gemini:

```
Commits totales: 25
├── Batch 1/5: Commits 1-5
├── Batch 2/5: Commits 6-10
├── Batch 3/5: Commits 11-15
├── Batch 4/5: Commits 16-20
└── Batch 5/5: Commits 21-25
```

### 2. Categorización automática

Gemini CLI analiza cada commit y lo categoriza en:

- **features**: Nuevas características
- **improvements**: Mejoras a funcionalidad existente
- **fixes**: Correcciones de bugs
- **breaking_changes**: Cambios que rompen compatibilidad
- **architecture**: Cambios arquitectónicos
- **dependencies**: Cambios en dependencias
- **performance**: Mejoras de rendimiento
- **security**: Parches de seguridad
- **testing**: Cambios en tests
- **docs**: Cambios en documentación
- **other**: Otros cambios

### 3. Generación de changelogs

Con los commits categorizados, Gemini CLI genera:
- **Changelog Comercial**: Enfocado en valor para el cliente
- **Changelog Técnico**: Con detalles de implementación

## 📊 Ejemplo de salida

```
============================================================
🚀 GitLab Changelog Generator with Gemini AI
============================================================

✔ Connected to GitLab project: my-project
✔ Gemini CLI initialized
✔ Found tags: v1.2.0 (to) and v1.1.0 (from)
✔ Found 25 commits between tags
✔ Fetched details for 25 commits
✔ Split 25 commits into 5 batches
✔ Analyzing batch 1/5 with Gemini CLI...
✔ Batch 1/5 analyzed
✔ Analyzing batch 2/5 with Gemini CLI...
✔ Batch 2/5 analyzed
✔ Analyzing batch 3/5 with Gemini CLI...
✔ Batch 3/5 analyzed
✔ Analyzing batch 4/5 with Gemini CLI...
✔ Batch 4/5 analyzed
✔ Analyzing batch 5/5 with Gemini CLI...
✔ Batch 5/5 analyzed
✔ Generating commercial changelog...
✔ Commercial changelog generated
✔ Generating technical changelog...
✔ Technical changelog generated
✔ Changelogs saved to: results/v1.2.0_20251107_153000

============================================================
✅ Changelog generation completed successfully!
============================================================
```

## 🐛 Troubleshooting

### Error: "Gemini CLI not found"

**Problema**: Gemini CLI no está instalado o no está en el PATH.

**Solución**:
```bash
# Verifica si está instalado
gemini --version

# Si no está instalado, visita:
# https://ai.google.dev/gemini-api/docs/cli
```

### Error: "Gemini CLI is not working properly"

**Problema**: Gemini CLI está instalado pero no funciona correctamente.

**Solución**:
1. Verifica que tienes la última versión
2. Reinstala Gemini CLI
3. Verifica permisos de ejecución

### Error: "Gemini CLI request timed out"

**Problema**: Una petición a Gemini CLI tardó más de 5 minutos.

**Solución**:
1. Verifica tu conexión a internet
2. Intenta de nuevo (puede ser un problema temporal)
3. Si persiste, usa el modo API: `python main.py --api`

### Advertencia: "Failed to analyze batch X"

**Problema**: Un lote específico falló al analizarse.

**Comportamiento**: El generador continúa con los lotes restantes.

**Solución**:
- El changelog se generará con los lotes exitosos
- Revisa el changelog generado para ver si falta información crítica
- Si es necesario, ejecuta de nuevo el generador

## 🔀 Comparación: CLI vs API

| Característica | Gemini CLI (Defecto) | Gemini API (--api) |
|----------------|----------------------|---------------------|
| **Límite de tamaño** | Sin límite práctico | Limitado por API |
| **Procesamiento** | Por lotes | Todo de una vez |
| **Requiere API key** | ❌ No | ✅ Sí |
| **Confiabilidad** | ⭐⭐⭐⭐⭐ Alta | ⭐⭐⭐ Media |
| **Velocidad** | Media | Rápida (si funciona) |
| **Manejo de errores** | Continúa con lotes restantes | Falla completamente |
| **Recomendado para** | Repos grandes | Repos pequeños |

## 💡 Mejores prácticas

### 1. Usa Gemini CLI por defecto

```bash
# ✅ Recomendado
python main.py

# ⚠️ Solo si tienes pocos commits
python main.py --api
```

### 2. Combina con caché para repos grandes

```bash
# Para repos con muchos commits
python main.py --cache --from-tag v1.0.0 --to-tag v2.0.0
```

### 3. Verifica la instalación antes de ejecutar

```bash
# Verifica que Gemini CLI funciona
gemini --version

# Luego ejecuta el generador
python main.py
```

## 🔧 Configuración avanzada

### Ajustar tamaño de lote

Si necesitas ajustar el tamaño de los lotes (por defecto 5 commits por lote), edita `src/changelog_generator.py`:

```python
# Línea 281
batches = self.split_commits_into_batches(commits, batch_size=5)
```

Cambia `batch_size=5` al valor deseado:
- **Lotes más pequeños (3-4)**: Más confiable, pero más lento
- **Lotes más grandes (7-10)**: Más rápido, pero puede fallar con commits grandes

### Timeout de Gemini CLI

Si necesitas más tiempo para peticiones (por defecto 5 minutos), edita `src/gemini_cli_analyzer.py`:

```python
# Línea 67
timeout=300  # 5 minutos
```

Cambia `300` al número de segundos deseado.

## 📚 Recursos adicionales

- **Documentación oficial de Gemini CLI**: https://ai.google.dev/gemini-api/docs/cli
- **README principal**: [README.md](README.md)
- **Guía de uso**: [USAGE_GUIDE.md](USAGE_GUIDE.md)
- **Troubleshooting**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## ❓ Preguntas frecuentes

### ¿Necesito una API key para usar Gemini CLI?

No, Gemini CLI no requiere configurar GEMINI_TOKEN en el archivo `.env`.

### ¿Puedo usar ambos modos?

Sí, puedes alternar entre CLI y API según tus necesidades:
- Sin flag: usa CLI (recomendado)
- Con `--api`: usa API

### ¿Qué pasa si un lote falla?

El generador continúa con los lotes restantes y genera el changelog con la información disponible. Verás una advertencia en la consola.

### ¿Es más lento que la API?

Puede ser ligeramente más lento porque procesa por lotes, pero es mucho más confiable para repositorios grandes.

---

**¿Problemas con Gemini CLI?** Consulta [TROUBLESHOOTING.md](TROUBLESHOOTING.md) o abre un issue en el repositorio.
