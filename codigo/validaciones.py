"""Validaciones de formato (expresiones regulares) y de coherencia. Lanzan ValueError con el formato esperado."""


def validar_fecha(fecha, fecha_referencia, ventana_dias):
    """Formato AAAA-MM-DD, fecha real y dentro de la ventana de ventana_dias hasta fecha_referencia (sin fechas futuras)."""
    raise NotImplementedError


def validar_codigo_sector(codigo, sectores):
    """Formato S## y existencia en el diccionario de sectores de la configuración."""
    raise NotImplementedError


def validar_humedad(humedad):
    """Formato numérico (hasta 2 decimales) y rango 0-100. Devuelve el valor como float."""
    raise NotImplementedError


def validar_usuario(usuario):
    """Formato de nombre de usuario: minúsculas, dígitos o guion bajo, de 3 a 20 caracteres."""
    raise NotImplementedError
