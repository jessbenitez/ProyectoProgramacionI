import json
import os
from datetime import date

import archivos
import autenticacion
import operaciones
import perfil_equipo
import reportes
import validaciones


def pedir_dato(mensaje, validador):
    """Pide un dato por consola hasta que el validador lo acepte (sin lanzar ValueError)."""
    while True:
        valor = input(mensaje).strip()
        try:
            return validador(valor)
        except ValueError as error:
            print(f"Error: {error}")


def pedir_sector(config):
    print("Sectores: " + ", ".join(f"{codigo} ({nombre})" for codigo, nombre in config["sectores"].items()))
    return pedir_dato("Sector (ej: S01): ",
                      lambda valor: validaciones.validar_codigo_sector(valor, config["sectores"]))


def pedir_fecha(config, hoy):
    return pedir_dato("Fecha (AAAA-MM-DD): ",
                      lambda valor: validaciones.validar_fecha(valor, hoy, config["ventana_dias"])).isoformat()


def pedir_humedad(mensaje="Humedad (0-100): "):
    return pedir_dato(mensaje, validaciones.validar_humedad)


def pedir_credenciales():
    usuario = input("Usuario: ").strip()
    contrasena = input("Contraseña: ").strip()
    return usuario, contrasena


def registrar_nueva_medicion(mediciones, config, hoy):
    sector = pedir_sector(config)
    fecha = pedir_fecha(config, hoy)
    humedad = pedir_humedad()
    try:
        operaciones.registrar_medicion(mediciones, sector, fecha, humedad)
    except ValueError as error:
        print(f"Error: {error}")
        return
    print("Medición registrada correctamente (se guardará en el archivo al salir).")


def modificar_medicion_existente(mediciones, config, hoy):
    sector = pedir_sector(config)
    fecha = pedir_fecha(config, hoy)
    try:
        actual = operaciones.buscar_medicion(mediciones, sector, fecha)
    except ValueError as error:
        print(f"Error: {error}")
        return

    print(f"Medición actual: {config['sectores'][sector]}, {fecha} -> {actual}%")
    nueva = pedir_humedad("Nuevo valor de humedad (0-100): ")
    confirmacion = input(f"¿Reemplazar {actual}% por {nueva}%? (s/n): ").strip().lower()
    if confirmacion != "s":
        print("Modificación cancelada.")
        return

    operaciones.modificar_medicion(mediciones, sector, fecha, nueva)
    print("Medición modificada correctamente (se guardará en el archivo al salir).")


def pedir_filtro(config, hoy):
    """Pregunta por qué filtrar y devuelve un diccionario para filtrar_registros."""
    print("Filtrar por:")
    print("1. Sector")
    print("2. Fecha")
    print("3. Rango de fechas")
    print("4. Todo el historial")
    opcion = input("Ingrese opción: ").strip()

    if opcion == "1":
        return {"codigo_sector": pedir_sector(config)}
    if opcion == "2":
        fecha = pedir_fecha(config, hoy)
        return {"desde": fecha, "hasta": fecha}
    if opcion == "3":
        desde = pedir_fecha(config, hoy)
        hasta = pedir_fecha(config, hoy)
        return {"desde": desde, "hasta": hasta}
    if opcion == "4":
        return {}
    raise ValueError("Opción de filtro inválida: se esperaba 1, 2, 3 o 4")


def consultar_mediciones(mediciones, config, hoy):
    try:
        filtro = pedir_filtro(config, hoy)
        filtradas = operaciones.filtrar_registros(mediciones, **filtro)
    except ValueError as error:
        print(f"Error: {error}")
        return

    hay_datos = False
    for codigo, fechas in filtradas.items():
        for fecha, humedad in fechas.items():
            print(f"{fecha} | {codigo} ({config['sectores'][codigo]}) | {humedad}%")
            hay_datos = True
    if not hay_datos:
        print("No hay mediciones para el filtro indicado.")


def mostrar_indicadores(mediciones, config):
    maximo = operaciones.getMaxHumidityValue(mediciones)
    if maximo is None:
        print("No hay mediciones registradas.")
        return

    print(f"Humedad máxima: {maximo}%")
    print(f"Humedad mínima: {operaciones.getMinHumidityValue(mediciones)}%")
    print(f"Humedad promedio total: {operaciones.getAverageHumidityTotal(mediciones):.2f}%")

    print("\nPromedio por sector:")
    promedios = operaciones.getAverageHumidityPerSector(mediciones)
    for codigo, promedio in promedios.items():
        nombre = config["sectores"][codigo]
        if promedio is None:
            print(f"{codigo} ({nombre}): sin mediciones")
        else:
            print(f"{codigo} ({nombre}): {promedio:.2f}%")

    print("\nPromedio por fecha:")
    por_fecha = operaciones.agrupar_por_fecha(mediciones)
    for fecha in sorted(por_fecha):
        print(f"{fecha}: {por_fecha[fecha]:.2f}%")


def mostrar_sectores_criticos(mediciones, config):
    promedios = operaciones.getAverageHumidityPerSector(mediciones)
    criticos = operaciones.getCriticalValues(promedios, config["limites"])

    print("Sectores con promedio crítico:")
    if criticos:
        for codigo in criticos:
            print(f"{codigo} ({config['sectores'][codigo]}): {promedios[codigo]:.2f}%")
    else:
        print("Ninguno.")

    print()
    print(reportes.reporte_alertas(mediciones, config["sectores"], config["limites"]))


def mostrar_sectores_ideales(mediciones, config):
    promedios = operaciones.getAverageHumidityPerSector(mediciones)
    ideales = operaciones.getIdealValues(promedios, config["limites"])

    print("Sectores con promedio ideal:")
    if ideales:
        for codigo in ideales:
            print(f"{codigo} ({config['sectores'][codigo]}): {promedios[codigo]:.2f}%")
    else:
        print("Ninguno.")


def mostrar_reporte_filtrado(mediciones, config, hoy):
    try:
        filtro = pedir_filtro(config, hoy)
        print(reportes.reporte_filtrado(mediciones, config["sectores"], filtro))
    except ValueError as error:
        print(f"Error: {error}")


def guardar_texto_reporte(carpeta, nombre_archivo, texto):
    """Escribe un reporte; ante un error informa cuál falló y sigue. Devuelve True si se pudo escribir."""
    ruta = os.path.join(carpeta, nombre_archivo)
    try:
        archivos.guardar_reporte(ruta, texto)
    except OSError as error:
        print(f"Error al escribir {nombre_archivo}: {error}")
        return False
    print(f"Reporte generado: {ruta}")
    return True


def mostrar_reporte_general(mediciones, config, hoy, carpeta_reportes):
    texto = reportes.reporte_general(mediciones, config["sectores"], config["limites"], hoy)
    print(texto)
    guardar_texto_reporte(carpeta_reportes, "reporte_general.txt", texto)


def generar_reportes_en_archivos(mediciones, config, hoy, carpeta_reportes):
    for codigo in config["sectores"]:
        texto = reportes.reporte_sector(mediciones, config["sectores"], codigo, config["limites"],
                                        hoy, config["ventana_dias"])
        guardar_texto_reporte(carpeta_reportes, f"reporte_{codigo}.txt", texto)

    texto = reportes.reporte_general(mediciones, config["sectores"], config["limites"], hoy)
    guardar_texto_reporte(carpeta_reportes, "reporte_general.txt", texto)


def menu(mediciones, config, hoy, carpeta_reportes):
    opcion = ""
    while opcion != "fin":
        print("\n=== SISTEMA DE MONITOREO DE HUMEDAD EN CULTIVOS ===")
        print("1. Registrar nueva medición")
        print("2. Modificar medición existente")
        print("3. Consultar mediciones")
        print("4. Ver indicadores generales")
        print("5. Ver sectores críticos")
        print("6. Ver sectores ideales")
        print("7. Reporte filtrado")
        print("8. Reporte general")
        print("9. Generar reportes en archivos (uno por sector + general)")
        print("fin. Salir (guarda los cambios en el archivo de registros)")
        opcion = input("Ingrese opción: ").strip().lower()

        if opcion == "fin":
            pass
        elif opcion == "1":
            registrar_nueva_medicion(mediciones, config, hoy)
        elif opcion == "2":
            modificar_medicion_existente(mediciones, config, hoy)
        elif opcion == "3":
            consultar_mediciones(mediciones, config, hoy)
        elif opcion == "4":
            mostrar_indicadores(mediciones, config)
        elif opcion == "5":
            mostrar_sectores_criticos(mediciones, config)
        elif opcion == "6":
            mostrar_sectores_ideales(mediciones, config)
        elif opcion == "7":
            mostrar_reporte_filtrado(mediciones, config, hoy)
        elif opcion == "8":
            mostrar_reporte_general(mediciones, config, hoy, carpeta_reportes)
        elif opcion == "9":
            generar_reportes_en_archivos(mediciones, config, hoy, carpeta_reportes)
        else:
            print("Opción inválida")


def guardar_con_reintento(ruta, mediciones):
    """Sobrescribe el CSV con el diccionario en memoria; ante un error de E/S ofrece reintentar."""
    while True:
        try:
            archivos.guardar_registros(ruta, mediciones)
            print("Cambios guardados.")
            return
        except OSError as error:
            print(f"Error al guardar {ruta}: {error}")
            try:
                reintentar = input("¿Reintentar? (s/n): ").strip().lower() == "s"
            except EOFError:
                reintentar = False
            if not reintentar:
                print("Se sale sin guardar los cambios.")
                return


def cargar_historial(ruta, config, hoy):
    """Lee el CSV al diccionario en memoria. Si no existe arranca vacío. Devuelve None si el archivo es inutilizable."""
    try:
        mediciones, rechazadas = archivos.cargar_registros(ruta, config["sectores"], hoy, config["ventana_dias"])
    except FileNotFoundError:
        print("No se encontró el archivo de registros: se arranca sin historial y se creará al salir.")
        return {codigo: {} for codigo in config["sectores"]}
    except (ValueError, OSError) as error:
        # No se continúa: al salir se sobrescribiría el archivo y se perdería su contenido.
        print(f"Error al leer {ruta}: {error}")
        return None

    for motivo in rechazadas:
        print(f"Registro descartado - {motivo}")
    return mediciones


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
    carpeta = os.path.dirname(os.path.abspath(__file__))
    hoy = date.today()

    # La configuración y los usuarios son obligatorios: si faltan o son inválidos no se continúa.
    try:
        config = archivos.cargar_configuracion(os.path.join(carpeta, "datos", "configuracion.json"))
        usuarios = autenticacion.cargar_usuarios(os.path.join(carpeta, config["archivos"]["usuarios"]))
    except FileNotFoundError as error:
        print(f"Error: no se encontró el archivo {error.filename}")
        return
    except json.JSONDecodeError as error:
        print(f"Error: JSON mal formado ({error})")
        return
    except KeyError as error:
        print(f"Error de configuración: {error.args[0]}")
        return
    except (ValueError, OSError) as error:
        print(f"Error de configuración: {error}")
        return

    try:
        usuario = autenticacion.autenticar(usuarios, pedir_credenciales, print)
    except autenticacion.AccesoDenegado as error:
        print(error)
        return
    print(f"\nBienvenido/a, {usuario}.")

    ruta_registros = os.path.join(carpeta, config["archivos"]["registros"])
    carpeta_reportes = os.path.join(carpeta, config["archivos"]["carpeta_reportes"])
    mediciones = cargar_historial(ruta_registros, config, hoy)
    if mediciones is None:
        return

    # El guardado va en finally para que también ocurra ante Ctrl+C o un error inesperado.
    try:
        menu(mediciones, config, hoy, carpeta_reportes)
    finally:
        guardar_con_reintento(ruta_registros, mediciones)


if __name__ == "__main__":
    main()
