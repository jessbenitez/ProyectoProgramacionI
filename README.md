# 🌾 Sistema de Monitoreo de Humedad en Cultivos

**Asignatura:** Programación I / Algoritmos y Estructuras I  
**Comisión:** 584514 | **Grupo:** Error 404  
**Cuatrimestre:** 2C 2026 — Etapa 2 (sistema persistente, verificable y mejor organizado)

---

## 📋 Descripción del problema

La humedad del suelo es crítica para los cultivos: por debajo del 20% hay estrés hídrico y por encima del 80% aparecen enfermedades por exceso de agua. El sistema permite registrar mediciones de 5 sectores de frutas, consultarlas, calcular indicadores y generar reportes con alertas.

Las reglas de dominio se mantienen desde la Etapa 1: **crítico < 20% o > 80%** (los valores 20 y 80 no son críticos) e **ideal 40-60%** (inclusive).

---

## 👥 Integrantes y responsabilidades (Etapa 2)

| Estudiante | Historias |
|------------|-----------|
| **Nicole Quilmore** | H1 (estructura, `configuracion.json`, `archivos.py`), H2 (validaciones, registro y modificación), H3 (login) |
| **Jesica Benitez** | H4 (consultas y alertas sobre diccionarios) |
| **Priscila Challa** | H5 (indicadores), H6 (reportes y archivos de texto) |
| **Todas** | H7 (integración en `main.py`) y H8 (documentación) |

---

## 🛠️ Requisitos

* **Python** 3.8 o superior.
* **Librería estándar:** `csv`, `json`, `re`, `datetime`, `os`.
* **Pruebas:** `pytest` (única dependencia externa): `pip install pytest`.

## 🚀 Ejecución

```bash
cd codigo
python main.py          # programa principal
python -m pytest        # pruebas unitarias
python generar_demo.py  # regenera los datos de demostración con fechas relativas a hoy
```

Usuarios de prueba: ver `codigo/datos/usuarios.json`.

---

## 🔄 Qué cambió respecto de la Etapa 1

| Etapa 1 | Limitación | Etapa 2 |
|---------|-----------|---------|
| Matriz 5×7 con `-1` como "sin medición" | Solo una semana; había que filtrar `-1` en cada cálculo | Diccionario `mediciones[sector][fecha] = humedad`; si no hay medición, simplemente no existe la clave |
| Datos iniciales con `random` | Nada se conservaba entre ejecuciones | Se carga `registros.csv` al iniciar y se sobrescribe al salir |
| Constantes en `datos.py` | Cambiar un límite obligaba a editar código | `configuracion.json` leído a un diccionario que se pasa por parámetro |
| Validaciones con `isnumeric()` y `range()`, devolvían `True/False` | No explicaban por qué fallaban | Expresiones regulares + excepciones (`ValueError`) con el formato esperado |
| Una medición cargada no se podía corregir | Un error de tipeo quedaba para siempre | Opción de **modificar** con confirmación del usuario |
| Sin control de acceso | Cualquiera usaba el sistema | Login contra `usuarios.json` (3 intentos) |
| Sin pruebas | No había verificación | Pruebas con pytest, un archivo por módulo |
| Reporte solo por pantalla | No quedaba evidencia | Reportes en archivos de texto: uno por sector y uno general |

---

## 📂 Estructura del proyecto

```
codigo/
├── main.py            # Login, menú y control de flujo (único módulo con input/print)
├── validaciones.py    # Regex y validaciones; lanzan excepciones
├── operaciones.py     # Cálculos, filtros, acumuladores y detección de críticos
├── reportes.py        # Arma los reportes como strings (sin I/O)
├── archivos.py        # Lectura/escritura de CSV, JSON y texto
├── autenticacion.py   # Login contra usuarios.json
├── perfil_equipo.py   # Se conserva de la Etapa 1
├── generar_demo.py    # Regenera los datos de demostración
├── datos/
│   ├── configuracion.json
│   ├── usuarios.json
│   ├── registros.csv
│   └── registros_con_errores.csv
├── salida/reportes/   # reporte_S01.txt ... reporte_S05.txt y reporte_general.txt
└── tests/             # test_validaciones, test_operaciones, test_reportes, test_archivos, test_autenticacion
```

No hay variables globales: todo lo que una función necesita (configuración, mediciones, fecha de referencia) se pasa por parámetro.

---

## ⚙️ Funcionamiento

1. **Inicio:** se lee `configuracion.json` y `usuarios.json`. Si falta alguno o es inválido, se informa el error y el programa termina (no se reemplaza en silencio).
2. **Login:** usuario y contraseña, máximo 3 intentos.
3. **Carga del historial:** `registros.csv` se lee una sola vez a un diccionario. Las filas inválidas, duplicadas (se conserva la primera) o fuera de la ventana se informan con número de línea y motivo, y no se incorporan. Si el archivo no existe se arranca vacío.
4. **Menú:** todas las acciones trabajan sobre el diccionario en memoria.
5. **Salida (`fin`):** el diccionario sobrescribe `registros.csv`, ordenado por fecha y sector. El guardado está en un `finally`, así que también ocurre ante `Ctrl+C`. Si falla, se ofrece reintentar.

### Menú

| Opción | Acción |
|--------|--------|
| 1 | Registrar nueva medición (no pisa una existente) |
| 2 | Modificar medición existente (con confirmación) |
| 3 | Consultar mediciones por sector, fecha, rango o todo el historial |
| 4 | Indicadores generales: máximo, mínimo, promedio total, por sector y por fecha |
| 5 | Sectores críticos (promedio) y alertas de mediciones críticas |
| 6 | Sectores ideales |
| 7 | Reporte filtrado (con promedio del filtro) |
| 8 | Reporte general en pantalla y en `reporte_general.txt` |
| 9 | Genera todos los reportes en archivos (uno por sector y el general) |
| fin | Guarda los cambios y sale |

### Ventana de 28 días

Las fechas son reales (`AAAA-MM-DD`) y solo se aceptan las de los últimos 28 días hasta hoy (no futuras). El valor `ventana_dias` está en `configuracion.json`. Al guardar, las filas más antiguas desaparecen del CSV: el archivo conserva solo las últimas 4 semanas (riesgo aceptado por el equipo).

### Validaciones con expresiones regulares

| Dato | Regex | Verificación posterior |
|------|-------|------------------------|
| Fecha | `[0-9]{4}-[0-9]{2}-[0-9]{2}` | Fecha real con `strptime` y dentro de la ventana |
| Sector | `S[0-9]{2}` | Existe en la configuración |
| Humedad | `[0-9]{1,3}(\.[0-9]{1,2})?` | Rango 0-100 |
| Usuario | `[a-z0-9_]{3,20}` | Existe en `usuarios.json` |

### Excepciones

Las funciones de validación y de archivos **lanzan** excepciones y `main.py` las **captura** para mostrar el mensaje: `FileNotFoundError`, `json.JSONDecodeError`, `KeyError`, `ValueError`, `OSError`, y `AccesoDenegado` para el login.

---

## 🧪 Pruebas

```bash
cd codigo
python -m pytest
```

Hay un archivo de pruebas por módulo. Los archivos se prueban con `tmp_path` y las pruebas no usan `input()`. Cubren: validación correcta e incorrecta, cálculos con resultado conocido, agrupación por fecha, detección de críticos, modificación de mediciones, casos límite (20, 40, 60, 80 y bordes de la ventana), reportes, persistencia (ida y vuelta CSV) y login.

---

## ⚠️ Decisiones y limitaciones aceptadas

* Las contraseñas se guardan en **texto plano** por alcance de la materia (en un sistema real irían con hash).
* El CSV se sobrescribe directamente, sin archivo temporal ni respaldo.
* Si el programa se cierra de forma anormal (corte de luz) se pierde la sesión.
* Recursividad y conjuntos (optativos) **no se implementaron**.
