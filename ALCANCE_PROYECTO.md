# DOCUMENTO DE ALCANCE DEL PROYECTO
## Proyecto Integrador - Etapa 1: Sistema de Monitoreo de Humedad en Cultivos

**Asignatura:** Programación I / Algoritmos y Estructuras I  
**Nombre del grupo:** Error 404  
**Participantes:**
- Nicole Quilmore
- Jesica Benitez
- Priscila Challa

**Comisión:** 584514  
**Cuatrimestre:** 2C 2026  
**Etapa:** 1 - Prototipo Funcional en Memoria  
**Versión:** 2.0 (Reducida)

---

## 1. DESCRIPCIÓN DEL PROBLEMA

La agricultura moderna requiere monitoreo constante de condiciones ambientales para optimizar el riego y asegurar la salud de los cultivos. En particular, la humedad del suelo es crítica: valores muy bajos (<20%) causan estrés hídrico; valores muy altos (>80%) favorecen enfermedades fúngicas. 

Los productores agrícolas necesitan un sistema que:
- Registre mediciones de humedad en múltiples sectores del campo
- Identifique rápidamente sectores en condiciones críticas
- Proporcione indicadores de tendencias para tomar decisiones de riego
- Permita consultar y analizar las mediciones registradas durante la semana actual

---

## 2. OBJETIVO GENERAL

Desarrollar un **prototipo funcional en Python** que permita monitorear, analizar y reportar la humedad del suelo en diferentes sectores de un cultivo, demostrando la capacidad de integrar estructuras de datos, funciones modulares, validaciones y procesamiento de información. 😉

---

## 3. ALCANCE FUNCIONAL MÍNIMO

El sistema debe incluir las siguientes capacidades:

### 3.1 Gestión de Datos
1. **Presentar información general** del dominio y los elementos que administra el sistema
2. **Registrar datos** ingresados por el usuario (mediciones de humedad)
3. **Consultar y mostrar** datos cargados por sector

### 3.2 Análisis y Cálculos (3+ Cálculos Requeridos)
4. **Calcular indicadores de humedad:**
   - Máximo global
   - Mínimo global
   - Promedio por sector
   - Promedio total del campo

5. **Buscar** un elemento por identificador (sector)

### 3.3 Detección de Condiciones
6. **Detectar y reportar:**
   - Sectores con humedad crítica (<20% o >80%)
   - Sectores con humedad ideal (40-60%)

### 3.4 Reporte
7. **Generar resumen general** del procesamiento con indicadores clave

### 3.5 Interacción
8. **Mantener un menú activo** hasta que el usuario seleccione salir, permitiendo acceso a todas las funcionalidades

---

## 4. ESTRUCTURA DE DATOS

### 4.1 Representación de Datos (En Memoria)

La información se mantendrá **únicamente en memoria** durante la ejecución. Los datos se estructuran de la siguiente manera:

| Estructura | Uso | Ejemplo |
|-----------|-----|---------|
| **Matriz** | Datos de humedad: filas = sectores, columnas = días | `[[45, 52, 48, 61, ...], [78, 82, 79, 88, ...]]` |
| **Lista** | Resultados de búsquedas y filtrados | `[45, 52, 48, 61, ...]` |
| **Tupla** | Datos fijos: nombres de sectores, días de semana | `("Sector A", "Sector B", "Sector C")` |
| **Cadena** | Identificadores, etiquetas, mensajes | `"Sector A"`, `"25.5%"` |

### 4.2 Especificaciones de Datos

- **Cantidad de sectores:** 5 (identificados para usuario como 1-5)
- **Cantidad de mediciones:** 7 días (una semana completa: Lunes a Domingo)
- **Período de análisis:** Una semana laboral
- **Rango de valores:** 0 a 100 (porcentaje de humedad)
- **Valor especial:** -1 (medición no cargada)

### 4.3 Identificación de Sectores

El sistema utiliza una representación clara para el usuario:

| ID Visible | Nombre | Índice Interno |
|-----------|--------|-----------------|
| 1 | Sector A | 0 |
| 2 | Sector B | 1 |
| 3 | Sector C | 2 |
| 4 | Sector D | 3 |
| 5 | Sector E | 4 |

**Nota:** El usuario ve IDs 1-5 y nombres descriptivos. Los índices 0-4 son internos de Python.

### 4.4 Clasificación de Estados de Humedad

| Rango | Estado | Descripción |
|-------|--------|-------------|
| 0-19% | 🔴 Crítico Bajo | Riego urgente requerido |
| 20-39% | 🟡 Baja | Por debajo del ideal |
| 40-60% | 🟢 Ideal | Condiciones óptimas |
| 61-80% | 🟡 Alta | Por encima del ideal |
| 81-100% | 🔴 Crítico Alto | Drenaje urgente requerido |

### 4.5 Representación de Medición No Cargada

- **-1:** Indica que no existe medición cargada para esa celda
- Se **excluye** de todos los cálculos (promedios, máximos, mínimos)
- Se reporta como "Sin medición" en la interfaz

**Ejemplo de matriz inicial:**
```
sectores = [
    [45, 52, 48, 61, -1, -1, -1],  # Sector A: 4 días con datos
    [78, 82, 79, -1, -1, -1, -1],  # Sector B: 3 días con datos
    [-1, -1, -1, -1, -1, -1, -1],  # Sector C: sin datos aún
    [35, 40, 38, 42, 39, 41, 36],  # Sector D: semana completa
    [65, 68, 70, 72, 71, 69, 67]   # Sector E: semana completa
]
```

---

## 5. COMPONENTES Y MÓDULOS

### 5.1 Estructura Modular

```
proyecto_etapa1/
├── main.py              # Menú interactivo
├── datos.py             # Constantes y datos iniciales
├── operaciones.py       # Funciones de cálculo y procesamiento
└── README.md            # Documentación
```

### 5.2 Responsabilidades por Módulo

**main.py:**
- Menú principal interactivo (6 opciones)
- Captura de entradas del usuario
- Validación de opciones de menú
- Llamada a funciones de operaciones.py
- Presentación de resultados

**datos.py:**
- Constantes configurables (límites de humedad)
- Tuplas inmutables (días de la semana, nombres de sectores)
- Función para cargar matriz inicial
- Datos preestablecidos para pruebas

**operaciones.py:**
- Todas las funciones de cálculo
- Todas las funciones de búsqueda y consulta
- Funciones de validación básica
- Función de generación de reporte

---

## 6. FUNCIONES PRINCIPALES A IMPLEMENTAR (8 Funciones)

### 6.1 Consulta de Datos
```python
def getValuesPerSector(sectores, id_sector) -> list:
    """
    Retorna lista de valores de humedad para un sector específico.
    
    Parámetros:
    - sectores: matriz de humedad
    - id_sector: ID del sector (1-5)
    
    Retorna: Lista con 7 valores (uno por día)
    
    Nota: Se excluyen valores -1 en presentación
    """

def orderHumidityValues(valores) -> list:
    """
    Ordena valores de humedad de mayor a menor.
    
    Parámetros:
    - valores: lista de valores numéricos
    
    Retorna: Lista ordenada (usa lambda como criterio)
    
    Ejemplo: [65, 50, 40, 30, 20] → [65, 50, 40, 30, 20]
    """
```

### 6.2 Indicadores Globales
```python
def getMaxHumidityValue(sectores) -> float:
    """
    Obtiene el valor máximo de humedad en toda la matriz.
    
    Excluye valores -1 (sin medición).
    
    Retorna: float con el máximo encontrado
    """

def getMinHumidityValue(sectores) -> float:
    """
    Obtiene el valor mínimo de humedad en toda la matriz.
    
    Excluye valores -1 (sin medición).
    
    Retorna: float con el mínimo encontrado
    """

def getAverageHumidityPerSector(sectores) -> list:
    """
    Calcula promedio de humedad por sector.
    
    Excluye valores -1 de los cálculos.
    Si un sector no tiene mediciones: devuelve -1.
    
    Retorna: Lista con promedio por cada sector
    
    Ejemplo: [45.3, 80.0, -1, 38.5, 68.2]
    """

def getAverageHumidityTotal(sectores) -> float:
    """
    Calcula el promedio total de humedad del campo.
    
    Excluye valores -1.
    
    Retorna: float con promedio semanal del campo
    """
```

### 6.3 Detección de Condiciones
```python
def getCriticalValues(sectores, limite_bajo=20, limite_alto=80) -> list:
    """
    Obtiene lista de sectores con humedad crítica.
    
    Considera ambos casos:
    - Crítico bajo: humedad < limite_bajo (20%)
    - Crítico alto: humedad > limite_alto (80%)
    
    Retorna: Lista con índices de sectores críticos
    
    Nota: Usa comprensión de listas
    """

def getIdealValues(sectores, ideal_bajo=40, ideal_alto=60) -> list:
    """
    Obtiene lista de sectores con humedad ideal.
    
    Rango: entre ideal_bajo y ideal_alto (40-60%)
    
    Retorna: Lista con índices de sectores ideales
    """
```

### 6.4 Reporte
```python
def generar_reporte_final(sectores, nombres_sectores, dias_semana) -> str:
    """
    Genera reporte simplificado con información clave.
    
    Incluye:
    - Indicadores generales (max, min, promedio)
    - Promedio por sector
    - Sectores críticos
    - Sectores ideales
    
    Retorna: String formateado para mostrar en consola
    """
```

---

## 7. CARACTERÍSTICAS TÉCNICAS OBLIGATORIAS

El proyecto **debe evidenciar**:

- ✅ **Funciones y parámetros:** 8 funciones modulares con parámetros claros
- ✅ **Módulos:** 3 archivos con responsabilidades separadas
- ✅ **Listas:** Para colecciones de datos y resultados
- ✅ **Matrices:** Para datos bidimensionales (sectores × días)
- ✅ **Tuplas:** Para datos fijos (días, nombres de sectores, límites)
- ✅ **Cadenas:** Validación y formato de mensajes
- ✅ **Lambda:** Uso en ordenamiento de valores
- ✅ **Comprensión:** Uso en filtrado de datos críticos/ideales
- ✅ **Ciclos y decisiones:** Menú repetitivo, recorridos, validaciones
- ✅ **Validaciones:** Sector (1-5), día (0-6), humedad (0-100), opción de menú
- ✅ **Git/GitHub:** Commits progresivos con participación verificable

---

## 8. LIMITACIONES Y RESTRICCIONES

### 8.1 Lo que SÍ está incluido en Etapa 1
- Estructuras de datos en memoria (listas, matrices, tuplas)
- Funciones modulares y validaciones básicas
- Menú interactivo por consola
- Cálculos e informes simplificados
- Control de errores sin cierre de programa
- Repositorio Git con commits progresivos

### 8.2 Lo que NO está incluido en Etapa 1
- ❌ Persistencia de datos (archivos, bases de datos)
- ❌ Interfaz gráfica
- ❌ Configuración de límites desde el menú (solo constantes)
- ❌ Actualización con confirmación de mediciones existentes
- ❌ Promedio por día
- ❌ Ranking ordenado de sectores
- ❌ Gráficos o visualización ASCII

---

## 9. INTEGRANTES Y RESPONSABILIDADES

| Estudiante | Rol Principal | Historias | Funciones Desarrolladas |
|-----------|---------------|-----------|------------------------|
| **Nicole** | Infraestructura | H1, H4 | Setup, registrar_medicion() |
| **Jesica** | Consultas | H2, H5 | getValuesPerSector(), getCriticalValues(), getIdealValues() |
| **Priscila** | Análisis | H3, H6 | Indicadores (Max, Min, Promedios), generar_reporte_final(), README |

**Requisito:** Cada integrante debe participar en funciones, módulos, interfaz y documentación.

---

## 10. VALIDACIONES NECESARIAS

El sistema validará:

- ✅ Sector ingresado (debe estar entre 1-5)
- ✅ Día ingresado (debe estar entre 0-6)
- ✅ Humedad ingresada (debe estar entre 0-100)
- ✅ Entrada numérica válida (rechazar caracteres no numéricos)
- ✅ Opción de menú válida (rechazar opciones inexistentes)

**Comportamiento:** Ante error, mostrar mensaje claro y permitir reintentar (sin cerrar programa)

---

## 11. TECNOLOGÍA Y HERRAMIENTAS

### 11.1 Lenguaje y Versión
- **Python:** 3.8 o superior
- **Interfaz:** Consola (terminal/cmd)

### 11.2 Control de Versiones
- **Git:** Sistema de control de versiones local
- **GitHub:** Repositorio remoto para trabajo colaborativo

### 11.3 Librerías
- Estándar de Python (sin dependencias externas)
- `random` para generación de datos de prueba (opcional)

### 11.4 Configuración
```python
# En datos.py - Constantes (NO modificables en tiempo de ejecución)
CRITICO_BAJO = 20
IDEAL_BAJO = 40
IDEAL_ALTO = 60
CRITICO_ALTO = 80
```

---

## 12. CRITERIOS DE ACEPTACIÓN GENERALES

El proyecto será aceptado cuando:

1. ✅ Se ejecuta desde `main.py` sin errores
2. ✅ El menú funciona correctamente (6 opciones funcionan)
3. ✅ Registro de mediciones: validar sector, día y humedad
4. ✅ Consulta de sector: mostrar los 7 valores del día
5. ✅ Indicadores: máximo, mínimo, promedios calculan correctamente
6. ✅ Alertas: detecta sectores críticos e ideales
7. ✅ Reporte final: muestra resumen con información clave
8. ✅ Validaciones: rechaza datos inválidos sin cerrar programa
9. ✅ Estructuras: matriz, listas, tuplas usadas correctamente
10. ✅ Lambda: utilizado en ordenamiento
11. ✅ Comprensión: utilizado en filtrado
12. ✅ Repositorio: contiene commits de todos los integrantes
13. ✅ README: explica problema, autores, ejecución, funcionalidades
14. ✅ Todos los integrantes comprenden el sistema completo

---

## 13. ESTIMACIÓN DE TRABAJO

| Componente | Líneas Aprox. | Tiempo Estimado |
|-----------|---------------|-----------------|
| main.py (menú simple) | 100-150 | 2-3 horas |
| datos.py (constantes) | 30-50 | 30 minutos |
| operaciones.py (8 funciones) | 200-250 | 5-6 horas |
| README.md | 150-200 | 1 hora |
| **TOTAL** | **~500 líneas** | **~10 horas** |

**Por persona:** ~3-4 horas (muy manejable)

---

## 14. PLAN DE TRABAJO (6 Historias)

### H1: Setup del Proyecto y Datos Base (Nicole)
- Crear estructura de carpetas y módulos
- Inicializar repositorio Git
- Definir constantes en datos.py
- Crear matriz inicial con datos de prueba

### H2: Consultas de Datos (Jesica)
- Implementar getValuesPerSector()
- Implementar orderHumidityValues() con lambda
- Crear menú "Consultar sector"
- Validar entrada de sector

### H3: Indicadores de Humedad (Priscila)
- Implementar getMaxHumidityValue()
- Implementar getMinHumidityValue()
- Implementar getAverageHumidityPerSector()
- Implementar getAverageHumidityTotal()
- Crear menú "Ver indicadores"

### H4: Registro de Mediciones (Nicole)
- Implementar registrar_medicion()
- Validar sector, día, humedad
- Crear menú "Registrar medición"
- Mensaje de confirmación

### H5: Alertas y Detección (Jesica)
- Implementar getCriticalValues()
- Implementar getIdealValues()
- Crear menú "Ver sectores críticos"
- Crear menú "Ver sectores ideales"

### H6: Reporte Final y Documentación (Priscila)
- Implementar generar_reporte_final()
- Crear menú "Generar reporte"
- Redactar README.md completo
- Documentar decisiones de diseño

---

## 15. MENÚ PRINCIPAL (6 Opciones)

```
=== SISTEMA DE MONITOREO DE HUMEDAD EN CULTIVOS ===

1. Consultar valores por sector
2. Ver indicadores generales
3. Ver sectores críticos
4. Ver sectores ideales
5. Registrar nueva medición
6. Generar reporte final
0. Salir

Ingrese opción:
```

---

## 16. REPORTE FINAL (Simplificado)

```
=== REPORTE SEMANAL DE HUMEDAD EN CULTIVOS ===

INDICADORES GENERALES:
- Promedio del campo: 55.2%
- Máximo: 82.0%
- Mínimo: 12.0%

PROMEDIO POR SECTOR:
- Sector A: 45.3%
- Sector B: 80.0%
- Sector C: N/A (sin mediciones)
- Sector D: 38.5%
- Sector E: 68.2%

SECTORES CRÍTICOS (< 20% o > 80%):
- Sector B (80.0%)

SECTORES IDEALES (40-60%):
- Sector A (45.3%)
- Sector D (38.5%)
```

---

## 17. NOTAS IMPORTANTES

- 📝 Las decisiones de diseño deben documentarse en el README
- 🔄 Los commits deben ser pequeños y descriptivos (mínimo 6 commits por persona)
- 👥 Todos deben tocar código, interfaz y documentación
- ✅ Lambda debe usarse en ordenamiento (orderHumidityValues)
- ✅ Comprensión debe usarse en filtrado (getCriticalValues, getIdealValues)
- 🎯 El sistema debe ser comprensible y usable sin instrucciones previas

