"""Login de usuario y contraseña contra usuarios.json."""


def cargar_usuarios(ruta):
    """Lee usuarios.json y devuelve el diccionario usuario -> contraseña."""
    raise NotImplementedError


def validar_credenciales(usuarios, usuario, contrasena):
    """Devuelve True si el usuario existe y la contraseña coincide; lanza ValueError si el usuario tiene formato inválido."""
    raise NotImplementedError
