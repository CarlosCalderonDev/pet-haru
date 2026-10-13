# Haru Urara · ChatGPT Pet

Repositorio de producción, validación y evolución de la mascota personalizada **Haru Urara**. El proyecto conserva el sprite sheet canónico, genera todos sus derivados de forma reproducible, ofrece un laboratorio visual para revisar animaciones y ejecuta controles automáticos antes de publicar cambios.

![Hoja de control de todos los estados](previews/contact-sheet.png)

## Contenido

- [Estado actual](#estado-actual)
- [Inicio rápido](#inicio-rápido)
- [Fuente de verdad y archivos generados](#fuente-de-verdad-y-archivos-generados)
- [Formato del sprite sheet](#formato-del-sprite-sheet)
- [Animation Lab](#animation-lab)
- [Construcción y comandos](#construcción-y-comandos)
- [Validación y reporte QA](#validación-y-reporte-qa)
- [Pruebas automatizadas](#pruebas-automatizadas)
- [Integración continua](#integración-continua)
- [Arquitectura del repositorio](#arquitectura-del-repositorio)
- [Flujo para editar o publicar una versión](#flujo-para-editar-o-publicar-una-versión)
- [Dirección artística](#dirección-artística)
- [Solución de problemas](#solución-de-problemas)

## Estado actual

| Propiedad | Valor |
| --- | --- |
| Nombre | Haru Urara |
| ID estable | `pet_6abd41eef0f481919d149ed7592aeb99` |
| Descripción | Alegre y perseverante, en estilo chibi anime |
| Formato | Sprite sheet v2, PNG con transparencia |
| Dimensiones | 1536 × 2288 px |
| Cuadrícula | 8 columnas × 11 filas |
| Tamaño de celda | 192 × 208 px |
| Estados | 11 |
| Frames utilizados | 73 |
| Validación | Aprobada, sin errores ni advertencias |
| Metadatos | [`docs/pet.json`](docs/pet.json) |
| Reporte QA | [`qa/validation.json`](qa/validation.json) |

El activo que determina el contenido de la mascota es [`assets/sprites/haru-urara-spritesheet.png`](assets/sprites/haru-urara-spritesheet.png). No depende de enlaces temporales ni de rutas personales.

## Inicio rápido

### Requisitos

- Python 3.10 o posterior.
- Pillow 12.3.0, fijado en [`requirements.txt`](requirements.txt).
- Git, únicamente si se desea versionar o publicar cambios.

Instala la dependencia:

```powershell
python -m pip install -r requirements.txt
```

Construye y valida todo el proyecto:

```powershell
python .\scripts\build.py
```

Ejecuta las pruebas:

```powershell
python -m unittest discover -s tests -v
```

Abre el visor local:

```powershell
python -m http.server 8000
```

Visita `http://localhost:8000/viewer/`. El servidor debe iniciarse desde la raíz del repositorio para que las rutas de sprites funcionen correctamente.

## Fuente de verdad y archivos generados

El proyecto diferencia deliberadamente los archivos que se editan de los que se regeneran.

### Fuente de verdad

- [`assets/sprites/haru-urara-spritesheet.png`](assets/sprites/haru-urara-spritesheet.png): imagen canónica.
- [`docs/pet.json`](docs/pet.json): identidad, geometría, versión, hash y distribución de frames.
- [`scripts/pet_config.py`](scripts/pet_config.py): carga centralizada de metadatos y nombres de estados.

### Derivados reproducibles

- `assets/frames/<estado>/*.png`: celdas individuales del atlas.
- `previews/animations/*.gif`: previsualizaciones animadas.
- [`previews/contact-sheet.png`](previews/contact-sheet.png): inspección de las 88 celdas.
- [`previews/look-directions.png`](previews/look-directions.png): revisión de las 16 direcciones de mirada.
- [`qa/validation.json`](qa/validation.json): resultado detallado de control de calidad.

No edites manualmente los derivados. Modifica el atlas o sus metadatos y vuelve a ejecutar `scripts/build.py`.

## Formato del sprite sheet

Cada celda mide 192 × 208 px. Los frames válidos de una fila empiezan en la primera columna; las celdas sobrantes deben permanecer completamente transparentes.

| Fila | Estado | Frames | Uso |
| ---: | --- | ---: | --- |
| 0 | `idle` | 6 | Reposo, respiración y parpadeo |
| 1 | `running-right` | 8 | Desplazamiento hacia la derecha |
| 2 | `running-left` | 8 | Desplazamiento hacia la izquierda |
| 3 | `waving` | 4 | Saludo |
| 4 | `jumping` | 5 | Anticipación, salto y aterrizaje |
| 5 | `failed` | 8 | Reacción de fallo |
| 6 | `waiting` | 6 | Espera de aprobación o ayuda |
| 7 | `running` | 6 | Trabajo o procesamiento |
| 8 | `review` | 6 | Revisión del resultado |
| 9 | `look-a` | 8 | Miradas de 0° a 157.5° |
| 10 | `look-b` | 8 | Miradas de 180° a 337.5° |

La especificación angular completa se encuentra en [`docs/sprite-layout.md`](docs/sprite-layout.md).

### Convenciones de frames

- Los archivos se nombran desde `00.png` con dos dígitos.
- El orden temporal coincide con el orden de columnas del atlas.
- El fondo debe ser transparente; no se admite un color usado como máscara.
- La línea de suelo debe permanecer estable, excepto durante movimientos deliberados como el salto.
- El último frame debe poder regresar al primero sin un salto visual brusco.

## Animation Lab

[`viewer/index.html`](viewer/index.html) es un visor estático sin framework ni proceso de compilación web. Consume directamente los frames del repositorio.

Funciones disponibles:

- Selección de los 11 estados.
- Reproducción y pausa.
- Navegación manual cuadro por cuadro.
- Velocidad configurable entre 60 y 500 ms.
- Escala configurable entre 1× y 3×.
- Fondos cuadriculado, claro, oscuro y rosa.
- Línea de suelo opcional.
- Diseño adaptable a escritorio y móvil.
- Compatibilidad con la preferencia `prefers-reduced-motion`.

Archivos del visor:

- [`viewer/index.html`](viewer/index.html): estructura y controles.
- [`viewer/styles.css`](viewer/styles.css): presentación adaptable.
- [`viewer/app.js`](viewer/app.js): estados, reproducción y navegación.

![Reposo](previews/animations/idle.gif)
![Carrera](previews/animations/running-right.gif)
![Saludo](previews/animations/waving.gif)
![Salto](previews/animations/jumping.gif)
![Revisión](previews/animations/review.gif)

## Construcción y comandos

### Build completo

```powershell
python .\scripts\build.py
```

El build ejecuta, en orden:

1. Extracción optimizada de todos los frames.
2. Generación de GIF animados.
3. Generación de hojas de contacto y miradas.
4. Actualización del tamaño y SHA-256 en `docs/pet.json`.
5. Escritura de `qa/validation.json`.
6. Terminación con código distinto de cero si el atlas es inválido.

### Solo generar derivados

```powershell
python .\scripts\generate_previews.py
```

Para conservar compatibilidad también existen:

```powershell
python .\scripts\extract-atlas-frames.py
.\scripts\generate-previews.ps1
```

### Solo validar

Validar sin modificar metadatos:

```powershell
python .\scripts\validate_pet.py
```

Validar y sincronizar el tamaño y hash guardados:

```powershell
python .\scripts\validate_pet.py --update-metadata
```

Escribir el reporte en otra ubicación:

```powershell
python .\scripts\validate_pet.py --output .\qa\validation-local.json
```

### Wrapper de PowerShell

[`scripts/build.ps1`](scripts/build.ps1) localiza Python 3.10+ y ejecuta el mismo build. Si Python no está en `PATH`, se puede indicar su ejecutable solo para la sesión actual:

```powershell
$env:PET_HARU_PYTHON = 'C:\ruta\a\python.exe'
.\scripts\build.ps1
```

El proyecto no requiere cambiar permanentemente la política de ejecución de PowerShell.

## Validación y reporte QA

[`scripts/validate_pet.py`](scripts/validate_pet.py) comprueba:

- Existencia y dimensiones exactas del atlas.
- Consistencia entre geometría y metadatos.
- Cantidad de estados y frames.
- Frames requeridos no vacíos.
- Celdas no utilizadas completamente transparentes.
- Frames duplicados.
- Coincidencia píxel a píxel entre atlas y frames derivados.
- Variación aproximada de la línea de suelo.
- Diferencia entre extremos de cada ciclo.
- Tamaño del archivo y hash SHA-256.

El reporte contiene:

- `valid`: resultado general.
- `errors`: problemas que invalidan el activo.
- `warnings`: aspectos visuales que requieren revisión.
- `alpha_bounds`: límites visibles de cada frame.
- `ground_line_spread_px`: variación vertical de la base.
- `loop_endpoint_delta`: diferencia media entre primer y último frame.

`loop_endpoint_delta` es una señal de revisión, no una medida absoluta de calidad: algunas acciones deben terminar lejos de su pose inicial.

## Pruebas automatizadas

La suite está en [`tests/test_project.py`](tests/test_project.py):

```powershell
python -m unittest discover -s tests -v
```

Actualmente verifica:

1. Validez del atlas y sus derivados.
2. Geometría declarada frente a la imagen real.
3. Correspondencia entre estados del visor y `pet.json`.
4. Existencia de todos los enlaces locales del README.
5. Ausencia de rutas personales en fuentes del proyecto.
6. Servicio HTTP real de HTML, CSS, JavaScript y un sprite.

## Integración continua

El workflow [`validate.yml`](.github/workflows/validate.yml) se ejecuta en cada `push` a `main` y en cada pull request.

Pasos de CI:

1. Descarga del repositorio.
2. Instalación de Python 3.12 y dependencias fijadas.
3. Build completo.
4. Ejecución de la suite de pruebas.
5. Verificación de que los derivados versionados ya estaban actualizados.
6. Publicación de `qa/validation.json` como artefacto, incluso si falla una comprobación.

Si el build cambia un derivado y ese cambio no estaba incluido en el commit, CI falla. Esto evita publicar un atlas con previews o metadatos obsoletos.

## Arquitectura del repositorio

```text
pet-haru/
├── .github/workflows/
│   └── validate.yml            # CI de build y pruebas
├── assets/
│   ├── sprites/                # Atlas canónico
│   └── frames/                 # Frames derivados por estado
├── docs/
│   ├── concepts/               # Referencias artísticas no canónicas
│   ├── pet.json                # Metadatos de la mascota y del atlas
│   ├── sprite-layout.md        # Contrato de filas y direcciones
│   └── visual-roadmap.md       # Criterios de animación
├── previews/
│   ├── animations/             # GIF derivados
│   ├── contact-sheet.png       # QA de todas las celdas
│   └── look-directions.png     # QA de miradas
├── qa/
│   └── validation.json         # Reporte reproducible
├── scripts/
│   ├── build.py                # Orquestador principal
│   ├── generate_previews.py    # Generador de derivados
│   ├── validate_pet.py         # Validador
│   └── pet_config.py           # Configuración compartida
├── tests/
│   └── test_project.py         # Integridad y smoke tests HTTP
├── viewer/                     # Animation Lab
├── CHANGELOG.md                # Historial funcional y visual
├── requirements.txt            # Dependencias fijadas
└── README.md                   # Documentación principal
```

## Flujo para editar o publicar una versión

1. Crea una rama de trabajo.
2. Conserva la versión publicada mediante una etiqueta antes de sustituir el atlas.
3. Modifica únicamente las filas necesarias de la imagen canónica.
4. Mantén dimensiones, cuadrícula, transparencia y orden de frames.
5. Ejecuta `python scripts/build.py`.
6. Ejecuta `python -m unittest discover -s tests -v`.
7. Abre Animation Lab y revisa cada estado a 80, 180 y 350 ms.
8. Examina fondo claro, oscuro y cuadriculado para detectar halos.
9. Revisa `qa/validation.json`; no publiques con errores.
10. Registra el cambio en [`CHANGELOG.md`](CHANGELOG.md).
11. Confirma que `git status` no muestre derivados sin incluir.
12. Crea el commit y publica la rama.

### Lista de control visual

- Identidad, proporciones y vestuario consistentes.
- Pies estables sobre la línea de suelo.
- Volumen constante de cabeza, cabello, orejas y cola.
- Siluetas distintas entre estados.
- Movimiento secundario con retraso natural.
- Primer y último frame compatibles con el ciclo.
- Lectura clara a 192 × 208 px.
- Sin píxeles visibles en celdas reservadas.

## Dirección artística

[`docs/visual-roadmap.md`](docs/visual-roadmap.md) describe objetivos concretos para respiración, carrera, salto, fallo, espera, trabajo, revisión y miradas.

[`docs/concepts/animation-polish-v1.png`](docs/concepts/animation-polish-v1.png) es una referencia conceptual generada para explorar poses más expresivas y movimiento secundario. No cumple el contrato técnico del atlas y no debe usarse como reemplazo directo.

![Referencia conceptual de pulido](docs/concepts/animation-polish-v1.png)

## Solución de problemas

### `python` abre Microsoft Store o no se encuentra

Instala Python 3.10+ y abre una terminal nueva. También puedes ejecutar el wrapper con una ruta explícita mediante `PET_HARU_PYTHON`.

### Falta Pillow

```powershell
python -m pip install -r requirements.txt
```

### PowerShell bloquea un archivo `.ps1`

No es necesario cambiar la configuración del sistema. Usa directamente:

```powershell
python .\scripts\build.py
```

### El visor aparece sin imágenes

No abras solamente el HTML mediante `file://`. Inicia `python -m http.server 8000` desde la raíz y visita `/viewer/`.

### El validador informa `derived frame is stale`

El atlas cambió, pero los frames extraídos no. Ejecuta:

```powershell
python .\scripts\build.py
```

### CI detecta diferencias después del build

Ejecuta el build local, revisa los archivos modificados y añade al commit los derivados legítimos. No edites el reporte o los frames manualmente para ocultar la diferencia.

### Se cambió el atlas por error

No regeneres ni publiques hasta comparar el archivo con la última versión confirmada. El hash esperado se conserva en `docs/pet.json` y en el historial Git.

## Archivos relacionados

- [`CHANGELOG.md`](CHANGELOG.md): cambios funcionales y visuales.
- [`AGENTS.md`](AGENTS.md): reglas obligatorias para agentes de IA.
- [`docs/sprite-layout.md`](docs/sprite-layout.md): disposición técnica.
- [`docs/visual-roadmap.md`](docs/visual-roadmap.md): guía artística.
- [`qa/validation.json`](qa/validation.json): evidencia de validación actual.
