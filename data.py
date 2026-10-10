"""
Módulo Data: Contiene la lista inicial RECETARIO_BASE con el esquema extendido de cocina.
Sirve como semilla (seed) para la primera ejecución o para agregar nuevas recetas iniciales.
"""

RECETARIO_BASE = [


    {
        "id": 1,
        "nombre": "Chipá o Pan de Yuca",
        "categoria": "Panadería / Snacking",
        "origen": "Sudamérica (Paraguay/Argentina)",
        "dificultad": "Fácil",
        "tiempo_preparacion_min": 35,
        "porciones": 45,
        "ingredientes": [
            "1000g Mix Quesos (Fresco, Sardo, Mar del Plata) (100%)",
            "800g Almidón de yuca (80%)",
            "200g Almidón de maíz (20%)",
            "15g Polvo de hornear (1.5%)",
            "15g Azúcar (1.5%)",
            "18g Sal (1.8%)",
            "20g Aceite de oliva (2%)",
            "4 Huevo(s)",
            "200g Leche (20%)"
        ],
        "pasos": [
            "Mezclar todos los secos.",
            "Incorporar huevos, leche y aceite.",
            "Sumar los quesos picados y unir.",
            "Formar bollos de 55g y congelar.",
            "Hornear 20 min en freidora de aire."
        ],
        "etiquetas": ["Horneo Rápido", "Tradicional"],
        "nota": "El horneado directo desde congelado preserva la forma y estructura final."
    },
        {
        "id": 2,
        "nombre": "Bondiola en Salsa al Disco",
        "categoria": "Plato Principal / Al Disco",
        "origen": "Argentina",
        "dificultad": "Media",
        "tiempo_preparacion_min": 60,
        "porciones": None,
        "ingredientes": [
            "Bondiola de cerdo en fetas de 2cm",
            "Mix Vegetales: Cebolla, morrón, ajo y apio picados gruesos",
            "Salsa de tomate",
            "Vino blanco o cerveza negra [Opcional]",
            "Aceite y agua",
            "Condimentos: Sal, orégano, pimienta y ají molido"
        ],
        "pasos": [
            "Calentar el disco con aceite, sellar la carne y retirar.",
            "Sofreír cebolla, morrón y apio; incorporar el ajo al final.",
            "Reincorporar la carne, desglasar con vino o cerveza y condimentar.",
            "Verter la salsa de tomate y cocinar a fuego lento.",
            "Hidratar con agua periódicamente hasta reducir la salsa."
        ],
        "etiquetas": ["Al Disco", "Cocción Lenta", "Tradicional"],
        "nota": "La cantidad de ingredientes se ajustan a gusto según la cantidad de comensales.\n  Mantener una buena base de brasas (leña y carbón) para controlar el hervor."
      },
        {
        "id": 3,
        "nombre": "Espresso",
        "categoria": "Café",
        "origen": "Italia",
        "dificultad": "Fácil",
        "tiempo_preparacion_min": 5,
        "porciones": 1,
        "ingredientes": [
            "16g Café molido fino (molienda 2.2)",
            "60ml Agua a 93°C"
        ],
        "pasos": [
            "Calibrar molienda para ratio 1:2.",
            "Distribución y prensado uniforme.",
            "Extraer durante 30 segundos (rendimiento ~30 ml)."
        ],
        "etiquetas": ["Café", "Bebida", "Barista"],
        "nota": "Ajustar la molienda a un punto más fino si la extracción ocurre demasiado rápido."
    }





        ]


