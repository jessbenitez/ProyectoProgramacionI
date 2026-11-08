# Lista de funciones del proyecto (Etapa 2)

Estructura de datos central: un **diccionario anidado** `mediciones[sector][fecha] = humedad` (por ejemplo `mediciones["S01"]["2026-10-12"] = 45.5`). Se carga desde `registros.csv` al iniciar y se vuelca al CSV al salir. La configuración (sectores, límites, ventana de días, rutas) viene de `configuracion.json` y se pasa por parámetro a las funciones.

## codigo/main.py
Único módulo con `input()` y `print()`: login, menú, control de flujo y captura de excepciones.

- [**main()**](codigo/main.py#L287): Muestra los datos del equipo, carga configuración y usuarios, hace el login, carga el historial y lanza el menú. El guardado va en un `finally` para que también ocurra ante `Ctrl+C`.
- [**pedir_dato(mensaje, validador)**](codigo/main.py#L13): Repite la pregunta hasta que el validador acepte el dato (captura el `ValueError` y muestra el mensaje con el formato esperado).
- [**pedir_sector(config)**](codigo/main.py#L23), [**pedir_fecha(config, hoy)**](codigo/main.py#L29), [**pedir_humedad(mensaje)**](codigo/main.py#L34): Piden y validan cada dato usando `validaciones.py`.
- [**pedir_credenciales()**](codigo/main.py#L38): Pide usuario y contraseña (se la pasa a `autenticar`).
- [**registrar_nueva_medicion(mediciones, config, hoy)**](codigo/main.py#L44): Opción 1. Si ya existe la medición, muestra el error y sugiere usar "Modificar".
- [**modificar_medicion_existente(mediciones, config, hoy)**](codigo/main.py#L56): Opción 2. Muestra el valor actual, pide el nuevo y confirma con `s/n` antes de reemplazar.
- [**pedir_filtro(config, hoy)**](codigo/main.py#L76): Pregunta si filtrar por sector, fecha, rango o todo, y devuelve un diccionario para `filtrar_registros`.
- [**consultar_mediciones(mediciones, config, hoy)**](codigo/main.py#L99): Opción 3. Muestra las mediciones filtradas y, si el usuario quiere, ordenadas por humedad de mayor a menor.
- [**mostrar_indicadores(mediciones, config)**](codigo/main.py#L123): Opción 4. Máximo, mínimo, promedio total, por sector y por fecha.
- [**mostrar_sectores_criticos(mediciones, config)**](codigo/main.py#L148): Opción 5. Sectores con promedio crítico y las mediciones críticas con fecha y valor.
- [**mostrar_sectores_ideales(mediciones, config)**](codigo/main.py#L163): Opción 6. Sectores con promedio ideal.
- [**mostrar_reporte_filtrado(mediciones, config, hoy)**](codigo/main.py#L175): Opción 7. Reporte filtrado con el promedio del filtro.
- [**guardar_texto_reporte(carpeta, nombre_archivo, texto)**](codigo/main.py#L183): Escribe un reporte; si hay `OSError` informa cuál archivo falló y sigue con los demás.
- [**mostrar_reporte_general(mediciones, config, hoy, carpeta_reportes)**](codigo/main.py#L195): Opción 8. Muestra el reporte general y lo guarda en `reporte_general.txt`.
- [**generar_reportes_en_archivos(mediciones, config, hoy, carpeta_reportes)**](codigo/main.py#L201): Opción 9. Un archivo por sector de la configuración más el general.
- [**menu(usuario, mediciones, config, hoy, carpeta_reportes)**](codigo/main.py#L211): Bucle principal (`while opcion != "fin"`) con `if/elif`.
- [**guardar_con_reintento(ruta, mediciones)**](codigo/main.py#L252): Sobrescribe el CSV; si falla por `OSError` ofrece reintentar o salir sin guardar.
- [**cargar_historial(ruta, config, hoy)**](codigo/main.py#L270): Lee el CSV al diccionario, informa las filas descartadas y, si el archivo no existe, arranca con historial vacío.

## codigo/validaciones.py
Validan con **expresiones regulares** el formato y después la coherencia. Siempre **lanzan `ValueError`** con el formato esperado.

- [**validar_fecha(fecha, fecha_referencia, ventana_dias)**](codigo/validaciones.py#L6): Formato `AAAA-MM-DD`, fecha real (`strptime`, rechaza `2026-02-30`) y dentro de la ventana de 28 días sin fechas futuras. La fecha de referencia llega por parámetro.
- [**validar_codigo_sector(codigo, sectores)**](codigo/validaciones.py#L26): Formato `S##` y que exista en la configuración.
- [**validar_humedad(humedad)**](codigo/validaciones.py#L35): Número con hasta 2 decimales y rango 0-100. Ya no acepta `-1`.
- [**validar_usuario(usuario)**](codigo/validaciones.py#L46): De 3 a 20 caracteres entre minúsculas, dígitos o guion bajo.

## codigo/operaciones.py
Lógica pura: sin `input()`/`print()` ni variables globales.

### Registro y modificación
- [**registrar_medicion(mediciones, sector, fecha, humedad)**](codigo/operaciones.py#L1): Agrega la medición al diccionario; si ya existe lanza `ValueError` (no pisa en silencio).
- [**buscar_medicion(mediciones, sector, fecha)**](codigo/operaciones.py#L13): Devuelve la humedad o lanza `ValueError` si no existe.
- [**modificar_medicion(mediciones, sector, fecha, nueva_humedad)**](codigo/operaciones.py#L20): Reemplaza solo esa medición; lanza `ValueError` si no existe.

### Indicadores
- [**getMaxHumidityValue(mediciones)**](codigo/operaciones.py#L32) y [**getMinHumidityValue(mediciones)**](codigo/operaciones.py#L51): Máximo y mínimo de todas las mediciones (`None` si no hay).
- [**getAverageHumidityPerSector(mediciones)**](codigo/operaciones.py#L75): Devuelve un diccionario `sector → promedio` (`None` si el sector no tiene mediciones).
- [**getAverageHumidityTotal(mediciones)**](codigo/operaciones.py#L101): Promedio de todas las mediciones.
- [**agrupar_por_fecha(mediciones)**](codigo/operaciones.py#L115): Reagrupa el diccionario por fecha y devuelve `fecha → promedio` (acumulador).

### Críticos e ideales
- [**es_critica(humedad, limites)**](codigo/operaciones.py#L139): `True` si es menor que `critico_bajo` o mayor que `critico_alto`. Los valores 20 y 80 **no** son críticos.
- [**es_ideal(humedad, limites)**](codigo/operaciones.py#L147): `True` si está entre `ideal_bajo` e `ideal_alto`, inclusive (40 y 60 son ideales).
- [**getCriticalValues(promedios_por_sector, limites)**](codigo/operaciones.py#L172): Lista de **códigos de sector** cuyo promedio es crítico (comprensión de listas).
- [**getIdealValues(promedios_por_sector, limites)**](codigo/operaciones.py#L184): Lista de códigos de sector cuyo promedio es ideal.
- [**obtener_mediciones_criticas(mediciones, limites)**](codigo/operaciones.py#L196): Por sector, solo las mediciones individuales críticas (las alertas). Usa una comprensión de diccionarios.

### Consultas
- [**getValuesPerSector(mediciones, codigo_sector)**](codigo/operaciones.py#L151): Devuelve una **copia** de las mediciones de un sector.
- [**orderHumidityValues(valores_sector, descendente=True)**](codigo/operaciones.py#L161): Ordena por humedad con `sorted` y una expresión `lambda`.
- [**filtrar_registros(mediciones, codigo_sector, desde, hasta)**](codigo/operaciones.py#L209): Filtra por sector, fecha o rango y devuelve un diccionario nuevo con la misma forma.

## codigo/reportes.py
Arma los reportes como **strings** (sin entrada/salida). Los escribe `archivos.py`.

- [**reporte_filtrado(mediciones, sectores, filtro)**](codigo/reportes.py#L19): Mediciones del filtro con su promedio.
- [**reporte_sector(mediciones, sectores, codigo_sector, limites, fecha_referencia, ventana_dias)**](codigo/reportes.py#L49): Período, mediciones ordenadas, máximo, mínimo, promedio, estado (crítico / ideal / fuera del rango ideal) y alertas del sector. Si no hay datos dice "Sin mediciones en el período".
- [**reporte_general(mediciones, sectores, limites, fecha_referencia)**](codigo/reportes.py#L134): Indicadores del campo, promedio por sector y por fecha, sectores críticos, alertas consolidadas y sectores sin mediciones.
- [**reporte_alertas(mediciones, sectores, limites)**](codigo/reportes.py#L219): Mediciones críticas con fecha y valor, agrupadas por sector.

## codigo/archivos.py
Lectura y escritura de CSV, JSON y texto. Lanza excepciones de E/S; las captura `main.py`.

- [**campos_csv()**](codigo/archivos.py#L8): Encabezado del CSV (`fecha,sector,humedad`), definido en una función para no usar variables globales.
- [**cargar_configuracion(ruta)**](codigo/archivos.py#L13): Lee `configuracion.json` y valida claves y valores; no lo reemplaza en silencio. Lanza `FileNotFoundError`, `json.JSONDecodeError`, `KeyError` o `ValueError`.
- [**cargar_registros(ruta, sectores, fecha_referencia, ventana_dias)**](codigo/archivos.py#L45): Lee el CSV al diccionario. Devuelve también la lista de filas rechazadas (inválidas, duplicadas o fuera de la ventana) con línea y motivo; ante un duplicado conserva la primera.
- [**guardar_registros(ruta, mediciones)**](codigo/archivos.py#L81): Sobrescribe el CSV con el diccionario, ordenado por fecha y sector, con encabezado.
- [**guardar_reporte(ruta, texto)**](codigo/archivos.py#L92): Escribe un archivo de texto y crea la carpeta si falta.

## codigo/autenticacion.py
- [**cargar_usuarios(ruta)**](codigo/autenticacion.py#L11): Lee `usuarios.json` y devuelve `usuario → contraseña`.
- [**validar_credenciales(usuarios, usuario, contrasena)**](codigo/autenticacion.py#L34): `True` si coincide; lanza `ValueError` si el usuario tiene formato inválido.
- [**autenticar(usuarios, pedir_credenciales, informar, max_intentos=3)**](codigo/autenticacion.py#L40): Repite el login hasta 3 intentos; si se agotan lanza `AccesoDenegado`. Recibe funciones por parámetro para no usar `input()`/`print()`.

## codigo/perfil_equipo.py
- [**normalizarNombres(nombres)**](codigo/perfil_equipo.py#L15): Nombres con formato título (`title()`).
- [**uppercaseTitle(nombre_equipo)**](codigo/perfil_equipo.py#L18): Nombre del equipo en mayúsculas.
- [**cantidadCaracteres(nombre_equipo)**](codigo/perfil_equipo.py#L21): Cantidad de caracteres del nombre.
- [**generarSigla(nombre_equipo)**](codigo/perfil_equipo.py#L24): Sigla con la inicial de cada palabra.
- [**contiene_digitos(texto)**](codigo/perfil_equipo.py#L29): `True` si el texto tiene al menos un dígito.

## codigo/generar_demo.py
- [**generar_mediciones(sectores, hoy, ventana_dias)**](codigo/generar_demo.py#L14): Arma datos de demostración con fechas relativas a hoy (críticos, ideales, valores límite, un registro anterior a la ventana y un sector sin datos).
- [**filas_invalidas(hoy, ventana_dias)**](codigo/generar_demo.py#L45): Filas con errores para `registros_con_errores.csv`.
- [**main()**](codigo/generar_demo.py#L60): Escribe `registros.csv` y `registros_con_errores.csv`.

---

## Notas para el examen oral
- **¿Por qué un diccionario en vez de la matriz?** La matriz cubría una sola semana y usaba `-1` como "sin medición", que había que filtrar en cada cálculo. Con `mediciones[sector][fecha]` el sentido está en las claves, y una medición que no existe simplemente no tiene clave.
- **Unicidad:** un sector admite una sola medición por fecha, y esto lo garantiza la propia estructura (no puede haber dos claves iguales). Registrar nunca pisa un valor: para corregir hay que usar "Modificar", con confirmación.
- **Lectura una vez, escritura una vez:** el CSV se lee al iniciar y se sobrescribe al salir. Durante la ejecución todo trabaja sobre el diccionario. El guardado está en un `finally`, así que también se guarda ante `Ctrl+C`.
- **Ventana de 28 días:** solo se aceptan fechas entre hoy menos 27 días y hoy. Las filas más viejas se informan al cargar y, al guardar, desaparecen del CSV (riesgo aceptado por el equipo). El valor está en `configuracion.json`.
- **Fecha de referencia por parámetro:** las funciones no llaman a `date.today()`; reciben la fecha, y así las pruebas dan siempre el mismo resultado.
- **Excepciones:** las funciones de validación y de archivos **lanzan** y `main.py` **captura**, en vez de devolver `True/False` como en la Etapa 1. El mensaje siempre dice qué formato se esperaba.
- **Regex:** validan la estructura (por ejemplo `S[0-9]{2}`) y después se verifica la coherencia (que el sector exista, que la fecha sea real, el rango 0-100).
- **Críticos e ideales:** 20 y 80 **no** son críticos (la condición es `<` y `>`); 40 y 60 **sí** son ideales (`<=`). `getCriticalValues` e `getIdealValues` trabajan sobre el **promedio de cada sector** y devuelven códigos de sector. Las alertas de mediciones individuales las calcula `obtener_mediciones_criticas`.
- **Sin variables globales:** todo se pasa por parámetro. Hasta las constantes (como los campos del CSV) se definen dentro de funciones.
- **Contraseñas en texto plano:** decisión de alcance de la materia; en un sistema real se guardarían con hash.
- **Pruebas:** hay un archivo `test_*.py` por módulo, 124 en total (`python -m pytest` dentro de `codigo`). No usan `input()` y los archivos se prueban con `tmp_path`.
- **Lo que no se implementó:** recursividad y conjuntos, que son optativos en los lineamientos.
- **Archivos eliminados:** `datos.py` (sus constantes pasaron a `configuracion.json`) e `interfaz.py` (no estaba en el alcance).
