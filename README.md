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
├── main.py           # Menú interactivo principal y control de flujo
├── datos.py          # Constantes globales, tuplas inmutables y matriz base
├── operaciones.py     # Lógica de cálculo, validaciones, alertas y reporte final
└── README.md         # Documentación completa del proyecto

⚙️ Funcionalidad Implementada por Módulo
1. Perfil del equipo (perfil_equipo.py)
normalizarNombres: Normaliza los nombres de los integrantes utilizando .title().

uppercaseTitle: Convierte el nombre del equipo a mayúsculas.

cantidadCaracteres: Informa la cantidad de caracteres del nombre del equipo.

generarSigla: Genera una sigla con la inicial de cada palabra del nombre.

contiene_digitos: Verifica si el nombre del equipo contiene al menos un dígito.

2. Datos de humedad (datos.py)
Constantes configurables: DIAS_SEMANA, NOMBRE_SECTORES y rangos de humedad (CRITICO_BAJO, IDEAL_BAJO, IDEAL_ALTO, CRITICO_ALTO).

cargar_datos_iniciales: Genera la matriz inicial de humedad (5 sectores × 7 días) con valores iniciales o centinelas (-1).

mostrar_matriz: Imprime la matriz de humedad en formato de tabla (filas = sectores, columnas = días) mostrando el porcentaje correspondiente.

3. Operaciones del sistema (operaciones.py)
Validaciones: validar_sector, validar_dia y validar_humedad comprueban que las entradas del usuario sean numéricas y respeten los rangos permitidos (sectores 1-5, días 0-6, humedad 0-100%).

Consultas: getValuesPerSector y orderHumidityValues (utilizando expresiones lambda para el ordenamiento).

Indicadores: getMaxHumidityValue, getMinHumidityValue, getAverageHumidityPerSector y getAverageHumidityTotal (excluyendo celdas con centinela -1).

Alertas: getCriticalValues y getIdealValues (implementados mediante comprensión de listas).

Reporte y Registro: registrar_medicion y generar_reporte_final.

4. Menú interactivo (main.py)
Presenta los datos del equipo formateados.

Despliega un menú repetitivo por consola con las siguientes opciones:

Option 1: Consultar valores por sector.

Option 2: Ver indicadores generales.

Option 3: Ver sectores críticos (<20% o >80%).

Option 4: Ver sectores ideales (40-60%).

Option 5: Registrar nueva medición.

Option 6: Generar reporte final.

Option 0: Salir del programa.

📊 Estructura de Datos
Matriz 5×7: Representa 5 sectores (filas) por 7 días de la semana (columnas).

Rango válido de humedad: Valores numéricos entre 0 y 100 (porcentaje).

Valor especial -1: Centinela que indica un día sin medición cargada (se excluye de promedios y cálculos).

🧪 Casos de Prueba Documentados
Caso 1: Registrar medición válida

Entrada: Sector = 1, Día = 0 (Lunes), Humedad = 55%

Resultado esperado: Registro exitoso y actualización de la matriz.

Caso 2: Registrar medición inválida

Entrada: Sector = 6 (inválido), Día = 7 (inválido), Humedad = 150% (inválido)

Resultado esperado: Rechazo con mensaje de error sin cerrar el programa.

Caso 3: Consultar sector con datos completos

Entrada: Sector 4 (Sector D).

Resultado esperado: Muestra los 7 valores numéricos correspondientes a la semana.

Caso 4: Consultar sector sin mediciones

Entrada: Sector 3 (Sector C, inicializado con -1).

Resultado esperado: Muestra N/A (sin mediciones) en los días vacíos.

Caso 5: Ver indicadores generales

Resultado esperado: Retorna Máximo, Mínimo y Promedios globales excluyendo celdas con -1.

Caso 6: Ver sectores críticos

Resultado esperado: Filtra y muestra los sectores con mediciones <20% o >80%.

Caso 7: Generar reporte final

Resultado esperado: Imprime la hoja de reporte consolidada con indicadores, promedios y alertas.

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



