from datetime import timedelta

from operaciones import (
    filtrar_registros,
    getAverageHumidityTotal,
    getMaxHumidityValue,
    getMinHumidityValue,
    getAverageHumidityPerSector,
    agrupar_por_fecha,
    es_critica,
    es_ideal,
    getCriticalValues,
    obtener_mediciones_criticas
)

def reporte_filtrado(mediciones, sectores, filtro):

    mediciones_filtradas = filtrar_registros(mediciones, **filtro)

    lineas = []
    lineas.append("REPORTE DE MEDICIONES FILTRADAS")
    lineas.append("=" * 40)

    for codigo_sector, fechas in mediciones_filtradas.items():
        nombre_sector = sectores[codigo_sector]
        lineas.append(f"\nSector: {nombre_sector} ({codigo_sector})")

        if not fechas:
            lineas.append("Sin mediciones para los filtros seleccionados.")
            continue

        for fecha, humedad in fechas.items():
            lineas.append(f"{fecha}: {humedad}%")

    promedio = getAverageHumidityTotal(mediciones_filtradas)

    if promedio is None:
        lineas.append("\nPromedio del filtro: Sin mediciones")
    else:
        lineas.append(f"\nPromedio del filtro: {promedio:.2f}%")

    return "\n".join(lineas)

def reporte_sector(mediciones, sectores, codigo_sector, limites, fecha_referencia, ventana_dias):

    nombre_sector = sectores[codigo_sector]

    fecha_desde = (
        fecha_referencia - timedelta(days=ventana_dias - 1)
    ).isoformat()

    fecha_hasta = fecha_referencia.isoformat()

    mediciones_filtradas = filtrar_registros(
        mediciones,
        codigo_sector=codigo_sector,
        desde=fecha_desde,
        hasta=fecha_hasta
    )

    mediciones_sector = mediciones_filtradas[codigo_sector]

    lineas = []
    lineas.append(f"REPORTE DEL SECTOR: {nombre_sector}")
    lineas.append(f"Código: {codigo_sector}")
    lineas.append(f"Período: {fecha_desde} al {fecha_hasta}")
    lineas.append(f"Generado: {fecha_referencia.isoformat()}")

    if not mediciones_sector:
        lineas.append("\nSin mediciones en el período.")
        return "\n".join(lineas)

    lineas.append("\nMEDICIONES:")

    for fecha, humedad in sorted(mediciones_sector.items()):
        lineas.append(f"{fecha}: {humedad}%")

    mediciones_un_sector = {
        codigo_sector: mediciones_sector
    }

    maximo = getMaxHumidityValue(mediciones_un_sector)
    minimo = getMinHumidityValue(mediciones_un_sector)
    promedio = getAverageHumidityTotal(mediciones_un_sector)

    lineas.append("\nINDICADORES:")
    lineas.append(f"Humedad máxima: {maximo}%")
    lineas.append(f"Humedad mínima: {minimo}%")
    lineas.append(f"Humedad promedio: {promedio:.2f}%")

    lineas.append("\nESTADO DEL SECTOR:")

    if es_critica(promedio, limites):
        lineas.append("CRÍTICO")
    elif es_ideal(promedio, limites):
        lineas.append("IDEAL")
    else:
        lineas.append("FUERA DEL RANGO IDEAL")

    alertas = obtener_mediciones_criticas(
        mediciones_un_sector, limites
    )

    lineas.append("\nALERTAS:")

    if alertas[codigo_sector]:
        for fecha, humedad in sorted(alertas[codigo_sector].items()):
            lineas.append(f"ALERTA - {fecha}: {humedad}%")
    else:
        lineas.append("No se registraron mediciones críticas.")

    return "\n".join(lineas)
def reporte_general(mediciones, sectores, limites, fecha_referencia):

    maximo = getMaxHumidityValue(mediciones)
    minimo = getMinHumidityValue(mediciones)
    promedio = getAverageHumidityTotal(mediciones)

    lineas = []
    lineas.append("REPORTE GENERAL DEL CAMPO")
    lineas.append("=" * 40)
    lineas.append(f"Fecha de generación: {fecha_referencia.isoformat()}")

    lineas.append("\nINDICADORES GENERALES:")

    if promedio is None:
        lineas.append("Sin mediciones registradas.")
    else:
        lineas.append(f"Humedad máxima: {maximo}%")
        lineas.append(f"Humedad mínima: {minimo}%")
        lineas.append(f"Humedad promedio: {promedio:.2f}%")

    promedios_sector = getAverageHumidityPerSector(mediciones)

    lineas.append("\nPROMEDIO POR SECTOR:")

    for codigo, promedio_sector in promedios_sector.items():
        nombre = sectores[codigo]

        if promedio_sector is None:
            lineas.append(f"{nombre} ({codigo}): Sin mediciones")
        else:
            lineas.append(
                f"{nombre} ({codigo}): {promedio_sector:.2f}%"
            )

    promedios_fecha = agrupar_por_fecha(mediciones)

    lineas.append("\nPROMEDIO POR FECHA:")

    if not promedios_fecha:
        lineas.append("Sin mediciones registradas.")
    else:
        for fecha, promedio_fecha in sorted(promedios_fecha.items()):
            lineas.append(f"{fecha}: {promedio_fecha:.2f}%")

    sectores_criticos = getCriticalValues(
        promedios_sector, limites
    )

    lineas.append("\nSECTORES CON PROMEDIO CRÍTICO:")

    if sectores_criticos:
        for codigo in sectores_criticos:
            nombre = sectores[codigo]
            valor = promedios_sector[codigo]
            lineas.append(f"{nombre} ({codigo}): {valor:.2f}%")
    else:
        lineas.append("No hay sectores con promedio crítico.")

    lineas.append("\nALERTAS CONSOLIDADAS:")
    lineas.append(reporte_alertas(mediciones, sectores, limites))

    lineas.append("\nSECTORES SIN MEDICIONES:")

    sectores_vacios = [
        codigo
        for codigo in sectores
        if not mediciones.get(codigo)
    ]

    if sectores_vacios:
        for codigo in sectores_vacios:
            lineas.append(f"{sectores[codigo]} ({codigo})")
    else:
        lineas.append("Todos los sectores tienen mediciones.")

    return "\n".join(lineas)
def reporte_alertas(mediciones, sectores, limites):

    alertas = obtener_mediciones_criticas(mediciones, limites)

    lineas = []
    lineas.append("REPORTE DE ALERTAS")
    lineas.append("=" * 40)

    hay_alertas = False

    for codigo_sector, fechas in alertas.items():

        if fechas:
            hay_alertas = True
            nombre_sector = sectores[codigo_sector]

            lineas.append(
                f"\nSector: {nombre_sector} ({codigo_sector})"
            )

            for fecha, humedad in sorted(fechas.items()):
                lineas.append(
                    f"ALERTA - {fecha}: {humedad}%"
                )

    if not hay_alertas:
        lineas.append("No se registraron mediciones críticas.")

    return "\n".join(lineas)