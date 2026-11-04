# 🌾 Sistema de Monitoreo de Humedad en Cultivos

**Asignatura:** Programación I / Algoritmos y Estructuras I  
**Comisión:** 584514 | **Grupo:** Error 404  
**Cuatrimestre:** 2C 2026 — Etapa 1  

---

## 📋 Descripción del Problema

La agricultura moderna requiere un monitoreo constante de las condiciones ambientales para optimizar el riego y asegurar la salud de los cultivos. En particular, la humedad del suelo es crítica:
* **Importancia:** Permite prevenir el estrés hídrico por falta de agua (<20%) y enfermedades fúngicas por exceso de agua (>80%).
* **Problema que resuelve:** Proporciona un control centralizado para registrar mediciones semanales, detectar alertas tempranas en sectores críticos y facilitar la toma de decisiones agrícolas de forma rápida y confiable.

---

## 🎯 Objetivo del Sistema

Desarrollar un prototipo funcional en Python que permita registrar, consultar, analizar y reportar la humedad del suelo en 5 sectores de un cultivo durante 7 días (una semana), procesando la información en memoria y generando indicadores técnicos junto a reportes ejecutivos.

---

## 👥 Integrantes y Responsabilidades

| Estudiante | Rol Principal | Historias de Usuario | Responsabilidades |
|------------|---------------|----------------------|--------------------|
| **Nicole Quilmore** | Infraestructura | H1, H4 | Setup del proyecto, datos base, función de registro y validaciones. |
| **Jesica Benitez** | Consultas y Alertas | H2, H5 | Consulta de sectores, ordenamiento y filtrado de sectores críticos e ideales. |
| **Priscila Challa** | Análisis y Doc | H3, H6 | Indicadores globales (máx, mín, promedios), reporte final y `README.md`. |

---

## 🛠️ Requisitos del Sistema

* **Lenguaje:** Python 3.8 o superior.
* **Librerías:** No requiere librerías externas (solo módulos estándar de Python).

---

## 🚀 Instrucciones de Ejecución

1. Abrir la terminal y navegar hasta la carpeta del proyecto:
   ```bash
   cd codigo
Ejecutar el menú principal de la aplicación:

Bash
python main.py

📂 Estructura del Proyecto
Plaintext
proyecto/
├── main.py            # Menú interactivo, entrada/salida por consola y control de flujo
├── datos.py           # Constantes globales, tuplas inmutables y matriz base (sin I/O)
├── operaciones.py      # Lógica de cálculo, validaciones y formateo de resultados (sin I/O)
├── perfil_equipo.py    # Funciones auxiliares sobre strings usadas al inicio del programa
└── README.md          # Documentación completa del proyecto

⚙️ Funcionalidad Implementada por Módulo
1. Perfil del equipo (perfil_equipo.py)
normalizarNombres: Normaliza los nombres de los integrantes utilizando .title().

uppercaseTitle: Convierte el nombre del equipo a mayúsculas.

cantidadCaracteres: Informa la cantidad de caracteres del nombre del equipo.

generarSigla: Genera una sigla con la inicial de cada palabra del nombre.

contiene_digitos: Verifica si el nombre del equipo contiene al menos un dígito.

2. Datos de humedad (datos.py)
Constantes configurables: DIAS_SEMANA, NOMBRE_SECTORES (Frutillas, Frambuesas, Arándanos, Moras, Cerezas) y rangos de humedad (CRITICO_BAJO, IDEAL_BAJO, IDEAL_ALTO, CRITICO_ALTO).

cargar_datos_iniciales: Genera la matriz inicial de humedad (5 sectores × 7 días). Solo una minoría de celdas (~30%) arranca con medición cargada; el resto queda en -1, para garantizar que siempre haya lugar para probar el registro de nuevas mediciones.

formatear_matriz: Arma el string con la matriz de humedad en formato de tabla (filas = sectores, columnas = días), mostrando "Sin medición" en las celdas con -1. No imprime nada — el módulo no hace I/O; quien la imprime es `main.py`.

3. Operaciones del sistema (operaciones.py)
Módulo de lógica pura: ninguna de sus funciones usa `input()` ni `print()`, ni depende de variables globales — todo lo que necesitan (nombres de sectores, días de la semana) se les pasa por parámetro.

Validaciones: validar_sector, validar_dia y validar_humedad comprueban que las entradas del usuario sean numéricas y respeten los rangos permitidos (sectores 1-5, días 0-6, humedad 0-100%). El ID de sector se maneja de forma consistente en todo el módulo: 1-5 de cara al usuario, y se resta 1 únicamente al indexar la matriz.

Consultas: getValuesPerSector y orderHumidityValues (utilizando expresiones lambda para el ordenamiento, y slicing para quedarse con el top 3 de mediciones más altas de un sector).

Indicadores: getMaxHumidityValue, getMinHumidityValue, getAverageHumidityPerSector y getAverageHumidityTotal (excluyendo celdas con centinela -1).

Alertas: getCriticalValues y getIdealValues (implementados mediante comprensión de listas). El rango ideal es inclusivo: 40% y 60% se consideran ideales.

Formateo de resultados: formatear_detalle_sector, formatear_sectores_criticos, formatear_sectores_ideales y generar_reporte_final devuelven el texto ya armado como string; es `main.py` quien lo imprime.

Registro: registrar_medicion recibe sector, día y humedad ya validados, y devuelve la matriz actualizada junto con un resultado (éxito/error y mensaje) — no valida ni usa try/except, porque las entradas ya llegan validadas desde `main.py`.

4. Menú interactivo (main.py)
Presenta los datos del equipo formateados.

Concentra toda la interacción con el usuario: pide los datos por consola (pedir_sector_valido, pedir_entero_positivo, pedir_rango_ideal, pedir_medicion) e imprime los resultados que calculan y formatean `operaciones.py` y `datos.py`.

Despliega un menú repetitivo por consola con las siguientes opciones:

Opción 1: Consultar valores por sector (matriz completa).

Opción 2: Ver indicadores generales.

Opción 3: Ver sectores críticos (<20% o >80%).

Opción 4: Ver sectores ideales (40-60%, inclusive).

Opción 5: Registrar nueva medición.

Opción 6: Generar reporte final.

fin: Salir del programa (la salida es escribiendo "fin", no un número de opción).

📊 Estructura de Datos
Matriz 5×7: Representa 5 sectores (filas) por 7 días de la semana (columnas).

Rango válido de humedad: Valores numéricos entre 0 y 100 (porcentaje).

Valor especial -1: Centinela que indica un día sin medición cargada (se excluye de promedios y cálculos, y se muestra como "Sin medición" en la matriz).

🧪 Casos de Prueba Documentados
Caso 1: Registrar medición válida

Entrada: Sector = 1, Día = 0 (Lunes), Humedad = 55%

Resultado esperado: Registro exitoso y actualización de la matriz.

Caso 2: Registrar medición inválida

Entrada: Sector = 6 (inválido), Día = 7 (inválido), Humedad = 150% (inválido)

Resultado esperado: Rechazo con mensaje de error sin cerrar el programa.

Caso 3: Consultar sector con datos completos

Entrada: Sector 4 (Moras).

Resultado esperado: Muestra los 7 valores numéricos correspondientes a la semana.

Caso 4: Consultar sector sin mediciones

Entrada: Sector 3 (Arándanos), sin mediciones cargadas.

Resultado esperado: Muestra "Sin registro" en los días sin medición.

Caso 5: Ver indicadores generales

Resultado esperado: Retorna Máximo, Mínimo y Promedios globales excluyendo celdas con -1.

Caso 6: Ver sectores críticos

Resultado esperado: Filtra y muestra los sectores con mediciones <20% o >80%.

Caso 7: Generar reporte final

Resultado esperado: Imprime la hoja de reporte consolidada con indicadores, promedios y alertas.

Caso 8: Casos de borde de humedad

Entrada: Humedad = 0, Humedad = 100.

Resultado esperado: Ambos se aceptan como válidos (0% suelo seco, 100% saturado).

Caso 9: Casos de borde del rango ideal

Entrada: Promedio de sector = 40%, Promedio de sector = 60%.

Resultado esperado: Ambos se consideran dentro de la zona ideal (rango inclusivo).

Caso 10: Sector fuera de rango

Entrada: Sector = 0, Sector = 6.

Resultado esperado: Rechazo con mensaje de error ("Sector inválido"), ya que los IDs válidos son 1 a 5.

🧠 Decisiones de Diseño
¿Por qué una matriz 5×7? Permite una representación bidimensional limpia para modelar de forma directa la relación entre sectores de tierra y días de la semana.

¿Por qué -1 representa "Sin Medición"? En humedad, el 0% representa un suelo completamente seco (un dato válido). Se usó -1 como centinela fuera de rango para filtrar casilleros sin datos sin distorsionar promedios.

¿Por qué separar el código en módulos (datos, operaciones, main)? Facilita la división de tareas en el equipo, evita conflictos en Git y cumple con la modularización exigida.

¿Por qué usar tuplas para datos fijos? Tanto la lista de días (DIAS_SEMANA) como la de sectores (NOMBRE_SECTORES) son inmutables y no deben ser modificadas en tiempo de ejecución.

🔮 Mejoras Futuras (Etapa 2)
Persistencia en archivos: Guardar y cargar las mediciones desde archivos .txt o .json.

Historial extendido: Ampliar el soporte para registrar múltiples semanas o meses completos.

Análisis de tendencias: Incorporar gráficos ASCII o estadísticas de variación diaria por sector.

Configuración interactiva: Permitir modificar los umbrales de alerta (crítico e ideal) directamente desde el menú.


---

### Comandos de Git para subirlo:

```bash
git add README.md
git commit -m "docs: agregar README completo con casos de prueba y decisiones de diseno"
git push origin main



