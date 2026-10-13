# Historial de cambios

## 2026-10-13 — Mascota de escritorio

- Aplicación flotante para Windows con transparencia y modo siempre visible.
- Seguimiento del cursor mediante las 16 direcciones del atlas v2.
- Caminata automática, arrastre, salto, saludo, revisión, pausa y menú contextual.
- Atlas canónico sincronizado con el diseño v3 activo en ChatGPT.
- Lanzador de doble clic y pruebas automatizadas de dirección de mirada.

## Próxima versión

### Añadido

- Visor interactivo para revisar estados, velocidad, escala, fondo y línea de suelo.
- Construcción portable con `scripts/build.ps1`.
- Generación local de frames, GIF y hojas de control usando Pillow.
- Validación detallada de transparencia, duplicados, línea de suelo y continuidad de ciclos.
- Validación automática mediante GitHub Actions.
- Pruebas de integridad para metadatos, enlaces, frames derivados y visor HTTP.
- Hoja conceptual de dirección artística para la siguiente revisión visual.

### Mejorado

- Los scripts ya no dependen de rutas personales ni herramientas externas de Codex.
- Los metadatos de tamaño y hash pueden sincronizarse automáticamente.
