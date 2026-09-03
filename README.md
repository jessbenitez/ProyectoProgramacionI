# ProyectoProgramacionI
Proyecto Integrador - Programación I

## Descripción

Sistema de monitoreo de humedad para sectores de producción de frutas. Registra y muestra los valores de humedad medidos por sector y por día de la semana.

## Estructura del proyecto

```
Codigo/
├── main.py           # Punto de entrada del programa
├── datos.py          # Constantes y carga/visualización de la matriz de humedad
├── operaciones.py     # Validaciones, registro de mediciones y menú interactivo
├── perfil_equipo.py  # Funciones de presentación del equipo (nombres, sigla, etc.)
└── principal.py       # Script inicial de pruebas
```

## Funcionalidad implementada

### Perfil del equipo (`perfil_equipo.py`)
- `normalizarNombres`: normaliza los nombres de los integrantes con `title()`.
- `uppercaseTitle`: convierte el nombre del equipo a mayúsculas.
- `cantidadCaracteres`: informa la cantidad de caracteres del nombre del equipo.
- `generarSigla`: genera una sigla con la inicial de cada palabra del nombre.
- `contiene_digitos`: verifica si el nombre del equipo contiene al menos un dígito.

### Datos de humedad (`datos.py`)
- Constantes: `DIAS_SEMANA`, `NOMBRE_SECTORES` y los rangos de humedad (`CRITICO_BAJO`, `IDEAL_BAJO`, `IDEAL_ALTO`, `CRITICO_ALTO`).
- `cargar_datos_iniciales`: genera una matriz de humedad (una fila por sector, una columna por día) con valores aleatorios entre -1 y 100, donde -1 representa un valor aún no medido.
- `mostrar_matriz`: imprime la matriz de humedad en formato de tabla (filas = sectores, columnas = días), con cada valor mostrado como porcentaje.

### Operaciones (`operaciones.py`)
- `validar_sector`, `validar_dia`, `validar_humedad`: validan que los datos ingresados por el usuario sean numéricos y estén dentro del rango permitido.
- `registrar_medicion`: solicita sector, día y humedad por consola, valida cada dato y registra la medición en la matriz (evita sobrescribir un valor ya cargado).
- `menu`: menú interactivo por consola que permite elegir entre ver la matriz de humedad (opción 1) o registrar una medición (opción 2), repitiéndose hasta que el usuario escribe `fin`.

### Programa principal (`main.py`)
1. Muestra los nombres normalizados de los integrantes del equipo.
2. Muestra el nombre del equipo en mayúsculas, su cantidad de caracteres, su sigla y si contiene dígitos.
3. Carga la matriz inicial de humedad.
4. Lanza el menú interactivo (`operaciones.menu`) para consultar o registrar mediciones hasta que el usuario decide finalizar.

## Cómo ejecutar

Desde la carpeta `codigo`:

```bash
python3 main.py
```
