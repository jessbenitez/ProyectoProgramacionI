"""Acceso a archivos: CSV, JSON y texto. Lanza excepciones de E/S; quien interactúa con el usuario las captura."""


def cargar_configuracion(ruta):
    """Lee configuracion.json y devuelve el diccionario de configuración. No reemplaza silenciosamente un archivo faltante o inválido."""
    raise NotImplementedError


def cargar_registros(ruta, sectores, fecha_referencia, ventana_dias):
    """Lee el CSV y devuelve (mediciones, rechazadas): mediciones[sector][fecha] = humedad, y la lista de filas rechazadas con línea y motivo."""
    raise NotImplementedError


def guardar_registros(ruta, mediciones):
    """Sobrescribe el CSV con el diccionario en memoria, ordenado por fecha y sector, con encabezado fecha,sector,humedad."""
    raise NotImplementedError


def guardar_reporte(ruta, texto):
    """Escribe un archivo de texto de reporte, creando la carpeta si falta."""
    raise NotImplementedError
