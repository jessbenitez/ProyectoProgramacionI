# Pruebas de autenticacion.py
import json

import pytest

import autenticacion

USUARIOS = {"nicole": "alumna123", "jesica": "alumna456"}


def escribir(ruta, contenido):
    ruta.write_text(contenido, encoding="utf-8")
    return str(ruta)


def simular(respuestas):
    """Devuelve una función que entrega las credenciales de a una, como si las tipeara el usuario."""
    pendientes = list(respuestas)
    return lambda: pendientes.pop(0)


# --- cargar_usuarios ---
def test_cargar_usuarios_validos(tmp_path):
    ruta = escribir(tmp_path / "u.json", json.dumps({"usuarios": USUARIOS}))
    assert autenticacion.cargar_usuarios(ruta) == USUARIOS


def test_cargar_usuarios_archivo_inexistente(tmp_path):
    with pytest.raises(FileNotFoundError):
        autenticacion.cargar_usuarios(str(tmp_path / "no_existe.json"))


def test_cargar_usuarios_json_mal_formado(tmp_path):
    with pytest.raises(json.JSONDecodeError):
        autenticacion.cargar_usuarios(escribir(tmp_path / "u.json", "{ no es json"))


def test_cargar_usuarios_sin_clave_usuarios(tmp_path):
    with pytest.raises(KeyError):
        autenticacion.cargar_usuarios(escribir(tmp_path / "u.json", "{}"))


@pytest.mark.parametrize("contenido", [{"usuarios": {}}, {"usuarios": {"nicole": 123}}, {"usuarios": {"nicole": ""}}, {"usuarios": []}])
def test_cargar_usuarios_contenido_invalido(tmp_path, contenido):
    with pytest.raises(ValueError):
        autenticacion.cargar_usuarios(escribir(tmp_path / "u.json", json.dumps(contenido)))


# --- validar_credenciales ---
def test_credenciales_correctas():
    assert autenticacion.validar_credenciales(USUARIOS, "nicole", "alumna123") is True


def test_contrasena_incorrecta():
    assert autenticacion.validar_credenciales(USUARIOS, "nicole", "otra") is False


def test_contrasena_distingue_mayusculas():
    assert autenticacion.validar_credenciales(USUARIOS, "nicole", "ALUMNA123") is False


def test_usuario_inexistente_con_formato_valido():
    assert autenticacion.validar_credenciales(USUARIOS, "fulano", "alumna123") is False


def test_usuario_con_formato_invalido_lanza_excepcion():
    with pytest.raises(ValueError, match="Usuario inválido"):
        autenticacion.validar_credenciales(USUARIOS, "Nicole!", "alumna123")


# --- autenticar (límite de intentos) ---
def test_autenticar_a_la_primera():
    mensajes = []
    usuario = autenticacion.autenticar(USUARIOS, simular([("nicole", "alumna123")]), mensajes.append)
    assert usuario == "nicole"
    assert mensajes == []


def test_autenticar_acierta_en_el_ultimo_intento():
    mensajes = []
    respuestas = [("nicole", "mal"), ("fulano", "x"), ("jesica", "alumna456")]
    assert autenticacion.autenticar(USUARIOS, simular(respuestas), mensajes.append) == "jesica"
    assert len(mensajes) == 2
    assert "intento 1 de 3" in mensajes[0]


def test_autenticar_agota_los_tres_intentos():
    mensajes = []
    respuestas = [("nicole", "a"), ("nicole", "b"), ("nicole", "c"), ("nicole", "alumna123")]
    with pytest.raises(autenticacion.AccesoDenegado):
        autenticacion.autenticar(USUARIOS, simular(respuestas), mensajes.append)
    assert len(mensajes) == 3


def test_autenticar_no_pide_credenciales_de_mas():
    pedidas = []

    def pedir():
        pedidas.append(1)
        return ("nicole", "mal")

    with pytest.raises(autenticacion.AccesoDenegado):
        autenticacion.autenticar(USUARIOS, pedir, lambda mensaje: None, max_intentos=2)
    assert len(pedidas) == 2


def test_autenticar_formato_invalido_cuenta_como_intento_y_explica_el_formato():
    mensajes = []
    respuestas = [("NICOLE", "x"), ("nicole", "alumna123")]
    assert autenticacion.autenticar(USUARIOS, simular(respuestas), mensajes.append) == "nicole"
    assert "Usuario inválido" in mensajes[0]


def test_mensaje_no_revela_si_el_usuario_existe():
    mensajes = []
    with pytest.raises(autenticacion.AccesoDenegado):
        autenticacion.autenticar(USUARIOS, simular([("nicole", "x"), ("fulano", "x")]), mensajes.append, max_intentos=2)
    assert mensajes[0].split(" (")[0] == mensajes[1].split(" (")[0]
