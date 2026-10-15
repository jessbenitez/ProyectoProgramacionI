#Funciones nuevas ETAPA 2
#Formato de fecha Fecha (AAAA-MM-DD): 2026-10-12

mediciones = {
    "S01": {
        "2026-10-01": 18.5,  # Crítico bajo
        "2026-10-05": 45.5,  # Ideal
        "2026-10-10": 60.0,  # Límite ideal alto
        "2026-10-12": 52.0
    },
    "S02": {
        "2026-10-02": 82.1,  # Crítico alto
        "2026-10-08": 79.0,
        "2026-10-12": 41.2
    },
    "S03": {},  # Sector sin mediciones (útil para probar reportes vacíos)
    "S04": {
        "2026-10-04": 20.0,  # Límite crítico bajo
        "2026-10-09": 39.5,
        "2026-10-11": 80.0   # Límite crítico alto
    },
    "S05": {
        "2026-10-03": 50.0,  # Ideal
        "2026-10-07": 55.0,
        "2026-10-13": 21.0
    }
}
# agrupar_por_fecha -devuelve el diccionario esperado a partir de un diccionario de mediciones conocido
def agrupar_por_fecha(mediciones):
    fecha_inicio = input("Agrupar desde :")
    Fecha_fin = input("Agrupar hasta :")

    for sector in mediciones:
        print(sector)
        


