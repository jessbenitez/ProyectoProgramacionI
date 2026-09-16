# Lista de funciones del proyecto

## codigo/main.py
- [**main()**](codigo/main.py#L6): Orquesta el programa: normaliza y muestra el equipo, prueba las funciones de `perfil_equipo`, carga los datos iniciales del campo y lanza el menú de `operaciones`.

## codigo/datos.py
- [**cargar_datos_iniciales()**](codigo/datos.py#L15): Genera la matriz de humedad (una fila por sector, una columna por día) con valores aleatorios entre -1 y 100.
- [**mostrar_matriz(datos)**](codigo/datos.py#L23): Imprime por consola la matriz de humedad con formato de tabla (sectores en filas, días en columnas).

## codigo/perfil_equipo.py
- [**normalizarNombres(nombres)**](codigo/perfil_equipo.py#L15): Devuelve la lista de nombres con formato título (`title()`).
- [**uppercaseTitle(nombre_equipo)**](codigo/perfil_equipo.py#L18): Devuelve el nombre del equipo en mayúsculas.
- [**cantidadCaracteres(nombre_equipo)**](codigo/perfil_equipo.py#L21): Devuelve la cantidad de caracteres del nombre del equipo.
- [**generarSigla(nombre_equipo)**](codigo/perfil_equipo.py#L24): Genera una sigla tomando la inicial de cada palabra del nombre del equipo.
- [**contiene_digitos(texto)**](codigo/perfil_equipo.py#L29): Recorre el texto carácter por carácter y devuelve `True` si contiene al menos un dígito.

## codigo/operaciones.py

### Validaciones
- [**validar_sector(sector)**](codigo/operaciones.py#L6): Verifica que el string ingresado sea un número válido dentro del rango de sectores existentes.
- [**validar_dia(dia)**](codigo/operaciones.py#L12): Verifica que el string ingresado sea un número válido dentro del rango de días de la semana.
- [**validar_humedad(humedad)**](codigo/operaciones.py#L18): Verifica que el string ingresado sea un número válido de humedad (entre -1 y 100).

### Registro de mediciones
- [**registrar_medicion(valores_actuales)**](codigo/operaciones.py#L24): Pide por consola sector, día y humedad (validando cada dato), y registra el valor en la matriz si esa celda aún no fue cargada.

### Indicadores generales
- [**getMaxHumidityValue(sectores)**](codigo/operaciones.py#L55): Devuelve el valor máximo de humedad registrado en toda la matriz (ignorando valores -1).
- [**getMinHumidityValue(sectores)**](codigo/operaciones.py#L60): Devuelve el valor mínimo de humedad registrado en toda la matriz (ignorando valores -1).
- [**getAverageHumidityPerSector(sectores)**](codigo/operaciones.py#L65): Devuelve una lista con el promedio de humedad de cada sector (-1 si no tiene mediciones).
- [**getAverageHumidityTotal(sectores)**](codigo/operaciones.py#L76): Devuelve el promedio general de humedad de todo el campo.

### Consulta por sector
- [**pedir_sector_valido()**](codigo/operaciones.py#L83): Pide por consola un número de sector válido y lo devuelve como entero.
- [**getValuesPerSector(sectores, id_sector)**](codigo/operaciones.py#L94): Devuelve la fila de mediciones correspondiente a un sector dado.
- [**orderHumidityValues(sector_id)**](codigo/operaciones.py#L101): Devuelve las mediciones válidas de un sector ordenadas de mayor a menor.
- [**mostrar_detalle_sector(sectores, id_sector)**](codigo/operaciones.py#L105): Imprime las mediciones diarias de un sector y sus valores ordenados de mayor a menor.

### Sectores críticos e ideales
- [**pedir_entero_positivo(mensaje)**](codigo/operaciones.py#L121): Pide por consola un entero mayor o igual a 0, validando la entrada.
- [**pedir_rango_ideal()**](codigo/operaciones.py#L128): Pregunta si se quiere personalizar el rango ideal de humedad; devuelve `(ideal, tolerancia)` (por defecto 50, 10).
- [**mostrar_sectores_criticos(sectores, nombres_sectores)**](codigo/operaciones.py#L138): Muestra por consola los sectores cuyo promedio está en rango crítico (<20% o >80%).
- [**mostrar_sectores_ideales(sectores, nombres_sectores)**](codigo/operaciones.py#L151): Pide el rango ideal y muestra por consola los sectores cuyo promedio cae dentro de ese rango.
- [**getIdealValues2(sectores, humedad_ideal=50, tolerancia=10)**](codigo/operaciones.py#L172): Calcula, a partir de la matriz completa, los sectores en zona ideal junto con su promedio y la cantidad y promedio general de esos sectores. *(No se usa en el flujo actual)*.
- [**getIdealValues(sectores, ideal_bajo=40.0, ideal_alto=60.0)**](codigo/operaciones.py#L195): A partir de una lista de promedios por sector, devuelve los valores que caen estrictamente dentro del rango ideal.
- [**getCriticalValues(sectores, limite_bajo=20.0, limite_alto=80.0)**](codigo/operaciones.py#L217): A partir de una lista de promedios por sector, devuelve los valores que están fuera del rango normal (críticos).

### Reporte final
- [**generar_reporte_final(sectores, nombres_sectores, dias_semana)**](codigo/operaciones.py#L238): Arma el string del reporte semanal completo (indicadores generales, promedio por sector, sectores críticos e ideales).

### Menú principal
- [**menu(valores_actuales)**](codigo/operaciones.py#L289): Bucle principal que muestra las opciones al usuario y llama a las demás funciones según la opción elegida (matriz, indicadores, críticos, ideales, registrar medición, reporte final, salir).

---

## Notas para el examen oral
- `getIdealValues` y `getCriticalValues` reciben una **lista de promedios**, no la matriz completa (a diferencia de `getIdealValues2`, que sí recibe la matriz).
- `perfil_equipo.py` tiene una función `contiene_digitos` definida dos veces (líneas 8 y 29 en el archivo original); la segunda es la que realmente se usa, la primera está dentro de un comentario/docstring.
- El valor `-1` se usa como marca de "sin medición" en toda la matriz de humedad.
