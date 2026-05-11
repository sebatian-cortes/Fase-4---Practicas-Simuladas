# ============================================================
# MÓDULO: Vista de Gestión de Servicios
# PROYECTO: Sistema Integral de Gestión - Software FJ
# AUTOR: César David Toro Fernández
# DESCRIPCIÓN: Ventana secundaria para configuración y registro
#              de los tres servicios especializados del sistema:
#              Salas, Equipos y Asesorías. Conectada al backend
#              de modelos con validaciones y logs integrados.
# ============================================================

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from models.servicios.sala import ReservaSala
from models.servicios.equipo import AlquilerEquipo
from models.servicios.asesoria import AsesoriaEspecializada
from exceptions.custom import (
    ServicioNoDisponibleError,
    ParametroFaltanteError,
    DuracionInvalidaError
)
from services.logger import Logger


class ServiciosView(ttk.Toplevel):
    """
    Vista modal para registro y administración de servicios.
    Renderiza un formulario dinámico adaptado al tipo de servicio
    seleccionado desde la pantalla principal del sistema.
    """

    _logger = Logger()

    # Configuración visual por tipo de servicio
    _CONFIG = {
        "sala": {
            "titulo":     "RESERVA DE SALAS EJECUTIVAS",
            "bootstyle":  "info",
            "emoji":      "🏢"
        },
        "equipo": {
            "titulo":     "ALQUILER DE EQUIPOS TECNOLÓGICOS",
            "bootstyle":  "primary",
            "emoji":      "💻"
        },
        "asesoria": {
            "titulo":     "ASESORÍAS ESPECIALIZADAS",
            "bootstyle":  "success",
            "emoji":      "🎓"
        }
    }

    def __init__(self, parent, tipo: str):
        super().__init__(parent)
        self.parent  = parent
        self.tipo    = tipo
        self.config  = self._CONFIG[tipo]
        self._next_id = len(parent.servicios) + 1

        self.title(f"Software FJ — {self.config['titulo']}")
        self.geometry("750x580")
        self.resizable(True, True)
        self.grab_set()
        self._build_ui()

    # -------------------------------------------------------
    # CONSTRUCCIÓN DE INTERFAZ
    # -------------------------------------------------------

    def _build_ui(self):
        """Construye la interfaz adaptada al tipo de servicio activo."""

        style = self.config["bootstyle"]

        # Header del módulo
        ttk.Label(
            self,
            text=f"{self.config['emoji']}  {self.config['titulo']}",
            font=("Helvetica", 18, "bold"),
            bootstyle=style
        ).pack(pady=(20, 5))

        ttk.Separator(self, orient=HORIZONTAL).pack(fill=X, padx=20)

        # Notebook con pestañas
        notebook = ttk.Notebook(self, bootstyle=style)
        notebook.pack(fill=BOTH, expand=True, padx=20, pady=15)

        # Pestaña 1 — Registrar servicio
        tab_registro = ttk.Frame(notebook, padding=20)
        notebook.add(tab_registro, text="  Registrar Servicio  ")
        self._build_form(tab_registro)

        # Pestaña 2 — Ver servicios registrados
        tab_lista = ttk.Frame(notebook, padding=20)
        notebook.add(tab_lista, text="  Servicios Registrados  ")
        self._build_lista(tab_lista)

    def _build_form(self, parent):
        """Renderiza el formulario dinámico según el tipo de servicio."""

        form = ttk.Frame(parent)
        form.pack(fill=X, pady=10)

        style = self.config["bootstyle"]
        row   = 0

        # ── Campos comunes a todos los servicios ──────────────
        ttk.Label(form, text="Duración (horas):", font=("Helvetica", 11)).grid(
            row=row, column=0, sticky=W, pady=8, padx=(0, 20)
        )
        self.entry_duracion = ttk.Entry(form, width=30, font=("Helvetica", 11))
        self.entry_duracion.grid(row=row, column=1, sticky=EW, pady=8)
        row += 1

        # ── Campos específicos por tipo ────────────────────────
        if self.tipo == "sala":
            ttk.Label(form, text="Capacidad (personas):", font=("Helvetica", 11)).grid(
                row=row, column=0, sticky=W, pady=8, padx=(0, 20)
            )
            self.entry_capacidad = ttk.Entry(form, width=30, font=("Helvetica", 11))
            self.entry_capacidad.grid(row=row, column=1, sticky=EW, pady=8)
            row += 1

        elif self.tipo == "equipo":
            ttk.Label(form, text="Tipo de equipo:", font=("Helvetica", 11)).grid(
                row=row, column=0, sticky=W, pady=8, padx=(0, 20)
            )
            self.combo_equipo = ttk.Combobox(
                form,
                values=["laptop", "servidor", "proyector", "camara", "drone"],
                state="readonly", width=28, font=("Helvetica", 11)
            )
            self.combo_equipo.current(0)
            self.combo_equipo.grid(row=row, column=1, sticky=EW, pady=8)
            row += 1

            ttk.Label(form, text="Cantidad:", font=("Helvetica", 11)).grid(
                row=row, column=0, sticky=W, pady=8, padx=(0, 20)
            )
            self.entry_cantidad = ttk.Entry(form, width=30, font=("Helvetica", 11))
            self.entry_cantidad.insert(0, "1")
            self.entry_cantidad.grid(row=row, column=1, sticky=EW, pady=8)
            row += 1

        elif self.tipo == "asesoria":
            ttk.Label(form, text="Nivel:", font=("Helvetica", 11)).grid(
                row=row, column=0, sticky=W, pady=8, padx=(0, 20)
            )
            self.combo_nivel = ttk.Combobox(
                form,
                values=["basico", "avanzado", "experto"],
                state="readonly", width=28, font=("Helvetica", 11)
            )
            self.combo_nivel.current(0)
            self.combo_nivel.grid(row=row, column=1, sticky=EW, pady=8)
            row += 1

            ttk.Label(form, text="Nombre del Asesor:", font=("Helvetica", 11)).grid(
                row=row, column=0, sticky=W, pady=8, padx=(0, 20)
            )
            self.entry_asesor = ttk.Entry(form, width=30, font=("Helvetica", 11))
            self.entry_asesor.grid(row=row, column=1, sticky=EW, pady=8)
            row += 1

        form.columnconfigure(1, weight=1)

        # Botón de registro
        ttk.Button(
            parent,
            text="REGISTRAR SERVICIO",
            bootstyle=self.config["bootstyle"],
            width=25,
            command=self._registrar_servicio
        ).pack(pady=20)

        # Área de feedback
        self.lbl_feedback = ttk.Label(parent, text="", font=("Helvetica", 10))
        self.lbl_feedback.pack()

    def _build_lista(self, parent):
        """Construye la tabla de servicios registrados del tipo activo."""

        cols = ("ID", "Nombre", "Precio Base", "Disponible", "Detalle")
        self.tabla = ttk.Treeview(
            parent, columns=cols,
            show="headings",
            bootstyle=self.config["bootstyle"]
        )

        anchos = [50, 220, 130, 90, 220]
        for col, ancho in zip(cols, anchos):
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=ancho, anchor=CENTER)

        self.tabla.pack(fill=BOTH, expand=True)

        scroll = ttk.Scrollbar(parent, orient=VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)
        scroll.pack(side=RIGHT, fill=Y)

        ttk.Button(
            parent, text="Actualizar lista",
            bootstyle=SECONDARY,
            command=self._cargar_tabla
        ).pack(pady=10)

        self._cargar_tabla()

    # -------------------------------------------------------
    # LÓGICA DE NEGOCIO — Registro de servicios
    # -------------------------------------------------------

    def _registrar_servicio(self):
        """Valida el formulario y registra el servicio correspondiente."""
        try:
            duracion = int(self.entry_duracion.get().strip())

            if self.tipo == "sala":
                capacidad = int(self.entry_capacidad.get().strip())
                servicio  = ReservaSala(self._next_id, capacidad)
                costo     = servicio.calcular_costo(duracion)

            elif self.tipo == "equipo":
                tipo_eq  = self.combo_equipo.get()
                cantidad = int(self.entry_cantidad.get().strip())
                servicio = AlquilerEquipo(self._next_id, tipo_eq, cantidad)
                costo    = servicio.calcular_costo(duracion)

            elif self.tipo == "asesoria":
                nivel   = self.combo_nivel.get()
                asesor  = self.entry_asesor.get().strip()
                servicio = AsesoriaEspecializada(self._next_id, nivel, asesor)
                costo    = servicio.calcular_costo_con_iva(duracion)

            self.parent.servicios.append(servicio)
            self._next_id += 1

            self._logger.info(f"Servicio registrado desde GUI: {servicio}")
            self.lbl_feedback.config(
                text=f"✅ Servicio registrado | Costo estimado: ${costo:,.0f} COP",
                bootstyle=SUCCESS
            )
            self._cargar_tabla()

        except ValueError:
            self.lbl_feedback.config(
                text="❌ Duración y cantidad deben ser números enteros.",
                bootstyle=DANGER
            )
        except (ServicioNoDisponibleError, ParametroFaltanteError, DuracionInvalidaError) as e:
            self.lbl_feedback.config(text=f"❌ {e.mensaje}", bootstyle=DANGER)
            self._logger.error(f"Error registrando servicio desde GUI: {e.mensaje}")
        except Exception as e:
            self.lbl_feedback.config(text=f"❌ Error inesperado: {str(e)}", bootstyle=DANGER)
            self._logger.error(f"Error inesperado registrando servicio: {str(e)}")

    def _cargar_tabla(self):
        """Carga en la tabla todos los servicios del tipo activo registrados."""
        self.tabla.delete(*self.tabla.get_children())
        filtrados = [
            s for s in self.parent.servicios
            if type(s).__name__.lower().find(
                {"sala": "sala", "equipo": "alquiler", "asesoria": "asesoria"}[self.tipo]
            ) >= 0
        ]
        for s in filtrados:
            d = s.to_dict()
            self.tabla.insert("", END, values=(
                d["id"],
                d["nombre"],
                f"${d['precio_base']:,.0f} COP",
                "✅ Sí" if d["disponible"] else "❌ No",
                s.describir()[:50] + "..."
            ))