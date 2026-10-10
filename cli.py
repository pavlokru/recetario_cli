"""
Módulo CLI: Interfaz colorida optimizada para vista vertical en pantallas reducidas.
"""

from core import CatalogEngine

# Códigos ANSI
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
BLUE = "\033[94m"
RED = "\033[91m"
DIM = "\033[2m"


class CatalogCLI:
    """Maneja la presentación visual adaptada a móviles (Termux / SSH)."""

    def __init__(self, engine: CatalogEngine):
        self.engine = engine

    def _separador(self):
        print(f"{DIM}{'─' * 38}{RESET}")

    def mostrar_menu(self):
        print(f"\n{CYAN}┌────────────────────────────────────┐{RESET}")
        print(f"{CYAN}│{BOLD}{YELLOW}        🍳 RECETARIO CLI            {RESET}{CYAN}│{RESET}")
        print(f"{CYAN}└────────────────────────────────────┘{RESET}")
        print(f" {GREEN}[1]{RESET} {BOLD}Ver recetario{RESET}")
        print(f" {GREEN}[2]{RESET} {BOLD}Buscar (ingrediente/etiqueta){RESET}")
        print(f" {GREEN}[3]{RESET} {BOLD}Ver detalle de receta{RESET}")
        print(f" {GREEN}[4]{RESET} {BOLD}Agregar nueva receta{RESET}")
        print(f" {GREEN}[5]{RESET} {BOLD}Salir{RESET}")
        self._separador()

    def mostrar_tarjetas(self, items: list[dict]):
        """Presentación resumida tipo tarjeta vertical."""
        if not items:
            print(f"{RED}⚠️  Sin resultados.{RESET}\n")
            return

        for item in items:
            etiq_str = ", ".join(item.get("etiquetas", [])) if isinstance(item.get("etiquetas"), list) else str(item.get("etiquetas", ""))
            tiempo = f"{item.get('tiempo_preparacion_min', 'N/A')} min"

            print(f"{YELLOW}#{item['id']}{RESET} | {BOLD}{CYAN}{item['nombre'][:28]}{RESET}")
            print(f"   {BLUE}Cat:{RESET} {item.get('categoria', 'N/A')[:28]}")
            print(f"   {GREEN}Tiempo:{RESET} {tiempo} | {MAGENTA}Dif:{RESET} {item.get('dificultad', 'N/A')}")
            print(f"   {DIM}Tags:{RESET} {etiq_str[:28]}")
            self._separador()

        print(f"{GREEN}✓ Total mostrados: {len(items)}{RESET}\n")

    def mostrar_ficha(self, item: dict):
        """Detalle completo de la receta adaptado a 38 columnas."""
        tiempo = f"{item.get('tiempo_preparacion_min', 'N/A')} min"
        porciones = f"{item.get('porciones', 'N/A')} porc."
        etiq_str = ", ".join(item.get("etiquetas", [])) if isinstance(item.get("etiquetas"), list) else str(item.get("etiquetas", ""))

        print(f"\n{CYAN}┌────────────────────────────────────┐{RESET}")
        print(f"{CYAN}│{RESET} {BOLD}{YELLOW}RECETA #{item['id']} - {item['nombre'][:19].upper():<19}{RESET} {CYAN}│{RESET}")
        print(f"{CYAN}└────────────────────────────────────┘{RESET}")
        print(f" {BLUE}• Nombre:{RESET} {BOLD}{item['nombre']}{RESET}")
        print(f" {BLUE}• Categoría:{RESET} {item.get('categoria', 'N/A')}")
        print(f" {BLUE}• Origen:{RESET} {item.get('origen', 'N/A')}")
        print(f" {BLUE}• Dificultad:{RESET} {MAGENTA}{item.get('dificultad', 'N/A')}{RESET}")
        print(f" {BLUE}• Rendimiento:{RESET} {YELLOW}{tiempo} | {porciones}{RESET}")
        print(f" {BLUE}• Etiquetas:{RESET} {DIM}{etiq_str}{RESET}")

        print(f"\n {BOLD}{CYAN}🛒 Ingredientes:{RESET}")
        for ing in item.get("ingredientes", []):
            print(f"   • {ing}")

        print(f"\n {BOLD}{CYAN}👨‍🍳 Pasos de Preparación:{RESET}")
        for idx, paso in enumerate(item.get("pasos", []), 1):
            print(f"   {GREEN}{idx}.{RESET} {paso}")

        if item.get("nota"):
            print(f"\n {BOLD}{YELLOW}💡 Tip / Nota del Chef:{RESET}")
            print(f"   {item['nota']}")

        self._separador()

    def ejecutar(self):
        while True:
            self.mostrar_menu()
            opcion = input(f"{BOLD}Opción (1-5): {RESET}").strip()

            if opcion == "1":
                print(f"\n{BOLD}{GREEN}─── 🍳 RECETARIO COMPLETO ───{RESET}")
                self._separador()
                self.mostrar_tarjetas(self.engine.obtener_todos())

            elif opcion == "2":
                criterio = input(f"\n{BOLD}Buscar término: {RESET}").strip()
                items = self.engine.buscar(criterio)
                print(f"\n{BOLD}{GREEN}─── 🔍 RESULTADOS ('{criterio}') ───{RESET}")
                self._separador()
                self.mostrar_tarjetas(items)
            
            elif opcion == "3":
                try:
                    art_id = int(input(f"\n{BOLD}ID del registro: {RESET}").strip())
                    item = self.engine.obtener_por_id(art_id)
                    if item:
                        self.mostrar_ficha(item)
                        sub_opcion = input(f"{BOLD}¿Desea agregar una nueva nota anexa? (s/n): {RESET}").strip().lower()
                        if sub_opcion == "s":
                            nota = input(f"{BOLD}Nota a anexar: {RESET}").strip()
                            if nota:
                                self.engine.agregar_nota(art_id, nota)
                                print(f"{GREEN}✓ Nueva nota anexada con éxito.{RESET}\n")
                    else:
                        print(f"{RED}⚠️ ID #{art_id} no encontrado.{RESET}\n")
                except ValueError:
                    print(f"{RED}⚠️ Ingrese un ID numérico.{RESET}\n")

            elif opcion == "4":
                print(f"\n{BOLD}{GREEN}─── ➕ NUEVA RECETA ───{RESET}")
                nombre = input(f"{BOLD}Nombre de la receta: {RESET}").strip()
                categoria = input(f"{BOLD}Categoría: {RESET}").strip()
                origen = input(f"{BOLD}Origen: {RESET}").strip()
                dificultad = input(f"{BOLD}Dificultad (Fácil/Media/Alta): {RESET}").strip()

                ing_raw = input(f"{BOLD}Ingredientes (sep por coma): {RESET}").strip()
                ingredientes = [i.strip() for i in ing_raw.split(",") if i.strip()]

                pasos_raw = input(f"{BOLD}Pasos (sep por punto '.'): {RESET}").strip()
                pasos = [p.strip() for p in pasos_raw.split(".") if p.strip()]

                etiquetas_raw = input(f"{BOLD}Etiquetas (sep por coma): {RESET}").strip()
                etiquetas = [e.strip() for e in etiquetas_raw.split(",") if e.strip()]

                try:
                    tiempo_in = input(f"{BOLD}Tiempo preparac. (min): {RESET}").strip()
                    tiempo_preparacion_min = int(tiempo_in) if tiempo_in else None

                    porc_in = input(f"{BOLD}Nº Porciones: {RESET}").strip()
                    porciones = int(porc_in) if porc_in else None
                except ValueError:
                    print(f"{RED}⚠️ Tiempos y porciones deben ser números.{RESET}\n")
                    continue

                if nombre:
                    nuevo_item = self.engine.agregar_item(
                        nombre=nombre,
                        categoria=categoria,
                        origen=origen,
                        dificultad=dificultad,
                        tiempo_preparacion_min=tiempo_preparacion_min,
                        porciones=porciones,
                        ingredientes=ingredientes,
                        pasos=pasos,
                        etiquetas=etiquetas,
                    )
                    print(f"\n{GREEN}💾 ¡'{nuevo_item['nombre']}' guardada con ID #{nuevo_item['id']}!{RESET}\n")
                else:
                    print(f"\n{RED}⚠️ El nombre no puede estar vacío.{RESET}\n")

            elif opcion == "5":
                print(f"\n{BOLD}{GREEN}¡Buen provecho! 👨‍🍳🍽️{RESET}\n")
                break
            else:
                print(f"{RED}⚠️ Opción inválida.{RESET}\n")

