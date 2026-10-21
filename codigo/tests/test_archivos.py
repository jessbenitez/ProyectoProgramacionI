# Pruebas de archivos.py
import json
from datetime import date

import pytest

import archivos

HOY = date(2026, 10, 14)
SECTORES = {"S01": "Frutillas", "S02": "Frambuesas"}
ENCABEZADO = "fecha,sector,humedad\n"


def escribir(ruta, texto):
    ruta.write_text(texto, encoding="utf-8")
    return str(ruta)


def config_valida():
    return {
        "sectores": SECTORES,
        "limites": {"critico_bajo": 20, "ideal_bajo": 40, "ideal_alto": 60, "critico_alto": 80},
        "ventana_dias": 28,
        "archivos": {"registros": "r.csv", "usuarios": "u.json", "carpeta_reportes": "salida"},
    }


# --- configuración ---
def test_cargar_configuracion_valida(tmp_path):
    ruta = escribir(tmp_path / "c.json", json.dumps(config_valida()))
    assert archivos.cargar_configuracion(ruta)["ventana_dias"] == 28


def test_cargar_configuracion_inexistente(tmp_path):
    with pytest.raises(FileNotFoundError):
        archivos.cargar_configuracion(str(tmp_path / "no_existe.json"))


def test_cargar_configuracion_json_mal_formado(tmp_path):
    ruta = escribir(tmp_path / "c.json", "{ esto no es json")
    with pytest.raises(json.JSONDecodeError):
        archivos.cargar_configuracion(ruta)


def test_cargar_configuracion_clave_faltante(tmp_path):
    config = config_valida()
    del config["limites"]
    ruta = escribir(tmp_path / "c.json", json.dumps(config))
    with pytest.raises(KeyError):
        archivos.cargar_configuracion(ruta)


def test_cargar_configuracion_ventana_invalida(tmp_path):
    config = config_valida()
    config["ventana_dias"] = 0
    ruta = escribir(tmp_path / "c.json", json.dumps(config))
    with pytest.raises(ValueError):
        archivos.cargar_configuracion(ruta)


# --- cargar registros ---
def test_cargar_registros_validos(tmp_path):
    ruta = escribir(tmp_path / "r.csv", ENCABEZADO + "2026-10-12,S01,45.5\n2026-10-13,S02,80\n")
    mediciones, rechazadas = archivos.cargar_registros(ruta, SECTORES, HOY, 28)
    assert mediciones == {"S01": {"2026-10-12": 45.5}, "S02": {"2026-10-13": 80.0}}
    assert rechazadas == []


def test_cargar_registros_incluye_sectores_sin_datos(tmp_path):
    ruta = escribir(tmp_path / "r.csv", ENCABEZADO)
    mediciones, _ = archivos.cargar_registros(ruta, SECTORES, HOY, 28)
    assert mediciones == {"S01": {}, "S02": {}}


def test_cargar_registros_archivo_inexistente(tmp_path):
    with pytest.raises(FileNotFoundError):
        archivos.cargar_registros(str(tmp_path / "no_existe.csv"), SECTORES, HOY, 28)


def test_cargar_registros_encabezado_incorrecto(tmp_path):
    ruta = escribir(tmp_path / "r.csv", "dia,lugar,valor\n2026-10-12,S01,45\n")
    with pytest.raises(ValueError, match="Encabezado"):
        archivos.cargar_registros(ruta, SECTORES, HOY, 28)


def test_cargar_registros_archivo_vacio(tmp_path):
    ruta = escribir(tmp_path / "r.csv", "")
    with pytest.raises(ValueError):
        archivos.cargar_registros(ruta, SECTORES, HOY, 28)


def test_cargar_registros_filas_invalidas_no_pierden_las_validas(tmp_path):
    ruta = escribir(tmp_path / "r.csv", ENCABEZADO
                    + "2026-10-12,S01,45.5\n"      # válida
                    + "2026-10-13,S09,50\n"        # sector inexistente
                    + "2026-02-30,S01,50\n"        # fecha inexistente
                    + "2026-10-13,S01,150\n"       # humedad fuera de rango
                    + "2026-10-13,S01\n"           # faltan columnas
                    + "2026-10-13,S01,50,extra\n"  # sobran columnas
                    + "2026-10-14,S02,60\n")       # válida
    mediciones, rechazadas = archivos.cargar_registros(ruta, SECTORES, HOY, 28)
    assert mediciones == {"S01": {"2026-10-12": 45.5}, "S02": {"2026-10-14": 60.0}}
    assert len(rechazadas) == 5
    assert rechazadas[0].startswith("Línea 3:")


def test_cargar_registros_fuera_de_ventana_no_se_incorpora(tmp_path):
    ruta = escribir(tmp_path / "r.csv", ENCABEZADO + "2026-09-16,S01,40\n2026-09-17,S01,41\n")
    mediciones, rechazadas = archivos.cargar_registros(ruta, SECTORES, HOY, 28)
    assert mediciones["S01"] == {"2026-09-17": 41.0}
    assert len(rechazadas) == 1


def test_cargar_registros_duplicado_conserva_el_primero(tmp_path):
    ruta = escribir(tmp_path / "r.csv", ENCABEZADO + "2026-10-12,S01,40\n2026-10-12,S01,70\n")
    mediciones, rechazadas = archivos.cargar_registros(ruta, SECTORES, HOY, 28)
    assert mediciones["S01"] == {"2026-10-12": 40.0}
    assert len(rechazadas) == 1 and "duplicada" in rechazadas[0]


# --- guardar registros ---
def test_guardar_registros_ordena_por_fecha_y_sector(tmp_path):
    ruta = str(tmp_path / "r.csv")
    mediciones = {"S02": {"2026-10-12": 52.0, "2026-10-10": 30.0}, "S01": {"2026-10-12": 45.5}}
    archivos.guardar_registros(ruta, mediciones)
    esperado = ENCABEZADO + "2026-10-10,S02,30.0\n2026-10-12,S01,45.5\n2026-10-12,S02,52.0\n"
    assert (tmp_path / "r.csv").read_text(encoding="utf-8") == esperado


def test_guardar_registros_vacio_deja_solo_encabezado(tmp_path):
    ruta = str(tmp_path / "r.csv")
    archivos.guardar_registros(ruta, {"S01": {}, "S02": {}})
    assert (tmp_path / "r.csv").read_text(encoding="utf-8") == ENCABEZADO


def test_guardar_registros_sobrescribe_el_contenido_anterior(tmp_path):
    ruta = escribir(tmp_path / "r.csv", ENCABEZADO + "2026-10-01,S01,10\n")
    archivos.guardar_registros(ruta, {"S01": {"2026-10-12": 45.5}})
    assert "2026-10-01" not in (tmp_path / "r.csv").read_text(encoding="utf-8")


def test_guardar_y_cargar_devuelve_el_mismo_diccionario(tmp_path):
    ruta = str(tmp_path / "r.csv")
    original = {"S01": {"2026-10-12": 45.5, "2026-10-13": 0.0}, "S02": {"2026-10-14": 100.0}}
    archivos.guardar_registros(ruta, original)
    recuperado, rechazadas = archivos.cargar_registros(ruta, SECTORES, HOY, 28)
    assert recuperado == original
    assert rechazadas == []


# --- guardar reporte ---
def test_guardar_reporte_crea_la_carpeta(tmp_path):
    ruta = str(tmp_path / "salida" / "reportes" / "reporte_S01.txt")
    archivos.guardar_reporte(ruta, "Sector Frutillas: Sin mediciones en el período\n")
    assert "Sin mediciones" in (tmp_path / "salida" / "reportes" / "reporte_S01.txt").read_text(encoding="utf-8")
