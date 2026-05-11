# ============================================================
# MÓDULO: Aplicación Principal - Ventana Central
# PROYECTO: Sistema Integral de Gestión - Software FJ
# AUTOR: César David Toro Fernández
# DESCRIPCIÓN: Ventana principal del sistema con navegación
#              centralizada hacia los tres módulos operativos,
#              fondo animado dinámico e internacionalización.
# ============================================================

import math
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from gui.usuarios_view import UsuariosView
from gui.servicios_view import ServiciosView
from gui.reservas_view import ReservasView


class SoftwareFJ_App(ttk.Window):
    """
    Ventana principal del sistema Software FJ. Orquesta la navegación
    entre los módulos operativos y mantiene el estado global compartido
    entre vistas, incluyendo clientes, servicios y reservas activas.
    """

    def __init__(self):
        super().__init__(themename="cosmo")
        self.title("Software FJ - Sistema Integral de Gestión")
        self.geometry("1200x850")
        self.resizable(True, True)

        # Estado global compartido entre todas las vistas
        self.clientes  = []
        self.servicios = []
        self.reservas  = []

        # Control de animación de fondo
        self.angle = 0

        # Diccionario maestro de internacionalización
        self.texts = {
            "en": {
                "welcome":  "INTEGRATED MANAGEMENT SYSTEM",
                "subtitle": "Select a specialized service to begin",
                "room":     "Room Reservation",
                "room_desc":"High-tech spaces for executive meetings.",
                "equip":    "Equipment Rental",
                "equip_desc":"Pro-level hardware for intensive workloads.",
                "consult":  "Specialized Consultancy",
                "consult_desc":"Strategic advice for software architecture.",
                "manage":   "OPEN SERVICE",
                "footer":   "Software FJ  —  Internal Operations Portal"
            },
            "es": {
                "welcome":  "SISTEMA INTEGRAL DE GESTIÓN",
                "subtitle": "Seleccione un servicio especializado para comenzar",
                "room":     "Reserva de Salas",
                "room_desc":"Espacios de alta tecnología para reuniones ejecutivas.",
                "equip":    "Alquiler de Equipos",
                "equip_desc":"Hardware nivel profesional para cargas intensas.",
                "consult":  "Asesoría Especializada",
                "consult_desc":"Consultoría estratégica en arquitectura de software.",
                "manage":   "ABRIR SERVICIO",
                "footer":   "Software FJ  —  Portal de Operaciones Internas"
            }
        }

        self.current_lang = "es"
        self._setup_ui()
        self._animate_background()

    # -------------------------------------------------------
    # CONSTRUCCIÓN DE INTERFAZ
    # -------------------------------------------------------

    def _setup_ui(self):
        """Construye la estructura visual principal de la aplicación."""

        # Canvas de fondo animado
        self.canvas = ttk.Canvas(self, highlightthickness=0)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)

        # Selector de idioma — esquina superior derecha
        lang_frame = ttk.Frame(self)
        lang_frame.place(relx=0.98, rely=0.02, anchor=NE)

        self.combo_lang = ttk.Combobox(
            lang_frame, values=["Español", "English"],
            state="readonly", width=12
        )
        self.combo_lang.current(0)
        self.combo_lang.pack()
        self.combo_lang.bind("<<ComboboxSelected>>", self._update_language)

        # Contenedor central principal
        self.main_frame = ttk.Frame(self, bootstyle=DEFAULT)
        self.main_frame.place(relx=0.5, rely=0.5, anchor=CENTER, relwidth=0.9)

        self._render_content()

    def _render_content(self):
        """Renderiza los componentes visuales según el idioma activo."""

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        t = self.texts[self.current_lang]

        # Header
        ttk.Label(
            self.main_frame, text=t["welcome"],
            font=("Helvetica", 28, "bold"), anchor=CENTER
        ).pack(pady=(0, 5))

        ttk.Label(
            self.main_frame, text=t["subtitle"],
            font=("Helvetica", 12), bootstyle=SECONDARY, anchor=CENTER
        ).pack(pady=(0, 50))

        # Tarjetas de servicios
        card_container = ttk.Frame(self.main_frame)
        card_container.pack(fill=X)

        servicios_config = [
            (t["room"],    t["room_desc"],    "info",    self._abrir_salas),
            (t["equip"],   t["equip_desc"],   "primary", self._abrir_equipos),
            (t["consult"], t["consult_desc"], "success", self._abrir_asesorias),
        ]

        for i, (titulo, desc, color, comando) in enumerate(servicios_config):
            card = ttk.Labelframe(card_container, text=f" 0{i+1} ", padding=30, bootstyle=color)
            card.grid(row=0, column=i, padx=15, sticky=NSEW)
            card_container.columnconfigure(i, weight=1)

            ttk.Label(card, text=titulo, font=("Helvetica", 14, "bold"), wraplength=200).pack(pady=10)
            ttk.Label(card, text=desc, font=("Helvetica", 10), wraplength=200, justify=CENTER).pack(pady=10)
            ttk.Button(card, text=t["manage"], bootstyle=color, width=20, command=comando).pack(pady=15)

        # Footer
        ttk.Label(
            self.main_frame, text=t["footer"],
            font=("Helvetica", 9), bootstyle=SECONDARY
        ).pack(pady=(60, 0))

    # -------------------------------------------------------
    # NAVEGACIÓN — Apertura de módulos especializados
    # -------------------------------------------------------

    def _abrir_salas(self):
        """Abre el módulo de gestión de reservas de salas."""
        ServiciosView(self, tipo="sala")

    def _abrir_equipos(self):
        """Abre el módulo de gestión de alquiler de equipos."""
        ServiciosView(self, tipo="equipo")

    def _abrir_asesorias(self):
        """Abre el módulo de gestión de asesorías especializadas."""
        ServiciosView(self, tipo="asesoria")

    # -------------------------------------------------------
    # IDIOMA — Actualización dinámica de textos
    # -------------------------------------------------------

    def _update_language(self, event):
        """Gestiona el cambio de idioma en toda la interfaz."""
        self.current_lang = "es" if self.combo_lang.get() == "Español" else "en"
        self._render_content()

    # -------------------------------------------------------
    # ANIMACIÓN — Fondo dinámico con oscilación de color
    # -------------------------------------------------------

    def _animate_background(self):
        """Genera un efecto de gradiente en movimiento sobre el fondo."""
        self.angle += 0.02
        val = int(240 + 10 * math.sin(self.angle))
        color = f'#{val:02x}{val:02x}{min(val+5, 255):02x}'
        self.canvas.config(bg=color)
        self.after(50, self._animate_background)