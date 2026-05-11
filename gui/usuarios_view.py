# ============================================================
# MÓDULO: Vista de Gestión de Usuarios
# PROYECTO: Sistema Integral de Gestión - Software FJ
# AUTOR: César David Toro Fernández
# DESCRIPCIÓN: Ventana secundaria para registro y consulta
#              de clientes del sistema, conectada directamente
#              al backend de Usuario mediante UserController.
# ============================================================

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from models.cliente import Cliente
from exceptions.custom import ClienteInvalidoError
from services.logger import Logger


class UsuariosView(ttk.Toplevel):
    """
    Vista modal para gestión integral de clientes. Permite registrar
    nuevos clientes con validación en tiempo real y consultar clientes
    existentes por nombre, mostrando resultados en tabla dinámica.
    """

    _logger = Logger()

    def __init__(self, parent):
        super().__init__(parent)
        self.parent   = parent
        self.title("Software FJ — Gestión de Clientes")
        self.geometry("800x600")
        self.resizable(True, True)
        self.grab_set()
        self._next_id = len(parent.clientes) + 1
        self._build_ui()

    # -------------------------------------------------------
    # CONSTRUCCIÓN DE INTERFAZ
    # -------------------------------------------------------

    def _build_ui(self):
        """Construye la interfaz completa del módulo de clientes."""

        # Header del módulo
        ttk.Label(
            self, text="GESTIÓN DE CLIENTES",
            font=("Helvetica", 20, "bold"), bootstyle=PRIMARY
        ).pack(pady=(20, 5))

        ttk.Separator(self, orient=HORIZONTAL).pack(fill=X, padx=20)

        # Notebook con pestañas Registrar / Consultar
        notebook = ttk.Notebook(self, bootstyle=PRIMARY)
        notebook.pack(fill=BOTH, expand=True, padx=20, pady=15)

        # Pestaña 1 — Registro de cliente
        tab_registro = ttk.Frame(notebook, padding=20)
        notebook.add(tab_registro, text="  Registrar Cliente  ")
        self._build_registro(tab_registro)

        # Pestaña 2 — Consulta de clientes
        tab_consulta = ttk.Frame(notebook, padding=20)
        notebook.add(tab_consulta, text="  Consultar Clientes  ")
        self._build_consulta(tab_consulta)

    def _build_registro(self, parent):
        """Construye el formulario de registro de nuevos clientes."""

        campos = [
            ("Nombre",    "entry_nombre"),
            ("Apellido",  "entry_apellido"),
            ("Teléfono",  "entry_telefono"),
            ("Email",     "entry_email"),
        ]

        form = ttk.Frame(parent)
        form.pack(fill=X, pady=10)

        for i, (label, attr) in enumerate(campos):
            ttk.Label(form, text=label, font=("Helvetica", 11)).grid(
                row=i, column=0, sticky=W, pady=8, padx=(0, 20)
            )
            entry = ttk.Entry(form, width=35, font=("Helvetica", 11))
            entry.grid(row=i, column=1, sticky=EW, pady=8)
            setattr(self, attr, entry)

        form.columnconfigure(1, weight=1)

        # Botón de registro
        ttk.Button(
            parent, text="REGISTRAR CLIENTE",
            bootstyle=SUCCESS, width=25,
            command=self._registrar_cliente
        ).pack(pady=20)

        # Área de feedback
        self.lbl_feedback_reg = ttk.Label(
            parent, text="", font=("Helvetica", 10)
        )
        self.lbl_feedback_reg.pack()

    def _build_consulta(self, parent):
        """Construye el panel de consulta y listado de clientes."""

        # Buscador por nombre
        search_frame = ttk.Frame(parent)
        search_frame.pack(fill=X, pady=(0, 15))

        ttk.Label(search_frame, text="Buscar por nombre:", font=("Helvetica", 11)).pack(side=LEFT, padx=(0, 10))
        self.entry_buscar = ttk.Entry(search_frame, width=25, font=("Helvetica", 11))
        self.entry_buscar.pack(side=LEFT, padx=(0, 10))

        ttk.Button(
            search_frame, text="Buscar",
            bootstyle=PRIMARY, command=self._buscar_cliente
        ).pack(side=LEFT, padx=(0, 10))

        ttk.Button(
            search_frame, text="Ver Todos",
            bootstyle=SECONDARY, command=self._cargar_tabla
        ).pack(side=LEFT)

        # Tabla de resultados
        cols = ("ID", "Nombre", "Apellido", "Teléfono", "Email")
        self.tabla = ttk.Treeview(parent, columns=cols, show="headings", bootstyle=PRIMARY)

        for col in cols:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=130, anchor=CENTER)

        self.tabla.pack(fill=BOTH, expand=True)

        # Scrollbar
        scroll = ttk.Scrollbar(parent, orient=VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)
        scroll.pack(side=RIGHT, fill=Y)

        self._cargar_tabla()

    # -------------------------------------------------------
    # LÓGICA DE NEGOCIO — Registro y consulta de clientes
    # -------------------------------------------------------

    def _registrar_cliente(self):
        """Valida los campos del formulario y registra un nuevo cliente."""
        try:
            cliente = Cliente(
                cliente_id=self._next_id,
                nombre=self.entry_nombre.get().strip(),
                apellido=self.entry_apellido.get().strip(),
                telefono=self.entry_telefono.get().strip(),
                email=self.entry_email.get().strip()
            )
            self.parent.clientes.append(cliente)
            self._next_id += 1

            self._logger.info(f"Cliente registrado desde GUI: {cliente}")
            self.lbl_feedback_reg.config(
                text=f"✅ Cliente '{cliente.get_nombre()}' registrado exitosamente.",
                bootstyle=SUCCESS
            )

            # Limpiar formulario
            for attr in ["entry_nombre", "entry_apellido", "entry_telefono", "entry_email"]:
                getattr(self, attr).delete(0, END)

        except ClienteInvalidoError as e:
            self.lbl_feedback_reg.config(
                text=f"❌ {e.mensaje}", bootstyle=DANGER
            )
            self._logger.error(f"Error registrando cliente desde GUI: {e.mensaje}")

        except Exception as e:
            self.lbl_feedback_reg.config(
                text=f"❌ Error inesperado: {str(e)}", bootstyle=DANGER
            )
            self._logger.error(f"Error inesperado en registro de cliente: {str(e)}")

    def _buscar_cliente(self):
        """Filtra la tabla mostrando solo clientes que coincidan con el nombre."""
        nombre = self.entry_buscar.get().strip().lower()
        self.tabla.delete(*self.tabla.get_children())

        resultados = [
            c for c in self.parent.clientes
            if nombre in c.get_nombre().lower()
        ]

        for c in resultados:
            self.tabla.insert("", END, values=(
                c.id, c.get_nombre(), c.get_apellido(),
                c.get_telefono(), c.get_email()
            ))

        if not resultados:
            self._logger.warning(f"Búsqueda sin resultados para: '{nombre}'")

    def _cargar_tabla(self):
        """Carga todos los clientes registrados en la tabla de resultados."""
        self.tabla.delete(*self.tabla.get_children())
        for c in self.parent.clientes:
            self.tabla.insert("", END, values=(
                c.id, c.get_nombre(), c.get_apellido(),
                c.get_telefono(), c.get_email()
            ))