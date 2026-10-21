# Pruebas de operaciones.py (registro y modificación de mediciones)
import pytest

import operaciones


def test_registrar_medicion_agrega_la_medicion():
    mediciones = {"S01": {}}
    operaciones.registrar_medicion(mediciones, "S01", "2026-10-12", 45.5)
    assert mediciones == {"S01": {"2026-10-12": 45.5}}


def test_registrar_duplicado_lanza_excepcion_y_no_pisa_el_valor():
    mediciones = {"S01": {"2026-10-12": 45.5}}
    with pytest.raises(ValueError, match="Modificar"):
        operaciones.registrar_medicion(mediciones, "S01", "2026-10-12", 70.0)
    assert mediciones["S01"]["2026-10-12"] == 45.5


def test_buscar_medicion_existente():
    assert operaciones.buscar_medicion({"S01": {"2026-10-12": 45.5}}, "S01", "2026-10-12") == 45.5


def test_buscar_medicion_inexistente():
    with pytest.raises(ValueError):
        operaciones.buscar_medicion({"S01": {}}, "S01", "2026-10-12")
    with pytest.raises(ValueError):
        operaciones.buscar_medicion({"S01": {}}, "S09", "2026-10-12")


def test_modificar_medicion_cambia_solo_la_indicada():
    mediciones = {"S01": {"2026-10-12": 45.5, "2026-10-13": 50.0}, "S02": {"2026-10-12": 70.0}}
    operaciones.modificar_medicion(mediciones, "S01", "2026-10-12", 52.0)
    assert mediciones == {"S01": {"2026-10-12": 52.0, "2026-10-13": 50.0}, "S02": {"2026-10-12": 70.0}}


def test_modificar_medicion_inexistente_lanza_excepcion():
    mediciones = {"S01": {}}
    with pytest.raises(ValueError):
        operaciones.modificar_medicion(mediciones, "S01", "2026-10-12", 52.0)
    assert mediciones == {"S01": {}}
