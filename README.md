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

## Ejecutable

Puedes crear un archivo ejecutable con `pyinstaller`.

Primero, instala `pyinstaller`:

```bash
pip install pyinstaller
```

Luego, ejecuta el siguiente comando:

```bash
pyinstaller --onefile --windowed --add-data "assets;assets" src/main.py
```

Esto creará un archivo ejecutable en la carpeta `dist`.

## Contribuir

Las contribuciones son bienvenidas. Si tienes alguna idea o sugerencia, por favor abre un *issue* o envía un *pull request*.

## Licencia

Este proyecto está bajo la Licencia MIT.