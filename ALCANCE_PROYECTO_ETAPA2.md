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
| Datos iniciales aleatorios (`random`) | Cada ejecución arranca distinto; nada se conserva | **Carga desde `registros.csv`** al iniciar y reescritura del archivo al cerrar el programa |
| Constantes en `datos.py` (sectores, días, límites) | Cambiar un límite exige editar código; son variables a nivel de módulo | **`configuracion.json`** leído a un diccionario que se pasa por parámetro |
| Validaciones con `isnumeric()` y `range()` | Formatos acotados; `validar_humedad` acepta `-1` por el `range(-1, 101)`; no valida estructura de códigos ni fechas | **Expresiones regulares** + verificación contra configuración + **excepciones** |
| Validaciones devuelven `True/False` | El llamador debe interpretar el booleano y no sabe *por qué* falló | Funciones que **lanzan excepciones** con mensaje del formato esperado |
| Una medición cargada no se podía corregir (`registrar_medicion` rechazaba pisar una celda) | Un error de tipeo quedaba grabado para siempre | **Modificación de mediciones** con confirmación del usuario; el cambio se persiste en el CSV al cerrar el programa |
| Sin control de acceso | Cualquiera usa el sistema | **Login** contra `usuarios.json` |
| Sin pruebas | No hay verificación automatizada | **`tests/test_*.py`** con pytest, un archivo por módulo de funciones |
| Reporte solo por pantalla | No queda evidencia | **Reportes en archivos de texto**, modularizados: uno por sector y uno general |

---

## 3. CONTENIDOS A INCORPORAR

| Contenido | Obligatorio | Aplicación en el proyecto |
|-----------|:-----------:|---------------------------|
| Expresiones regulares | ✅ | Validar fecha, código de sector, usuario y humedad (ver sección 7) |
| Diccionarios | ✅ | Estructura principal en memoria (sector → fecha → humedad), acumuladores y configuración (reemplazan matriz y listas) |
| Archivos CSV | ✅ | Persistencia del historial de mediciones (`registros.csv`) |
| Excepciones | ✅ | Archivos inexistentes, formatos inválidos, errores de lectura/escritura |
| Pruebas unitarias | ✅ | pytest, mínimo 7 pruebas, un archivo de pruebas por módulo |
| Login de usuario y contraseña | ✅ | Validación contra `usuarios.json` |
| Archivos JSON | Optativo (se implementa) | `configuracion.json` y `usuarios.json` |
| Archivos de texto | Opcional (se implementa) | Reportes en `salida/reportes/` (un archivo por sector y uno general) con alertas e incidencias |
| Conjuntos | Optativo (**no se implementa**) | — |
| Recursividad | Optativo (**no se implementa**, ver sección 10) | — |

---

## 4. ALCANCE FUNCIONAL

### 4.1 Funcionalidades nuevas

1. **Login:** al iniciar, solicitar usuario y contraseña y validarlos contra `usuarios.json`. Máximo 3 intentos; luego el programa termina.
2. **Carga de configuración** desde `configuracion.json` (sectores, límites críticos e ideales, archivos). Si falta o es inválido **no se reemplaza silenciosamente**: se informa el error y el programa no continúa.
3. **Carga del historial (una sola vez, al iniciar):** se lee `registros.csv` y se guarda en un **diccionario en memoria**. Cada fila se valida (formato, sector existente, fecha real y dentro de la ventana de 28 días, humedad en rango). Las filas incorrectas, duplicadas o fuera de la ventana se informan (número de línea y motivo) y **no se incorporan** al diccionario. Si el archivo no existe, se informa y se arranca con un historial vacío.
4. **Registro de mediciones** con fecha, sector y humedad: se agrega al diccionario en memoria (no escribe el CSV en ese momento). Si ya existe una medición para ese sector y fecha, no se pisa: se informa y se sugiere usar la opción de modificar.
5. **Modificación de mediciones ya cargadas:** el usuario indica sector y fecha, el sistema muestra el valor actual, pide el nuevo valor (validado igual que en el registro) y solicita **confirmación** antes de reemplazarlo en el diccionario en memoria. Solo pueden modificarse mediciones dentro de la ventana de 28 días.
6. **Guardado al salir:** al finalizar la ejecución (opción `fin`), el contenido completo del diccionario **sobrescribe** `registros.csv`, de modo que los registros y modificaciones de la sesión persistan. Durante la ejecución todas las acciones (registrar, modificar, consultar, calcular) trabajan sobre el diccionario.
7. **Consulta con filtros** por sector, por fecha y por rango de fechas.
8. **Reportes:** filtrado, general y de alertas (ver sección 8).
9. **Detección de condiciones críticas** sobre el historial completo, con generación de los archivos de reporte (uno por sector y uno general).

### 4.2 Funcionalidades de la Etapa 1 que se conservan

Se mantienen, adaptadas a la nueva estructura de datos: máximo, mínimo, promedio por sector, promedio total, sectores críticos, sectores ideales, ordenamiento con `lambda`, comprensiones de listas/diccionarios y el menú repetitivo.

---

## 5. MODELO DE DATOS

### 5.1 Diccionario principal de mediciones (en memoria)

Al iniciar, el CSV se carga en un diccionario anidado: **sector → fecha → humedad**. Es la única fuente de datos durante la ejecución y es lo que se vuelca al CSV al salir.

```python
mediciones = {
    "S01": {"2026-10-12": 45.5, "2026-10-13": 52.0},
    "S02": {"2026-10-12": 79.0},
    "S03": {},
}
```

- Cada fila del CSV (`fecha,sector,humedad`) se transforma en una entrada `mediciones[sector][fecha] = humedad`.
- La unicidad (una medición por sector y fecha) queda garantizada por la propia estructura: no pueden existir dos claves iguales.
- Registrar es agregar una clave; modificar es reemplazar el valor de una clave existente; consultar por sector es un acceso directo.
- Los valores son homogéneos (todas las claves interiores son fechas y todos los valores son números), sin listas ni matrices heterogéneas.

### 5.2 Diccionarios acumuladores

Se calculan a partir del diccionario principal:

```python
# Promedio por sector (clave = código de sector)
{"S01": 48.75, "S02": 79.0}

# Promedio por fecha (clave = fecha ISO); resulta de reagrupar el diccionario principal
{"2026-10-12": 62.25, "2026-10-13": 52.0}
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
    "carpeta_reportes": "salida/reportes"
  }
}
```

### 5.4 Qué reemplaza a qué

| Etapa 1 | Etapa 2 |
|---------|---------|
| Matriz `sectores[5][7]` | Diccionario anidado en memoria `mediciones[sector][fecha] = humedad`, cargado desde CSV |
| Centinela `-1` | Ausencia de registro (no existe la fila) |
| Tupla `NOMBRE_SECTORES` y constantes de límites | Diccionario de configuración (JSON) |
| ID de sector 1-5 | Código `S01`-`S05`, validado por regex y contra la configuración |
| Día 0-6 | Fecha real `AAAA-MM-DD`, validada con `datetime` |

> **Decisión de diseño: ventana de 4 semanas.** Al pasar a fechas reales, el límite deja de ser "una semana de 7 días" y pasa a ser una **ventana móvil de 4 semanas (28 días) hacia atrás desde la fecha actual**, equivalente a un mes de historial. El valor se define en `configuracion.json` (`ventana_dias: 28`) y no en el código.
> - **Registro:** solo se aceptan fechas dentro de la ventana (entre hoy menos 27 días y hoy). No se permiten fechas futuras ni anteriores a la ventana.
> - **Consultas, indicadores y reportes:** operan solo sobre los registros dentro de la ventana.
> - **CSV:** las filas más antiguas que la ventana se informan al cargar y **no se incorporan** al diccionario en memoria; como el archivo se sobrescribe desde el diccionario al salir, **desaparecen del CSV**. El archivo conserva, entonces, solo las últimas 4 semanas (ver riesgos en sección 20).

**Se debe validar que los datos que se carguen pertenezcan a esta ventana, tanto si son cargados por el usuario o por el csv**

---

## 6. ARCHIVOS DEL SISTEMA

| Archivo | Formato | Propósito | Se crea si falta |
|---------|---------|-----------|:----------------:|
| `datos/configuracion.json` | JSON | Sectores, límites y rutas | ❌ Obligatorio, error si falta o es inválido |
| `datos/usuarios.json` | JSON | Usuarios y contraseñas para el login | ❌ Obligatorio |
| `datos/registros.csv` | CSV (`fecha,sector,humedad`) | Historial de mediciones | ✅ Se crea al salir si no existía (con encabezado) |
| `salida/reportes/reporte_S01.txt` ... `reporte_S05.txt` | Texto | Un archivo por sector: mediciones, indicadores y alertas del sector | ✅ La carpeta y los archivos se crean si faltan; se sobrescriben en cada generación |
| `salida/reportes/reporte_general.txt` | Texto | Indicadores de todo el campo, alertas consolidadas | ✅ Ídem |
| `tests/test_*.py` | Python | Pruebas automatizadas | — |

**Reglas de persistencia:**
- Todos los archivos se abren indicando `encoding="utf-8"` y el modo adecuado (`r`, `a`, `w`), con `newline=""` en CSV.
- La escritura respeta siempre el mismo separador (`,`), encabezado y orden de campos.
- **Lectura una sola vez, escritura una sola vez:** el CSV se lee al iniciar y se sobrescribe al salir (modo `w`) con el contenido del diccionario en memoria. Registrar y modificar **no tocan el archivo** durante la ejecución.
- **Escritura directa (decisión de alcance):** el archivo se pisa directamente, sin archivo temporal ni copia de respaldo. Se acepta como limitación que una falla durante la escritura pueda dejar el archivo incompleto.
- **Orden determinista:** al guardar, las filas se escriben ordenadas por fecha y luego por sector, con el mismo encabezado y orden de campos.
- Los registros inválidos o fuera de la ventana se reportan al cargar (línea y motivo), sin descartar los válidos. Como no se incorporan a memoria, **no se reescriben** al guardar.
- **Contraseñas:** se guardan en **texto plano** en `usuarios.json` y se comparan directamente. Es una decisión de alcance del equipo; en un sistema real deberían almacenarse con hash.

Ejemplo de `usuarios.json`:

```json
{
  "usuarios": {
    "nicole": "<contraseña>",
    "jesica": "<contraseña>",
    "priscila": "<contraseña>"
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
| **Filtrado** | Mediciones de una fecha, un sector o un rango, con promedio del filtro | Pantalla |
| **General** | Máximo, mínimo, promedio total, promedio por sector y por fecha sobre todo el historial | Pantalla y `reporte_general.txt` |
| **Alertas** | Mediciones y sectores críticos (<20% o >80%) con fecha y valor | Sección de alertas de cada `reporte_<sector>.txt` y consolidado en `reporte_general.txt` |

### 8.1 Reportes en archivos de texto: uno por sector

La salida a texto no es un único archivo sino un conjunto modular dentro de `salida/reportes/`, de modo que cada sector pueda consultarse de forma independiente:

| Archivo | Contenido |
|---------|-----------|
| `reporte_S01.txt` ... `reporte_S05.txt` | Nombre del sector, período cubierto (ventana de 28 días), mediciones ordenadas por fecha, máximo, mínimo, promedio y estado (crítico / ideal / otro), y **alertas del sector** (fecha y valor de cada medición crítica) |
| `reporte_general.txt` | Indicadores de todo el campo (máximo, mínimo, promedio total), promedio por sector, **alertas consolidadas** (sectores con mediciones críticas) y los sectores sin mediciones |

Reglas:
- Se genera un archivo por **cada sector de la configuración**, incluso si no tiene mediciones (el archivo indica "Sin mediciones en el período"). Así agregar un sector al JSON crea su reporte sin cambiar código.
- Nombre de archivo basado en el **código** del sector (`S01`), no en el nombre, para evitar acentos y espacios.
- La carpeta `salida/reportes/` se crea si no existe; los archivos se sobrescriben en cada generación, y el encabezado incluye la fecha de generación.
- El contenido se arma como string en `reportes.py` (sin I/O) y `archivos.py` lo escribe, manteniendo la separación entre lógica y acceso a archivos.
- Un error al escribir un archivo (`OSError`) se informa indicando cuál falló y se continúa con los demás.

---

## 9. MANEJO DE EXCEPCIONES

**Principio:** las funciones de validación y acceso a archivos **lanzan** excepciones; quien interactúa con el usuario (`main.py`) las **captura** y muestra el mensaje. Esto reemplaza el patrón de Etapa 1 (`True/False` y tuplas de resultado).

| Situación | Excepción | Tratamiento |
|-----------|-----------|-------------|
| `configuracion.json` ausente | `FileNotFoundError` | Mensaje claro y fin del programa |
| JSON mal formado o claves faltantes | `json.JSONDecodeError` / `KeyError` | Mensaje y fin del programa |
| `registros.csv` ausente | `FileNotFoundError` | Se informa y se arranca con historial vacío; el archivo se crea al salir |
| Fila de CSV inválida, duplicada o fuera de la ventana | `ValueError` (propia o estándar) | Se informa línea y motivo, no se incorpora a memoria |
| Error de lectura/escritura | `OSError` / `PermissionError` | Mensaje y vuelta al menú |
| Formato de dato inválido | `ValueError` con formato esperado | Reintento sin cerrar el programa |
| Login fallido | Excepción propia o `ValueError` | Reintento, máximo 3 |
| Medición duplicada al registrar (mismo sector y fecha) | `ValueError` | Mensaje que sugiere usar "Modificar medición" y vuelta al menú |
| Modificar una medición inexistente (sector y fecha sin registro) | `ValueError` | Mensaje y vuelta al menú |
| Falla al guardar el CSV al salir | `OSError` / `PermissionError` | Mensaje claro; se ofrece reintentar o salir sin guardar (los datos siguen en memoria mientras no se salga) |
| Fecha fuera de la ventana de 28 días | `ValueError` con el rango permitido | Reintento sin cerrar el programa |

> **Regla de unicidad (decisión nueva):** un sector admite **una medición por fecha**. A diferencia de la Etapa 1, donde una celda cargada era definitiva, ahora la medición existente puede corregirse, pero **solo mediante la opción explícita de modificar** y con confirmación. Registrar nunca pisa un valor en silencio. Como el diccionario usa `sector → fecha` como clave, la unicidad es inherente a la estructura.

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
├── reportes.py              # Armado de reportes como strings (por sector y general)
├── archivos.py              # Lectura/escritura de CSV, JSON y texto; manejo de errores de E/S
├── autenticacion.py         # Login contra usuarios.json
├── perfil_equipo.py         # Se conserva de Etapa 1
├── datos/
│   ├── configuracion.json
│   ├── usuarios.json
│   └── registros.csv        # Datos de demostración
├── salida/
│   └── reportes/
│       ├── reporte_S01.txt     # Un archivo por sector (S01 a S05)
│       └── reporte_general.txt
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
| `getMaxHumidityValue`, `getMinHumidityValue` | Reciben el diccionario de mediciones; ya no filtran `-1` |
| `getAverageHumidityPerSector`, `getAverageHumidityTotal` | Devuelven diccionario por sector / promedio sobre todas las mediciones |
| `getValuesPerSector` | Devuelve las mediciones de un código de sector (`mediciones[sector]`) |
| `orderHumidityValues` | Se mantiene `lambda`, ahora ordena las mediciones por humedad |
| `getCriticalValues`, `getIdealValues` | Reciben límites desde configuración; se mantienen las comprensiones. Pendiente de la devolución de Etapa 1: revisar su lógica |
| `registrar_medicion` | Valida y agrega la medición al diccionario en memoria; lanza excepción ante duplicado (ya no devuelve tupla de resultado) |
| `validar_sector`, `validar_dia`, `validar_humedad` | Pasan a `validaciones.py`, usan regex y lanzan excepciones; `validar_dia` se reemplaza por `validar_fecha` |
| `generar_reporte_final` | Se divide en los cuatro reportes de la sección 8 |

### 12.2 Funciones nuevas

| Módulo | Funciones |
|--------|-----------|
| `archivos.py` | `cargar_configuracion`, `cargar_registros` (CSV → diccionario, informando filas rechazadas), `guardar_registros` (diccionario → CSV, sobrescribe el archivo), `guardar_reporte` (escribe un archivo de texto y crea la carpeta si falta) |
| `autenticacion.py` | `cargar_usuarios`, `validar_credenciales` |
| `operaciones.py` | `buscar_medicion` (devuelve la humedad de un sector y fecha, o lanza excepción), `modificar_medicion`, `agrupar_por_fecha` (reagrupa el diccionario por fecha), `filtrar_registros` (por sector, fecha o rango) |
| `validaciones.py` | `validar_fecha`, `validar_codigo_sector`, `validar_humedad`, `validar_usuario` |
| `reportes.py` | `reporte_filtrado`, `reporte_sector` (mediciones, indicadores y alertas de un sector), `reporte_general`, `reporte_alertas` |

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
| 4 | Acumulación o agrupación por clave | `agrupar_por_fecha` devuelve el diccionario esperado a partir de un diccionario de mediciones conocido |
| 5 | Detección de condición crítica | Humedad `15` y `85` detectadas como críticas |
| 6 | Regla del negocio con persistencia | `modificar_medicion` cambia solo la medición indicada y rechaza una medición inexistente |
| 7 | Caso límite | Lista vacía, humedad exactamente igual a `20`, `40`, `60`, `80`, y fecha exactamente en el borde de la ventana (hoy y hoy menos 27 días aceptadas; hoy menos 28 días rechazada) |

Pruebas adicionales previstas: `reporte_sector` incluye las alertas del sector y solo las de ese sector, un sector sin mediciones genera su reporte con la leyenda correspondiente, `guardar_reporte` crea la carpeta si falta, CSV inexistente, fila inválida omitida, login válido e inválido, `configuracion.json` inválido, y para la persistencia: guardar con `guardar_registros` y volver a leer con `cargar_registros` devuelve el mismo diccionario (ida y vuelta), una fila fuera de la ventana no se incorpora al cargar, una fila duplicada no pisa a la primera, registrar un duplicado lanza excepción y modificar una medición inexistente lanza excepción.

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
9. Generar reportes en archivos (uno por sector + general)
fin. Salir (guarda los cambios en registros.csv)
```

Flujo de "Modificar medición existente":

```
Sector (ej: S01): S01
Fecha (AAAA-MM-DD): 2026-10-12
Medición actual: Frutillas, 2026-10-12 -> 45.5%
Nuevo valor de humedad (0-100): 52
¿Reemplazar 45.5% por 52.0%? (s/n): s
Medición modificada correctamente (se guardará en el archivo al salir).
```

---

## 15. DATOS DE DEMOSTRACIÓN

`registros.csv` incluirá datos suficientes para probar filtros, reportes y alertas:
- Fechas distribuidas en las **4 semanas** de la ventana. Como la ventana es móvil, el equipo prepara una forma de regenerar el CSV de demostración con fechas relativas a la fecha de ejecución (o usa una fecha de referencia inyectable por parámetro en las pruebas).
- Al menos **un registro anterior a la ventana**, para demostrar que se informa al cargar, no entra en los cálculos y no se reescribe al guardar.
- Los **5 sectores** con distinta cantidad de mediciones, y al menos **un sector sin ninguna** (para probar el reporte de un sector sin mediciones).
- Valores críticos bajos, críticos altos, ideales y **valores límite** (20, 40, 60, 80).
- Al menos **una fila inválida** en una copia aparte (`registros_con_errores.csv`) para demostrar el manejo de errores sin perder las filas válidas (las inválidas se informan y no se reescriben al guardar). Se incluye también un caso de dos filas con el mismo sector y fecha.

---

## 16. CRITERIOS DE ACEPTACIÓN

Alineados con la lista de control y la rúbrica de los lineamientos.

| # | Criterio | Rúbrica |
|---|----------|---------|
| 1 | El sistema recupera la información de ejecuciones anteriores | CSV (20%) |
| 2 | La configuración se lee desde JSON y no se reemplaza silenciosamente | CSV/JSON/texto (20%) |
| 3 | Los registros se leen del CSV al iniciar y se escriben al salir, con formato constante | CSV/JSON/texto (20%) |
| 4 | Se genera al menos un archivo de texto | CSV/JSON/texto (20%) |
| 4b | Se puede modificar una medición ya cargada, con confirmación, y el cambio persiste en el CSV al salir | CSV/JSON/texto (20%) |
| 5 | Diccionarios (mediciones, acumuladores, configuración) usados de forma visible y justificada | Diccionarios y conjuntos (15%) |
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
| **H1** | Reestructurar proyecto: nuevas carpetas y módulos, `configuracion.json`, `archivos.py` (config, carga de CSV a diccionario y guardado del diccionario a CSV), datos de demostración | Nicole | — |
| **H2** | `validaciones.py` con regex y excepciones; adaptar `registrar_medicion` al diccionario en memoria; implementar modificación de mediciones (`buscar_medicion`, `modificar_medicion`); migrar las validaciones de Etapa 1; `test_validaciones.py` y `test_archivos.py` | Nicole | H1 |
| **H3** | Login: `autenticacion.py`, `usuarios.json`, límite de intentos; `test_autenticacion.py` | Nicole | H1 |
| **H4** | Adaptar consultas y alertas a diccionarios: `getValuesPerSector`, `orderHumidityValues`, `getCriticalValues`, `getIdealValues`, `filtrar_registros`; `test_operaciones.py` (parte consultas) | Jesica | H1 |
| **H5** | Adaptar indicadores a diccionarios: máximo, mínimo, promedios, `agrupar_por_fecha`; `test_operaciones.py` (parte indicadores) | Priscila | H1 |
| **H6** | `reportes.py` (filtrado, sector, general, alertas) y generación de los archivos de reporte (uno por sector y uno general); `test_reportes.py` | Priscila | H4, H5 |
| **H7** | Integración en `main.py`: login, carga inicial del diccionario, menú nuevo, guardado al salir (también ante interrupción) y manejo de excepciones | Todas | H2-H6 |
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
- **Librería estándar:** `csv`, `json`, `re`, `datetime`
- **Herramienta de pruebas:** `pytest` (única dependencia externa; `pip install pytest`)
- **Git/GitHub** para control de versiones

---

## 20. RIESGOS Y PUNTOS A DEFINIR

| Punto | Propuesta |
|-------|-----------|
| ¿Mantener la semana de 7 días o pasar a fechas libres? | Resuelto: fechas reales con ventana de 4 semanas (28 días), configurable en JSON |
| La ventana depende de la fecha actual, lo que complica las pruebas | `validar_fecha` y los filtros reciben la fecha de referencia como parámetro (sin variables globales ni `date.today()` escondido), así las pruebas son deterministas |
| ¿Contraseñas en texto plano o con hash? | Resuelto: texto plano, por alcance de la materia (riesgo aceptado) |
| ¿Qué ocurre si el CSV tiene dos mediciones para el mismo sector y fecha? | Se informa como fila inválida y se conserva la primera |
| Los cambios solo se guardan al salir: si el programa se cierra de forma anormal (corte de luz, cierre forzado) se pierde la sesión | Se acepta por alcance. Para cierres controlados, `main.py` guarda en un bloque `finally`, de modo que también se guarde ante `Ctrl+C` o una excepción inesperada |
| El CSV se sobrescribe directamente: una falla durante la escritura puede dejarlo incompleto | Se acepta por alcance (sin temporal ni respaldo); el error se informa y se ofrece reintentar |
| Al sobrescribir desde memoria, las filas fuera de la ventana y las inválidas se eliminan del archivo | **Riesgo aceptado por el equipo** dado el alcance de la materia: el CSV conserva solo las últimas 4 semanas y el historial anterior se pierde. Si en el futuro se necesitara historial completo, habría que conservar esas filas aparte |
| ¿Se registra quién y cuándo modificó una medición? | Fuera de alcance por ahora; se puede evaluar una bitácora de texto aparte si sobra tiempo |
| Pendientes de la devolución de Etapa 1 en `getCriticalValues` y `getIdealValues` | Resolver en H4 junto con su adaptación |
| `README.md` actual tiene comandos de Git pegados al final | Limpiar al actualizarlo en H8 |
