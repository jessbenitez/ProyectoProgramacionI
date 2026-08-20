""" • Normalizar los nombres con title().
• Convertir el nombre del equipo a mayúsculas.
• Informar la cantidad de caracteres del nombre del equipo.
• Generar una sigla con la inicial de cada palabra.
• Verificar si el nombre del equipo contiene al menos un dígito recorriendo sus caracteres y utilizando isdigit().
• Mostrar toda la información mediante f-strings.
• Mantener las operaciones de procesamiento dentro de funciones y la entrada/salida general en el programa principal.
def contiene_digitos(texto):
 val= False
 for caracter in texto:
 if caracter.isdigit():
 val= True
 return val """

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