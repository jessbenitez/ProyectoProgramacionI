# Pruebas de reportes.py
from datetime import date

from reportes import (
    reporte_filtrado,
    reporte_sector,
    reporte_general,
    reporte_alertas
)

# DATOS FICTICIOS PARA LAS PRUEBAS


def datos_mediciones():
    return {
        "S01": {
            "2026-10-12": 15,
            "2026-10-13": 45,
            "2026-10-14": 55
        },
        "S02": {
            "2026-10-12": 85,
            "2026-10-13": 50
        },
        "S03": {}
    }


def datos_sectores():
    return {
        "S01": "Frutillas",
        "S02": "Frambuesas",
        "S03": "Arándanos"
    }


def datos_hoy():
    return date(2026, 10, 14)


def datos_limites():
    return {
        "critico_bajo": 20,
        "ideal_bajo": 40,
        "ideal_alto": 60,
        "critico_alto": 80
    }


# 1. PRUEBA DEL REPORTE DE ALERTAS

def test_reporte_alertas():
    resultado = reporte_alertas(datos_mediciones(), datos_sectores(), datos_limites())

    assert "Frutillas (S01)" in resultado
    assert "2026-10-12: 15%" in resultado
    assert "Frambuesas (S02)" in resultado
    assert "2026-10-12: 85%" in resultado


# 2. PRUEBA DEL REPORTE POR SECTOR

def test_reporte_sector():
    resultado = reporte_sector(
        datos_mediciones(),
        datos_sectores(),
        "S01",
        datos_limites(),
        datos_hoy(),
        28
    )

    assert "Frutillas" in resultado
    assert "Humedad máxima: 55%" in resultado
    assert "Humedad mínima: 15%" in resultado
    assert "ALERTA" in resultado


# 3. PRUEBA DEL REPORTE GENERAL

def test_reporte_general():
    resultado = reporte_general(datos_mediciones(), datos_sectores(), datos_limites(), datos_hoy())

    assert "REPORTE GENERAL DEL CAMPO" in resultado
    assert "PROMEDIO POR SECTOR" in resultado
    assert "PROMEDIO POR FECHA" in resultado
    assert "SECTORES SIN MEDICIONES" in resultado
    assert "Arándanos (S03)" in resultado


# 4. PRUEBA DEL REPORTE FILTRADO

def test_reporte_filtrado():
    filtro = {
        "codigo_sector": "S01",
        "desde": "2026-10-12",
        "hasta": "2026-10-14"
    }

    resultado = reporte_filtrado(datos_mediciones(), datos_sectores(), filtro)

    assert "Frutillas" in resultado
    assert "2026-10-12: 15%" in resultado
    assert "Promedio del filtro: 38.33%" in resultado


# 5. PRUEBAS ADICIONALES

def test_reporte_sector_sin_mediciones():
    resultado = reporte_sector(datos_mediciones(), datos_sectores(), "S03", datos_limites(), datos_hoy(), 28)

    assert "Arándanos" in resultado
    assert "Sin mediciones en el período" in resultado


def test_reporte_sector_incluye_solo_sus_alertas():
    resultado = reporte_sector(datos_mediciones(), datos_sectores(), "S01", datos_limites(), datos_hoy(), 28)

    assert "ALERTA - 2026-10-12: 15%" in resultado
    assert "85%" not in resultado


def test_reporte_sector_ignora_mediciones_fuera_de_la_ventana():
    con_antigua = {"S01": {"2026-10-14": 50, "2026-08-01": 10}}
    resultado = reporte_sector(con_antigua, datos_sectores(), "S01", datos_limites(), datos_hoy(), 28)

    assert "2026-08-01" not in resultado
    assert "Humedad mínima: 50%" in resultado


def test_reporte_alertas_sin_criticas():
    sin_alertas = {"S01": {"2026-10-12": 20, "2026-10-13": 80}}
    resultado = reporte_alertas(sin_alertas, datos_sectores(), datos_limites())

    assert "No se registraron mediciones críticas." in resultado


def test_reporte_general_sin_mediciones():
    vacias = {"S01": {}, "S02": {}}
    resultado = reporte_general(vacias, datos_sectores(), datos_limites(), datos_hoy())

    assert "Sin mediciones registradas." in resultado
    assert "Todos los sectores tienen mediciones." not in resultado


def test_reporte_filtrado_sin_resultados():
    filtro = {"codigo_sector": "S03"}
    resultado = reporte_filtrado(datos_mediciones(), datos_sectores(), filtro)

    assert "Sin mediciones para los filtros seleccionados." in resultado
    assert "Promedio del filtro: Sin mediciones" in resultado
