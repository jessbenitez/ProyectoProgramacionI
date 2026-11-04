"""Acceso a archivos: CSV, JSON y texto. Lanza excepciones de E/S; quien interactúa con el usuario las captura."""
import csv
import json
import os

import validaciones

CAMPOS_CSV = ("fecha", "sector", "humedad")


def cargar_configuracion(ruta):
    """Lee configuracion.json y devuelve el diccionario de configuración. No reemplaza silenciosamente un archivo faltante o inválido.

    Lanza FileNotFoundError si no existe, json.JSONDecodeError si no es JSON válido,
    KeyError si falta una clave obligatoria y ValueError si un valor es inválido.
    """
    with open(ruta, "r", encoding="utf-8") as archivo:
        config = json.load(archivo)

    if not isinstance(config, dict):
        raise ValueError("configuracion.json: se esperaba un objeto JSON")

    for clave in ("sectores", "limites", "ventana_dias", "archivos"):
        if clave not in config:
            raise KeyError(f"configuracion.json: falta la clave '{clave}'")
    for clave in ("critico_bajo", "ideal_bajo", "ideal_alto", "critico_alto"):
        if clave not in config["limites"]:
            raise KeyError(f"configuracion.json: falta el límite '{clave}'")
    for clave in ("registros", "usuarios", "carpeta_reportes"):
        if clave not in config["archivos"]:
            raise KeyError(f"configuracion.json: falta el archivo '{clave}'")

    if not isinstance(config["sectores"], dict) or not config["sectores"]:
        raise ValueError("configuracion.json: 'sectores' debe ser un objeto no vacío")
    if not isinstance(config["ventana_dias"], int) or config["ventana_dias"] < 1:
        raise ValueError("configuracion.json: 'ventana_dias' debe ser un entero positivo")
    return config


def cargar_registros(ruta, sectores, fecha_referencia, ventana_dias):
    """Lee el CSV y devuelve (mediciones, rechazadas): mediciones[sector][fecha] = humedad, y la lista de filas rechazadas con línea y motivo.

    Todos los sectores de la configuración aparecen en mediciones, aunque no tengan datos.
    Las filas inválidas, duplicadas o fuera de la ventana no se incorporan: se informan en rechazadas
    como textos "Línea N: motivo". Si hay duplicados se conserva la primera medición.
    Lanza FileNotFoundError si el archivo no existe y ValueError si el encabezado es incorrecto.
    """
    mediciones = {codigo: {} for codigo in sectores}
    rechazadas = []

    with open(ruta, "r", encoding="utf-8", newline="") as archivo:
        lector = csv.DictReader(archivo)
        if lector.fieldnames is None or tuple(lector.fieldnames) != CAMPOS_CSV:
            raise ValueError(f"Encabezado de CSV inválido: se esperaba {','.join(CAMPOS_CSV)}")

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
    """Sobrescribe el CSV con el diccionario en memoria, ordenado por fecha y sector, con encabezado fecha,sector,humedad."""
    claves = sorted((fecha, sector) for sector, fechas in mediciones.items() for fecha in fechas)

    with open(ruta, "w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=CAMPOS_CSV, lineterminator="\n")
        escritor.writeheader()
        for fecha, sector in claves:
            escritor.writerow({"fecha": fecha, "sector": sector, "humedad": mediciones[sector][fecha]})


def guardar_reporte(ruta, texto):
    """Escribe un archivo de texto de reporte, creando la carpeta si falta."""
    carpeta = os.path.dirname(ruta)
    if carpeta:
        os.makedirs(carpeta, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(texto)
