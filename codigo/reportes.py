"""Armado de reportes como strings (sin I/O). La escritura a archivo está en archivos.py."""


def reporte_filtrado(mediciones, sectores, filtro):
    """Mediciones de un sector, fecha o rango, con el promedio del filtro."""
    raise NotImplementedError


def reporte_sector(mediciones, sectores, codigo_sector, limites):
    """Mediciones, indicadores y alertas de un sector."""
    raise NotImplementedError


def reporte_general(mediciones, sectores, limites):
    """Indicadores de todo el campo, promedio por sector, alertas consolidadas y sectores sin mediciones."""
    raise NotImplementedError


def reporte_alertas(mediciones, sectores, limites):
    """Mediciones y sectores críticos con fecha y valor."""
    raise NotImplementedError
