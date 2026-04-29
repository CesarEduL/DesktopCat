# DesktopCat

¡Un gato para tu escritorio!

Este proyecto es una simple aplicación de un gato que camina por tu escritorio y hace cosas.

## Características

- El gato camina por tu escritorio.
- Puedes interactuar con el gato arrastrándolo.
- El gato tiene diferentes estados: quieto, caminando, idle, cayendo y un estado especial.

## Capturas de pantalla

*(Opcional: Puedes agregar capturas de pantalla de la aplicación aquí)*

## Instalación

1.  **Clona el repositorio:**

    ```bash
    git clone https://github.com/tu_usuario/DesktopCat.git
    cd DesktopCat
    ```

2.  **Crea un entorno virtual:**

    ```bash
    python -m venv venv
    ```

3.  **Activa el entorno virtual:**

    -   **Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    -   **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Instala las dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

## Uso

Para ejecutar la aplicación, simplemente corre el siguiente comando:

```bash
python src/main.py
```

El gato aparecerá en tu escritorio. ¡Disfruta!

## Recursos

| Imagen    | Estado     |
| --------- | ---------- |
| gato.png  | QUIETO     |
| gato1.png | CAMINAR 1  |
| gato2.png | CAMINAR 2  |
| gato3.png | IDLE       |
| gato4.png | ESPECIAL   |
| gato5.png | CAÍDA      |
| gato6.png | ATERRIZAJE |
| gato7.png | AGARRADO   |
| icon.ico  | ÍCONO ejecutable |
| gato8.png  | JUGANDO (minijuego) |
| gato9.png  | SALTANDO |
| gato10.png | ACROBACIA |
| gato11.png | ACECHANDO |

### Tipo y tamaño de imágenes

- Usa `PNG` para todas las imágenes del gato. `PNG` mantiene transparencia y calidad cuando el sprite se redimensiona.
- El icono del ejecutable debe ser `ICO` (`assets/icon.ico`) para que Windows lo use correctamente. También puedes crear el icono desde un `PNG` de alta resolución y convertirlo a `ICO`.
- En el código, hay un código comentado para redimensionar las imágenes a `46x44` píxeles en pantalla. Por eso es mejor que las fuentes sean más grandes que ese tamaño, idealmente:
    - `96x92` o `128x120` para las animaciones del gato.
    - `256x256` para el icono del ejecutable.
- Mantén la relación de aspecto aproximada de 46:44 para que la imagen no se vea distorsionada al escalar.
- Si reemplazas imágenes, guarda los nuevos archivos en `assets/` con el mismo nombre y formato `PNG`.

Si necesitas más animaciones en el futuro, crea nuevas imágenes `PNG` con transparencia y añádelas al proyecto. El código usará las nuevas imágenes si se agregan con los nombres sugeridos.

## Ejecutable

Puedes crear un archivo ejecutable con `pyinstaller` usando el archivo de configuración del proyecto (recomendado):

1. Instala `pyinstaller`:

```bash
pip install pyinstaller
```

2. Desde la **raíz del proyecto**, genera el ejecutable:

```bash
pyinstaller DesktopCat.spec
```

El ejecutable `DesktopCat.exe` se creará en la carpeta `dist/`, con el ícono `assets/icon.ico` y opciones pensadas para reducir falsos positivos de antivirus (sin compresión UPX).

> Nota: si usas `main.spec`, también está configurado para `upx=False` y así evitar la compresión que suelen marcar los antivirus.

### Si el antivirus lo marca

Los ejecutables empaquetados con PyInstaller a veces son detectados por error. Para reducir falsos positivos:

- **El `.spec` ya desactiva UPX** (compresión que suelen marcar los antivirus).
- **Añade una excepción** en Windows Defender: Configuración → Privacidad y seguridad → Seguridad de Windows → Protección contra virus → Exclusiones.
- **Reporta falsos positivos**: en [Microsoft Security Intelligence](https://www.microsoft.com/en-us/wdsi/filesubmission) puedes enviar el ejecutable como “False positive” para que lo whitelisten.
- **Los ejecutables PyInstaller pueden seguir siendo escaneados**: incluso sin UPX, algunos antivirus muestran el archivo como sospechoso por heurística. Si el archivo sigue siendo detectado, lo más efectivo es añadir una exclusión local o enviar el ejecutable como falso positivo.

## Nuevas interacciones del gato

- Haz `clic derecho` sobre el gato para que ejecute una acción especial aleatoria.
- Haz `doble clic` sobre el gato para iniciar un minijuego de atrapar al gato. Durante 10 segundos, haz clic sobre el gato para sumar puntos.

### Build manual (sin .spec)

Si prefieres no usar el `.spec`:

```bash
pyinstaller --onefile --windowed --icon=assets/icon.ico --add-data "assets;assets" --noupx src/main.py
```

En Linux/macOS usa `:` en lugar de `;` en `--add-data`.

## Contribuir

Las contribuciones son bienvenidas. Si tienes alguna idea o sugerencia, por favor abre un *issue* o envía un *pull request*.

## Licencia

Este proyecto está bajo la Licencia MIT.