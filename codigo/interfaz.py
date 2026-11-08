"""Interfaz gráfica (tkinter) del sistema de monitoreo de humedad.

Es una vista alternativa a main.py: usa los mismos módulos de lógica (archivos, autenticacion,
operaciones, validaciones) y sigue el mismo flujo: configuración -> login -> carga del CSV ->
operar sobre el diccionario en memoria -> guardar al cerrar. Ejecutar con: python interfaz.py
"""
import json
import os
import tkinter as tk
from datetime import date
from tkinter import messagebox, ttk

import archivos
import autenticacion
import operaciones
import validaciones

MAX_INTENTOS = 3
COLORES = {"Crítico": "#f8c9c9", "Ideal": "#c9f0d2", "Regular": "#ffffff"}


def clasificar(humedad, limites):
    """Devuelve 'Crítico', 'Ideal' o 'Regular' según los límites de la configuración."""
    if humedad < limites["critico_bajo"] or humedad > limites["critico_alto"]:
        return "Crítico"
    if limites["ideal_bajo"] <= humedad <= limites["ideal_alto"]:
        return "Ideal"
    return "Regular"


class VentanaLogin(tk.Tk):
    """Pide usuario y contraseña; guarda en self.usuario el usuario autenticado (o None si se cancela o se agotan los intentos)."""

    def __init__(self, usuarios):
        super().__init__()
        self.title("Ingreso al sistema")
        self.resizable(False, False)
        self.usuarios = usuarios
        self.usuario = None
        self.intentos = 0

        marco = ttk.Frame(self, padding=20)
        marco.grid()
        ttk.Label(marco, text="Monitoreo de humedad en cultivos", font=("Helvetica", 14, "bold")).grid(columnspan=2, pady=(0, 10))
        ttk.Label(marco, text="Usuario:").grid(row=1, column=0, sticky="e", pady=3)
        ttk.Label(marco, text="Contraseña:").grid(row=2, column=0, sticky="e", pady=3)
        self.entrada_usuario = ttk.Entry(marco, width=25)
        self.entrada_contrasena = ttk.Entry(marco, width=25, show="*")
        self.entrada_usuario.grid(row=1, column=1, pady=3)
        self.entrada_contrasena.grid(row=2, column=1, pady=3)
        self.mensaje = ttk.Label(marco, text="", foreground="#b00020")
        self.mensaje.grid(row=3, columnspan=2, pady=5)
        ttk.Button(marco, text="Ingresar", command=self.ingresar).grid(row=4, columnspan=2)

        self.bind("<Return>", lambda evento: self.ingresar())
        self.entrada_usuario.focus()

    def ingresar(self):
        self.intentos += 1
        usuario = self.entrada_usuario.get().strip()
        try:
            if autenticacion.validar_credenciales(self.usuarios, usuario, self.entrada_contrasena.get().strip()):
                self.usuario = usuario
                self.destroy()
                return
            motivo = "Usuario o contraseña incorrectos"
        except ValueError as error:
            motivo = str(error)

        if self.intentos >= MAX_INTENTOS:
            messagebox.showerror("Acceso denegado", f"Se agotaron los {MAX_INTENTOS} intentos de login")
            self.destroy()
            return
        self.mensaje.config(text=f"{motivo} (intento {self.intentos} de {MAX_INTENTOS})", wraplength=320)
        self.entrada_contrasena.delete(0, tk.END)


class App(tk.Tk):
    """Ventana principal. El estado (mediciones, config, rechazadas) vive en la instancia, no en variables globales."""

    def __init__(self, usuario, config, mediciones, rechazadas, ruta_registros, hoy):
        super().__init__()
        self.title("Sistema de monitoreo de humedad en cultivos")
        self.geometry("820x560")
        self.usuario = usuario
        self.config_datos = config
        self.mediciones = mediciones
        self.rechazadas = rechazadas
        self.ruta_registros = ruta_registros
        self.hoy = hoy

        encabezado = ttk.Frame(self, padding=(10, 8))
        encabezado.pack(fill="x")
        ttk.Label(encabezado, text=f"Usuario: {usuario}", font=("Helvetica", 11, "bold")).pack(side="left")
        ttk.Label(encabezado, text=f"Ventana: últimos {config['ventana_dias']} días hasta {hoy}").pack(side="right")

        pestanas = ttk.Notebook(self)
        pestanas.pack(fill="both", expand=True, padx=10, pady=(0, 5))
        self.armar_pestana_registros(pestanas)
        self.armar_pestana_sectores(pestanas)
        self.armar_pestana_cargar(pestanas)
        self.armar_pestana_descartadas(pestanas)

        self.estado = ttk.Label(self, text="Los cambios se guardan en el archivo al cerrar la ventana.", padding=(10, 4))
        self.estado.pack(fill="x")

        self.refrescar()
        self.protocol("WM_DELETE_WINDOW", self.cerrar)

    # ---------- Pestaña: registros cargados ----------
    def armar_pestana_registros(self, pestanas):
        marco = ttk.Frame(pestanas, padding=10)
        pestanas.add(marco, text="Registros")

        filtro = ttk.Frame(marco)
        filtro.pack(fill="x", pady=(0, 6))
        ttk.Label(filtro, text="Sector:").pack(side="left")
        self.filtro_sector = ttk.Combobox(filtro, state="readonly", width=22,
                                          values=["Todos"] + [f"{c} - {n}" for c, n in self.config_datos["sectores"].items()])
        self.filtro_sector.current(0)
        self.filtro_sector.pack(side="left", padx=5)
        self.filtro_sector.bind("<<ComboboxSelected>>", lambda evento: self.refrescar())
        self.resumen = ttk.Label(filtro, text="")
        self.resumen.pack(side="right")

        columnas = ("fecha", "sector", "nombre", "humedad", "estado")
        self.tabla = ttk.Treeview(marco, columns=columnas, show="headings", height=14)
        for columna, titulo, ancho in (("fecha", "Fecha", 110), ("sector", "Sector", 70), ("nombre", "Cultivo", 160),
                                       ("humedad", "Humedad (%)", 100), ("estado", "Estado", 100)):
            self.tabla.heading(columna, text=titulo)
            self.tabla.column(columna, width=ancho, anchor="center")
        for estado, color in COLORES.items():
            self.tabla.tag_configure(estado, background=color, foreground="black")
        barra = ttk.Scrollbar(marco, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=barra.set)
        self.tabla.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

    # ---------- Pestaña: tarjetas por sector ----------
    def armar_pestana_sectores(self, pestanas):
        marco = ttk.Frame(pestanas, padding=10)
        pestanas.add(marco, text="Sectores")
        self.tarjetas = {}
        for fila, (codigo, nombre) in enumerate(self.config_datos["sectores"].items()):
            tarjeta = tk.Frame(marco, bd=1, relief="solid", padx=10, pady=8)
            tarjeta.grid(row=fila, column=0, sticky="ew", pady=3)
            marco.columnconfigure(0, weight=1)
            titulo = tk.Label(tarjeta, text=f"{codigo} - {nombre}", font=("Helvetica", 12, "bold"), anchor="w", fg="black")
            detalle = tk.Label(tarjeta, text="", anchor="w", justify="left", fg="black")
            titulo.pack(fill="x")
            detalle.pack(fill="x")
            self.tarjetas[codigo] = (tarjeta, titulo, detalle)

    # ---------- Pestaña: registrar / modificar ----------
    def armar_pestana_cargar(self, pestanas):
        marco = ttk.Frame(pestanas, padding=20)
        pestanas.add(marco, text="Registrar / Modificar")

        ttk.Label(marco, text="Sector:").grid(row=0, column=0, sticky="e", pady=4)
        ttk.Label(marco, text="Fecha (AAAA-MM-DD):").grid(row=1, column=0, sticky="e", pady=4)
        ttk.Label(marco, text="Humedad (0-100):").grid(row=2, column=0, sticky="e", pady=4)

        self.campo_sector = ttk.Combobox(marco, state="readonly", width=25,
                                         values=[f"{c} - {n}" for c, n in self.config_datos["sectores"].items()])
        self.campo_sector.current(0)
        self.campo_fecha = ttk.Entry(marco, width=28)
        self.campo_fecha.insert(0, self.hoy.isoformat())
        self.campo_humedad = ttk.Entry(marco, width=28)
        self.campo_sector.grid(row=0, column=1, padx=8, pady=4)
        self.campo_fecha.grid(row=1, column=1, padx=8, pady=4)
        self.campo_humedad.grid(row=2, column=1, padx=8, pady=4)

        botones = ttk.Frame(marco)
        botones.grid(row=3, columnspan=2, pady=12)
        ttk.Button(botones, text="Registrar nueva", command=self.registrar).pack(side="left", padx=5)
        ttk.Button(botones, text="Modificar existente", command=self.modificar).pack(side="left", padx=5)

        self.mensaje_form = ttk.Label(marco, text="", wraplength=500)
        self.mensaje_form.grid(row=4, columnspan=2)

    # ---------- Pestaña: filas descartadas al cargar ----------
    def armar_pestana_descartadas(self, pestanas):
        marco = ttk.Frame(pestanas, padding=10)
        pestanas.add(marco, text=f"Descartadas ({len(self.rechazadas)})")
        ttk.Label(marco, text="Filas del archivo que no se incorporaron al cargar (no se reescriben al guardar):").pack(anchor="w")
        lista = tk.Listbox(marco)
        lista.pack(fill="both", expand=True, pady=5)
        for motivo in self.rechazadas or ["Ninguna: todas las filas del archivo eran válidas."]:
            lista.insert(tk.END, motivo)

    # ---------- Lógica de la vista ----------
    def refrescar(self):
        """Vuelve a dibujar la tabla y las tarjetas a partir del diccionario en memoria."""
        sectores = self.config_datos["sectores"]
        limites = self.config_datos["limites"]
        seleccion = self.filtro_sector.get()
        codigo_filtro = None if seleccion == "Todos" else seleccion.split(" - ")[0]

        self.tabla.delete(*self.tabla.get_children())
        filas = sorted((fecha, codigo, humedad)
                       for codigo, fechas in self.mediciones.items() for fecha, humedad in fechas.items()
                       if codigo_filtro is None or codigo == codigo_filtro)
        for fecha, codigo, humedad in filas:
            estado = clasificar(humedad, limites)
            self.tabla.insert("", tk.END, values=(fecha, codigo, sectores[codigo], f"{humedad:.2f}", estado), tags=(estado,))
        self.resumen.config(text=f"{len(filas)} mediciones mostradas")

        for codigo, (tarjeta, titulo, detalle) in self.tarjetas.items():
            fechas = self.mediciones[codigo]
            if fechas:
                promedio = sum(fechas.values()) / len(fechas)
                ultima = max(fechas)
                estado = clasificar(promedio, limites)
                texto = (f"{len(fechas)} mediciones | Promedio: {promedio:.2f}% ({estado}) | "
                         f"Última: {fechas[ultima]:.2f}% el {ultima}")
                color = COLORES[estado]
            else:
                texto, color = "Sin mediciones en el período", "#eeeeee"
            for widget in (tarjeta, titulo, detalle):
                widget.config(bg=color)
            detalle.config(text=texto)

    def leer_formulario(self, con_humedad):
        """Valida los campos del formulario y devuelve (sector, fecha_iso, humedad). Lanza ValueError con el formato esperado."""
        sector = validaciones.validar_codigo_sector(self.campo_sector.get().split(" - ")[0], self.config_datos["sectores"])
        fecha = validaciones.validar_fecha(self.campo_fecha.get().strip(), self.hoy, self.config_datos["ventana_dias"]).isoformat()
        humedad = validaciones.validar_humedad(self.campo_humedad.get().strip()) if con_humedad else None
        return sector, fecha, humedad

    def registrar(self):
        try:
            sector, fecha, humedad = self.leer_formulario(True)
            operaciones.registrar_medicion(self.mediciones, sector, fecha, humedad)
        except ValueError as error:
            messagebox.showerror("Error", str(error))
            return
        self.mensaje_form.config(text="Medición registrada correctamente (se guardará en el archivo al salir).")
        self.campo_humedad.delete(0, tk.END)
        self.refrescar()

    def modificar(self):
        try:
            sector, fecha, _ = self.leer_formulario(False)
            actual = operaciones.buscar_medicion(self.mediciones, sector, fecha)
            nueva = validaciones.validar_humedad(self.campo_humedad.get().strip())
        except ValueError as error:
            messagebox.showerror("Error", str(error))
            return
        if not messagebox.askyesno("Confirmar", f"¿Reemplazar {actual}% por {nueva}% en {sector} el {fecha}?"):
            self.mensaje_form.config(text="Modificación cancelada.")
            return
        operaciones.modificar_medicion(self.mediciones, sector, fecha, nueva)
        self.mensaje_form.config(text="Medición modificada correctamente (se guardará en el archivo al salir).")
        self.campo_humedad.delete(0, tk.END)
        self.refrescar()

    def cerrar(self):
        """Sobrescribe el CSV con el diccionario en memoria; ante un error ofrece reintentar o salir sin guardar."""
        while True:
            try:
                archivos.guardar_registros(self.ruta_registros, self.mediciones)
                break
            except OSError as error:
                if not messagebox.askretrycancel("Error al guardar", f"No se pudo guardar {self.ruta_registros}:\n{error}\n\n¿Reintentar? (Cancelar sale sin guardar)"):
                    break
        self.destroy()


def cargar_historial(ruta, config, hoy):
    """Lee el CSV al diccionario en memoria. Devuelve (mediciones, rechazadas) o None si el archivo es inutilizable."""
    try:
        return archivos.cargar_registros(ruta, config["sectores"], hoy, config["ventana_dias"])
    except FileNotFoundError:
        messagebox.showinfo("Registros", "No se encontró el archivo de registros: se arranca sin historial y se creará al salir.")
        return {codigo: {} for codigo in config["sectores"]}, []
    except (ValueError, OSError) as error:
        # No se continúa: al salir se sobrescribiría el archivo y se perdería su contenido.
        messagebox.showerror("Error", f"Error al leer {ruta}:\n{error}")
        return None


def main():
    carpeta = os.path.dirname(os.path.abspath(__file__))
    hoy = date.today()

    # Los mensajes de error previos a la ventana principal usan una raíz oculta.
    raiz = tk.Tk()
    raiz.withdraw()
    try:
        config = archivos.cargar_configuracion(os.path.join(carpeta, "datos", "configuracion.json"))
        usuarios = autenticacion.cargar_usuarios(os.path.join(carpeta, config["archivos"]["usuarios"]))
    except FileNotFoundError as error:
        messagebox.showerror("Error", f"No se encontró el archivo {error.filename}")
        return
    except json.JSONDecodeError as error:
        messagebox.showerror("Error", f"JSON mal formado ({error})")
        return
    except KeyError as error:
        messagebox.showerror("Error de configuración", str(error.args[0]))
        return
    except (ValueError, OSError) as error:
        messagebox.showerror("Error de configuración", str(error))
        return

    login = VentanaLogin(usuarios)
    raiz.destroy()
    login.mainloop()
    if login.usuario is None:
        return

    # Segunda raíz oculta para los diálogos de carga (la del login ya se cerró).
    raiz = tk.Tk()
    raiz.withdraw()
    ruta_registros = os.path.join(carpeta, config["archivos"]["registros"])
    resultado = cargar_historial(ruta_registros, config, hoy)
    raiz.destroy()
    if resultado is None:
        return
    mediciones, rechazadas = resultado

    App(login.usuario, config, mediciones, rechazadas, ruta_registros, hoy).mainloop()


if __name__ == "__main__":
    main()
