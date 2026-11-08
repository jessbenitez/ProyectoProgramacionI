import csv
import json
import os

import validaciones

def campos_csv():
    return ("fecha", "sector", "humedad")


def cargar_configuracion(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        config = json.load(archivo)

    try:
        for clave in ("sectores", "limites", "ventana_dias", "archivos"):
            if clave not in config:
                raise KeyError(f"configuracion.json: falta la clave '{clave}'")
        for clave in ("critico_bajo", "ideal_bajo", "ideal_alto", "critico_alto"):
            if clave not in config["limites"]:
                raise KeyError(f"configuracion.json: falta el límite '{clave}'")
        for clave in ("registros", "usuarios", "carpeta_reportes"):
            if clave not in config["archivos"]:
                raise KeyError(f"configuracion.json: falta el archivo '{clave}'")

        codigos_sectores = list(config["sectores"].keys())
        if not codigos_sectores:
            raise ValueError("configuracion.json: debe haber al menos un sector")
        if config["ventana_dias"] < 1:
            raise ValueError("configuracion.json: 'ventana_dias' debe ser un número positivo")
    except (TypeError, AttributeError):
        raise ValueError("configuracion.json: estructura inválida, revise que cada valor tenga el tipo esperado") from None
    return config


def cargar_registros(ruta, sectores, fecha_referencia, ventana_dias):
    mediciones = {codigo: {} for codigo in sectores}
    rechazadas = []

    with open(ruta, "r", encoding="utf-8", newline="") as archivo:
        lector = csv.DictReader(archivo)
        if lector.fieldnames is None or tuple(lector.fieldnames) != campos_csv():
            raise ValueError(f"Encabezado de CSV inválido: se esperaba {','.join(campos_csv())}")

        for fila in lector:
            linea = lector.line_num
            try:
                if None in fila or None in fila.values():
                    raise ValueError("cantidad de columnas incorrecta")
                fecha = fila["fecha"].strip()
                sector = fila["sector"].strip()
                validaciones.validar_fecha(fecha, fecha_referencia, ventana_dias)
                validaciones.validar_codigo_sector(sector, sectores)
                humedad = validaciones.validar_humedad(fila["humedad"].strip())
                if fecha in mediciones[sector]:
                    raise ValueError(f"medición duplicada para {sector} en {fecha}")
            except ValueError as error:
                rechazadas.append(f"Línea {linea}: {error}")
                continue
            mediciones[sector][fecha] = humedad

    return mediciones, rechazadas


def guardar_registros(ruta, mediciones):
    claves = sorted((fecha, sector) for sector, fechas in mediciones.items() for fecha in fechas)

    with open(ruta, "w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos_csv(), lineterminator="\n")
        escritor.writeheader()
        for fecha, sector in claves:
            escritor.writerow({"fecha": fecha, "sector": sector, "humedad": mediciones[sector][fecha]})


def guardar_reporte(ruta, texto):
    carpeta = os.path.dirname(ruta)
    if carpeta:
        os.makedirs(carpeta, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(texto)
