from datos import NOMBRE_SECTORES
from datos import DIAS_SEMANA
from datos import mostrar_matriz


def validar_sector(sector):
   if (sector.isnumeric() and int(sector) in range(len(NOMBRE_SECTORES))):
       return True
   else:
       return False

def validar_dia(dia):
   if (dia.isnumeric() and int(dia) in range(len(DIAS_SEMANA))):
       return True
   else:
       return False

def validar_humedad(humedad):
   if (humedad.isnumeric() and int(humedad) in range(-1, 101)):
       return True
   else:
       return False

def registrar_medicion(valores_actuales):

    try:
        id_sector = input("Ingrese el numero de sector: ")
        while not validar_sector(id_sector):
            print("Sector inválido")
            id_sector = input("Ingrese el numero de sector: ")

        id_dia = input("Ingrese el numero de dia, siendo 0 = Lunes, 6 = Domingo: ")
        while not validar_dia(id_dia):
            print("Día inválido")
            id_dia = input("Ingrese el numero de dia, siendo 0 = Lunes, 6 = Domingo: ")

        humedad = input("Ingrese la humedad: ")
        while not validar_humedad(humedad):
            print("Humedad inválida")
            humedad = input("Ingrese la humedad: ")

        if valores_actuales[int(id_sector)][int(id_dia)] != -1:
            print("Error: Ese valor ya fue registrado")
        else:
            valores_actuales[int(id_sector)][int(id_dia)] = int(humedad)

        return valores_actuales

    except:
        print("Error: ocurrió un problema al registrar la medición")
        return valores_actuales


# Indicacores -------------------------------------------------------------------------------------
def getMaxHumidityValue(sectores: list) -> float:
    valores_validos = [val for fila in sectores for val in fila if val >= 0]
    return float(max(valores_validos)) if valores_validos else -1.0


def getMinHumidityValue(sectores: list) -> float:
    valores_validos = [val for fila in sectores for val in fila if val >= 0]
    return float(min(valores_validos)) if valores_validos else -1.0


def getAverageHumidityPerSector(sectores: list) -> list:
    promedios = []
    for fila in sectores:
        validos = [val for val in fila if val >= 0]
        if validos:
            promedios.append(sum(validos) / len(validos))
        else:
            promedios.append(-1.0)
    return promedios


def getAverageHumidityTotal(sectores: list) -> float:
    valores_validos = [val for fila in sectores for val in fila if val >= 0]
    if not valores_validos:
        return -1.0
    return sum(valores_validos) / len(valores_validos)

#----------------------------------------------------------------------------------------------------------
def pedir_sector_valido():
    sec_input = input("Ingrese el número de sector (1-5): ")
    
    while not validar_sector(sec_input):
        print("Error: Sector inválido. Ingrese un número del 1 al 5.")
        sec_input = input("Ingrese el número de sector (1-5): ")
        
    return int(sec_input)

def getValuesPerSector(valores_actuales, sector_id):
    posicion_sector = sector_id - 1
    return valores_actuales[posicion_sector]

def orderHumidityValues(sector_id):
    mediciones_validas = [v for v in sector_id if v != -1]
    return sorted(mediciones_validas, key=lambda x: x, reverse=True)

def mostrar_detalle_sector(sectores: list, id_sector: int):
    valores_sector = getValuesPerSector(sectores, id_sector)
    nombre_sector = NOMBRE_SECTORES[id_sector - 1]

    print(f"\n--- Mediciones del Sector {id_sector} ({nombre_sector}) ---")
    
    for idx, humedad in enumerate(valores_sector):
        dia_nombre = DIAS_SEMANA[idx]
        if humedad == -1:
            print(f"{dia_nombre}: Sin registro")
        else:
            print(f"{dia_nombre}: {humedad}% de humedad")

    valores_ordenados = orderHumidityValues(valores_sector)
    print(f"\nValores ordenados (mayor a menor): {valores_ordenados}\n")

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


def mostrar_sectores_ideales(sectores: list):
    print("\n--- Identificación de Zona Ideal ---")
    ideal_target, tolerancia = pedir_rango_ideal()
    ideales, total, prom_general = getIdealValues(sectores, ideal_target, tolerancia)
    
    rango_min = ideal_target - tolerancia
    rango_max = ideal_target + tolerancia

    print(f"\nSectores en Zona Ideal ({rango_min}% - {rango_max}%):")
    if total > 0:
        for nombre, prom in ideales:
            barra = generar_barra_ascii(prom)
            print(f" • {nombre:<12}: {prom:.1f}% [{barra}]")
    else:
        print(" No hay sectores con promedio dentro del rango ideal.")
    
    print(f"\nCantidad total de sectores ideales: {total}")
    print(f"Promedio general de sectores ideales: {prom_general:.1f}%\n")

def getIdealValues(sectores: list, humedad_ideal: int = 50, tolerancia: int = 10) -> tuple:
    limite_inferior = humedad_ideal - tolerancia
    limite_superior = humedad_ideal + tolerancia
    
    sectores_ideales = []
    suma_promedios_ideales = 0
    
    for idx, fila in enumerate(sectores):
        mediciones_validas = [val for val in fila if val != -1]
        
        if len(mediciones_validas) > 0:
            promedio_sector = sum(mediciones_validas) / len(mediciones_validas)
            
            if limite_inferior <= promedio_sector <= limite_superior:
                nombre = NOMBRE_SECTORES[idx]
                sectores_ideales.append((nombre, promedio_sector))
                suma_promedios_ideales += promedio_sector

    cantidad_total = len(sectores_ideales)
    promedio_general_ideal = (suma_promedios_ideales / cantidad_total) if cantidad_total > 0 else 0.0

    return (sectores_ideales, cantidad_total, promedio_general_ideal)

# H5 ------------------------------------------------------------------------------------------------------
def getCriticalValues(sectores, limite_bajo=20, limite_alto=80) -> list:
    """
    Obtiene lista de sectores con humedad crítica (<20% o >80%).
    """
    # TODO: Jesica - Desarrollar la lógica definitiva usando comprensión de listas
    # Retorna índices ficticios de ejemplo (ejemplo: Sector B que es índice 1)
    return [1]


def getIdealValues(sectores, ideal_bajo=40, ideal_alto=60) -> list:
    """
    Obtiene lista de sectores con humedad ideal (entre 40% y 60%).
    """
    # TODO: Jesica - Desarrollar la lógica definitiva usando comprensión de listas
    # Retorna índices ficticios de ejemplo (ejemplo: Sector A que es índice 0 y Sector D que es índice 3)
    return [0, 3]


# HISTORIA H6: REPORTE FINAL-------------------------------------------------------------------------------------
def generar_reporte_final(sectores: list, nombres_sectores: tuple, dias_semana: tuple) -> str:
    """
    Genera el reporte ejecutivo semanal consolidado en formato string.
    """
    promedio_global = getAverageHumidityTotal(sectores)
    promedios_por_sector = getAverageHumidityPerSector(sectores)
    max_global = getMaxHumidityValue(sectores)
    min_global = getMinHumidityValue(sectores)
    
    # Consumo de las funciones de Jesica (H5)
    indices_criticos = getCriticalValues(sectores)
    indices_ideales = getIdealValues(sectores)

    reporte = [
        "=== REPORTE SEMANAL DE HUMEDAD EN CULTIVOS ===",
        "",
        "INDICADORES GENERALES:",
        f"- Promedio del campo: {promedio_global:.1f}%" if promedio_global >= 0 else "- Promedio del campo: N/A",
        f"- Máximo: {max_global:.1f}%" if max_global >= 0 else "- Máximo: N/A",
        f"- Mínimo: {min_global:.1f}%" if min_global >= 0 else "- Mínimo: N/A",
        "",
        "PROMEDIO POR SECTOR:"
    ]

    for nombre, prom in zip(nombres_sectores, promedios_por_sector):
        if prom < 0:
            reporte.append(f"- {nombre}: N/A (sin mediciones)")
        else:
            reporte.append(f"- {nombre}: {prom:.1f}%")

    reporte.append("\nSECTORES CRÍTICOS (< 20% o > 80%):")
    if indices_criticos:
        for i in indices_criticos:
            prom = promedios_por_sector[i]
            prom_str = f" ({prom:.1f}%)" if prom >= 0 else " (N/A)"
            reporte.append(f"- {nombres_sectores[i]}{prom_str}")
    else:
        reporte.append("- Ninguno")

    reporte.append("\nSECTORES IDEALES (40-60%):")
    if indices_ideales:
        for i in indices_ideales:
            prom = promedios_por_sector[i]
            prom_str = f" ({prom:.1f}%)" if prom >= 0 else " (N/A)"
            reporte.append(f"- {nombres_sectores[i]}{prom_str}")
    else:
        reporte.append("- Ninguno")

    return "\n".join(reporte)

#------------------------------------------------------------------------------------------------------------------------------
def menu(valores_actuales):
    while True:
        opcion = input("¿Qué desea hacer? (" \
                                "1 = Ver matriz de humedad / " \
                                "2 = Registrar medición / " \
                                "3 = Obtener valores de un sector / " \
                                "4 = Ver sectores ideales / " \
                                "6 = Generar Reporte Final / " \
                                "fin = Salir): " \
                                ).strip().lower()

        match opcion:
            case "fin":
                break
            case "1":
                mostrar_matriz(valores_actuales)
            case "2":
                registrar_medicion(valores_actuales)
            case "3":
                sector_id = pedir_sector_valido()
                mostrar_detalle_sector(valores_actuales, sector_id)
            case "4":
                mostrar_sectores_ideales(valores_actuales)
            case "6":
                reporte_texto = generar_reporte_final(valores_actuales, NOMBRE_SECTORES, DIAS_SEMANA)
                print("\n" + reporte_texto)
                input("\n¿Desea volver al menú? (Presione Enter): ")
            case _:
                print("Opción inválida")