# Pruebas de validaciones.py
from datetime import date

import pytest

import validaciones

HOY = date(2026, 10, 14)
SECTORES = {"S01": "Frutillas", "S02": "Frambuesas"}


# --- fecha ---
def test_fecha_valida():
    assert validaciones.validar_fecha("2026-10-12", HOY, 28) == date(2026, 10, 12)


@pytest.mark.parametrize("fecha", ["2026-02-30", "2026-13-01", "12/10/2026", "2026-1-5", "", "abc", "2026-10-12\n"])
def test_fecha_formato_o_calendario_invalido(fecha):
    with pytest.raises(ValueError):
        validaciones.validar_fecha(fecha, HOY, 28)


def test_fecha_mensaje_indica_formato_esperado():
    with pytest.raises(ValueError, match="AAAA-MM-DD"):
        validaciones.validar_fecha("12/10/2026", HOY, 28)


def test_fecha_limites_de_la_ventana():
    # hoy y hoy menos 27 días se aceptan; hoy menos 28 días y mañana se rechazan
    assert validaciones.validar_fecha("2026-10-14", HOY, 28) == HOY
    assert validaciones.validar_fecha("2026-09-17", HOY, 28) == date(2026, 9, 17)
    with pytest.raises(ValueError):
        validaciones.validar_fecha("2026-09-16", HOY, 28)
    with pytest.raises(ValueError):
        validaciones.validar_fecha("2026-10-15", HOY, 28)


# --- sector ---
def test_sector_valido():
    assert validaciones.validar_codigo_sector("S01", SECTORES) == "S01"


@pytest.mark.parametrize("codigo", ["s01", "S1", "S001", "1", "", "S01 "])
def test_sector_formato_invalido(codigo):
    with pytest.raises(ValueError, match="S##"):
        validaciones.validar_codigo_sector(codigo, SECTORES)


def test_sector_con_formato_correcto_pero_inexistente():
    with pytest.raises(ValueError, match="inexistente"):
        validaciones.validar_codigo_sector("S09", SECTORES)


# --- humedad ---
@pytest.mark.parametrize("texto, esperado", [("0", 0.0), ("45", 45.0), ("45.5", 45.5), ("100", 100.0), ("99.99", 99.99)])
def test_humedad_valida_incluye_limites(texto, esperado):
    assert validaciones.validar_humedad(texto) == esperado


@pytest.mark.parametrize("texto", ["-1", "101", "100.5", "abc", "", "45,5", "45.555", "1e2", " 45"])
def test_humedad_invalida(texto):
    with pytest.raises(ValueError):
        validaciones.validar_humedad(texto)


def test_humedad_rechaza_el_centinela_de_etapa_1():
    with pytest.raises(ValueError):
        validaciones.validar_humedad("-1")


# --- usuario ---
def test_usuario_valido():
    assert validaciones.validar_usuario("nicole_96") == "nicole_96"


@pytest.mark.parametrize("usuario", ["ab", "Nicole", "nicole!", "a" * 21, ""])
def test_usuario_invalido(usuario):
    with pytest.raises(ValueError):
        validaciones.validar_usuario(usuario)
