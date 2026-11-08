import json
import os
from datetime import date

import archivos
import autenticacion
import operaciones
import perfil_equipo
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


def menu(mediciones, config, hoy):
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
        elif opcion in ("3", "4", "5", "6", "7", "8", "9"):
            print("Opción todavía no disponible: falta adaptarla al nuevo modelo de datos.")
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
    mediciones = cargar_historial(ruta_registros, config, hoy)
    if mediciones is None:
        return

    # El guardado va en finally para que también ocurra ante Ctrl+C o un error inesperado.
    try:
        menu(mediciones, config, hoy)
    finally:
        guardar_con_reintento(ruta_registros, mediciones)


if __name__ == "__main__":
    main()
