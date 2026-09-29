from datos import cargar_datos_iniciales, formatear_matriz, NOMBRE_SECTORES, DIAS_SEMANA
import perfil_equipo
import operaciones


def pedir_sector_valido(nombres_sectores):
    sec_input = input("Ingrese el número de sector (1-5): ")

    while not operaciones.validar_sector(sec_input, nombres_sectores):
        print("Error: Sector inválido. Ingrese un número del 1 al 5.")
        sec_input = input("Ingrese el número de sector (1-5): ")

    return int(sec_input)


def pedir_entero_positivo(mensaje: str) -> int:
    val_input = input(mensaje)
    while not (val_input.isnumeric() and int(val_input) >= 0):
        print("Error: Ingrese un entero válido mayor o igual a 0.")
        val_input = input(mensaje)
    return int(val_input)


def pedir_rango_ideal() -> tuple:
    cambiar = input("¿Desea personalizar el rango ideal? (Por defecto 40%-60%) [s/N]: ").strip().lower()

    if cambiar == "s":
        ideal = pedir_entero_positivo("Ingrese la humedad ideal base (%): ")
        tolerancia = pedir_entero_positivo("Ingrese la tolerancia (±%): ")
        return ideal, tolerancia
    return 50, 10


def pedir_medicion(nombres_sectores, dias_semana):
    id_sector = input("Ingrese el numero de sector (1-5): ")
    while not operaciones.validar_sector(id_sector, nombres_sectores):
        print("Sector inválido")
        id_sector = input("Ingrese el numero de sector (1-5): ")

    id_dia = input("Ingrese el numero de dia, siendo 0 = Lunes, 6 = Domingo: ")
    while not operaciones.validar_dia(id_dia, dias_semana):
        print("Día inválido")
        id_dia = input("Ingrese el numero de dia, siendo 0 = Lunes, 6 = Domingo: ")

    humedad = input("Ingrese la humedad: ")
    while not operaciones.validar_humedad(humedad):
        print("Humedad inválida")
        humedad = input("Ingrese la humedad: ")

    return int(id_sector), int(id_dia), int(humedad)


def menu(valores_actuales, nombres_sectores, dias_semana):
    opcion = ""
    while opcion != "fin":
        opcion = input("¿Qué desea hacer? ("
                                "1 = Consultar valores por sector (Matriz) / "
                                "2 = Ver indicadores generales / "
                                "3 = Ver sectores críticos / "
                                "4 = Ver sectores ideales / "
                                "5 = Registrar nueva medición / "
                                "6 = Generar Reporte Final / "
                                "fin = Salir): "
                                ).strip().lower()

        match opcion:
            case "fin":
                pass
            case "1":
                print(formatear_matriz(valores_actuales))
            case "2":
                print("\n=== INDICADORES GENERALES ===")
                print(f"Máximo global:    {operaciones.getMaxHumidityValue(valores_actuales):.1f}%")
                print(f"Mínimo global:    {operaciones.getMinHumidityValue(valores_actuales):.1f}%")
                print(f"Promedio campo:   {operaciones.getAverageHumidityTotal(valores_actuales):.1f}%\n")

                print("PROMEDIO POR SECTOR:")
                for nom, prom in zip(nombres_sectores, operaciones.getAverageHumidityPerSector(valores_actuales)):
                    print(f"{nom}: {f'{prom:.1f}%' if prom >= 0 else 'N/A (sin mediciones)'}")
            case "3":
                sector_id = pedir_sector_valido(nombres_sectores)
                print(operaciones.formatear_detalle_sector(valores_actuales, sector_id, nombres_sectores, dias_semana))
                print(operaciones.formatear_sectores_criticos(valores_actuales, nombres_sectores))
            case "4":
                ideal_target, tolerancia = pedir_rango_ideal()
                print(operaciones.formatear_sectores_ideales(valores_actuales, nombres_sectores, ideal_target, tolerancia))
            case "5":
                id_sector, id_dia, humedad = pedir_medicion(nombres_sectores, dias_semana)
                valores_actuales, exito, mensaje = operaciones.registrar_medicion(valores_actuales, id_sector, id_dia, humedad)
                print(mensaje)
            case "6":
                reporte_texto = operaciones.generar_reporte_final(valores_actuales, nombres_sectores, dias_semana)
                print("\n" + reporte_texto)
                input("\n¿Desea volver al menú? (Presione Enter): ")
            case _:
                print("Opción inválida")


def main():
    equipo = ("Nicole Quilmore", "Jesica Benitez", "Priscila Challa")

    nombres_normalizados = perfil_equipo.normalizarNombres(equipo)

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

    #A partir de este punto comenzamos a implementar el programa
    valores_actuales = cargar_datos_iniciales()

    menu(valores_actuales, NOMBRE_SECTORES, DIAS_SEMANA)



if __name__ == "__main__":
    main()
