"""
Punto de Entrada: Conecta el recetario semilla con el motor y la interfaz CLI.
"""

import sys
import os



# Activa la navegación con flechas en la consola para sistemas POSIX (Linux/Android/macOS)
try:
    import readline
except ImportError:
    pass  # En Windows readline no existe por defecto, pero tampoco suele necesitarlo



# Agrega la carpeta actual al sys.path para evitar el error de importación en venv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data import RECETARIO_BASE
from core import CatalogEngine
from cli import CatalogCLI


def main():
    engine = CatalogEngine(archivo_json="recetario.json", datos_iniciales=RECETARIO_BASE)
    app = CatalogCLI(engine)
    app.ejecutar()


if __name__ == "__main__":
    main()






