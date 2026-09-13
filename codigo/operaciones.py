from datos import NOMBRE_SECTORES
from datos import DIAS_SEMANA
from datos import mostrar_matriz


def validar_sector(sector):
   #modificacion en el rango 
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

# 2. EL CAPTURADOR (Tu función nueva)
# Usa a la función de tu compañera dentro del while not para insistir hasta que sea correcto
def pedir_sector_valido():
    sec_input = input("Ingrese el número de sector (1-5): ")
    
    # Aquí REUTILIZAMOS la función de tu compañera:
    while not validar_sector(sec_input):
        print("Error: Sector inválido. Ingrese un número del 1 al 5.")
        sec_input = input("Ingrese el número de sector (1-5): ")
        
    return int(sec_input)

# 3. EL CONSULTOR (Tu función pura)
# Solo busca en la matriz el sector que ya sabemos que es 100% válido
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
    
    # Impresión día por día
    for idx, humedad in enumerate(valores_sector):
        dia_nombre = DIAS_SEMANA[idx]
        if humedad == -1:
            print(f"{dia_nombre}: Sin registro")
        else:
            print(f"{dia_nombre}: {humedad}% de humedad")

    # Llamada interna a la función de ordenamiento requerida
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
    
    # Si no desea cambiar, retorna los valores por defecto (50 ± 10)
    return 50, 10

def mostrar_sectores_ideales(sectores: list):
    """Maneja la presentación completa del módulo de Zona Ideal."""
    print("\n--- Identificación de Zona Ideal ---")
    
    # 1. Captura de parámetros (reutilizando la función de captura)
    ideal_target, tolerancia = pedir_rango_ideal()
    
    # 2. Obtención de datos calculados
    ideales, total, prom_general = getIdealValues(sectores, ideal_target, tolerancia)
    
    rango_min = ideal_target - tolerancia
    rango_max = ideal_target + tolerancia

    # 3. Impresión de resultados
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
        # Filtramos los días sin registro (-1)
        mediciones_validas = [val for val in fila if val != -1]
        
        if len(mediciones_validas) > 0:
            promedio_sector = sum(mediciones_validas) / len(mediciones_validas)
            
            # Verificamos si el promedio cae dentro del rango [40%, 60%]
            if limite_inferior <= promedio_sector <= limite_superior:
                nombre = NOMBRE_SECTORES[idx]
                sectores_ideales.append((nombre, promedio_sector))
                suma_promedios_ideales += promedio_sector

    cantidad_total = len(sectores_ideales)
    promedio_general_ideal = (suma_promedios_ideales / cantidad_total) if cantidad_total > 0 else 0.0

    return (sectores_ideales, cantidad_total, promedio_general_ideal)

#-------------------------------------------------------------------------------------------
def menu(valores_actuales):
    while True:
        opcion = input("¿Qué desea hacer? (" \
                                "1 = Ver matriz de humedad / " \
                                "2 = Registrar medición / " \
                                "3 = Obtener valores de un sector / " \
                                "4 = Ver sectores ideales / " \
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
            case _:
                print("Opción inválida")