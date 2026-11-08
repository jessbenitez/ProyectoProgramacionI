# Pruebas de reportes.py
from datetime import date

from reportes import (
    reporte_filtrado,
    reporte_sector,
    reporte_general,
    reporte_alertas
)

# DATOS FICTICIOS PARA LAS PRUEBAS

mediciones = {
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

sectores = {
    "S01": "Frutillas",
    "S02": "Frambuesas",
    "S03": "Arándanos"
}

HOY = date(2026, 10, 14)

limites = {
    "critico_bajo": 20,
    "ideal_bajo": 40,
    "ideal_alto": 60,
    "critico_alto": 80
}


# 1. PRUEBA DEL REPORTE DE ALERTAS

def test_reporte_alertas():
    resultado = reporte_alertas(mediciones, sectores, limites)

    assert "Frutillas (S01)" in resultado
    assert "2026-10-12: 15%" in resultado
    assert "Frambuesas (S02)" in resultado
    assert "2026-10-12: 85%" in resultado


# 2. PRUEBA DEL REPORTE POR SECTOR

def test_reporte_sector():
    resultado = reporte_sector(
        mediciones,
        sectores,
        "S01",
        limites,
        HOY,
        28
    )

    assert "Frutillas" in resultado
    assert "Humedad máxima: 55%" in resultado
    assert "Humedad mínima: 15%" in resultado
    assert "ALERTA" in resultado


# 3. PRUEBA DEL REPORTE GENERAL

def test_reporte_general():
    resultado = reporte_general(mediciones, sectores, limites, HOY)

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

    resultado = reporte_filtrado(mediciones, sectores, filtro)

    assert "Frutillas" in resultado
    assert "2026-10-12: 15%" in resultado
    assert "Promedio del filtro: 38.33%" in resultado
