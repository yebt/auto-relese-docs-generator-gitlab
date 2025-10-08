# 📄 Ejemplo de Salida

Este documento muestra ejemplos de cómo se verán los changelogs generados.

---

## 📊 Changelog Comercial (Ejemplo)

```markdown
*📋 CHANGELOG COMERCIAL - Release v1.2.0*

*🎯 RESUMEN EJECUTIVO*
Esta versión introduce mejoras significativas en el sistema de autenticación, optimiza el rendimiento de las búsquedas y corrige problemas reportados por clientes en el módulo de reportes.

*✨ NUEVAS CARACTERÍSTICAS*
🟢 *Autenticación de dos factores*: Mayor seguridad para las cuentas de usuario con verificación por SMS o email
🟢 *Exportación a Excel*: Los reportes ahora se pueden descargar directamente en formato Excel
🟢 *Dashboard personalizable*: Los usuarios pueden configurar sus propios widgets en el panel principal

*🔧 MEJORAS*
🔵 *Búsqueda más rápida*: Las búsquedas en el catálogo son ahora 3x más rápidas
🔵 *Interfaz más intuitiva*: Rediseño del menú principal para mejor navegación
🔵 *Notificaciones mejoradas*: Sistema de alertas más claro y organizado

*🐛 CORRECCIONES*
🟡 *Reportes duplicados*: Solucionado el problema que generaba reportes repetidos
🟡 *Error en filtros*: Corregido el fallo al aplicar múltiples filtros simultáneamente
🟡 *Carga de imágenes*: Resuelto el problema al subir archivos grandes

*⚠️ CAMBIOS IMPORTANTES*
🔴 *Nueva pantalla de login*: Los usuarios verán un nuevo diseño al iniciar sesión
🔴 *Cambio en formato de reportes*: Los reportes antiguos deben regenerarse con el nuevo formato

*💡 VALOR APORTADO*
Esta versión mejora significativamente la seguridad y la experiencia del usuario, reduciendo el tiempo de respuesta del sistema y eliminando errores críticos que afectaban la productividad diaria.

*🎯 OBJETIVOS ALCANZADOS*
✅ Implementar autenticación de dos factores
✅ Mejorar performance del sistema en 50%
✅ Resolver todos los bugs críticos reportados
✅ Actualizar interfaz de usuario

*📌 NOTAS ADICIONALES*
Se recomienda informar a los usuarios sobre la nueva pantalla de login y la opción de activar la autenticación de dos factores para mayor seguridad.
```

---

## 🔧 Changelog Técnico (Ejemplo)

```markdown
*🔧 CHANGELOG TÉCNICO - Release v1.2.0*

*📊 RESUMEN TÉCNICO*
Implementación de sistema de autenticación OAuth 2.0 con soporte para 2FA, refactorización del módulo de búsqueda utilizando índices Elasticsearch, y migración de reportes a arquitectura asíncrona con Celery.

*✨ NUEVAS FUNCIONALIDADES*
🟢 *OAuth 2.0 + 2FA*: Implementado en `auth/oauth.py`, integración con Twilio para SMS
🟢 *Export Service*: Nuevo microservicio `services/export.py` usando pandas y openpyxl
🟢 *Widget System*: Framework de widgets en `frontend/widgets/` con React hooks

*🔧 MEJORAS TÉCNICAS*
🔵 *Elasticsearch Integration*: Migración de búsquedas a ES, índices optimizados
🔵 *React 18 Upgrade*: Actualización del frontend con nuevas APIs de concurrencia
🔵 *Redis Caching*: Implementación de caché distribuido para queries frecuentes

*🐛 BUGS CORREGIDOS*
🟡 *Race condition en reportes*: Fix en `reports/generator.py` línea 145
🟡 *Memory leak en filtros*: Corregido en `filters/engine.py`, proper cleanup
🟡 *File upload timeout*: Aumentado timeout y chunked upload en `upload/handler.py`

*⚠️ BREAKING CHANGES*
🔴 *API v1 deprecated*: Migrar a API v2, v1 será removida en v2.0.0
🔴 *Database schema change*: Nueva tabla `user_preferences`, requiere migración

*🏗️ CAMBIOS DE ARQUITECTURA*
🟣 *Microservices split*: Separación de auth y export en servicios independientes
🟣 *Event-driven reports*: Reportes ahora usan message queue (RabbitMQ)

*📦 DEPENDENCIAS*
- Añadido: `elasticsearch==8.9.0`, `celery==5.3.1`, `twilio==8.5.0`
- Actualizado: `react@18.2.0`, `django@4.2.5`
- Removido: `deprecated-search-lib`

*⚡ PERFORMANCE*
- Búsquedas: 200ms → 60ms (70% mejora)
- Carga de dashboard: 1.5s → 0.8s (47% mejora)
- Generación de reportes: Ahora asíncrono, no bloquea UI

*🔒 SEGURIDAD*
- Implementado rate limiting en endpoints de autenticación
- Actualizado bcrypt para hashing de passwords
- Añadido CSRF protection en todos los formularios

*🧪 TESTING*
- Cobertura aumentada de 65% a 82%
- Nuevos tests de integración para OAuth flow
- Tests E2E con Playwright para flujo de reportes

*⚠️ PROBLEMAS CONOCIDOS*
- Safari < 15: Widget drag-and-drop puede tener glitches
- Workaround: Usar Chrome/Firefox o actualizar Safari

*🎯 OBJETIVOS TÉCNICOS ALCANZADOS*
✅ Migrar a arquitectura de microservicios
✅ Implementar OAuth 2.0 compliant
✅ Mejorar performance en 50%+
✅ Aumentar cobertura de tests a 80%+

*💡 VALOR TÉCNICO APORTADO*
Mejora significativa en escalabilidad y mantenibilidad del código. La separación en microservicios permite desarrollo independiente y despliegues más seguros. La integración con Elasticsearch prepara el sistema para manejar 10x más datos.

*📝 NOTAS PARA DESARROLLADORES*
- Ejecutar migración: `python manage.py migrate`
- Actualizar variables de entorno: ver `.env.example`
- Elasticsearch debe estar corriendo en puerto 9200
- Configurar Celery workers: `celery -A app worker -l info`
- Documentación de API v2: `/docs/api/v2/`
```

---

## 🎨 Características del Formato

### Emojis por Tipo de Cambio

- 🟢 **Verde**: Nuevas características/funcionalidades
- 🔵 **Azul**: Mejoras y optimizaciones
- 🟡 **Amarillo**: Correcciones de bugs
- 🔴 **Rojo**: Cambios importantes/breaking changes
- 🟣 **Morado**: Cambios de arquitectura

### Formato Compatible

- ✅ WhatsApp
- ✅ Telegram
- ✅ Slack
- ✅ Discord
- ✅ Email
- ✅ Markdown viewers

### Secciones Estructuradas

Cada changelog tiene secciones claras y organizadas que facilitan:
- Lectura rápida
- Búsqueda de información específica
- Comunicación efectiva con diferentes audiencias

---

**Nota**: Los ejemplos mostrados son ficticios. El contenido real será generado por Gemini AI basándose en los commits de tu repositorio.
