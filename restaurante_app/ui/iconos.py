import tkinter as tk
from pathlib import Path

# Carpeta donde se guardan los recursos visuales del proyecto.
RUTA_ASSETS = Path(__file__).resolve().parent.parent / "assets"


class GestorIconos:
    """Carga los iconos PNG de assets y los conserva en memoria."""

    def __init__(self, ruta_assets=RUTA_ASSETS):
        self.ruta_assets = Path(ruta_assets)
        self.iconos_cargados = {}

    def obtener(self, nombre):
        # Devuelve el icono solicitado o None si el archivo no existe.
        if nombre in self.iconos_cargados:
            return self.iconos_cargados[nombre]

        # El logo vive en assets/logo/, el resto de iconos en assets/icons/.
        # Se revisan ambas carpetas (y la raiz de assets, por compatibilidad)
        # asi no importa en cual este guardado el archivo.
        posibles_rutas = [
            self.ruta_assets / "logo" / f"{nombre}.png",
            self.ruta_assets / "icons" / f"{nombre}.png",
            self.ruta_assets / f"{nombre}.png",
        ]

        icono = None
        for ruta in posibles_rutas:
            if ruta.exists():
                try:
                    icono = tk.PhotoImage(file=str(ruta))
                except tk.TclError:
                    icono = None
                break

        # Se guarda la referencia para que Tkinter no elimine la imagen.
        self.iconos_cargados[nombre] = icono
        return icono


# Instancia compartida por todas las vistas de la aplicacion.
iconos = GestorIconos()
