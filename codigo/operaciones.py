def registrar_medicion(mediciones, sector, fecha, humedad):
    """Agrega una medición al diccionario en memoria (mediciones[sector][fecha] = humedad).

    Los datos llegan ya validados desde main.py. Lanza ValueError si ya existe una medición
    para ese sector y fecha (para corregirla se usa modificar_medicion). Devuelve el diccionario.
    """
    if fecha in mediciones.setdefault(sector, {}):
        raise ValueError(f"Ya existe una medición para {sector} en {fecha}: use 'Modificar medición' para cambiarla")
    mediciones[sector][fecha] = humedad
    return mediciones


def buscar_medicion(mediciones, sector, fecha):
    """Devuelve la humedad registrada para un sector y fecha. Lanza ValueError si no existe."""
    if fecha not in mediciones.get(sector, {}):
        raise ValueError(f"No existe una medición para {sector} en {fecha}")
    return mediciones[sector][fecha]


def modificar_medicion(mediciones, sector, fecha, nueva_humedad):
    """Reemplaza la humedad de una medición existente. Lanza ValueError si no existe. Devuelve el diccionario."""
    buscar_medicion(mediciones, sector, fecha)
    mediciones[sector][fecha] = nueva_humedad
    return mediciones


# Indicacores H5 actualizar funciones ---------------------------------------------------------------
# def getMaxHumidityValue(sectores: list) -> float:
#     valores_validos = [val for fila in sectores for val in fila if val >= 0]
#     return float(max(valores_validos)) if valores_validos else -1.0

def getMaxHumidityValue(mediciones):
    valores = [
        humedad
        for mediciones_sector in mediciones.values()
        for humedad in mediciones_sector.values()
    ]

    if not valores:
        return None

    return max(valores)
#-------------------------------------------------------------------------------------------------

# def getMinHumidityValue(sectores: list) -> float:
#     valores_validos = [val for fila in sectores for val in fila if val >= 0]
#     return float(min(valores_validos)) if valores_validos else -1.0



def getMinHumidityValue(mediciones):
    valores = [
        humedad
        for mediciones_sector in mediciones.values()
        for humedad in mediciones_sector.values()
    ]

    if not valores:
        return None

    return min(valores)
#------------------------------------------------------


# def getAverageHumidityPerSector(sectores: list) -> list:
#     promedios = []
#     for fila in sectores:
#         validos = [val for val in fila if val >= 0]
#         if validos:
#             promedios.append(sum(validos) / len(validos))
#         else:
#             promedios.append(-1.0)
#     return promedios

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


#------------------------------------------------------



# def getAverageHumidityTotal(sectores: list) -> float:
#     valores_validos = [val for fila in sectores for val in fila if val >= 0]
#     if not valores_validos:
#         return -1.0
#     return sum(valores_validos) / len(valores_validos)

def getAverageHumidityTotal(mediciones):
    valores = [
        humedad
        for mediciones_sector in mediciones.values()
        for humedad in mediciones_sector.values()
    ]

    if not valores:
        return None

    return sum(valores) / len(valores)

#---------------------------------------------------------

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


#----------------------------------------------------------------------------------------------------------

def es_critica(humedad, limites):
    """Devuelve True si la humedad está en zona crítica (menor que critico_bajo o mayor que critico_alto).

    Los límites no son críticos: con los valores por defecto, 20 y 80 NO son críticos.
    """
    return humedad < limites["critico_bajo"] or humedad > limites["critico_alto"]


def es_ideal(humedad, limites):
    """Devuelve True si la humedad está en zona ideal (entre ideal_bajo e ideal_alto, inclusive)."""
    return limites["ideal_bajo"] <= humedad <= limites["ideal_alto"]

def getValuesPerSector(mediciones, codigo_sector):
    """Devuelve las mediciones de un sector como diccionario fecha -> humedad.

    Devuelve una COPIA, para que quien la use no modifique el diccionario principal por accidente.
    Lanza ValueError si el sector no existe en las mediciones.
    """
    if codigo_sector not in mediciones:
        raise ValueError(f"No hay datos para el sector {codigo_sector}")
    return dict(mediciones[codigo_sector])

def orderHumidityValues(valores_sector, descendente=True):
    """Ordena las mediciones de un sector por humedad.

    Recibe un diccionario fecha -> humedad (por ejemplo, el que devuelve getValuesPerSector)
    y devuelve una lista de tuplas (fecha, humedad), de mayor a menor por defecto.
    Con un diccionario vacío devuelve una lista vacía.
    """
    return sorted(valores_sector.items(), key=lambda par: par[1], reverse=descendente)



def getCriticalValues(promedios_por_sector, limites):
    """Devuelve la lista de códigos de sector cuyo PROMEDIO está en zona crítica.

    Recibe un diccionario código -> promedio (lo calcula getAverageHumidityPerSector, H5).
    Los sectores sin mediciones (promedio None) no se consideran.
    Ejemplo: {"S01": 15.0, "S02": 50.0, "S03": None} -> ["S01"]
    """
    return [
        codigo for codigo, promedio in promedios_por_sector.items()
        if promedio is not None and es_critica(promedio, limites)
    ]

def getIdealValues(promedios_por_sector, limites):
    """Devuelve la lista de códigos de sector cuyo PROMEDIO está en zona ideal (límites inclusive).

    Recibe un diccionario código -> promedio. Los sectores sin mediciones (None) no se consideran.
    Ejemplo: {"S01": 40.0, "S02": 61.0} -> ["S01"]
    """
    return [
        codigo for codigo, promedio in promedios_por_sector.items()
        if promedio is not None and es_ideal(promedio, limites)
    ]


def obtener_mediciones_criticas(mediciones, limites):
    """Devuelve, por sector, solo las mediciones individuales en zona crítica (las alertas).

    El resultado tiene la misma forma que mediciones: código -> {fecha: humedad}.
    Todos los sectores aparecen, aunque no tengan alertas (con un diccionario vacío), para que
    el reporte de cada sector pueda pedir alertas["S01"] sin riesgo de KeyError.
    """
    return {
        codigo: {fecha: humedad for fecha, humedad in fechas.items() if es_critica(humedad, limites)}
        for codigo, fechas in mediciones.items()
    }


def filtrar_registros(mediciones, codigo_sector=None, desde=None, hasta=None):
    """Filtra las mediciones por sector, por fecha o por rango de fechas.

    - codigo_sector: un código ("S01") o None para incluir todos los sectores.
    - desde / hasta: fechas "AAAA-MM-DD" (inclusive). None significa "sin límite" de ese lado.
      Para filtrar UNA fecha se pasa la misma fecha en desde y hasta.

    Devuelve un diccionario NUEVO con la misma forma que mediciones (código -> {fecha: humedad}),
    con las fechas ordenadas. Así, al resultado se le pueden aplicar las mismas funciones de
    indicadores (por ejemplo, el promedio del filtro). No modifica el diccionario original.

    Lanza ValueError si el sector no existe o si desde es posterior a hasta.
    Las fechas deben llegar ya validadas (validaciones.validar_fecha) desde main.py.
    """
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



# HISTORIA H6: REPORTE FINAL-------------------------------------------------------------------------------------
def generar_reporte_final(sectores: list, nombres_sectores: tuple, dias_semana: tuple) -> str:
    """
    Genera el reporte ejecutivo semanal consolidado en formato string.
    """
    promedio_global = getAverageHumidityTotal(sectores)
    promedios_por_sector = getAverageHumidityPerSector(sectores)
    max_global = getMaxHumidityValue(sectores)
    min_global = getMinHumidityValue(sectores)

    # Consumo de las funciones de Jesica (H5)
    indices_criticos = getCriticalValues(promedios_por_sector)
    indices_ideales = getIdealValues(promedios_por_sector)

    reporte = [
        "=== REPORTE SEMANAL DE HUMEDAD EN CULTIVOS ===",
        "",
        "INDICADORES GENERALES:",
        f"- Promedio del campo: {promedio_global:.1f}%" if promedio_global >= 0 else "- Promedio del campo: N/A",
        f"- Máximo: {max_global:.1f}%" if max_global >= 0 else "- Máximo: N/A",
        f"- Mínimo: {min_global:.1f}%" if min_global >= 0 else "- Mínimo: N/A",
        "",
        "PROMEDIO POR SECTOR:"
    ]

    for nombre, prom in zip(nombres_sectores, promedios_por_sector):
        if prom < 0:
            reporte.append(f"- {nombre}: N/A (sin mediciones)")
        else:
            reporte.append(f"- {nombre}: {prom:.1f}%")

    reporte.append("\nSECTORES CRÍTICOS (< 20% o > 80%):")
    if indices_criticos:
        for i in indices_criticos:
            prom = promedios_por_sector[i]
            reporte.append(f"- {nombres_sectores[i]}: ({prom:.1f}%)")
    else:
        reporte.append("- Ninguno")

    reporte.append("\nSECTORES IDEALES (40-60%):")
    if indices_ideales:
        for i in indices_ideales:
            prom = promedios_por_sector[i]
            reporte.append(f"- {nombres_sectores[i]}: ({prom:.1f}%)")
    else:
        reporte.append("- Ninguno")

    return "\n".join(reporte)
