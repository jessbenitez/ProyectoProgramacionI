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
- Permita consultar y analizar datos históricos de forma sencilla

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

### 3.3 Detección y Alertas
6. **Detectar condiciones destacables:**
   - Sectores con humedad crítica (<20% o >80%)
   - Sectores con humedad ideal (40-60%)
   - Sectores con máximo y mínimo de humedad

### 3.4 Reportes
7. **Generar resumen general** del procesamiento con:
   - Indicadores globales
   - Ranking de sectores
   - Estado de cada sector (crítico, ideal, normal)

### 3.5 Interacción
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
- **Cantidad de mediciones:** 7 días (puede ampliarse)
- **Rango de valores:** 0 a 100 (porcentaje de humedad)
- **Límite crítico bajo:** 20% (configurable)
- **Límite crítico alto:** 80% (configurable)
- **Rango ideal:** 40-60% (configurable)

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

### 6.1 Consulta de Datos
- `getValuesPerSector(sectores, id_sector)` → Lista de valores
- `orderHumidityValues(valores)` → Lista ordenada (mayor a menor)

### 6.2 Indicadores Globales
- `getMaxHumidityValue(sectores, sector_id=None)` → float (máximo)
- `getMinHumidityValue(sectores)` → float (mínimo)
- `getTrendingHumidityPerSector(sectores)` → list (promedios por sector)
- `getTotalTrendingHumidity(sectores)` → float (promedio global)

### 6.3 Detección de Condiciones
- `getCriticalValues(sectores, limite_bajo=20, limite_alto=80)` → tuple (sectores críticos)
- `getIdealValues(sectores, humedad_ideal=50, tolerancia=10)` → tuple (sectores ideales)

### 6.4 Registro de Datos
- `registrar_medicion(sectores, id_sector, humedad)` → bool
- `validar_rango_humedad(valor)` → bool
- `validar_sector(id_sector, total_sectores)` → bool

### 6.5 Reportes
- `generar_reporte_final(sectores, nombres_sectores)` → str (reporte formateado)

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

### 10.3 Librerías
- Estándar de Python (sin dependencias externas en Etapa 1)
- `random` para generación de datos de prueba
- `os` para limpiar pantalla (opcional)

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

