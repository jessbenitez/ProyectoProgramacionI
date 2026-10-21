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


# Indicacores -------------------------------------------------------------------------------------
def getMaxHumidityValue(sectores: list) -> float:
    valores_validos = [val for fila in sectores for val in fila if val >= 0]
    return float(max(valores_validos)) if valores_validos else -1.0


def getMinHumidityValue(sectores: list) -> float:
    valores_validos = [val for fila in sectores for val in fila if val >= 0]
    return float(min(valores_validos)) if valores_validos else -1.0


def getAverageHumidityPerSector(sectores: list) -> list:
    promedios = []
    for fila in sectores:
        validos = [val for val in fila if val >= 0]
        if validos:
            promedios.append(sum(validos) / len(validos))
        else:
            promedios.append(-1.0)
    return promedios


def getAverageHumidityTotal(sectores: list) -> float:
    valores_validos = [val for fila in sectores for val in fila if val >= 0]
    if not valores_validos:
        return -1.0
    return sum(valores_validos) / len(valores_validos)

#----------------------------------------------------------------------------------------------------------
def getValuesPerSector(sectores, id_sector):
    return sectores[id_sector - 1]

def orderHumidityValues(sector_id):
    mediciones_validas = [v for v in sector_id if v != -1]
    return sorted(mediciones_validas, key=lambda x: x, reverse=True)

def formatear_detalle_sector(sectores: list, id_sector: int, nombres_sectores: tuple, dias_semana: tuple) -> str:
    valores_sector = getValuesPerSector(sectores, id_sector)
    nombre_sector = nombres_sectores[id_sector - 1]

    lineas = [f"\n--- Mediciones del Sector {id_sector} ({nombre_sector}) ---"]

    for idx, humedad in enumerate(valores_sector):
        dia_nombre = dias_semana[idx]
        if humedad == -1:
            lineas.append(f"{dia_nombre}: Sin registro")
        else:
            lineas.append(f"{dia_nombre}: {humedad}% de humedad")

    valores_ordenados = orderHumidityValues(valores_sector)
    lineas.append(f"\nValores ordenados (mayor a menor): {valores_ordenados}")
    lineas.append(f"Top 3 mediciones más altas: {valores_ordenados[:3]}\n")
    return "\n".join(lineas)


def formatear_sectores_criticos(sectores: list, nombres_sectores: tuple) -> str:
    promedios_por_sector = getAverageHumidityPerSector(sectores)
    indices_criticos = getCriticalValues(promedios_por_sector)
    lineas = ["\n--- Identificación de Sectores Críticos (< 20% o > 80%) ---"]
    if indices_criticos:
        for i in indices_criticos:
            prom = promedios_por_sector[i]
            lineas.append(f"- {nombres_sectores[i]}: ({prom:.1f}%)")
    else:
        lineas.append(" No hay sectores con promedio que alcancen rango crítico.")
    return "\n".join(lineas)


def formatear_sectores_ideales(sectores: list, nombres_sectores: tuple, ideal_target: int, tolerancia: int) -> str:
    rango_min = ideal_target - tolerancia
    rango_max = ideal_target + tolerancia

    promedios_por_sector = getAverageHumidityPerSector(sectores)
    indices_ideales = getIdealValues(promedios_por_sector, float(rango_min), float(rango_max))

    lineas = ["\n--- Identificación de Zona Ideal ---", f"\nSectores en Zona Ideal ({rango_min}% - {rango_max}%):"]
    if indices_ideales:
        for i in indices_ideales:
            prom = promedios_por_sector[i]
            lineas.append(f"- {nombres_sectores[i]}: ({prom:.1f}%)")
    else:
        lineas.append("No hay sectores con promedio dentro del rango ideal.")
    return "\n".join(lineas)

def getIdealValues(promedios_por_sector, ideal_bajo = 40.0, ideal_alto = 60.0) -> list:
    """
    Obtiene los índices de los sectores con humedad ideal.

    Rango: entre ideal_bajo e ideal_alto (40-60%, inclusive)
    Se calcula sobre el promedio del sector, excluyendo valores -1.
    Los sectores sin mediciones (promedio -1) no se consideran.

    Retorna: Lista con índices (0 a 4) de los sectores ideales

    Nota: Usa comprensión de listas
    """
    return [i for i, valor in enumerate(promedios_por_sector) if valor >= ideal_bajo and valor <= ideal_alto]

# H5 ------------------------------------------------------------------------------------------------------
def getCriticalValues(promedios_por_sector, limite_bajo=20.0, limite_alto=80.0) -> list:
    """
    Obtiene los índices de los sectores con humedad crítica (<20% o >80%).

    Qué recibe: una lista de promedios por sector, y dos límites con valor por defecto (20 y 80).
    Qué devuelve: una lista de índices internos (0 a 4), no de IDs ni de nombres.
    Ejemplo: [0, 1, 4] significa sectores A, B y E. Si no hay críticos, lista vacía.
    Los sectores sin mediciones (promedio -1) no se consideran críticos.

    Nota: Usa comprensión de listas
    """
    return [
        i for i, valor in enumerate(promedios_por_sector)
        if valor >= 0 and (valor < limite_bajo or valor > limite_alto)
    ]

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
