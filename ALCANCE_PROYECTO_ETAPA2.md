# DOCUMENTO DE ALCANCE DEL PROYECTO
## Proyecto Integrador - Etapa 2: Evolución, Persistencia y Pruebas
### Sistema de Monitoreo de Humedad en Cultivos

**Asignatura:** Programación I / Algoritmos y Estructuras I  
**Nombre del grupo:** Error 404  
**Participantes:**
- Nicole Quilmore
- Jesica Benitez
- Priscila Challa

**Comisión:** 584514  
**Cuatrimestre:** 2C 2026  
**Etapa:** 2 - Sistema persistente, verificable y mejor organizado  
**Versión:** 1.0  
**Documento base:** `ALCANCE_PROYECTO.md` (Etapa 1) y `ProyectoLineamientosEtapa2.pdf`

---

## 1. SENTIDO DE LA SEGUNDA ITERACIÓN

La Etapa 1 entregó un prototipo que vive **solo en memoria**: cada vez que se cierra el programa se pierden las mediciones y la matriz inicial se regenera de forma aleatoria. La Etapa 2 transforma ese prototipo en un sistema que:

- **Conserva** la información entre ejecuciones (CSV).
- **Trabaja con datos históricos** (varias semanas, no solo una).
- **Se configura sin tocar el código** (JSON).
- **Controla el acceso** mediante login de usuarios.
- **Verifica automáticamente** su funcionamiento (pruebas unitarias).

**Principio de continuidad:** se mantiene el mismo problema (monitoreo de humedad de 5 sectores de frutas), las mismas reglas de dominio (crítico <20% o >80%, ideal 40-60%) y se reutilizan las funciones válidas de la Etapa 1. Cada vez que una estructura sea reemplazada, este documento y el README explican qué limitación resolvió el cambio.

---

## 2. DIAGNÓSTICO DE LA ETAPA 1 (PUNTO DE PARTIDA)

| Aspecto en Etapa 1 | Limitación | Solución en Etapa 2 |
|--------------------|-----------|---------------------|
| Matriz 5×7 (`-1` = sin medición) | Solo cubre una semana; el centinela `-1` obliga a filtrar en cada cálculo; la posición (fila/columna) carga el significado | Lista de **diccionarios de registro** leídos desde CSV, con campos por nombre |
| Datos iniciales aleatorios (`random`) | Cada ejecución arranca distinto; nada se conserva | **Carga desde `registros.csv`** al iniciar y escritura al registrar |
| Constantes en `datos.py` (sectores, días, límites) | Cambiar un límite exige editar código; son variables a nivel de módulo | **`configuracion.json`** leído a un diccionario que se pasa por parámetro |
| Validaciones con `isnumeric()` y `range()` | Formatos acotados; `validar_humedad` acepta `-1` por el `range(-1, 101)`; no valida estructura de códigos ni fechas | **Expresiones regulares** + verificación contra configuración + **excepciones** |
| Validaciones devuelven `True/False` | El llamador debe interpretar el booleano y no sabe *por qué* falló | Funciones que **lanzan excepciones** con mensaje del formato esperado |
| Una medición cargada no se podía corregir (`registrar_medicion` rechazaba pisar una celda) | Un error de tipeo quedaba grabado para siempre | **Modificación de mediciones** con confirmación del usuario y persistencia en el CSV |
| Sin control de acceso | Cualquiera usa el sistema | **Login** contra `usuarios.json` |
| Sin pruebas | No hay verificación automatizada | **`tests/test_*.py`** con pytest, un archivo por módulo de funciones |
| Reporte solo por pantalla | No queda evidencia | **`reporte.txt`** / `alertas.txt` generados |

---

## 3. CONTENIDOS A INCORPORAR

| Contenido | Obligatorio | Aplicación en el proyecto |
|-----------|:-----------:|---------------------------|
| Expresiones regulares | ✅ | Validar fecha, código de sector, usuario y humedad (ver sección 7) |
| Diccionarios | ✅ | Registro, acumulador por sector/fecha y configuración (reemplazan matriz y listas) |
| Archivos CSV | ✅ | Persistencia del historial de mediciones (`registros.csv`) |
| Excepciones | ✅ | Archivos inexistentes, formatos inválidos, errores de lectura/escritura |
| Pruebas unitarias | ✅ | pytest, mínimo 7 pruebas, un archivo de pruebas por módulo |
| Login de usuario y contraseña | ✅ | Validación contra `usuarios.json` |
| Archivos JSON | Optativo (se implementa) | `configuracion.json` y `usuarios.json` |
| Archivos de texto | Opcional (se implementa) | `reporte.txt` con alertas e incidencias |
| Conjuntos | Optativo (se implementa) | Sectores y fechas únicos con medición |
| Recursividad | Optativo (**no se implementa**, ver sección 10) | — |

---

## 4. ALCANCE FUNCIONAL

### 4.1 Funcionalidades nuevas

1. **Login:** al iniciar, solicitar usuario y contraseña y validarlos contra `usuarios.json`. Máximo 3 intentos; luego el programa termina.
2. **Carga de configuración** desde `configuracion.json` (sectores, límites críticos e ideales, archivos). Si falta o es inválido **no se reemplaza silenciosamente**: se informa el error y el programa no continúa.
3. **Carga del historial** desde `registros.csv` al iniciar. Si el archivo no existe se crea con encabezado. Las filas incorrectas se informan (número de línea y motivo) sin perder las válidas.
4. **Registro de mediciones** con fecha, sector y humedad, persistido en el CSV (modo *append*, mismo separador, encabezado y orden de campos). Si ya existe una medición para ese sector y fecha, no se pisa: se informa y se sugiere usar la opción de modificar.
5. **Modificación de mediciones ya cargadas:** el usuario indica sector y fecha, el sistema muestra el valor actual, pide el nuevo valor (validado igual que en el registro) y solicita **confirmación** antes de reemplazarlo. El cambio se persiste en el CSV. Solo pueden modificarse mediciones dentro de la ventana de 28 días.
6. **Consulta con filtros** por sector, por fecha y por rango de fechas.
7. **Reportes:** filtrado, general, de alertas y resumen de únicos (ver sección 8).
8. **Detección de condiciones críticas** sobre el historial completo, con generación de `reporte.txt`.

### 4.2 Funcionalidades de la Etapa 1 que se conservan

Se mantienen, adaptadas a la nueva estructura de datos: máximo, mínimo, promedio por sector, promedio total, sectores críticos, sectores ideales, ordenamiento con `lambda`, comprensiones de listas/diccionarios y el menú repetitivo.

---

## 5. MODELO DE DATOS

### 5.1 Registro de medición (diccionario)

Cada fila del CSV se transforma en un diccionario con campos por nombre. Los tres valores del registro son homogéneos por campo (no hay listas ni matrices heterogéneas).

```python
{"fecha": "2026-10-12", "sector": "S01", "humedad": 45.5}
```

### 5.2 Diccionarios acumuladores

```python
# Humedades agrupadas por sector (clave = código de sector)
{"S01": [45.5, 52.0], "S02": [79.0], "S03": []}

# Promedio por fecha (clave = fecha ISO)
{"2026-10-12": 58.3, "2026-10-13": 61.0}
```

### 5.3 Diccionario de configuración

Cargado desde `configuracion.json`:

```json
{
  "sectores": {
    "S01": "Frutillas",
    "S02": "Frambuesas",
    "S03": "Arándanos",
    "S04": "Moras",
    "S05": "Cerezas"
  },
  "limites": {
    "critico_bajo": 20,
    "ideal_bajo": 40,
    "ideal_alto": 60,
    "critico_alto": 80
  },
  "ventana_dias": 28,
  "archivos": {
    "registros": "datos/registros.csv",
    "usuarios": "datos/usuarios.json",
    "reporte": "salida/reporte.txt"
  }
}
```

### 5.4 Conjuntos

```python
sectores_con_medicion = {r["sector"] for r in registros}   # sectores distintos con datos
fechas_con_medicion   = {r["fecha"] for r in registros}    # días distintos con datos
sectores_sin_medicion = set(config["sectores"]) - sectores_con_medicion
```

### 5.5 Qué reemplaza a qué

| Etapa 1 | Etapa 2 |
|---------|---------|
| Matriz `sectores[5][7]` | Lista de diccionarios de registro (`fecha`, `sector`, `humedad`) |
| Centinela `-1` | Ausencia de registro (no existe la fila) |
| Tupla `NOMBRE_SECTORES` y constantes de límites | Diccionario de configuración (JSON) |
| ID de sector 1-5 | Código `S01`-`S05`, validado por regex y contra la configuración |
| Día 0-6 | Fecha real `AAAA-MM-DD`, validada con `datetime` |

> **Decisión de diseño: ventana de 4 semanas.** Al pasar a fechas reales, el límite deja de ser "una semana de 7 días" y pasa a ser una **ventana móvil de 4 semanas (28 días) hacia atrás desde la fecha actual**, equivalente a un mes de historial. El valor se define en `configuracion.json` (`ventana_dias: 28`) y no en el código.
> - **Registro:** solo se aceptan fechas dentro de la ventana (entre hoy menos 27 días y hoy). No se permiten fechas futuras ni anteriores a la ventana.
> - **Consultas, indicadores y reportes:** operan solo sobre los registros dentro de la ventana.
> - **CSV:** las filas más antiguas que la ventana **no se borran** del archivo; simplemente quedan fuera de los cálculos. Así no se pierde información histórica.

**Se debe validar que los datos que se carguen pertenezcan a esta ventana, tanto si son cargados por el usuario o por el csv**

---

## 6. ARCHIVOS DEL SISTEMA

| Archivo | Formato | Propósito | Se crea si falta |
|---------|---------|-----------|:----------------:|
| `datos/configuracion.json` | JSON | Sectores, límites y rutas | ❌ Obligatorio, error si falta o es inválido |
| `datos/usuarios.json` | JSON | Usuarios y contraseñas para el login | ❌ Obligatorio |
| `datos/registros.csv` | CSV (`fecha,sector,humedad`) | Historial de mediciones | ✅ Con encabezado |
| `salida/reporte.txt` | Texto | Alertas, resumen e incidencias legibles | ✅ Se sobrescribe en cada generación |
| `tests/test_*.py` | Python | Pruebas automatizadas | — |

**Reglas de persistencia:**
- Todos los archivos se abren indicando `encoding="utf-8"` y el modo adecuado (`r`, `a`, `w`), con `newline=""` en CSV.
- La escritura respeta siempre el mismo separador (`,`), encabezado y orden de campos.
- **Registrar** agrega una fila al final (modo `a`). **Modificar** obliga a reescribir el archivo (modo `w`), porque CSV no permite editar una fila en el lugar: se leen **todas** las filas del archivo, se reemplaza la humedad de la fila que coincide en sector y fecha, y se escribe todo de nuevo con el mismo encabezado y orden. Las filas anteriores a la ventana y las filas inválidas **se conservan tal cual** (nunca se pierde información por modificar otra fila). 
De ser posible de implementar: Para no corromper el archivo si falla la escritura, se escribe primero en un archivo temporal y luego se reemplaza el original.
- Los registros inválidos dentro del CSV se reportan (línea y motivo) sin descartar los válidos.
- **Contraseñas:** se propone guardarlas como hash (`hashlib.sha256`) en `usuarios.json` en lugar de texto plano. Si el equipo prefiere simplicidad, se documenta como limitación.

Ejemplo de `usuarios.json`:

```json
{
  "usuarios": {
    "nicole": "<hash>",
    "jesica": "<hash>",
    "priscila": "<hash>"
  }
}
```

---

## 7. EXPRESIONES REGULARES Y VALIDACIONES

La regex valida **estructura**; después se verifica coherencia (pertenencia a la configuración, fecha real, rango numérico).

| Dato | Expresión regular | Verificación posterior |
|------|-------------------|------------------------|
| Fecha | `^\d{4}-\d{2}-\d{2}$` | Fecha real con `datetime.strptime` (rechaza `2026-02-30`) y dentro de la ventana de 28 días (no futura) |
| Código de sector | `^S\d{2}$` | Existe en `config["sectores"]` |
| Humedad | `^\d{1,3}(\.\d{1,2})?$` | Conversión a `float` y rango 0-100 |
| Usuario (login) | `^[a-z0-9_]{3,20}$` | Existe en `usuarios.json` |

**Mensajes de error:** siempre indican el formato esperado, por ejemplo `Fecha inválida: se esperaba AAAA-MM-DD (ej: 2026-10-12)`.

**Corrección heredada:** `validar_humedad` deja de aceptar `-1` (el centinela desaparece con el nuevo modelo).

---

## 8. REPORTES

| Reporte | Contenido mínimo | Salida |
|---------|------------------|--------|
| **Filtrado** | Mediciones de una fecha, un sector o un rango, con promedio del filtro | Pantalla y `reporte.txt` |
| **General** | Máximo, mínimo, promedio total, promedio por sector y por fecha sobre todo el historial | Pantalla y `reporte.txt` |
| **Alertas** | Mediciones y sectores críticos (<20% o >80%) con fecha y valor | `reporte.txt` |
| **Resumen de únicos** | Cantidad y listado de sectores y fechas con medición, y sectores sin medición (conjuntos) | Pantalla y `reporte.txt` |

---

## 9. MANEJO DE EXCEPCIONES

**Principio:** las funciones de validación y acceso a archivos **lanzan** excepciones; quien interactúa con el usuario (`main.py`) las **captura** y muestra el mensaje. Esto reemplaza el patrón de Etapa 1 (`True/False` y tuplas de resultado).

| Situación | Excepción | Tratamiento |
|-----------|-----------|-------------|
| `configuracion.json` ausente | `FileNotFoundError` | Mensaje claro y fin del programa |
| JSON mal formado o claves faltantes | `json.JSONDecodeError` / `KeyError` | Mensaje y fin del programa |
| `registros.csv` ausente | `FileNotFoundError` | Se crea con encabezado y se continúa |
| Fila de CSV inválida | `ValueError` (propia o estándar) | Se informa línea y motivo, se omite la fila |
| Error de lectura/escritura | `OSError` / `PermissionError` | Mensaje y vuelta al menú |
| Formato de dato inválido | `ValueError` con formato esperado | Reintento sin cerrar el programa |
| Login fallido | Excepción propia o `ValueError` | Reintento, máximo 3 |
| Medición duplicada al registrar (mismo sector y fecha) | `ValueError` | Mensaje que sugiere usar "Modificar medición" y vuelta al menú |
| Modificar una medición inexistente (sector y fecha sin registro) | `ValueError` | Mensaje y vuelta al menú |
| Falla al reescribir el CSV al modificar | `OSError` | Mensaje; el archivo original queda intacto (escritura vía temporal) |
| Fecha fuera de la ventana de 28 días | `ValueError` con el rango permitido | Reintento sin cerrar el programa |

> **Regla de unicidad (decisión nueva):** un sector admite **una medición por fecha**. A diferencia de la Etapa 1, donde una celda cargada era definitiva, ahora la medición existente puede corregirse, pero **solo mediante la opción explícita de modificar** y con confirmación. Registrar nunca pisa un valor en silencio.

---

## 10. RECURSIVIDAD (NO INCLUIDA)

La recursividad es un contenido **optativo** en los lineamientos y el equipo decide **no implementarla** en esta etapa. Ninguna operación del sistema (promedios, filtros, agrupaciones, recorridos de registros) se beneficia de forzar una solución recursiva, y los lineamientos advierten que no debe reemplazar artificialmente los ciclos. Se asume la pérdida del 5% de la rúbrica correspondiente.

---

## 11. ARQUITECTURA

Separación clara entre interacción, lógica del dominio, validaciones, acceso a archivos y pruebas. **No se usan variables globales:** todo lo que una función necesita (configuración, registros) se pasa por parámetro.

```
proyecto_etapa2/
├── main.py                  # Login, menú y control de flujo (único módulo con input/print)
├── validaciones.py          # Regex y validaciones; lanzan excepciones
├── operaciones.py           # Cálculos, filtros, acumuladores, detección crítica
├── reportes.py              # Armado de reportes como strings y generación de reporte.txt
├── archivos.py              # Lectura/escritura de CSV, JSON y texto; manejo de errores de E/S
├── autenticacion.py         # Login contra usuarios.json
├── perfil_equipo.py         # Se conserva de Etapa 1
├── datos/
│   ├── configuracion.json
│   ├── usuarios.json
│   └── registros.csv        # Datos de demostración
├── salida/
│   └── reporte.txt
├── tests/
│   ├── test_validaciones.py
│   ├── test_operaciones.py
│   ├── test_reportes.py
│   ├── test_archivos.py
│   └── test_autenticacion.py
└── README.md
```

**Cambios respecto de la estructura de Etapa 1:**
- `datos.py` desaparece: sus constantes pasan a `configuracion.json` y la carga inicial a `archivos.py`.
- Se separan `validaciones.py` y `reportes.py` de `operaciones.py`, que concentraba demasiadas responsabilidades.
- Se agregan `archivos.py` y `autenticacion.py`.

---

## 12. FUNCIONES: QUÉ SE REUTILIZA, ADAPTA Y AGREGA

### 12.1 Se adaptan (misma intención, nueva estructura)

| Función Etapa 1 | Cambio |
|-----------------|--------|
| `getMaxHumidityValue`, `getMinHumidityValue` | Reciben lista de registros; ya no filtran `-1` |
| `getAverageHumidityPerSector`, `getAverageHumidityTotal` | Devuelven diccionario por sector / promedio sobre registros |
| `getValuesPerSector` | Filtra registros por código de sector |
| `orderHumidityValues` | Se mantiene `lambda`, ahora ordena registros por `humedad` |
| `getCriticalValues`, `getIdealValues` | Reciben límites desde configuración; se mantienen las comprensiones. Pendiente de la devolución de Etapa 1: revisar su lógica |
| `registrar_medicion` | Valida, agrega el registro y lo persiste en CSV; lanza excepción ante duplicado (ya no devuelve tupla de resultado) |
| `validar_sector`, `validar_dia`, `validar_humedad` | Pasan a `validaciones.py`, usan regex y lanzan excepciones; `validar_dia` se reemplaza por `validar_fecha` |
| `generar_reporte_final` | Se divide en los cuatro reportes de la sección 8 |

### 12.2 Funciones nuevas

| Módulo | Funciones |
|--------|-----------|
| `archivos.py` | `cargar_configuracion`, `cargar_registros`, `guardar_registro`, `actualizar_registro` (reescribe el CSV conservando el resto de las filas), `guardar_reporte` |
| `autenticacion.py` | `cargar_usuarios`, `validar_credenciales` |
| `operaciones.py` | `buscar_medicion` (devuelve el registro de un sector y fecha, o lanza excepción), `modificar_medicion`, `agrupar_por_sector`, `agrupar_por_fecha`, `filtrar_registros`, `obtener_sectores_unicos`, `obtener_fechas_unicas` |
| `validaciones.py` | `validar_fecha`, `validar_codigo_sector`, `validar_humedad`, `validar_usuario` |
| `reportes.py` | `reporte_filtrado`, `reporte_general`, `reporte_alertas`, `reporte_unicos` |

---

## 13. PRUEBAS UNITARIAS

- Herramienta: **pytest** (`pytest` desde la raíz del proyecto).
- Un archivo `test_*.py` por cada módulo de funciones.
- Las pruebas **no usan `input()` ni dependen de lo impreso en pantalla**; los archivos se prueban con `tmp_path` de pytest.
- Mínimo **7 pruebas**, de las cuales se cubren obligatoriamente:

| # | Caso requerido | Prueba propuesta |
|---|----------------|------------------|
| 1 | Validación correcta | `validar_fecha("2026-10-12")` no lanza excepción |
| 2 | Validación incorrecta con excepción | `validar_fecha("2026-02-30")` lanza `ValueError` |
| 3 | Cálculo simple con resultado conocido | Promedio de `[40, 60]` = `50.0` |
| 4 | Acumulación o agrupación por clave | `agrupar_por_sector` devuelve el diccionario esperado |
| 5 | Detección de condición crítica | Humedad `15` y `85` detectadas como críticas |
| 6 | Regla del negocio con persistencia | `modificar_medicion` cambia solo la fila indicada y rechaza una medición inexistente |
| 7 | Caso límite | Lista vacía, humedad exactamente igual a `20`, `40`, `60`, `80`, y fecha exactamente en el borde de la ventana (hoy y hoy menos 27 días aceptadas; hoy menos 28 días rechazada) |

Pruebas adicionales previstas: CSV inexistente, fila inválida omitida, login válido e inválido, `configuracion.json` inválido, y para la modificación: modificar una medición existente cambia solo esa fila en el CSV, modificar una inexistente lanza excepción, registrar un duplicado lanza excepción, y modificar conserva las filas anteriores a la ventana.

---

## 14. MENÚ PRINCIPAL

```
=== SISTEMA DE MONITOREO DE HUMEDAD EN CULTIVOS ===
Usuario: nicole

1. Registrar nueva medición
2. Modificar medición existente
3. Consultar mediciones (filtrar por sector / fecha / rango)
4. Ver indicadores generales
5. Ver sectores críticos
6. Ver sectores ideales
7. Reporte filtrado
8. Reporte general
9. Reporte de alertas (genera reporte.txt)
10. Resumen de únicos
fin. Salir
```

Flujo de "Modificar medición existente":

```
Sector (ej: S01): S01
Fecha (AAAA-MM-DD): 2026-10-12
Medición actual: Frutillas, 2026-10-12 -> 45.5%
Nuevo valor de humedad (0-100): 52
¿Reemplazar 45.5% por 52.0%? (s/n): s
Medición modificada correctamente.
```

---

## 15. DATOS DE DEMOSTRACIÓN

`registros.csv` incluirá datos suficientes para probar filtros, reportes y alertas:
- Fechas distribuidas en las **4 semanas** de la ventana. Como la ventana es móvil, el equipo prepara una forma de regenerar el CSV de demostración con fechas relativas a la fecha de ejecución (o usa una fecha de referencia inyectable por parámetro en las pruebas).
- Al menos **un registro anterior a la ventana**, para demostrar que se conserva en el archivo pero queda fuera de los reportes.
- Los **5 sectores** con distinta cantidad de mediciones, y al menos **un sector sin ninguna** (para el resumen de únicos).
- Valores críticos bajos, críticos altos, ideales y **valores límite** (20, 40, 60, 80).
- Al menos **una fila inválida** en una copia aparte (`registros_con_errores.csv`) para demostrar el manejo de errores sin perder las filas válidas.

---

## 16. CRITERIOS DE ACEPTACIÓN

Alineados con la lista de control y la rúbrica de los lineamientos.

| # | Criterio | Rúbrica |
|---|----------|---------|
| 1 | El sistema recupera la información de ejecuciones anteriores | CSV (20%) |
| 2 | La configuración se lee desde JSON y no se reemplaza silenciosamente | CSV/JSON/texto (20%) |
| 3 | Los registros se leen y escriben en CSV con formato constante | CSV/JSON/texto (20%) |
| 4 | Se genera al menos un archivo de texto | CSV/JSON/texto (20%) |
| 4b | Se puede modificar una medición ya cargada, con confirmación, y el cambio persiste en el CSV sin perder otras filas | CSV/JSON/texto (20%) |
| 5 | Diccionarios (registro, acumulador, configuración) y conjuntos usados de forma visible y justificada | Diccionarios y conjuntos (15%) |
| 6 | Al menos dos validaciones con regex y mensajes que explican el formato esperado | Regex (10%) |
| 7 | Errores de archivos y formatos controlados con excepciones | Excepciones (10%) |
| 8 | Reportes filtrado, general y de alertas funcionando | Reportes (15%) |
| 10 | `pytest` ejecuta correctamente (mínimo 7 pruebas) | Pruebas (10%) |
| 11 | Login funcional contra `usuarios.json` | Obligatorio |
| 12 | Sin variables globales y sin listas/matrices heterogéneas | Restricción de rúbrica |
| 13 | La documentación explica los cambios respecto de la Etapa 1 | Evolución (10%) |
| 14 | Commits progresivos de todos los integrantes; README actualizado | Documentación (5%) |
| 15 | Todos los integrantes pueden defender las decisiones técnicas | Control final |

---

## 17. PLAN DE TRABAJO (HISTORIAS)

| Historia | Descripción | Responsable | Depende de |
|----------|-------------|-------------|-----------|
| **H1** | Reestructurar proyecto: nuevas carpetas y módulos, `configuracion.json`, `archivos.py` (config, carga y guardado de CSV), datos de demostración | Nicole | — |
| **H2** | `validaciones.py` con regex y excepciones; adaptar `registrar_medicion` con persistencia; implementar modificación de mediciones (`buscar_medicion`, `modificar_medicion`, `actualizar_registro`); migrar las validaciones de Etapa 1; `test_validaciones.py` y `test_archivos.py` | Nicole | H1 |
| **H3** | Login: `autenticacion.py`, `usuarios.json`, límite de intentos; `test_autenticacion.py` | Nicole | H1 |
| **H4** | Adaptar consultas y alertas a diccionarios: `getValuesPerSector`, `orderHumidityValues`, `getCriticalValues`, `getIdealValues`, `filtrar_registros`; conjuntos de únicos; `test_operaciones.py` (parte consultas) | Jesica | H1 |
| **H5** | Adaptar indicadores a diccionarios: máximo, mínimo, promedios, `agrupar_por_sector`, `agrupar_por_fecha`; `test_operaciones.py` (parte indicadores) | Priscila | H1 |
| **H6** | `reportes.py` (filtrado, general, alertas, únicos) y generación de `reporte.txt`; `test_reportes.py` | Priscila | H4, H5 |
| **H7** | Integración en `main.py`: login, menú nuevo y manejo de excepciones | Todas | H2-H6 |
| **H8** | README actualizado, documento de evolución y evidencia de resultados de `pytest` | Todas | H7 |

**Requisito:** cada integrante toca código, pruebas y documentación; commits pequeños y descriptivos (mínimo 6 por persona).

---

## 18. ENTREGABLES

| Entregable | Contenido |
|-----------|-----------|
| Repositorio final | Código integrado, archivos de datos, carpeta `tests/` y commits progresivos |
| Documento de evolución | Este documento + README: cambios respecto de la Etapa 1, decisiones y refactorizaciones |
| Datos de demostración | `registros.csv` con registros suficientes (sección 15) |
| Resultados de pruebas | Captura de `pytest` y explicación de los casos cubiertos |
| Archivos `.py` | Todos los archivos del proyecto (entrega por Teams) |

---

## 19. TECNOLOGÍA

- **Python** 3.8 o superior
- **Librería estándar:** `csv`, `json`, `re`, `datetime`, `hashlib`
- **Herramienta de pruebas:** `pytest` (única dependencia externa; `pip install pytest`)
- **Git/GitHub** para control de versiones

---

## 20. RIESGOS Y PUNTOS A DEFINIR

| Punto | Propuesta |
|-------|-----------|
| ¿Mantener la semana de 7 días o pasar a fechas libres? | Resuelto: fechas reales con ventana de 4 semanas (28 días), configurable en JSON |
| La ventana depende de la fecha actual, lo que complica las pruebas | `validar_fecha` y los filtros reciben la fecha de referencia como parámetro (sin variables globales ni `date.today()` escondido), así las pruebas son deterministas |
| ¿Contraseñas en texto plano o con hash? | A definir |
| ¿Qué ocurre si el CSV tiene dos mediciones para el mismo sector y fecha? | Se informa como fila inválida y se conserva la primera |
| Modificar exige reescribir todo el CSV, con riesgo de perder filas si falla la escritura | Escritura en archivo temporal + reemplazo, y conservación de filas fuera de la ventana e inválidas (ver sección 6) |
| ¿Se registra quién y cuándo modificó una medición? | Fuera de alcance por ahora; se puede evaluar una bitácora en `reporte.txt` si sobra tiempo |
| Pendientes de la devolución de Etapa 1 en `getCriticalValues` y `getIdealValues` | Resolver en H4 junto con su adaptación |
| `README.md` actual tiene comandos de Git pegados al final | Limpiar al actualizarlo en H8 |
