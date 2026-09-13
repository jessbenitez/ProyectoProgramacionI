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


# Reemplazar cuando estén listas las funciones definitivas

def getTotalTrendingHumidity(sectores: list) -> float:
    # Aca va a ir la logica de la funcion definitiva
    return 53.4

def getTrendingHumidityPerSector(sectores: list) -> list:
    # Aca va a ir la logica de la funcion definitiva
    # Devuelve un promedio ficticio para cada uno de los 5 sectores
    return [59.3, 61.3, 73.8, 35.5, 47.6]

def getMaxHumidityValue(sectores: list) -> float:
    # Aca va a ir la logica de la funcion definitiva
    return 99.0

def getMinHumidityValue(sectores: list) -> float:
    # Aca va a ir la logica de la funcion definitiva
    return 13.0


#
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

def generar_reporte_final(sectores: list, limite_bajo: float = 20.0, limite_alto: float = 80.0) -> str:
    """Consume las métricas del sistema y construye el informe ejecutivo formateado."""
    
    promedio_global = getTotalTrendingHumidity(sectores)
    promedios_por_sector = getTrendingHumidityPerSector(sectores)
    max_global = getMaxHumidityValue(sectores)
    min_global = getMinHumidityValue(sectores)

    promedios = list(zip(NOMBRE_SECTORES, promedios_por_sector))

    mejor = min(promedios, key=lambda x: abs(x[1] - 50.0))
    peor = max(promedios, key=lambda x: abs(x[1] - 50.0))


    criticos = sum(1 for _, p in promedios if p < limite_bajo or p > limite_alto)
    ideales = sum(1 for _, p in promedios if 40.0 <= p <= 60.0)


    linea = "=" * 72
    reporte = [
        linea,
        "                     REPORTE EJECUTIVO FINAL                      ",
        linea,
        f"Promedio Global del Campo : {promedio_global:.1f}%",
        f"Máximo Global Registrado  : {max_global:.1f}%",
        f"Mínimo Global Registrado  : {min_global:.1f}%",
        f"Mejor Sector (ref 50%)    : {mejor[0]} ({mejor[1]:.1f}%)",
        f"Peor Sector (ref 50%)     : {peor[0]} ({peor[1]:.1f}%)",
        f"Sectores Críticos         : {criticos}",
        f"Sectores Ideales          : {ideales}",
        linea,
        f"| {'Sector':<12} | {'Promedio':<8} | {'Estado':<10} | {'Gráfico (0-100%)':<14} |",
        "-" * 72
    ]


    for nom, p in promedios:
        barra = generar_barra_ascii(p)
        if p < limite_bajo or p > limite_alto:
            est = "CRÍTICO"
        elif 40.0 <= p <= 60.0:
            est = "IDEAL"
        else:
            est = "Aceptable"
            
        reporte.append(f"| {nom:<12} | {p:.1f}%   | {est:<10} | [{barra}] |")


    ranking = sorted(promedios, key=lambda x: abs(x[1] - 50.0))
    reporte.append(linea)
    reporte.append("RANKING DE SECTORES (De mejor a peor según humedad ideal 50%):")
    reporte.append("-" * 72)
    for pos, (nom, p_val) in enumerate(ranking, start=1):
        reporte.append(f" {pos}. {nom:<12} -> Promedio: {p_val:.1f}%")
    reporte.append(linea)

    return "\n".join(reporte)

#--------------------------------------------codigo ascii------------------------------------------------
def generar_barra_ascii(porcentaje, escala: int = 10, caracter_lleno: str = "█", caracter_vacio: str = "░") -> str:
    if porcentaje is None or porcentaje != porcentaje:
        return "N/A"
    
    try:
        val = float(porcentaje)
        val_clamped = max(0.0, min(100.0, val))
        
        # Con escala 10, el máximo de bloques es 10 (100 // 10 = 10)
        bloques_llenos = int(val_clamped // escala)
        bloques_vacios = 10 - bloques_llenos
        
        return (caracter_lleno * bloques_llenos) + (caracter_vacio * bloques_vacios)
    except (ValueError, TypeError):
        return "N/A"



#------------------------------------------------------------------------------------------------------------------------------
def menu(valores_actuales):
    while True:
        opcion = input("¿Qué desea hacer? (" \
                                "1 = Ver matriz de humedad / " \
                                "2 = Registrar medición / " \
                                "3 = Obtener valores de un sector / " \
                                "4 = Ver sectores ideales / " \
                                "5 = Generar Reporte Final / " \
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
            case "5":
                print(generar_reporte_final(valores_actuales))
            case _:
                print("Opción inválida")