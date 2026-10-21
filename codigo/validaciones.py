"""Validaciones de formato (expresiones regulares) y de coherencia. Lanzan ValueError con el formato esperado."""
import re
from datetime import datetime, timedelta


def validar_fecha(fecha, fecha_referencia, ventana_dias):
    """Formato AAAA-MM-DD, fecha real y dentro de la ventana de ventana_dias hasta fecha_referencia (sin fechas futuras).

    fecha_referencia es un objeto date (normalmente la fecha de hoy), recibido por parámetro.
    Devuelve la fecha como objeto date.
    """
    if not isinstance(fecha, str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", fecha):
        raise ValueError("Fecha inválida: se esperaba el formato AAAA-MM-DD (ej: 2026-10-12)")

    try:
        fecha_real = datetime.strptime(fecha, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(f"Fecha inválida: {fecha} no existe en el calendario") from None

    desde = fecha_referencia - timedelta(days=ventana_dias - 1)
    if fecha_real > fecha_referencia or fecha_real < desde:
        raise ValueError(f"Fecha fuera de rango: debe estar entre {desde} y {fecha_referencia}")
    return fecha_real


def validar_codigo_sector(codigo, sectores):
    """Formato S## y existencia en el diccionario de sectores de la configuración. Devuelve el código."""
    if not isinstance(codigo, str) or not re.fullmatch(r"S[0-9]{2}", codigo):
        raise ValueError("Sector inválido: se esperaba el formato S## (ej: S01)")
    if codigo not in sectores:
        raise ValueError(f"Sector inexistente: los sectores válidos son {', '.join(sectores)}")
    return codigo


def validar_humedad(humedad):
    """Formato numérico (hasta 2 decimales) y rango 0-100. Devuelve el valor como float."""
    texto = str(humedad)
    if not re.fullmatch(r"[0-9]{1,3}(\.[0-9]{1,2})?", texto):
        raise ValueError("Humedad inválida: se esperaba un número de 0 a 100 con hasta 2 decimales, usando punto (ej: 45.5)")
    valor = float(texto)
    if valor > 100:
        raise ValueError("Humedad fuera de rango: debe estar entre 0 y 100")
    return valor


def validar_usuario(usuario):
    """Formato de nombre de usuario: minúsculas, dígitos o guion bajo, de 3 a 20 caracteres."""
    if not isinstance(usuario, str) or not re.fullmatch(r"[a-z0-9_]{3,20}", usuario):
        raise ValueError("Usuario inválido: se esperaban de 3 a 20 caracteres entre minúsculas, dígitos o guion bajo")
    return usuario
