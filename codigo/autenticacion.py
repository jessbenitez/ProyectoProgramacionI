"""Login de usuario y contraseña contra usuarios.json. Sin input ni print: la interacción la aporta main.py."""
import json

import validaciones


class AccesoDenegado(Exception):
    """Se agotaron los intentos de login permitidos."""


def cargar_usuarios(ruta):
    """Lee usuarios.json y devuelve el diccionario usuario -> contraseña.

    Lanza FileNotFoundError si no existe, json.JSONDecodeError si no es JSON válido,
    KeyError si falta la clave 'usuarios' y ValueError si su contenido no es válido.
    """
    with open(ruta, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    if not isinstance(datos, dict) or "usuarios" not in datos:
        raise KeyError("usuarios.json: falta la clave 'usuarios'")

    usuarios = datos["usuarios"]
    if not isinstance(usuarios, dict) or not usuarios:
        raise ValueError("usuarios.json: 'usuarios' debe ser un objeto no vacío")
    if not all(isinstance(contrasena, str) and contrasena for contrasena in usuarios.values()):
        raise ValueError("usuarios.json: todas las contraseñas deben ser texto no vacío")
    return usuarios


def validar_credenciales(usuarios, usuario, contrasena):
    """Devuelve True si el usuario existe y la contraseña coincide; lanza ValueError si el usuario tiene formato inválido."""
    validaciones.validar_usuario(usuario)
    return usuarios.get(usuario) == contrasena


def autenticar(usuarios, pedir_credenciales, informar, max_intentos=3):
    """Repite el login hasta acertar o agotar max_intentos. Devuelve el nombre del usuario autenticado.

    pedir_credenciales: función sin argumentos que devuelve (usuario, contrasena).
    informar: función que recibe el mensaje de error a mostrar.
    Lanza AccesoDenegado si se agotan los intentos.
    """
    for intento in range(1, max_intentos + 1):
        usuario, contrasena = pedir_credenciales()
        try:
            if validar_credenciales(usuarios, usuario, contrasena):
                return usuario
            motivo = "Usuario o contraseña incorrectos"
        except ValueError as error:
            motivo = str(error)
        informar(f"{motivo} (intento {intento} de {max_intentos})")
    raise AccesoDenegado(f"Se agotaron los {max_intentos} intentos de login")
