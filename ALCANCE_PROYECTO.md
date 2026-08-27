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

---

## 1. DESCRIPCIÓN DEL PROBLEMA

La agricultura moderna requiere monitoreo constante de condiciones ambientales para optimizar el riego y asegurar la salud de los cultivos. En particular, la humedad del suelo es crítica: valores muy bajos (<20%) causan estrés hídrico; valores muy altos (>80%) favorecen enfermedades fúngicas. 

Los productores agrícolas necesitan un sistema que:
- Registre mediciones de humedad en múltiples sectores del campo
- Identifique rápidamente sectores en condiciones críticas
- Proporcione indicadores de tendencias para tomar decisiones de riego
(FLAG)
- Permita consultar y analizar las mediciones registradas durante la semana actual

---

## 2. OBJETIVO GENERAL

Desarrollar un **prototipo funcional en Python** que permita monitorear, analizar y reportar la humedad del suelo en diferentes sectores de un cultivo, demostrando la capacidad de integrar estructuras de datos, funciones modulares, validaciones y procesamiento de información. (Que buena scrum master 😉)

---

## 3. ALCANCE FUNCIONAL MÍNIMO

El sistema debe incluir, como mínimo, las siguientes capacidades:

### 3.1 Gestión de Datos
1. **Presentar información general** del dominio y los elementos que administra el sistema
2. **Registrar datos** ingresados por el usuario (carga/actualización de mediciones)
3. **Consultar y mostrar** datos cargados con formato claro (listados por sector)

### 3.2 Análisis y Cálculos
4. **Realizar al menos tres cálculos** o indicadores relevantes:
   - Promedio de humedad por sector
   - Promedio total de humedad
   - Máximo y mínimo global

5. **Buscar** un elemento por identificador (sector) o criterio definido
(FLAG)
### 3.3 Detección y Alertas
6. **Detectar condiciones destacables:**
   - Sectores con humedad crítica baja (<20%)
   - Sectores con humedad crítica alta (>80%)
   - Sectores con humedad ideal (40-60%)

### 3.4 Conteos
7. **Contar y reportar:**
   - Cantidad de sectores en estado crítico (bajo y alto)
   - Cantidad de sectores en estado ideal
   - Cantidad total de mediciones cargadas

### 3.5 Reportes
8. **Generar resumen general** del procesamiento con:
   - Indicadores globales
   - Ranking de sectores
   - Estado de cada sector (crítico, ideal, normal)

### 3.6 Interacción
8. **Mantener un menú activo** hasta que el usuario seleccione salir, permitiendo acceso a todas las funcionalidades

---

## 4. ESTRUCTURA DE DATOS

### 4.1 Representación de Datos (En Memoria)

La información se mantendrá **únicamente en memoria** durante la ejecución. Los datos se estructuran de la siguiente manera:

| Estructura | Uso | Ejemplo |
|-----------|-----|---------|
| **Matriz** | Datos de humedad: filas = sectores, columnas = días | `[[45, 52, 48, 61, ...], [78, 82, 79, 88, ...]]` |
| **Lista** | Colección de valores o resultados de consultas | `[45, 52, 48, 61, ...]` |
| **Tupla** | Datos fijos: nombres de sectores, límites críticos | `("Sector A", "Sector B", "Sector C")` |
| **Cadena** | Identificadores, etiquetas, mensajes de usuario | `"Sector A"`, `"25.5%"` |

### 4.2 Especificaciones de Datos

- **Cantidad de sectores:** 5 (identificados como 0-4)
(FLAG)
- **Cantidad de mediciones:** 7 días (una semana completa)
- **Período de análisis**: Semana laboral (Lunes a Domingo)
- **Rango de valores:** 0 a 100 (porcentaje de humedad)
- **Límite crítico por baja humedad:** (0-19)%
- **Fuera del rango ideal:** (20-39)%
- **Ideal:** (40-60)%
- **Fuera del rango ideal:** (61-80)%
- **Crítico por exceso de humedad:** (81-100)%

(FLAG)
### 4.2.1 Identificación de Sectores

El sistema utiliza:
- ID visible para el usuario: 1 a 5
- Etiqueta clara: Sector A, Sector B, Sector C, Sector D, Sector E
- Índice interno en Python: 0-4 (para acceso a matriz)

Ejemplo:
ID 1 → Sector A → Índice 0
ID 2 → Sector B → Índice 1
ID 3 → Sector C → Índice 2
ID 4 → Sector D → Índice 3
ID 5 → Sector E → Índice 4

El usuario nunca ve los índices 0-4. Todos los mensajes mostrarán ID 1-5 y nombres descriptivos.

### 4.2.2 Comportamiento de Actualización
El sistema informa: "Ya existe una medición para Sector A el Lunes"

### 4.2.3 Valores Especiales
La matriz se debe inicializar con valores -1 ya que el valor 0% es un valor posible entre los ingresados.
---

## 5. COMPONENTES Y MÓDULOS

### 5.1 Estructura Modular Mínima

```
proyecto_etapa1/
├── main.py              # Menú, entradas, coordinación general
├── datos.py             # Constantes y datos iniciales
├── operaciones.py       # Validaciones, búsquedas, cálculos e informes
└── README.md            # Documentación
```

### 5.2 Responsabilidades por Módulo

**main.py:**
- Menú principal interactivo
- Captura de entradas del usuario
- Validación de opciones
- Coordinación del flujo de la aplicación
- Presentación de resultados al usuario

**datos.py:**
- Constantes configurables (límites, nombres de sectores)
- Tuplas inmutables (días de la semana, sectores)
- Función para cargar datos iniciales
- Datos preestablecidos para pruebas

**operaciones.py:**
- Todas las funciones de validación
- Funciones de búsqueda y consulta
- Funciones de cálculo e indicadores
- Funciones de análisis y detección de condiciones
- Generación de reportes

---

## 6. FUNCIONES PRINCIPALES A IMPLEMENTAR
(FLAG)
### 6.1 Consulta de Datos
- `getValuesPerSector(sectores, id_sector)` → Lista de valores
    """
    Consulta completa de un sector.
    
    Retorna información:
    {
        'nombre': 'Sector B',
        'mediciones': {
            'Lunes': 45.0,
            'Martes': 52.0,
            'Miércoles': -1,  # Sin medición
            ...
        },
        'promedio': 48.5,
        'maximo': 52.0,
        'maximo_dia': 'Martes',
        'minimo': 45.0,
        'minimo_dia': 'Lunes',
        'estado': 'IDEAL'
    }
    """
- `orderHumidityValues(valores)` → Lista ordenada (mayor a menor)
(FLAG)
### 6.2 Indicadores Globales
- `getMaxHumidityValue(sector_id=None)` → objeto con valor, sector y dia (máximo)
- `getMinHumidityValue(sector_id=None)` → objeto con valor, sector y dia (máximo)
- `getAverageHumidityPerSector(sectores)` → list (promedios por sector)
"""
    Calcula promedio de humedad por sector.
    
    - Excluye valores -1 (sin medición)
    - Si un sector no tiene mediciones: retorna -1 y mensaje informativo
    - Si un sector tiene algunas mediciones: promedia solo las válidas
    
    Retorna: Lista de promedios por sector
    
    Ejemplo:
    [45.3, 80.0, -1, 38.5, 68.2]  # Sector C sin datos
"""
- `getTotalAverageHumidity(sectores)` → float (promedio global)

### 6.3 Detección de Condiciones
- `getCriticalLowHumidity(sectores, limite=20)` → lista (sectores críticos)
- `getCriticalHighHumidity(sectores, limite=80)` → lista (sectores críticos)
- `getIdealValues(sectores, humedad_ideal=50, tolerancia=10)` → lista (sectores ideales)

### 6.4 Registro de Datos
(FLAG)
- `registrar_medicion(sectores, id_sector, humedad, dia)` → bool
- `getRankingSectoresPorPromedio(valor)` → bool (lambda)
""" Ordena sectores de MENOR a MAYOR promedio semanal de humedad. """
- `validar_sector(id_sector, total_sectores)` → bool
### 6.5 Reportes

Función principal:
def generar_reporte_final(sectores, nombres_sectores, dias_semana) -> str:
    """Genera resumen general integrando todos los informes"""

El reporte debe incluir estos 5 informes:

1. **Informe por Sector (Tabla Semanal)**
   - Para cada sector: mediciones de cada día, promedio, estado
   
2. **Informe Diario**
   - Para cada día: promedio del campo, cantidad de mediciones cargadas
   
3. **Alertas - Sectores Críticos Bajos**
   - Lista de sectores con humedad <20% (días específicos)
   
4. **Alertas - Sectores Críticos Altos**
   - Lista de sectores con humedad >80% (días específicos)
   
5. **Ranking de Sectores**
   - Ordenados de menor a mayor promedio semanal
   - Interpretación: primeros = más secos, últimos = más húmedos

### 6.6 Contadores
-  `countCriticalLowHumidity(sectores, limite=20)` -> int:
    """Cuenta sectores con humedad crítica baja"""

-  `countCriticalHighHumidity(sectores, limite=80)` -> int:
    """Cuenta sectores con humedad crítica alta"""

-  `countIdealHumidity(sectores, ideal_bajo=40, ideal_alto=60)` -> int:
    """Cuenta sectores con humedad ideal"""
---

## 7. CARACTERÍSTICAS TÉCNICAS OBLIGATORIAS

El proyecto **debe evidenciar**:

- ✅ **Funciones y parámetros:** Descomposición en operaciones cohesivas
- ✅ **Módulos:** Separación de responsabilidades entre archivos
- ✅ **Listas:** Para colecciones de datos
- ✅ **Matrices:** Para datos bidimensionales (sectores × días)
- ✅ **Tuplas:** Para datos inmutables (constantes)
- ✅ **Cadenas:** Normalización y validación
- ✅ **Comprensión, slicing y/o lambda:** Uso justificado en al menos una operación
- ✅ **Ciclos y decisiones:** Menú repetitivo, recorridos, búsquedas
- ✅ **Validaciones:** Sin cerrar el programa ante errores
- ✅ **Git/GitHub:** Commits progresivos con participación verificable

---

## 8. LIMITACIONES Y RESTRICCIONES

### 8.1 Lo que SÍ está incluido en Etapa 1
- Estructuras de datos en memoria (listas, matrices, tuplas)
- Funciones modulares y validaciones
- Menú interactivo por consola
- Cálculos e informes
- Control de errores sin cierre de programa
- Repositorio Git con commits progresivos

### 8.2 Lo que NO está incluido en Etapa 1
- ❌ Persistencia de datos (archivos, bases de datos)
- ❌ Interfaz gráfica
- ❌ Diccionarios o conjuntos
- ❌ Conexión a servidores remotos
- ❌ Importación desde archivos externos

---

## 9. INTEGRANTES Y RESPONSABILIDADES

| Estudiante | Rol Principal | Historias Asignadas | Responsabilidades |
|-----------|---------------|-------------------|------------------|
| **Nicole** | Coordinación/Infraestructura | H1, H4, H7 | Setup, validaciones, menú principal |
| **Jesica** | Consultas/Reportes | H2, H5, H8 | Lectura de datos, ideales, reporte |
| **Priscila** | Análisis/Cálculos | H3, H6, H9 | Indicadores, registro, documentación |

**Requisito:** Cada integrante debe participar en funciones, módulos, interfaz y documentación.

---

## 10. TECNOLOGÍA Y HERRAMIENTAS

### 10.1 Lenguaje y Versión
- **Python:** 3.8 o superior
- **Interfaz:** Consola (terminal/cmd)

### 10.2 Control de Versiones
- **Git:** Sistema de control de versiones local
- **GitHub:** Repositorio remoto para trabajo colaborativo

(FLAG)
### 10.3 Librerías y Configuración

Los límites de humedad se definen como **constantes** en datos.py:

```python
# En datos.py
HUMEDAD_CRITICO_BAJO = 20      # Límite inferior
HUMEDAD_IDEAL_BAJO = 40        # Rango ideal
HUMEDAD_IDEAL_ALTO = 60        # Rango ideal
HUMEDAD_CRITICO_ALTO = 80      # Límite superior
```

Durante ESTA ETAPA (Etapa 1):
- ❌ El usuario NO puede modificar estos límites desde el menú
- ✅ Son constantes de configuración centralizadas
- ✅ Se pueden cambiar editando datos.py (no en tiempo de ejecución)

---

## 11. CRITERIOS DE ACEPTACIÓN GENERALES

El proyecto será aceptado cuando:

1. ✅ Se ejecute desde `main.py` sin errores
2. ✅ El menú funcione correctamente y acceda a todas las funcionalidades
3. ✅ Todas las funciones validadas devuelvan resultados correctos
4. ✅ Los datos inválidos se rechacen sin cerrar el programa
5. ✅ Las estructuras de datos (lista, matriz, tupla) se utilicen correctamente
6. ✅ El repositorio contenga commits de todos los integrantes
7. ✅ El README explique problema, integrantes, ejecución y funcionalidades
8. ✅ Todos los integrantes comprendan y puedan explicar el sistema completo

---

## 12. DELIVERABLES

| Entregable | Contenido | Responsable |
|-----------|-----------|-------------|
| **Repositorio Git** | Código funcional + commits progresivos | Todos |
| **README.md** | Descripción, instrucciones, autores | Estudiante 3 |
| **Documento de Análisis** | Este alcance + decisiones de diseño | Equipo |
| **Casos de Prueba** | Datos válidos, inválidos, límites | Todos |
| **Presentación (8-10 min)** | Demo + explicación de funcionamiento | Todos |

---

## 13. TIMELINE ESTIMADO

| Semana | Actividad |
|--------|-----------|
| **Semana 1** | Setup del proyecto (H1), Consultas (H2), Indicadores (H3) |
| **Semana 2** | Validaciones (H4), Ideales (H5), Registro (H6) |
| **Semana 2-3** | Menú (H7), Reportes (H8), Documentación (H9) |
| **Semana 3** | Testing, integración, ensayo de presentación |

---

## 14. NOTAS IMPORTANTES

- 📝 Las decisiones de diseño deben documentarse en el README
- 🔄 Los commits deben ser pequeños y descriptivos
- 👥 Todos deben tocar código, interfaz y documentación
- ✅ Las funciones lambda deben usarse en cálculos de promedios
- 🎯 El sistema debe ser comprensible y usable sin instrucciones previas

