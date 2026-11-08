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


def datos_limites():
    return {"critico_bajo": 20, "ideal_bajo": 40, "ideal_alto": 60, "critico_alto": 80}


def datos_mediciones():
    return {
        "S01": {"2026-10-12": 45.5, "2026-10-10": 15.0, "2026-10-14": 85.0},
        "S02": {"2026-10-12": 79.0, "2026-10-13": 20.0},
        "S03": {},
    }


def test_humedad_15_y_85_son_criticas():
    assert operaciones.es_critica(15, datos_limites())
    assert operaciones.es_critica(85, datos_limites())


def test_limites_20_y_80_no_son_criticos():
    assert not operaciones.es_critica(20, datos_limites())
    assert not operaciones.es_critica(80, datos_limites())
    assert operaciones.es_critica(19.99, datos_limites())
    assert operaciones.es_critica(80.01, datos_limites())


def test_limites_40_y_60_son_ideales():
    assert operaciones.es_ideal(40, datos_limites())
    assert operaciones.es_ideal(60, datos_limites())
    assert not operaciones.es_ideal(39.99, datos_limites())
    assert not operaciones.es_ideal(60.01, datos_limites())


def test_values_per_sector_devuelve_las_mediciones_del_sector():
    assert operaciones.getValuesPerSector(datos_mediciones(), "S02") == {"2026-10-12": 79.0, "2026-10-13": 20.0}


def test_values_per_sector_devuelve_una_copia():
    mediciones = {"S01": {"2026-10-12": 45.5}}
    valores = operaciones.getValuesPerSector(mediciones, "S01")
    valores["2026-10-13"] = 99.0
    assert mediciones == {"S01": {"2026-10-12": 45.5}}


def test_values_per_sector_inexistente_lanza_excepcion():
    with pytest.raises(ValueError):
        operaciones.getValuesPerSector(datos_mediciones(), "S09")


def test_order_humidity_de_mayor_a_menor():
    resultado = operaciones.orderHumidityValues(datos_mediciones()["S01"])
    assert resultado == [("2026-10-14", 85.0), ("2026-10-12", 45.5), ("2026-10-10", 15.0)]


def test_order_humidity_de_menor_a_mayor():
    resultado = operaciones.orderHumidityValues(datos_mediciones()["S01"], descendente=False)
    assert resultado == [("2026-10-10", 15.0), ("2026-10-12", 45.5), ("2026-10-14", 85.0)]


def test_order_humidity_sector_vacio():
    assert operaciones.orderHumidityValues({}) == []


def test_critical_values_devuelve_codigos_de_sector():
    promedios = {"S01": 15.0, "S02": 50.0, "S03": 85.0, "S04": None, "S05": 20.0}
    assert operaciones.getCriticalValues(promedios, datos_limites()) == ["S01", "S03"]


def test_ideal_values_devuelve_codigos_de_sector():
    promedios = {"S01": 40.0, "S02": 61.0, "S03": 60.0, "S04": None, "S05": 39.0}
    assert operaciones.getIdealValues(promedios, datos_limites()) == ["S01", "S03"]


def test_critical_e_ideal_sin_sectores():
    assert operaciones.getCriticalValues({}, datos_limites()) == []
    assert operaciones.getIdealValues({}, datos_limites()) == []


def test_mediciones_criticas_solo_incluye_las_del_sector_correspondiente():
    alertas = operaciones.obtener_mediciones_criticas(datos_mediciones(), datos_limites())
    assert alertas == {
        "S01": {"2026-10-10": 15.0, "2026-10-14": 85.0},
        "S02": {},
        "S03": {},
    }


def test_filtrar_por_sector():
    resultado = operaciones.filtrar_registros(datos_mediciones(), codigo_sector="S02")
    assert resultado == {"S02": {"2026-10-12": 79.0, "2026-10-13": 20.0}}


def test_filtrar_por_una_fecha():
    resultado = operaciones.filtrar_registros(datos_mediciones(), desde="2026-10-12", hasta="2026-10-12")
    assert resultado == {"S01": {"2026-10-12": 45.5}, "S02": {"2026-10-12": 79.0}, "S03": {}}


def test_filtrar_por_rango_incluye_los_bordes():
    resultado = operaciones.filtrar_registros(datos_mediciones(), codigo_sector="S01",
                                              desde="2026-10-10", hasta="2026-10-12")
    assert resultado == {"S01": {"2026-10-10": 15.0, "2026-10-12": 45.5}}


def test_filtrar_devuelve_fechas_ordenadas():
    resultado = operaciones.filtrar_registros(datos_mediciones(), codigo_sector="S01")
    assert list(resultado["S01"]) == ["2026-10-10", "2026-10-12", "2026-10-14"]


def test_filtrar_sin_criterios_devuelve_todo():
    assert operaciones.filtrar_registros(datos_mediciones()) == datos_mediciones()


def test_filtrar_no_modifica_el_original():
    mediciones = {"S01": {"2026-10-12": 45.5, "2026-10-13": 50.0}}
    operaciones.filtrar_registros(mediciones, desde="2026-10-13")
    assert mediciones == {"S01": {"2026-10-12": 45.5, "2026-10-13": 50.0}}


def test_filtrar_rango_invertido_lanza_excepcion():
    with pytest.raises(ValueError, match="Rango inválido"):
        operaciones.filtrar_registros(datos_mediciones(), desde="2026-10-14", hasta="2026-10-10")


def test_filtrar_sector_inexistente_lanza_excepcion():
    with pytest.raises(ValueError):
        operaciones.filtrar_registros(datos_mediciones(), codigo_sector="S09")

        
# ==========================================================
# PRUEBAS DE INDICADORES ADAPTADOS A DICCIONARIOS (H5)
# ==========================================================

def test_humedad_maxima_global():
    mediciones = {
        "S01": {"2026-10-12": 40, "2026-10-13": 60},
        "S02": {"2026-10-12": 80},
        "S03": {}
    }

    assert operaciones.getMaxHumidityValue(mediciones) == 80


def test_humedad_minima_global():
    mediciones = {
        "S01": {"2026-10-12": 40, "2026-10-13": 60},
        "S02": {"2026-10-12": 80},
        "S03": {}
    }

    assert operaciones.getMinHumidityValue(mediciones) == 40


def test_humedad_maxima_sin_mediciones():
    mediciones = {"S01": {}, "S02": {}}

    assert operaciones.getMaxHumidityValue(mediciones) is None


def test_humedad_minima_sin_mediciones():
    mediciones = {"S01": {}, "S02": {}}

    assert operaciones.getMinHumidityValue(mediciones) is None


def test_promedio_por_sector():
    mediciones = {
        "S01": {"2026-10-12": 40, "2026-10-13": 60},
        "S02": {"2026-10-12": 80},
        "S03": {}
    }

    assert operaciones.getAverageHumidityPerSector(mediciones) == {
        "S01": 50.0,
        "S02": 80.0,
        "S03": None
    }


def test_promedio_global():
    mediciones = {
        "S01": {"2026-10-12": 40, "2026-10-13": 60},
        "S02": {"2026-10-12": 80},
        "S03": {}
    }

    assert operaciones.getAverageHumidityTotal(mediciones) == 60.0


def test_promedio_global_sin_mediciones():
    mediciones = {"S01": {}, "S02": {}}

    assert operaciones.getAverageHumidityTotal(mediciones) is None


def test_agrupar_por_fecha_calcula_promedio():
    mediciones = {
        "S01": {
            "2026-10-12": 40,
            "2026-10-13": 60
        },
        "S02": {
            "2026-10-12": 80
        },
        "S03": {}
    }

    assert operaciones.agrupar_por_fecha(mediciones) == {
        "2026-10-12": 60.0,
        "2026-10-13": 60.0
    }


def test_agrupar_por_fecha_sin_mediciones():
    mediciones = {"S01": {}, "S02": {}}

    assert operaciones.agrupar_por_fecha(mediciones) == {}
