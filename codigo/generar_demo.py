"""Regenera los datos de demostración con fechas relativas a hoy (la ventana es móvil).

Uso: python generar_demo.py [AAAA-MM-DD]   (sin argumento usa la fecha actual)
Escribe datos/registros.csv (válido) y datos/registros_con_errores.csv (con filas inválidas).
"""
import os
import random
import sys
from datetime import date, timedelta

import archivos

# Cada sector tiene distinta cantidad de mediciones: se registra cada N días hacia atrás. S05 queda sin datos.
PASO_POR_SECTOR = {"S01": 1, "S02": 2, "S03": 4}
DIAS_FIJOS_S04 = (0, 13, 27)

# (sector, días hacia atrás desde hoy) -> humedad. Cubre críticos, ideales y valores límite.
VALORES_FIJOS = {
    ("S01", 27): 20, ("S01", 20): 40, ("S01", 13): 60, ("S01", 6): 80,
    ("S01", 2): 12.5, ("S01", 9): 91.0,
    ("S02", 0): 15, ("S02", 8): 85.5,
    ("S03", 4): 18.25,
    ("S04", 13): 79.9,
}


def generar_mediciones(sectores, hoy, ventana_dias):
    rng = random.Random(404)  # semilla fija: mismos valores en cada regeneración
    mediciones = {codigo: {} for codigo in sectores}
    for sector in sectores:
        if sector in PASO_POR_SECTOR:
            dias = range(0, ventana_dias, PASO_POR_SECTOR[sector])
        elif sector == "S04":
            dias = DIAS_FIJOS_S04
        else:
            dias = ()
        for atras in dias:
            fecha = (hoy - timedelta(days=atras)).isoformat()
            mediciones[sector][fecha] = VALORES_FIJOS.get((sector, atras), round(rng.uniform(25, 75), 1))
    # Un registro anterior a la ventana: se informa al cargar y no se reescribe al guardar.
    mediciones["S01"][(hoy - timedelta(days=ventana_dias + 2)).isoformat()] = 47.2
    return mediciones


def filas_invalidas(hoy, ventana_dias):
    dentro = (hoy - timedelta(days=5)).isoformat()
    return [
        f"{hoy - timedelta(days=ventana_dias)},S02,50",  # justo fuera de la ventana
        f"{hoy + timedelta(days=1)},S02,50",  # fecha futura
        "12/10/2026,S02,50",  # formato de fecha
        f"{hoy.year}-02-30,S02,50",  # fecha inexistente
        f"{dentro},S99,50",  # sector inexistente
        f"{dentro},S02,150",  # humedad fuera de rango
        f"{dentro},S02,abc",  # humedad no numérica
        f"{dentro},S02",  # faltan columnas
        f"{(hoy - timedelta(days=1)).isoformat()},S01,33.3",  # duplicado de una fila válida (se conserva la primera)
    ]


def main():
    hoy = date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else date.today()
    carpeta = os.path.dirname(os.path.abspath(__file__))
    config = archivos.cargar_configuracion(os.path.join(carpeta, "datos", "configuracion.json"))
    ventana = config["ventana_dias"]
    mediciones = generar_mediciones(config["sectores"], hoy, ventana)

    ruta_ok = os.path.join(carpeta, config["archivos"]["registros"])
    archivos.guardar_registros(ruta_ok, mediciones)

    ruta_errores = os.path.join(os.path.dirname(ruta_ok), "registros_con_errores.csv")
    archivos.guardar_registros(ruta_errores, mediciones)
    with open(ruta_errores, "a", encoding="utf-8", newline="") as archivo:
        archivo.write("\n".join(filas_invalidas(hoy, ventana)) + "\n")

    print(f"Datos de demostración generados con fecha de referencia {hoy}:\n  {ruta_ok}\n  {ruta_errores}")


if __name__ == "__main__":
    main()
