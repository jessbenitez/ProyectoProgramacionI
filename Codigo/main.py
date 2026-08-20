import perfil_equipo


def main():
    equipo = {
        "nombres": ["Nicole Quilmore", "Jesica Benitez", "Priscila Challa"]
    }

    nombres_normalizados = perfil_equipo.normalizarNombres(equipo["nombres"])

    for nombre in nombres_normalizados:
        print(f"Integrante: {nombre}")

    nombre_equipo = "Error 404"
    nombre_equipo_mayusculas = perfil_equipo.uppercaseTitle(nombre_equipo)
    print(f"Nombre del equipo en mayúsculas: {nombre_equipo_mayusculas}")

    cantidad_caracteres = perfil_equipo.cantidadCaracteres(nombre_equipo)
    print(f"Cantidad de caracteres del nombre del equipo: {cantidad_caracteres}")

    sigla = perfil_equipo.generarSigla(nombre_equipo)
    print(f"Sigla del equipo: {sigla}")

    tiene_digitos = perfil_equipo.contiene_digitos(nombre_equipo)
    print(f"El nombre del equipo contiene dígitos: {tiene_digitos}")

if __name__ == "__main__":
    main()
