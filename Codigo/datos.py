import random

# Días de la semana
DIAS_SEMANA = ("Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo")

# Sectores de producción de frutas
NOMBRE_SECTORES = ("Frutillas", "Frambuesas", "Arándanos", "Moras", "Cerezas")

# Rangos de valores críticos e ideales para los sectores
CRITICO_BAJO = 20
IDEAL_BAJO = 40
IDEAL_ALTO = 60
CRITICO_ALTO = 80

def cargar_datos_iniciales():
    # Matriz de humedad: una fila por sector, una columna por día
    datos = []
    for sector in NOMBRE_SECTORES:
        fila = [random.randint(-1, 100) for dia in DIAS_SEMANA]
        datos.append(fila)
    return datos

def mostrar_matriz(datos):
    ancho = 12
    encabezado = "Sector".ljust(ancho) + "".join(dia.ljust(ancho) for dia in DIAS_SEMANA)
    print(encabezado)
    for sector, fila in zip(NOMBRE_SECTORES, datos):
        linea = sector.ljust(ancho) + "".join(f"{valor}%".ljust(ancho) for valor in fila)
        print(linea)

if __name__ == "__main__":
    print("Datos iniciales cargados:", cargar_datos_iniciales())
