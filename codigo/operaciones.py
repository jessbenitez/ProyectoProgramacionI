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

#-------------------------------------------------------------------------------------------
def menu(valores_actuales):
    while True:
        opcion = input("¿Qué desea hacer? (" \
                                "1 = Ver matriz de humedad / " \
                                "2 = Registrar medición / " \
                                "3 = Obtener valores de un sector / " \
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
            case _:
                print("Opción inválida")