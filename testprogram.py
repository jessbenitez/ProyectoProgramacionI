#Datos definidos para el programa-------------------------------------------------------------------------------------------------------------
import random

DIAS_SEMANA = ("Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo")
# Sectores de producción de frutas
NOMBRE_SECTORES = ("Frutillas", "Frambuesas", "Arándanos", "Moras", "Cerezas")

# Rangos de valores críticos e ideales para los sectores
CRITICO_BAJO = 20
IDEAL_BAJO = 40
IDEAL_ALTO = 60
CRITICO_ALTO = 80




def validar_sector(sector): #valida que el sector ingresado por el usuario sea un numero y que este dentro del rango de sectores definidos
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

#crea los valores de la matriz
def cargar_datos_iniciales():
    # Matriz de humedad: una fila por sector, una columna por día
    datos = [] #lista vacia
    for sector in NOMBRE_SECTORES: #itera por cada sector en NOMBRE_SECTORES
        fila = [random.randint(-1, 100) for dia in DIAS_SEMANA] #lista por compresion, genera un numero aleatorio entre -1 y 100 para cada dia en DIAS_SEMANA
        #print(fila) #imprime la fila generada
        datos.append(fila)
    return datos

def mostrar_matriz(datos): #pasa los valores de la matriz generada en la funcion cargar_datos_iniciales
    ancho = 12 
    encabezado = "Sector".ljust(ancho) + "".join(dia.ljust(ancho) for dia in DIAS_SEMANA)
    print(encabezado)
    for sector, fila in zip(NOMBRE_SECTORES, datos):
        linea = sector.ljust(ancho) + "".join(f"{valor}%".ljust(ancho) for valor in fila)
        print(linea)

#funcion que devuelve los valores de un sector en especifico, lo indica el usuario
def getValuesPerSector(matriz, sector_id): #fecive el nro de sector que el usuario quiere ver de 1 a 5
    indiceSeleccionado = sector_id - 1
    return matriz[indiceSeleccionado]


def orderHumidityValues(sector_id):
    """Retorna valores ordenados de mayor a menor (usar lambda)"""
    mediciones_validas = [v for v in sector_id if v != -1]
    return sorted(mediciones_validas, key=lambda x: x, reverse=True)

    
#operaciones y funciones de la seccion priscila---------------------------------------------------------------------------------
def getIdealValues(sectores, humedad_ideal: int = 50, tolerancia: int = 10):
    """Retorna (lista_sectores_ideales, cantidad_total, promedio_ideal)"""
    min_ideal = humedad_ideal - tolerancia
    max_ideal = humedad_ideal + tolerancia

    sectores_ideales = []
    suma_promedios = 0

    for i, sector in enumerate(sectores):
        valores_validos = [valor for valor in sector if valor != -1]
        
        if len(valores_validos) > 0:
            promedio_sector = sum(valores_validos) / len(valores_validos)
            
            if min_ideal <= promedio_sector <= max_ideal:
                print(f"El sector {NOMBRE_SECTORES[i]} tiene un promedio ideal de humedad: {promedio_sector}")
                # Guardamos el sector encontrado
                sectores_ideales.append(NOMBRE_SECTORES[i])
                suma_promedios += promedio_sector
            elif promedio_sector < min_ideal:
                print(f"El sector {NOMBRE_SECTORES[i]} humedad baja: {promedio_sector}")

    # --- FUERA DEL FOR ---
    cantidad_total = len(sectores_ideales)
    promedio_general = (suma_promedios / cantidad_total) if cantidad_total > 0 else 0

    # Ahora sí retorna TODOS los sectores agrupados al finalizar
    return sectores_ideales, cantidad_total, promedio_general
    




def generar_reporte_final(sectores):

    #tiene que recorrer toda la matriz y acceder a cada lista y hacer la suma.. la suma de las 5 listas,
    #hay que dividirlo entre las 5
    

    total = 0
    for lista in sectores: #recorro la lista osea son 5 vueltas , de la matriz
        print(lista), #devuelve cada una de las listas que forman la matriz NIVEL LISTA
        cant_lista = len(sectores) #devuelve la cant de listas dentro de matriz
        for valores in lista: #NIVEL ELEMENTO DENTRO DE LA LISTA, entra a cada elemento de la lista
            if valores != -1:
                sumar_valores = sum(lista) #suma de los elementos de una lista
                print(sumar_valores)
                total = sumar_valores + sumar_valores
        print(total)
#
#



# funcion pricipal--------------------------------------------------------------------------------------------------------------------------------------
# print("Bienvenido al programa de registro de humedad")
# print()
matrizInicial = cargar_datos_iniciales() # Carga los datos iniciales en la matriz
print(matrizInicial)
# print()
# print("Datos iniciales cargados:", matrizInicial) # Imprime los datos iniciales cargados
# print()
# #print(cargar_datos_iniciales()) # Imprime los datos iniciales cargados
# print()
print(mostrar_matriz(matrizInicial)) # Imprime la matriz creda con el formato
# print()
# print(getValuesPerSector(matrizInicial,2)) # Imprime los valores de un sector en especifico, lo indica el usuario
# print()
# print(orderHumidityValues(getValuesPerSector(matrizInicial,2))) # Imprime los valores ordenados de mayor a menor
# print()
# print(getIdealValues(matrizInicial)) # Imprime los valores ideales de cada sector


print()
valores_ideales, cantidad_total, promedio_ideal = getIdealValues(matrizInicial)
print(f"Valores ideales(lista): {valores_ideales}")
print(f"Cantidad total(cant elementos de la lista): {cantidad_total}")
print(f"Promedio ideal: {promedio_ideal}")
print("generar reporte", generar_reporte_final(matrizInicial))



# ==============================================================================
# 1. FUNCIONES FALSAS (MOCKS) 
# Simulamos que son las funciones de Jessi para probar tu reporte de forma aislada
# ==============================================================================
def getTotalTrendingHumidity(sectores):
    return 55.2  # Simulamos que calcula el promedio global

def getMaxHumidityValue(sectores):
    return 82.0  # Simulamos el máximo

def getMinHumidityValue(sectores):
    return 12.0  # Simulamos el mínimo

def getTrendingHumidityPerSector(sectores):
    return [45.3, 80.0, -1, 38.5, 68.2]  # Simulamos la lista de promedios por sector

# ==============================================================================
# 2. TU FUNCIÓN A PROBAR (generar_reporte_final)
# ==============================================================================
def generar_reporte_final(sectores: list, nombres_sectores: tuple, dias_semana: tuple) -> str:
    """Arma el reporte ejecutivo consumiendo los datos."""
    prom_global = getTotalTrendingHumidity(sectores)
    max_global = getMaxHumidityValue(sectores)
    min_global = getMinHumidityValue(sectores)
    promedios_por_sector = getTrendingHumidityPerSector(sectores)
    
    reporte = []
    reporte.append("=== REPORTE SEMANAL DE HUMEDAD EN CULTIVOS ===")
    reporte.append("")
    reporte.append("INDICADORES GENERALES:")
    reporte.append(f"- Promedio del campo: {prom_global}%")
    reporte.append(f"- Máximo global     : {max_global}%")
    reporte.append(f"- Mínimo global     : {min_global}%")
    reporte.append("")
    reporte.append("PROMEDIO POR SECTOR:")
    
    for i, promedio in enumerate(promedios_por_sector):
        nombre = nombres_sectores[i]
        texto_prom = f"{promedio}%" if promedio != -1 else "N/A (sin mediciones)"
        reporte.append(f"- {nombre}: {texto_prom}")
        
    return "\n".join(reporte)

# ==============================================================================
# 3. DATOS DE PRUEBA Y EJECUCIÓN
# ==============================================================================
# Datos de prueba simulados
sectores_prueba = [[0]]  # Matriz ficticia (no importa el contenido porque usamos mocks)
nombres_prueba = ("Sector A", "Sector B", "Sector C", "Sector D", "Sector E")
dias_prueba = ("Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo")

# Ejecutamos tu función y mostramos el resultado
resultado = generar_reporte_final(sectores_prueba, nombres_prueba, dias_prueba)

print("--- RESULTADO IMPRESO EN CONSOLA ---")
print(resultado)