import json

import validaciones

def cargar_usuarios(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    try:
        usuarios = datos["usuarios"]
        contrasenas = list(usuarios.values())
    except KeyError:
        raise KeyError("usuarios.json: falta la clave 'usuarios'") from None
    except (TypeError, AttributeError):
        raise ValueError("usuarios.json: estructura inválida, se esperaba {\"usuarios\": {usuario: contraseña}}") from None

    if not usuarios or not all(contrasenas):
        raise ValueError("usuarios.json: debe haber al menos un usuario y ninguna contraseña puede estar vacía")
    return usuarios

def validar_credenciales(usuarios, usuario, contrasena):
    validaciones.validar_usuario(usuario)
    return usuarios.get(usuario) == contrasena

def autenticar(usuarios, pedir_credenciales, informar, max_intentos=3):
    for intento in range(1, max_intentos + 1):
        usuario, contrasena = pedir_credenciales()
        try:
            if validar_credenciales(usuarios, usuario, contrasena):
                return usuario
            motivo = "Usuario o contraseña incorrectos"
        except ValueError as error:
            motivo = str(error)
        informar(f"{motivo} (intento {intento} de {max_intentos})")
    raise ValueError(f"Se agotaron los {max_intentos} intentos de login")
