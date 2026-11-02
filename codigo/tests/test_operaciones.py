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


LIMITES = {"critico_bajo": 20, "ideal_bajo": 40, "ideal_alto": 60, "critico_alto": 80}

MEDICIONES = {
    "S01": {"2026-10-12": 45.5, "2026-10-10": 15.0, "2026-10-14": 85.0},
    "S02": {"2026-10-12": 79.0, "2026-10-13": 20.0},
    "S03": {},
}


def test_humedad_15_y_85_son_criticas():
    assert operaciones.es_critica(15, LIMITES)
    assert operaciones.es_critica(85, LIMITES)


def test_limites_20_y_80_no_son_criticos():
    assert not operaciones.es_critica(20, LIMITES)
    assert not operaciones.es_critica(80, LIMITES)
    assert operaciones.es_critica(19.99, LIMITES)
    assert operaciones.es_critica(80.01, LIMITES)


def test_limites_40_y_60_son_ideales():
    assert operaciones.es_ideal(40, LIMITES)
    assert operaciones.es_ideal(60, LIMITES)
    assert not operaciones.es_ideal(39.99, LIMITES)
    assert not operaciones.es_ideal(60.01, LIMITES)


def test_values_per_sector_devuelve_las_mediciones_del_sector():
    assert operaciones.getValuesPerSector(MEDICIONES, "S02") == {"2026-10-12": 79.0, "2026-10-13": 20.0}


def test_values_per_sector_devuelve_una_copia():
    mediciones = {"S01": {"2026-10-12": 45.5}}
    valores = operaciones.getValuesPerSector(mediciones, "S01")
    valores["2026-10-13"] = 99.0
    assert mediciones == {"S01": {"2026-10-12": 45.5}}


def test_values_per_sector_inexistente_lanza_excepcion():
    with pytest.raises(ValueError):
        operaciones.getValuesPerSector(MEDICIONES, "S09")


def test_order_humidity_de_mayor_a_menor():
    resultado = operaciones.orderHumidityValues(MEDICIONES["S01"])
    assert resultado == [("2026-10-14", 85.0), ("2026-10-12", 45.5), ("2026-10-10", 15.0)]


def test_order_humidity_de_menor_a_mayor():
    resultado = operaciones.orderHumidityValues(MEDICIONES["S01"], descendente=False)
    assert resultado == [("2026-10-10", 15.0), ("2026-10-12", 45.5), ("2026-10-14", 85.0)]


def test_order_humidity_sector_vacio():
    assert operaciones.orderHumidityValues({}) == []


def test_critical_values_devuelve_codigos_de_sector():
    promedios = {"S01": 15.0, "S02": 50.0, "S03": 85.0, "S04": None, "S05": 20.0}
    assert operaciones.getCriticalValues(promedios, LIMITES) == ["S01", "S03"]


def test_ideal_values_devuelve_codigos_de_sector():
    promedios = {"S01": 40.0, "S02": 61.0, "S03": 60.0, "S04": None, "S05": 39.0}
    assert operaciones.getIdealValues(promedios, LIMITES) == ["S01", "S03"]


def test_critical_e_ideal_sin_sectores():
    assert operaciones.getCriticalValues({}, LIMITES) == []
    assert operaciones.getIdealValues({}, LIMITES) == []


def test_mediciones_criticas_solo_incluye_las_del_sector_correspondiente():
    alertas = operaciones.obtener_mediciones_criticas(MEDICIONES, LIMITES)
    assert alertas == {
        "S01": {"2026-10-10": 15.0, "2026-10-14": 85.0},
        "S02": {},
        "S03": {},
    }


def test_filtrar_por_sector():
    resultado = operaciones.filtrar_registros(MEDICIONES, codigo_sector="S02")
    assert resultado == {"S02": {"2026-10-12": 79.0, "2026-10-13": 20.0}}


def test_filtrar_por_una_fecha():
    resultado = operaciones.filtrar_registros(MEDICIONES, desde="2026-10-12", hasta="2026-10-12")
    assert resultado == {"S01": {"2026-10-12": 45.5}, "S02": {"2026-10-12": 79.0}, "S03": {}}


def test_filtrar_por_rango_incluye_los_bordes():
    resultado = operaciones.filtrar_registros(MEDICIONES, codigo_sector="S01",
                                              desde="2026-10-10", hasta="2026-10-12")
    assert resultado == {"S01": {"2026-10-10": 15.0, "2026-10-12": 45.5}}


def test_filtrar_devuelve_fechas_ordenadas():
    resultado = operaciones.filtrar_registros(MEDICIONES, codigo_sector="S01")
    assert list(resultado["S01"]) == ["2026-10-10", "2026-10-12", "2026-10-14"]


def test_filtrar_sin_criterios_devuelve_todo():
    assert operaciones.filtrar_registros(MEDICIONES) == MEDICIONES


def test_filtrar_no_modifica_el_original():
    mediciones = {"S01": {"2026-10-12": 45.5, "2026-10-13": 50.0}}
    operaciones.filtrar_registros(mediciones, desde="2026-10-13")
    assert mediciones == {"S01": {"2026-10-12": 45.5, "2026-10-13": 50.0}}


def test_filtrar_rango_invertido_lanza_excepcion():
    with pytest.raises(ValueError, match="Rango inválido"):
        operaciones.filtrar_registros(MEDICIONES, desde="2026-10-14", hasta="2026-10-10")


def test_filtrar_sector_inexistente_lanza_excepcion():
    with pytest.raises(ValueError):
        operaciones.filtrar_registros(MEDICIONES, codigo_sector="S09")