# ============================================================
# MÓDULO: Vista de Gestión de Reservas
# PROYECTO: Sistema Integral de Gestión - Software FJ
# AUTOR: César David Toro Fernández
# DESCRIPCIÓN: Ventana secundaria para creación, confirmación,
#              cancelación y procesamiento de reservas. Integra
#              clientes y servicios registrados en el sistema
#              con validaciones completas y registro de logs.
# ============================================================

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from models.reserva import Reserva
from exceptions.custom import (
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    DuracionInvalidaError,
    ServicioNoDisponibleError
)
from services.logger import Logger


class ReservasView(ttk.Toplevel):
    """
    Vista modal para gestión integral del ciclo de vida de reservas.
    Permite crear, confirmar, cancelar y procesar reservas vinculando
    clientes y servicios previamente registrados en el sistema.
    """

    _logger = Logger()

    def __init__(self, parent):
        super().__init__(parent)
        self.parent   = parent
        self.title("Software FJ — Gestión de Reservas")
        self.geometry("900x650")
        self.resizable(True, True)
        self.grab_set()
        self._next_id = len(parent.reservas) + 1
        self._build_ui()

    # -------------------------------------------------------
    # CONSTRUCCIÓN DE INTERFAZ
    # -------------------------------------------------------

    def _build_ui(self):
        """Construye la interfaz completa del módulo de reservas."""

        ttk.Label(
            self, text="📋  GESTIÓN DE RESERVAS",
            font=("Helvetica", 20, "bold"), bootstyle=WARNING
        ).pack(pady=(20, 5))

        ttk.Separator(self, orient=HORIZONTAL).pack(fill=X, padx=20)

        notebook = ttk.Notebook(self, bootstyle=WARNING)
        notebook.pack(fill=BOTH, expand=True, padx=20, pady=15)

        # Pestaña 1 — Crear reserva
        tab_crear = ttk.Frame(notebook, padding=20)
        notebook.add(tab_crear, text="  Nueva Reserva  ")
        self._build_crear(tab_crear)

        # Pestaña 2 — Administrar reservas
        tab_admin = ttk.Frame(notebook, padding=20)
        notebook.add(tab_admin, text="  Administrar Reservas  ")
        self._build_admin(tab_admin)

    def _build_crear(self, parent):
        """Construye el formulario de creación de nuevas reservas."""

        form = ttk.Frame(parent)
        form.pack(fill=X, pady=10)

        # Selector de cliente
        ttk.Label(form, text="Cliente:", font=("Helvetica", 11)).grid(
            row=0, column=0, sticky=W, pady=8, padx=(0, 20)
        )
        self.combo_cliente = ttk.Combobox(
            form, state="readonly", width=35, font=("Helvetica", 11)
        )
        self.combo_cliente.grid(row=0, column=1, sticky=EW, pady=8)

        # Selector de servicio
        ttk.Label(form, text="Servicio:", font=("Helvetica", 11)).grid(
            row=1, column=0, sticky=W, pady=8, padx=(0, 20)
        )
        self.combo_servicio = ttk.Combobox(
            form, state="readonly", width=35, font=("Helvetica", 11)
        )
        self.combo_servicio.grid(row=1, column=1, sticky=EW, pady=8)

        # Duración
        ttk.Label(form, text="Duración (horas):", font=("Helvetica", 11)).grid(
            row=2, column=0, sticky=W, pady=8, padx=(0, 20)
        )
        self.entry_duracion = ttk.Entry(form, width=35, font=("Helvetica", 11))
        self.entry_duracion.grid(row=2, column=1, sticky=EW, pady=8)

        # Descuento opcional
        ttk.Label(form, text="Descuento % (opcional):", font=("Helvetica", 11)).grid(
            row=3, column=0, sticky=W, pady=8, padx=(0, 20)
        )
        self.entry_descuento = ttk.Entry(form, width=35, font=("Helvetica", 11))
        self.entry_descuento.insert(0, "0")
        self.entry_descuento.grid(row=3, column=1, sticky=EW, pady=8)

        form.columnconfigure(1, weight=1)

        # Botón actualizar selectores
        ttk.Button(
            parent, text="🔄 Actualizar listas",
            bootstyle=SECONDARY, width=20,
            command=self._actualizar_combos
        ).pack(pady=(10, 0))

        # Botón crear reserva
        ttk.Button(
            parent, text="CREAR RESERVA",
            bootstyle=WARNING, width=25,
            command=self._crear_reserva
        ).pack(pady=15)

        # Feedback
        self.lbl_feedback = ttk.Label(parent, text="", font=("Helvetica", 10))
        self.lbl_feedback.pack()

        self._actualizar_combos()

    def _build_admin(self, parent):
        """Construye el panel de administración del ciclo de vida de reservas."""

        # Tabla de reservas
        cols = ("ID", "Cliente", "Servicio", "Horas", "Costo", "Estado")
        self.tabla = ttk.Treeview(
            parent, columns=cols,
            show="headings", bootstyle=WARNING
        )

        anchos = [50, 180, 200, 60, 130, 100]
        for col, ancho in zip(cols, anchos):
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=ancho, anchor=CENTER)

        self.tabla.pack(fill=BOTH, expand=True)

        scroll = ttk.Scrollbar(parent, orient=VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)
        scroll.pack(side=RIGHT, fill=Y)

        # Botones de acción
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=X, pady=10)

        ttk.Button(
            btn_frame, text="✅ Confirmar",
            bootstyle=SUCCESS, width=16,
            command=self._confirmar_reserva
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            btn_frame, text="⚙️ Procesar",
            bootstyle=PRIMARY, width=16,
            command=self._procesar_reserva
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            btn_frame, text="❌ Cancelar",
            bootstyle=DANGER, width=16,
            command=self._cancelar_reserva
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            btn_frame, text="🔄 Actualizar",
            bootstyle=SECONDARY, width=16,
            command=self._cargar_tabla
        ).pack(side=LEFT, padx=5)

        # Feedback administración
        self.lbl_feedback_admin = ttk.Label(
            parent, text="", font=("Helvetica", 10)
        )
        self.lbl_feedback_admin.pack()

        self._cargar_tabla()

    # -------------------------------------------------------
    # LÓGICA DE NEGOCIO — Ciclo de vida de reservas
    # -------------------------------------------------------

    def _actualizar_combos(self):
        """Sincroniza los selectores con los clientes y servicios registrados."""
        self.combo_cliente["values"] = [
            f"{c.id} — {c.get_nombre()} {c.get_apellido()}"
            for c in self.parent.clientes
        ]
        self.combo_servicio["values"] = [
            f"{s.id} — {s.nombre}"
            for s in self.parent.servicios
            if s.disponible
        ]
        if self.parent.clientes:
            self.combo_cliente.current(0)
        if self.parent.servicios:
            self.combo_servicio.current(0)

    def _crear_reserva(self):
        """Valida los campos y crea una nueva reserva en el sistema."""
        try:
            if not self.parent.clientes:
                raise ReservaInvalidaError("No hay clientes registrados. Registre un cliente primero.")
            if not self.parent.servicios:
                raise ReservaInvalidaError("No hay servicios registrados. Registre un servicio primero.")

            idx_cliente  = self.combo_cliente.current()
            idx_servicio = self.combo_servicio.current()
            duracion     = int(self.entry_duracion.get().strip())
            descuento    = float(self.entry_descuento.get().strip())

            cliente  = self.parent.clientes[idx_cliente]
            servicio = self.parent.servicios[idx_servicio]

            reserva = Reserva(self._next_id, cliente, servicio, duracion)

            if descuento > 0:
                reserva.confirmar()
                costo_final = reserva.procesar(descuento)
                msg = (
                    f"✅ Reserva #{reserva.id} creada, confirmada y procesada | "
                    f"Descuento: {descuento}% | Total: ${costo_final:,.0f} COP"
                )
            else:
                msg = f"✅ Reserva #{reserva.id} creada | Costo: ${reserva.costo:,.0f} COP | Estado: PENDIENTE"

            self.parent.reservas.append(reserva)
            self._next_id += 1

            self._logger.info(f"Reserva creada desde GUI: {reserva}")
            self.lbl_feedback.config(text=msg, bootstyle=SUCCESS)
            self._cargar_tabla()

        except ValueError:
            self.lbl_feedback.config(
                text="❌ Duración y descuento deben ser valores numéricos.",
                bootstyle=DANGER
            )
        except (ReservaInvalidaError, DuracionInvalidaError, ServicioNoDisponibleError) as e:
            self.lbl_feedback.config(text=f"❌ {e.mensaje}", bootstyle=DANGER)
            self._logger.error(f"Error creando reserva desde GUI: {e.mensaje}")
        except Exception as e:
            self.lbl_feedback.config(text=f"❌ Error inesperado: {str(e)}", bootstyle=DANGER)
            self._logger.error(f"Error inesperado creando reserva: {str(e)}")

    def _get_reserva_seleccionada(self):
        """Retorna la reserva seleccionada en la tabla o None si no hay selección."""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione una reserva de la tabla.")
            return None
        reserva_id = int(self.tabla.item(seleccion[0])["values"][0])
        return next((r for r in self.parent.reservas if r.id == reserva_id), None)

    def _confirmar_reserva(self):
        """Confirma la reserva seleccionada en la tabla."""
        try:
            reserva = self._get_reserva_seleccionada()
            if not reserva:
                return
            reserva.confirmar()
            self.lbl_feedback_admin.config(
                text=f"✅ Reserva #{reserva.id} confirmada exitosamente.",
                bootstyle=SUCCESS
            )
            self._cargar_tabla()
        except OperacionNoPermitidaError as e:
            self.lbl_feedback_admin.config(text=f"❌ {e.mensaje}", bootstyle=DANGER)
            self._logger.error(f"Error confirmando reserva: {e.mensaje}")

    def _procesar_reserva(self):
        """Procesa la reserva confirmada seleccionada en la tabla."""
        try:
            reserva = self._get_reserva_seleccionada()
            if not reserva:
                return
            costo = reserva.procesar()
            self.lbl_feedback_admin.config(
                text=f"⚙️ Reserva #{reserva.id} procesada | Total: ${costo:,.0f} COP",
                bootstyle=PRIMARY
            )
            self._cargar_tabla()
        except OperacionNoPermitidaError as e:
            self.lbl_feedback_admin.config(text=f"❌ {e.mensaje}", bootstyle=DANGER)
            self._logger.error(f"Error procesando reserva: {e.mensaje}")

    def _cancelar_reserva(self):
        """Cancela la reserva seleccionada en la tabla."""
        try:
            reserva = self._get_reserva_seleccionada()
            if not reserva:
                return
            confirmar = messagebox.askyesno(
                "Confirmar cancelación",
                f"¿Está seguro que desea cancelar la Reserva #{reserva.id}?"
            )
            if confirmar:
                reserva.cancelar()
                self.lbl_feedback_admin.config(
                    text=f"❌ Reserva #{reserva.id} cancelada.",
                    bootstyle=WARNING
                )
                self._cargar_tabla()
        except OperacionNoPermitidaError as e:
            self.lbl_feedback_admin.config(text=f"❌ {e.mensaje}", bootstyle=DANGER)
            self._logger.error(f"Error cancelando reserva: {e.mensaje}")

    def _cargar_tabla(self):
        """Carga todas las reservas registradas en la tabla de administración."""
        self.tabla.delete(*self.tabla.get_children())
        for r in self.parent.reservas:
            self.tabla.insert("", END, values=(
                r.id,
                f"{r.cliente.get_nombre()} {r.cliente.get_apellido()}",
                r.servicio.nombre,
                f"{r.duracion}h",
                f"${r.costo:,.0f} COP",
                r.estado.upper()
            ))