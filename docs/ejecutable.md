# Ejecutable

[← Volver al README](../README.md) · [Instalación](instalacion.md) · [Recursos](recursos.md)

Puedes crear un archivo ejecutable con `pyinstaller` usando el archivo de configuración del proyecto (recomendado).

## Con el archivo `.spec`

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

## Build manual (sin `.spec`)

Si prefieres no usar el `.spec`:

```bash
pyinstaller --onefile --windowed --icon=assets/icon.ico --add-data "assets;assets" --noupx src/main.py
```

En Linux/macOS usa `:` en lugar de `;` en `--add-data`.

## Si el antivirus lo marca

Los ejecutables empaquetados con PyInstaller a veces son detectados por error. Para reducir falsos positivos:

- **El `.spec` ya desactiva UPX** (compresión que suelen marcar los antivirus).
- **Añade una excepción** en Windows Defender: Configuración → Privacidad y seguridad → Seguridad de Windows → Protección contra virus → Exclusiones.
- **Reporta falsos positivos**: en [Microsoft Security Intelligence](https://www.microsoft.com/en-us/wdsi/filesubmission) puedes enviar el ejecutable como “False positive” para que lo whitelisten.
- **Los ejecutables PyInstaller pueden seguir siendo escaneados**: incluso sin UPX, algunos antivirus muestran el archivo como sospechoso por heurística. Si el archivo sigue siendo detectado, lo más efectivo es añadir una exclusión local o enviar el ejecutable como falso positivo.

## Ver también

- [Instalación](instalacion.md) — entorno y dependencias previas
- [Recursos](recursos.md) — assets incluidos en el ejecutable
