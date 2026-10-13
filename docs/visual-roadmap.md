# Dirección visual y de animación

Esta guía convierte la hoja conceptual `concepts/animation-polish-v1.png` en criterios aplicables al atlas técnico. La referencia es deliberadamente expresiva; cada cambio final debe adaptarse a celdas de 192 × 208 px y pasar la validación.

## Principios

1. **Silueta primero.** Cada estado debe reconocerse sin depender de detalles faciales.
2. **Una línea de suelo estable.** Los pies no deben vibrar entre frames, salvo durante un salto deliberado.
3. **Anticipación y recuperación.** Acciones enérgicas necesitan preparación, acción y retorno.
4. **Movimiento secundario retrasado.** Cabello, orejas, falda, cintas y cola siguen al torso con uno o dos frames de retraso.
5. **Optimismo persistente.** Incluso el fallo debe terminar con recuperación, reflejando la personalidad perseverante de Haru.
6. **Lectura a tamaño real.** Revisar siempre a 192 × 208 px y no solamente ampliado.

## Objetivos por estado

### Idle

- Mantener los pies fijos.
- Respiración vertical de 1–2 px en torso y hombros.
- Un parpadeo rápido, no perfectamente periódico.
- Una oreja reacciona antes que la otra.
- La cola completa un arco lento sin cambiar de volumen.

### Running right / left

- Inclinar el torso hacia el destino.
- Separar claramente contacto, compresión, impulso y vuelo.
- Mantener constante el volumen de cabeza y cabello.
- Retrasar cola y cintas respecto al cambio de dirección del cuerpo.
- Asegurar continuidad entre el último y primer frame.

### Waving

- Anticipar con hombro y codo antes de levantar la mano.
- Dibujar un arco claro con la muñeca.
- Mantener una expresión abierta y contacto visual.

### Jumping

- Comprimir la pose antes del despegue.
- Usar una silueta amplia y alegre en el ápice.
- Mostrar un aterrizaje comprimido antes de volver a reposo.

### Failed

- Secuencia narrativa: sorpresa, caída emocional, pausa y recuperación.
- Evitar mantener ocho frames casi idénticos.
- Finalizar con una señal pequeña de determinación.

### Waiting

- Cambiar el foco de mirada antes de mover la cabeza.
- Alternar paciencia y curiosidad sin transmitir tristeza.
- Usar orejas y cola para mantener viva una pose contenida.

### Working

- Postura enfocada y ritmo algo más rápido que `idle`.
- Evitar que se confunda con una carrera espacial.
- Concentrar movimiento en manos, ojos y accesorios.

### Review

- Secuencia: observar, considerar, detectar y aprobar.
- Terminar con sonrisa, asentimiento o gesto afirmativo.

### Look directions

- Priorizar ojos y cabeza; el torso solo acompaña gradualmente.
- Mantener escala, centro y línea de suelo constantes.
- Evitar saltos de peinado o volumen entre ángulos vecinos.

## Orden recomendado de producción

1. Corregir línea de suelo y escala en todas las filas.
2. Pulir `idle` y las dos carreras; son los estados más visibles.
3. Rediseñar la narrativa de `failed`, `waiting` y `review`.
4. Ajustar movimiento secundario.
5. Revisar las 16 miradas como una rotación continua.
6. Ejecutar `scripts/build.py` y revisar Animation Lab a 80, 180 y 350 ms.
