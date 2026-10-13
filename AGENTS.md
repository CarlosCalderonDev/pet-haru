# Instrucciones para agentes de IA

Estas reglas aplican a todos los agentes de IA que trabajen en este repositorio y deben respetarse en cada tarea.

## Reglas

1. Al completar una tarea que produzca cambios, subir automáticamente al repositorio remoto todos los cambios pertenecientes a la tarea:
   - Revisar el estado y las diferencias antes de preparar el commit.
   - Incluir únicamente cambios relacionados con la tarea; no modificar, descartar ni subir cambios ajenos del usuario.
   - Crear un commit descriptivo y ejecutar `git push` sobre la rama actual.
   - No reescribir el historial ni usar `--force`.
   - Si Git, el remoto, las credenciales o la conexión no están disponibles, informar claramente el impedimento y dejar los cambios locales intactos.

2. Ningún agente de IA puede salir del directorio raíz de este repositorio ni realizar acciones fuera de él sin autorización explícita del usuario:
   - No leer, inspeccionar, crear, modificar, mover ni eliminar archivos o directorios externos al repositorio.
   - No cambiar configuraciones del sistema, otras aplicaciones, cuentas, servicios, repositorios ni recursos externos.
   - Si una tarea requiere actuar fuera del repositorio, explicar previamente la acción y su destino exacto, y esperar la autorización del usuario.
   - Una autorización aplica únicamente a la acción y al alcance expresamente aprobados; no concede permiso general para otras operaciones externas.
   - Las autorizaciones permanentes escritas en este archivo, incluida la subida automática establecida en la regla 1, siguen siendo válidas dentro de su alcance específico.

## Incorporación de reglas nuevas

- Agregar a este archivo las reglas nuevas que solicite el usuario.
- Mantener las reglas claras, numeradas y compatibles con las instrucciones de mayor prioridad.
