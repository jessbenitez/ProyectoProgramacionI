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

PROBABILIDAD_MEDICION_INICIAL = 0.3

def cargar_datos_iniciales():
    # Matriz de humedad: una fila por sector, una columna por día.
    # La mayoría de las celdas arranca sin medición (-1) para poder probar el registro.
    datos = []
    for sector in NOMBRE_SECTORES:
        fila = [
            random.randint(0, 100) if random.random() < PROBABILIDAD_MEDICION_INICIAL else -1
            for dia in DIAS_SEMANA
        ]
        datos.append(fila)
    return datos

def formatear_matriz(datos):
    ancho = 12
    encabezado = "Sector".ljust(ancho) + "".join(dia.ljust(ancho) for dia in DIAS_SEMANA)
    lineas = [encabezado]
    for sector, fila in zip(NOMBRE_SECTORES, datos):
        valores = ["Sin medición" if valor == -1 else f"{valor}%" for valor in fila]
        linea = sector.ljust(ancho) + "".join(valor.ljust(ancho) for valor in valores)
        lineas.append(linea)
    return "\n".join(lineas)

if __name__ == "__main__":
    print("Datos iniciales cargados:", cargar_datos_iniciales())
