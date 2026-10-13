# Haru Urara — ChatGPT Pet

Repositorio de trabajo para desarrollar y conservar la mascota personalizada **Haru Urara**.

## Estado actual

- Nombre registrado: `Haru Urara`
- ID estable de la mascota: `pet_6abd41eef0f481919d149ed7592aeb99`
- Descripción: `Haru Urara de Uma Musume: alegre y perseverante, en estilo chibi anime.`
- Estado al exportar: activa
- Formato: sprite sheet v2, PNG transparente
- Dimensiones: 1536 × 2288 px
- Cuadrícula: 8 columnas × 11 filas
- Celda: 192 × 208 px
- Validación estructural: aprobada

El archivo canónico está en [`assets/sprites/haru-urara-spritesheet.png`](assets/sprites/haru-urara-spritesheet.png). No depende del enlace temporal usado para descargarlo.

## Estructura

```text
assets/sprites/   Sprite sheet canónico
assets/frames/    Frames extraídos por estado
docs/             Metadatos y especificación
previews/         Contact sheets y GIF de cada animación
qa/               Resultados de validación
scripts/          Herramientas reproducibles del proyecto
```

## Regenerar frames y vistas previas

En PowerShell:

```powershell
.\scripts\generate-previews.ps1
```

El script utiliza Pillow y las herramientas oficiales de creación de mascotas instaladas con Codex.

## Flujo recomendado para futuras versiones

1. Conservar el sprite sheet actual como una versión etiquetada.
2. Modificar únicamente las filas afectadas y mantener la identidad visual.
3. Regenerar frames y vistas previas.
4. Validar los bytes finales antes de actualizar la mascota registrada.
5. Mostrar y revisar las animaciones antes de subir una nueva versión.

Consulta [`docs/sprite-layout.md`](docs/sprite-layout.md) para el significado exacto de cada fila.

