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



def getValuesPerSector(sectores, id_sector):
    return sectores[id_sector -1]

"""def getValuesPerSector(valores_actuales, sector_id):
    posicion_sector = sector_id - 1
    return valores_actuales[posicion_sector]"""

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


def mostrar_sectores_criticos(sectores: list, nombres_sectores: tuple):
    promedios_por_sector = getAverageHumidityPerSector(sectores)
    indices_criticos = getCriticalValues(promedios_por_sector)
    print("\n--- Identificación de Sectores Críticos (< 20% o > 80%) ---")
    if indices_criticos:
        for i in range(len(indices_criticos)):
            prom = indices_criticos[i]
            prom_str = f" ({prom:.1f}%)" if prom >= 0 else " (N/A)"
            print(f"- {nombres_sectores[i]}: {prom_str}")
    else:
        print(" No hay sectores con promedio que alcancen rango crítico.")


def mostrar_sectores_ideales(sectores: list, nombres_sectores: tuple):
    print("\n--- Identificación de Zona Ideal ---")
    ideal_target, tolerancia = pedir_rango_ideal()
    
    rango_min = ideal_target - tolerancia
    rango_max = ideal_target + tolerancia

    promedios_por_sector = getAverageHumidityPerSector(sectores)
    indices_ideales = getIdealValues(promedios_por_sector, float(rango_min), float(rango_max))
    

    print(f"\nSectores en Zona Ideal ({rango_min}% - {rango_max}%):")
    if indices_ideales:
        for i in range(len(indices_ideales)):
            prom = indices_ideales[i]
            prom_str = f" ({prom:.1f}%)" if prom >= 0 else " (N/A)"
            print(f"- {nombres_sectores[i]}: {prom_str}")
    else:
        print("No hay sectores con promedio dentro del rango ideal.")

def getIdealValues(sectores, ideal_bajo = 40.0, ideal_alto = 60.0) -> list:
    """
    Obtiene lista de sectores con humedad ideal.

    Rango: entre ideal_bajo e ideal_alto (40-60%)
    Se calcula sobre el promedio del sector, excluyendo valores -1.
    Los sectores sin mediciones no se consideran.

    Retorna: Lista con índices de sectores ideales

    Nota: Usa comprensión de listas
    """
    
    lista_ideales = []

    for valor in sectores:
        if valor > ideal_bajo and valor < ideal_alto:
            if valor not in lista_ideales:
                lista_ideales.append(valor)
    return lista_ideales

# H5 ------------------------------------------------------------------------------------------------------
def getCriticalValues(sectores, limite_bajo=20.0, limite_alto=80.0) -> list:
    """
    Obtiene lista de sectores con humedad crítica (<20% o >80%).
    """
    # TODO: Jesica - Desarrollar la lógica definitiva usando comprensión de listas
    # Retorna índices ficticios de ejemplo (ejemplo: Sector B que es índice 1)
    """
    Qué hace: identifica qué sectores están en estado crítico.
    Qué recibe: la matriz, y dos límites que tienen valor por defecto (20 y 80) pero podrían cambiarse al llamarla.
    Qué devuelve: una lista de índices internos (0 a 4), no de IDs ni de nombres. Ejemplo: [0, 1, 4] significa sectores A, B y E. Si no hay críticos, lista vacía.
    """

    lista_criticos = []
    for valor in sectores:
        if valor < limite_bajo or valor > limite_alto:
            if valor not in lista_criticos:
                lista_criticos.append(valor)
    
    return lista_criticos

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
    indices_criticos = getCriticalValues(promedios_por_sector)
    indices_ideales = getIdealValues(promedios_por_sector)

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
        for i in range(len(indices_criticos)):
            prom = indices_criticos[i]
            prom_str = f" ({prom:.1f}%)" if prom >= 0 else " (N/A)"
            reporte.append(f"- {nombres_sectores[i]}: {prom_str}")
    else:
        reporte.append("- Ninguno")

    reporte.append("\nSECTORES IDEALES (40-60%):")
    if indices_ideales:
        for i in range(len(indices_ideales)):
            prom = indices_ideales[i]
            prom_str = f" ({prom:.1f}%)" if prom >= 0 else " (N/A)"
            reporte.append(f"- {nombres_sectores[i]}: {prom_str}")
    else:
        reporte.append("- Ninguno")

    return "\n".join(reporte)

#------------------------------------------------------------------------------------------------------------------------------
def menu(valores_actuales):
    while True:
        opcion = input("¿Qué desea hacer? (" \
                                "1 = Consultar valores por sector (Matriz) / " \
                                "2 = Ver indicadores generales / " \
                                "3 = Ver sectores críticos / " \
                                "4 = Ver sectores ideales / " \
                                "5 = Registrar nueva medición / " \
                                "6 = Generar Reporte Final / " \
                                "fin = Salir): " \
                                ).strip().lower()

        match opcion:
            case "fin":
                break
            case "1":
                mostrar_matriz(valores_actuales)
            case "2":
                print("\n=== INDICADORES GENERALES ===")
                print(f"Máximo global:    {getMaxHumidityValue(valores_actuales):.1f}%")
                print(f"Mínimo global:    {getMinHumidityValue(valores_actuales):.1f}%")
                print(f"Promedio campo:   {getAverageHumidityTotal(valores_actuales):.1f}%\n")
                
                print("PROMEDIO POR SECTOR:")
                for nom, prom in zip(NOMBRE_SECTORES, getAverageHumidityPerSector(valores_actuales)):
                    print(f"{nom}: {f'{prom:.1f}%' if prom >= 0 else 'N/A (sin mediciones)'}")
            case "3":
                sector_id = pedir_sector_valido()
                mostrar_detalle_sector(valores_actuales, sector_id)
                mostrar_sectores_criticos(valores_actuales, NOMBRE_SECTORES)
            case "4":
                mostrar_sectores_ideales(valores_actuales, NOMBRE_SECTORES)
            case "5":
                registrar_medicion(valores_actuales)
            case "6":
                reporte_texto = generar_reporte_final(valores_actuales, NOMBRE_SECTORES, DIAS_SEMANA)
                print("\n" + reporte_texto)
                input("\n¿Desea volver al menú? (Presione Enter): ")
            case _:
                print("Opción inválida")