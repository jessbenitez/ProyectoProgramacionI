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
