# Recursos

[← Volver al README](../README.md) · [Uso](uso.md) · [Ejecutable](ejecutable.md)

Los archivos gráficos viven en la carpeta `assets/`.

## Sprites y estados

| Imagen     | Estado              |
| ---------- | ------------------- |
| gato.png   | QUIETO              |
| gato1.png  | CAMINAR 1           |
| gato2.png  | CAMINAR 2           |
| gato3.png  | IDLE                |
| gato4.png  | ESPECIAL            |
| gato5.png  | CAÍDA               |
| gato6.png  | ATERRIZAJE          |
| gato7.png  | AGARRADO            |
| icon.ico   | ÍCONO ejecutable    |
| gato8.png  | JUGANDO (minijuego) |
| gato9.png  | SALTANDO            |
| gato10.png | ACROBACIA           |
| gato11.png | ACECHANDO           |

## Tipo y tamaño de imágenes

- Usa `PNG` para todas las imágenes del gato. `PNG` mantiene transparencia y calidad cuando el sprite se redimensiona.
- El icono del ejecutable debe ser `ICO` (`assets/icon.ico`) para que Windows lo use correctamente. También puedes crear el icono desde un `PNG` de alta resolución y convertirlo a `ICO`.
- En el código, hay un código comentado para redimensionar las imágenes a `46x44` píxeles en pantalla. Por eso es mejor que las fuentes sean más grandes que ese tamaño, idealmente:
    - `96x92` o `128x120` para las animaciones del gato.
    - `256x256` para el icono del ejecutable.
- Mantén la relación de aspecto aproximada de 46:44 para que la imagen no se vea distorsionada al escalar.
- Si reemplazas imágenes, guarda los nuevos archivos en `assets/` con el mismo nombre y formato `PNG`.

Si necesitas más animaciones en el futuro, crea nuevas imágenes `PNG` con transparencia y añádelas al proyecto. El código usará las nuevas imágenes si se agregan con los nombres sugeridos.

## Ver también

- [Uso](uso.md) — interacciones que activan algunos de estos estados
- [Ejecutable](ejecutable.md) — cómo empaquetar los assets en el `.exe`
