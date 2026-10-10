"""
Módulo Core: Lógica de negocio, búsqueda profunda y fusión automática entre data.py y recetario.json.
"""

import json
import os
from typing import List, Dict, Optional


class CatalogEngine:
    """Motor de búsqueda, persistencia y sincronización de recetas."""

    def __init__(self, archivo_json: str = "recetario.json", datos_iniciales: Optional[List[Dict]] = None):
        self.archivo_json = archivo_json
        self.items = self._cargar_datos(datos_iniciales)

    def _cargar_datos(self, datos_iniciales: Optional[List[Dict]] = None) -> List[Dict]:
        """Carga datos del JSON y fusiona nuevos registros por ID desde data.py."""
        datos_iniciales = datos_iniciales or []

        if not os.path.exists(self.archivo_json):
            self._guardar_en_disco(datos_iniciales)
            return datos_iniciales

        try:
            with open(self.archivo_json, "r", encoding="utf-8") as f:
                items_json = json.load(f)
        except (json.JSONDecodeError, OSError):
            items_json = []

        ids_existentes = {item["id"] for item in items_json if "id" in item}

        hubo_cambios = False
        for receta in datos_iniciales:
            if receta.get("id") not in ids_existentes:
                items_json.append(receta)
                hubo_cambios = True

        if hubo_cambios:
            items_json.sort(key=lambda x: x.get("id", 0))
            self._guardar_en_disco(items_json)

        return items_json

    def _guardar_en_disco(self, items: Optional[List[Dict]] = None):
        """Persiste el estado del recetario en el archivo JSON."""
        datos_a_guardar = items if items is not None else self.items
        with open(self.archivo_json, "w", encoding="utf-8") as f:
            json.dump(datos_a_guardar, f, ensure_ascii=False, indent=4)

    def obtener_todos(self) -> List[Dict]:
        return self.items

    def buscar(self, criterio: str) -> List[Dict]:
        """Búsqueda recursiva en campos simples y listas (ingredientes, etiquetas, pasos)."""
        criterio_norm = criterio.strip().lower()
        if not criterio_norm:
            return self.items

        resultados = []
        for item in self.items:
            buffer_texto = []
            for val in item.values():
                if isinstance(val, list):
                    buffer_texto.append(" ".join(str(v) for v in val))
                elif val is not None:
                    buffer_texto.append(str(val))

            texto_completo = " ".join(buffer_texto).lower()
            if criterio_norm in texto_completo:
                resultados.append(item)
        return resultados

    def obtener_por_id(self, item_id: int) -> Optional[Dict]:
        for item in self.items:
            if item.get("id") == item_id:
                return item
        return None

    def agregar_nota(self, item_id: int, nueva_nota: str) -> bool:
        """Agrega una nota anexa acumulándola al historial de notas del registro."""
        item = self.obtener_por_id(item_id)
        if item:
            nota_actual = item.get("nota")
            if nota_actual:
                item["nota"] = f"{nota_actual}\n   • {nueva_nota}"
            else:
                item["nota"] = f"• {nueva_nota}"

            self._guardar_en_disco()
            return True
        return False

    def agregar_item(
        self,
        nombre: str,
        categoria: str,
        origen: str,
        dificultad: str,
        tiempo_preparacion_min: Optional[int],
        porciones: Optional[int],
        ingredientes: List[str],
        pasos: List[str],
        etiquetas: List[str],
    ) -> Dict:
        """Inserta una receta nueva asignando un ID incremental."""
        nuevo_id = max([item["id"] for item in self.items], default=0) + 1
        nuevo_item = {
            "id": nuevo_id,
            "nombre": nombre,
            "categoria": categoria,
            "origen": origen,
            "dificultad": dificultad,
            "tiempo_preparacion_min": tiempo_preparacion_min,
            "porciones": porciones,
            "ingredientes": ingredientes,
            "pasos": pasos,
            "etiquetas": etiquetas,
            "nota": None,
        }
        self.items.append(nuevo_item)
        self._guardar_en_disco()
        return nuevo_item

