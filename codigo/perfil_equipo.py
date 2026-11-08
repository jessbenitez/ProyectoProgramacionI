
def normalizarNombres(nombres):
    return [nombre.title() for nombre in nombres]

def uppercaseTitle(nombre_equipo):
    return nombre_equipo.upper()

def cantidadCaracteres(nombre_equipo):
    return len(nombre_equipo)

def generarSigla(nombre_equipo):
    palabras = nombre_equipo.split()
    sigla = ''.join(palabra[0].upper() for palabra in palabras)
    return sigla

def contiene_digitos(texto):
    for caracter in texto:
        if caracter.isdigit():
            return True
    return False
