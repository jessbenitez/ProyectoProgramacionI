import os
import random
import sys
from datetime import date, timedelta

import archivos


def generar_mediciones(sectores, hoy, ventana_dias):
    paso_por_sector = {"S01": 1, "S02": 2, "S03": 4}
    dias_fijos_s04 = (0, 13, 27)

    valores_fijos = {
        ("S01", 27): 20, ("S01", 20): 40, ("S01", 13): 60, ("S01", 6): 80,
        ("S01", 2): 12.5, ("S01", 9): 91.0,
        ("S02", 0): 15, ("S02", 8): 85.5,
        ("S03", 4): 18.25,
        ("S04", 13): 79.9,
    }

    rng = random.Random(404)
    mediciones = {codigo: {} for codigo in sectores}
    for sector in sectores:
        if sector in paso_por_sector:
            dias = range(0, ventana_dias, paso_por_sector[sector])
        elif sector == "S04":
            dias = dias_fijos_s04
        else:
            dias = ()
        for atras in dias:
            fecha = (hoy - timedelta(days=atras)).isoformat()
            mediciones[sector][fecha] = valores_fijos.get((sector, atras), round(rng.uniform(25, 75), 1))
    mediciones["S01"][(hoy - timedelta(days=ventana_dias + 2)).isoformat()] = 47.2
    return mediciones


def filas_invalidas(hoy, ventana_dias):
    dentro = (hoy - timedelta(days=5)).isoformat()
    return [
        f"{hoy - timedelta(days=ventana_dias)},S02,50",
        f"{hoy + timedelta(days=1)},S02,50",
        "12/10/2026,S02,50",
        f"{hoy.year}-02-30,S02,50",
        f"{dentro},S99,50",
        f"{dentro},S02,150",
        f"{dentro},S02,abc",
        f"{dentro},S02",
        f"{(hoy - timedelta(days=1)).isoformat()},S01,33.3",
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
