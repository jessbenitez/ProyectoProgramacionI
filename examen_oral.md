# Lista de funciones del proyecto

## codigo/main.py
Concentra el menú, toda la entrada/salida por consola y el punto de entrada del programa.

- [**main()**](codigo/main.py#L99): Orquesta el programa: normaliza y muestra el equipo, prueba las funciones de `perfil_equipo`, carga los datos iniciales del campo y lanza el menú.
- [**pedir_sector_valido(nombres_sectores)**](codigo/main.py#L6): Pide por consola un número de sector válido (1-5) y lo devuelve como entero.
- [**pedir_entero_positivo(mensaje)**](codigo/main.py#L15): Pide por consola un entero mayor o igual a 0, validando la entrada.
- [**pedir_rango_ideal()**](codigo/main.py#L23): Pregunta si se quiere personalizar el rango ideal de humedad; devuelve `(ideal, tolerancia)` (por defecto 50, 10).
- [**pedir_medicion(nombres_sectores, dias_semana)**](codigo/main.py#L32): Pide sector, día y humedad por consola (validando cada dato) y devuelve los tres valores como enteros.
- [**menu(valores_actuales, nombres_sectores, dias_semana)**](codigo/main.py#L53): Bucle principal (`while opcion != "fin"`) que muestra las opciones al usuario y llama a `operaciones`/`datos` según la opción elegida, imprimiendo los resultados.

## codigo/datos.py
Solo datos: constantes, generación de la matriz inicial y formateo de texto (sin `print`).

- [**cargar_datos_iniciales()**](codigo/datos.py#L17): Genera la matriz de humedad (una fila por sector, una columna por día). Solo ~30% de las celdas arranca con medición (0-100); el resto queda en -1, para que siempre haya lugar donde registrar.
- [**formatear_matriz(datos)**](codigo/datos.py#L29): Devuelve el string con la matriz de humedad en formato de tabla (sectores en filas, días en columnas), mostrando "Sin medición" en las celdas con -1.

## codigo/perfil_equipo.py
- [**normalizarNombres(nombres)**](codigo/perfil_equipo.py#L15): Devuelve la lista de nombres con formato título (`title()`).
- [**uppercaseTitle(nombre_equipo)**](codigo/perfil_equipo.py#L18): Devuelve el nombre del equipo en mayúsculas.
- [**cantidadCaracteres(nombre_equipo)**](codigo/perfil_equipo.py#L21): Devuelve la cantidad de caracteres del nombre del equipo.
- [**generarSigla(nombre_equipo)**](codigo/perfil_equipo.py#L24): Genera una sigla tomando la inicial de cada palabra del nombre del equipo.
- [**contiene_digitos(texto)**](codigo/perfil_equipo.py#L29): Recorre el texto carácter por carácter y devuelve `True` si contiene al menos un dígito.

## codigo/operaciones.py
Módulo de lógica pura: ninguna función usa `input()`/`print()` ni variables globales; todo se recibe por parámetro.

### Validaciones
- [**validar_sector(sector, nombres_sectores)**](codigo/operaciones.py#L1): Verifica que el string sea un número entre 1 y `len(nombres_sectores)` (1-5).
- [**validar_dia(dia, dias_semana)**](codigo/operaciones.py#L7): Verifica que el string sea un número entre 0 y `len(dias_semana) - 1` (0-6).
- [**validar_humedad(humedad)**](codigo/operaciones.py#L13): Verifica que el string sea un número entre -1 y 100.

### Registro de mediciones
- [**registrar_medicion(valores_actuales, id_sector, id_dia, humedad)**](codigo/operaciones.py#L19): Recibe sector/día/humedad ya validados (sector en 1-5), resta 1 solo al indexar la matriz, y registra el valor si la celda estaba en -1. Devuelve `(matriz, éxito, mensaje)`.

### Indicadores generales
- [**getMaxHumidityValue(sectores)**](codigo/operaciones.py#L29): Devuelve el valor máximo de humedad registrado en toda la matriz (ignorando -1).
- [**getMinHumidityValue(sectores)**](codigo/operaciones.py#L34): Devuelve el valor mínimo de humedad registrado en toda la matriz (ignorando -1).
- [**getAverageHumidityPerSector(sectores)**](codigo/operaciones.py#L39): Devuelve una lista con el promedio de humedad de cada sector (-1 si no tiene mediciones).
- [**getAverageHumidityTotal(sectores)**](codigo/operaciones.py#L50): Devuelve el promedio general de humedad de todo el campo.

### Consulta por sector
- [**getValuesPerSector(sectores, id_sector)**](codigo/operaciones.py#L57): Devuelve la fila de mediciones correspondiente a un sector dado (ID 1-5).
- [**orderHumidityValues(sector_id)**](codigo/operaciones.py#L60): Devuelve las mediciones válidas de un sector ordenadas de mayor a menor.
- [**formatear_detalle_sector(sectores, id_sector, nombres_sectores, dias_semana)**](codigo/operaciones.py#L64): Arma el string con las mediciones diarias de un sector, sus valores ordenados y el top 3 más alto (usando slicing).

### Sectores críticos e ideales
- [**formatear_sectores_criticos(sectores, nombres_sectores)**](codigo/operaciones.py#L83): Arma el string con los sectores cuyo promedio está en rango crítico (<20% o >80%).
- [**formatear_sectores_ideales(sectores, nombres_sectores, ideal_target, tolerancia)**](codigo/operaciones.py#L97): Arma el string con los sectores cuyo promedio cae dentro del rango ideal pedido.
- [**getIdealValues(sectores, ideal_bajo=40.0, ideal_alto=60.0)**](codigo/operaciones.py#L114): A partir de una lista de promedios por sector, devuelve los valores que caen dentro del rango ideal (inclusive: `>=` y `<=`).
- [**getCriticalValues(sectores, limite_bajo=20.0, limite_alto=80.0)**](codigo/operaciones.py#L136): A partir de una lista de promedios por sector, devuelve los valores fuera del rango normal (críticos).

### Reporte final
- [**generar_reporte_final(sectores, nombres_sectores, dias_semana)**](codigo/operaciones.py#L157): Arma el string del reporte semanal completo (indicadores generales, promedio por sector, sectores críticos e ideales).

---

## Notas para el examen oral
- `getIdealValues` y `getCriticalValues` reciben una **lista de promedios**, no la matriz completa. **Pendiente de corrección:** ambas devuelven los *valores* de promedio que cumplen la condición, no los *índices* de sector — por eso las funciones que arman el texto (`formatear_sectores_criticos`, `formatear_sectores_ideales`, `generar_reporte_final`) todavía pueden mostrar un nombre de sector que no corresponde al promedio real (usan la posición dentro de la lista filtrada, no el índice real del sector). Es la próxima corrección pendiente.
- El ID de sector es consistente en todo el proyecto: se pide y valida como 1-5, y solo se resta 1 al indexar la matriz (en `registrar_medicion` y `getValuesPerSector`).
- El rango ideal (40-60%) es inclusivo: 40 y 60 exactos cuentan como ideal.
- El valor `-1` se usa como marca de "sin medición" en toda la matriz de humedad, y se excluye de todos los cálculos.
- La matriz inicial se genera con ~30% de probabilidad de tener medición por celda, para que siempre queden celdas en -1 disponibles para registrar.
- El archivo `principal.py` (residual, solo imprimía un mensaje de prueba) fue eliminado por no usarse en el flujo del programa.
