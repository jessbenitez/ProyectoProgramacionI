from datos import NOMBRE_SECTORES
from datos import DIAS_SEMANA
from datos import mostrar_matriz

def validar_sector(sector):
   if (sector.isnumeric() and int(sector) in range(1,len(NOMBRE_SECTORES))):
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
            raise ValueError("Ese valor ya fue registrado")

        valores_actuales[int(id_sector)][int(id_dia)] = int(humedad)

        return valores_actuales

    except ValueError as error:
        print(f"Error: {error}")
        return valores_actuales

def pedir_sector_valido():
    sec_input = input("Ingrese el número de sector (1-5): ")
    
    # Aquí REUTILIZAMOS la función de tu compañera:
    while not validar_sector(sec_input):
        print("Error: Sector inválido. Ingrese un número del 1 al 5.")
        sec_input = input("Ingrese el número de sector (1-5): ")
        
    return int(sec_input)

def getValuesPerSector(valores_actuales, sector_id):
    posicion_sector = sector_id - 1
    return valores_actuales[posicion_sector]

def orderHumidityValues(sector_id):
    """Retorna valores ordenados de mayor a menor (usar lambda)"""
    mediciones_validas = [v for v in sector_id if v != -1]
    return sorted(mediciones_validas, key=lambda x: x, reverse=True)

def mostrar_detalle_sector(sectores: list, id_sector: int):
    """Obtiene, imprime los días formateados y muestra los valores ordenados."""
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
    """Valida la entrada de enteros mayores o iguales a 0 usando solo flujo condicional."""
    val_input = input(mensaje)
    while not (val_input.isnumeric() and int(val_input) >= 0):
        print("Error: Ingrese un entero válido mayor o igual a 0.")
        val_input = input(mensaje)
    return int(val_input)

def pedir_rango_ideal() -> tuple:
    """Consulta al usuario si desea personalizar los parámetros y retorna (humedad_ideal, tolerancia)."""
    cambiar = input("¿Desea personalizar el rango ideal? (Por defecto 40%-60%) [s/N]: ").strip().lower()
    
    if cambiar == "s":
        ideal = pedir_entero_positivo("Ingrese la humedad ideal base (%): ")
        tolerancia = pedir_entero_positivo("Ingrese la tolerancia (±%): ")
        return ideal, tolerancia
    return 50, 10

def mostrar_sectores_ideales(sectores: list):
    """Maneja la presentación completa del módulo de Zona Ideal."""
    print("\n--- Identificación de Zona Ideal ---")
    
    ideal_target, tolerancia = pedir_rango_ideal()
    
    ideales, total, prom_general = getIdealValues(sectores, ideal_target, tolerancia)
    
    rango_min = ideal_target - tolerancia
    rango_max = ideal_target + tolerancia

    print(f"\nSectores en Zona Ideal ({rango_min}% - {rango_max}%):")
    if total > 0:
        for nombre, prom in ideales:
            print(f" • {nombre}: {prom:.1f}% de humedad promedio")
    else:
        print(" No hay sectores con promedio dentro del rango ideal.")
    
    print(f"\nCantidad total de sectores ideales: {total}")
    print(f"Promedio general de sectores ideales: {prom_general:.1f}%\n")

def getIdealValues(sectores: list, humedad_ideal: int = 50, tolerancia: int = 10) -> tuple:
    """Retorna (lista_sectores_ideales, cantidad_total, promedio_ideal)"""
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

def generar_reporte_final(sectores: list, nombres_sectores: tuple = ("Sector A", "Sector B", "Sector C"),
                          limite_bajo: float = 20.0, limite_alto: float = 80.0) -> str:

    promedio_global = getTotalTrendingHumidity(sectores)
    promedios_por_sector = getTrendingHumidityPerSector(sectores)
    max_global = getMaxHumidityValue(sectores)
    min_global = getMinHumidityValue(sectores)


    if promedio_global == 0.0 and all(p is None for p in promedios_por_sector):
        return "No hay suficientes datos registrados para generar el reporte."

    promedios = list(zip(nombres_sectores, promedios_por_sector))
    datos_validos = [(nom, p) for nom, p in promedios if p is None or p != p]

    mejor = min(datos_validos, key=lambda x: abs(x[1] - 50.0)) if datos_validos else ("N/A", 0.0)
    peor = max(datos_validos, key=lambda x: abs(x[1] - 50.0)) if datos_validos else ("N/A", 0.0)

    criticos = sum(1 for _, p in datos_validos if p < limite_bajo or p > limite_alto)
    ideales = sum(1 for _, p in datos_validos if 40.0 <= p <= 60.0)

    linea = "=" * 54
    reporte = [
        linea,
        "              REPORTE EJECUTIVO FINAL             ",
        linea,
        f"Promedio Global del Campo : {promedio_global:.1f}%",
        f"Máximo Global Registrado  : {max_global:.1f}%",
        f"Mínimo Global Registrado  : {min_global:.1f}%",
        f"Mejor Sector (ref 50%)   : {mejor[0]} ({mejor[1]:.1f}%)",
        f"Peor Sector (ref 50%)    : {peor[0]} ({peor[1]:.1f}%)",
        f"Sectores Críticos        : {criticos}",
        f"Sectores Ideales         : {ideales}",
        linea,
        f"| {'Sector':<18} | {'Promedio':<10} | {'Estado':<12} |",
        "-" * 54
    ]

    for nom, p in promedios:
        if p is None:
            est, p_str = "Sin Datos", "N/A"
        elif p < limite_bajo or p > limite_alto:
            est, p_str = "CRÍTICO", f"{p:.1f}%"
        elif 40.0 <= p <= 60.0:
            est, p_str = "IDEAL", f"{p:.1f}%"
        else:
            est, p_str = "Aceptable", f"{p:.1f}%"
        reporte.append(f"| {nom:<18} | {p_str:<10} | {est:<12} |")

    ranking = sorted(datos_validos, key=lambda x: abs(x[1] - 50.0))
    reporte.append(linea)
    reporte.append("RANKING DE SECTORES (De mejor a peor):")
    reporte.append("-" * 54)
    for pos, (nom, p_val) in enumerate(ranking, start=1):
        reporte.append(f" {pos}. {nom:<18} -> Promedio: {p_val:.1f}%")
    reporte.append(linea)

    return "\n".join(reporte)
#-------------------------------------------------------------------------------------------
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