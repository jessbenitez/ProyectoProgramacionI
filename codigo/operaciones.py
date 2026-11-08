
def registrar_medicion(mediciones, sector, fecha, humedad):
    if fecha in mediciones.setdefault(sector, {}):
        raise ValueError(f"Ya existe una medición para {sector} en {fecha}: use 'Modificar medición' para cambiarla")
    mediciones[sector][fecha] = humedad
    return mediciones

def buscar_medicion(mediciones, sector, fecha):
    if fecha not in mediciones.get(sector, {}):
        raise ValueError(f"No existe una medición para {sector} en {fecha}")
    return mediciones[sector][fecha]

def modificar_medicion(mediciones, sector, fecha, nueva_humedad):
    buscar_medicion(mediciones, sector, fecha)
    mediciones[sector][fecha] = nueva_humedad
    return mediciones

def getMaxHumidityValue(mediciones):
    valores = [
        humedad
        for mediciones_sector in mediciones.values()
        for humedad in mediciones_sector.values()
    ]

    if not valores:
        return None

    return max(valores)

def getMinHumidityValue(mediciones):
    valores = [
        humedad
        for mediciones_sector in mediciones.values()
        for humedad in mediciones_sector.values()
    ]

    if not valores:
        return None

    return min(valores)

def getAverageHumidityPerSector(mediciones):
    promedios = {}

    for codigo_sector, mediciones_sector in mediciones.items():

        if not mediciones_sector:
            promedios[codigo_sector] = None

        else:
            valores = mediciones_sector.values()
            promedio = sum(valores) / len(valores)
            promedios[codigo_sector] = promedio

    return promedios

def getAverageHumidityTotal(mediciones):
    valores = [
        humedad
        for mediciones_sector in mediciones.values()
        for humedad in mediciones_sector.values()
    ]

    if not valores:
        return None

    return sum(valores) / len(valores)

def agrupar_por_fecha(mediciones):
    acumulador = {}

    for mediciones_sector in mediciones.values():

        for fecha, humedad in mediciones_sector.items():

            if fecha not in acumulador:
                acumulador[fecha] = []

            acumulador[fecha].append(humedad)

    promedios_por_fecha = {}

    for fecha, valores in acumulador.items():

        promedio = sum(valores) / len(valores)
        promedios_por_fecha[fecha] = promedio

    return promedios_por_fecha

def es_critica(humedad, limites):
    return humedad < limites["critico_bajo"] or humedad > limites["critico_alto"]

def es_ideal(humedad, limites):
    return limites["ideal_bajo"] <= humedad <= limites["ideal_alto"]

def getValuesPerSector(mediciones, codigo_sector):
    if codigo_sector not in mediciones:
        raise ValueError(f"No hay datos para el sector {codigo_sector}")
    return dict(mediciones[codigo_sector])

def orderHumidityValues(valores_sector, descendente=True):
    return sorted(valores_sector.items(), key=lambda par: par[1], reverse=descendente)

def getCriticalValues(promedios_por_sector, limites):
    return [
        codigo for codigo, promedio in promedios_por_sector.items()
        if promedio is not None and es_critica(promedio, limites)
    ]

def getIdealValues(promedios_por_sector, limites):
    return [
        codigo for codigo, promedio in promedios_por_sector.items()
        if promedio is not None and es_ideal(promedio, limites)
    ]


def obtener_mediciones_criticas(mediciones, limites):
    return {
        codigo: {fecha: humedad for fecha, humedad in fechas.items() if es_critica(humedad, limites)}
        for codigo, fechas in mediciones.items()
    }


def filtrar_registros(mediciones, codigo_sector=None, desde=None, hasta=None):
    if codigo_sector is not None and codigo_sector not in mediciones:
        raise ValueError(f"No hay datos para el sector {codigo_sector}")
    if desde is not None and hasta is not None and desde > hasta:
        raise ValueError(f"Rango inválido: la fecha inicial ({desde}) es posterior a la final ({hasta})")

    codigos = [codigo_sector] if codigo_sector is not None else list(mediciones)

    return {
        codigo: {
            fecha: humedad
            for fecha, humedad in sorted(mediciones[codigo].items())
            if (desde is None or desde <= fecha) and (hasta is None or fecha <= hasta)
        }
        for codigo in codigos
    }
