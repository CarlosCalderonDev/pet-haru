# Diseño de la hoja de sprites v2

Cada celda mide 192 × 208 px. Los frames requeridos comienzan en la columna izquierda; las celdas restantes deben ser completamente transparentes.

| Fila | Estado | Frames | Propósito |
| ---: | --- | ---: | --- |
| 0 | idle | 6 | Reposo vivo y calmado |
| 1 | running-right | 8 | Desplazamiento hacia la derecha |
| 2 | running-left | 8 | Desplazamiento hacia la izquierda |
| 3 | waving | 4 | Saludo |
| 4 | jumping | 5 | Salto y regreso a la base |
| 5 | failed | 8 | Reacción de fallo |
| 6 | waiting | 6 | Espera de aprobación o ayuda |
| 7 | running | 6 | Trabajo, procesamiento o concentración |
| 8 | review | 6 | Inspección del trabajo terminado |
| 9 | look directions A | 8 | 000° a 157,5°, en sentido horario |
| 10 | look directions B | 8 | 180° a 337,5°, en sentido horario |

Orden de miradas:

```text
Fila 9:  000, 022.5, 045, 067.5, 090, 112.5, 135, 157.5
Fila 10: 180, 202.5, 225, 247.5, 270, 292.5, 315, 337.5
```

`000` mira hacia arriba; `090` a la derecha de la pantalla; `180` hacia abajo; `270` a la izquierda.

