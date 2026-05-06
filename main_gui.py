# ----------------------------------------------------------------------------
# PROYECTO: Sistema Integral de Gestión Software FJ
# COMPONENTE: Interfaz de Usuario Premium (UX/UI Dinámica)
# AUTOR: César David Toro Fernández
# TECNOLOGÍAS: Python 3.14 / ttkbootstrap (Customized Canvas)
# ----------------------------------------------------------------------------

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import math

class SoftwareFJ_GUI(ttk.Window):
    """
    Interfaz avanzada con fondo animado sutil y arquitectura de 
    vistas centralizadas para Software FJ.
    """
    def __init__(self):
        super().__init__(themename="cosmo")
        self.title("Software FJ - Digital Experience")
        self.geometry("1200x850")
        
        self.current_lang = "en"
        self.angle = 0 # Para el movimiento del fondo
        
        # Diccionario maestro de internacionalización
        self.texts = {
            "en": {
                "welcome": "INTEGRATED MANAGEMENT SYSTEM",
                "subtitle": "Select a specialized service to begin",
                "btn_lang": "Language: English",
                "room": "Room Reservation",
                "room_desc": "High-tech spaces for executive meetings.",
                "equip": "Equipment Rental",
                "equip_desc": "Pro-level hardware for intensive workloads.",
                "consult": "Specialized Consultancy",
                "consult_desc": "Strategic advice for software architecture.",
                "manage": "OPEN SERVICE",
                "footer": "Software FJ - Internal Operations Portal"
            },
            "es": {
                "welcome": "SISTEMA INTEGRAL DE GESTIÓN",
                "subtitle": "Seleccione un servicio especializado para comenzar",
                "btn_lang": "Idioma: Español",
                "room": "Reserva de Salas",
                "room_desc": "Espacios de alta tecnología para reuniones ejecutivas.",
                "equip": "Alquiler de Equipos",
                "equip_desc": "Hardware nivel profesional para cargas intensas.",
                "consult": "Asesoría Especializada",
                "consult_desc": "Consultoría estratégica en arquitectura de software.",
                "manage": "ABRIR SERVICIO",
                "footer": "Software FJ - Portal de Operaciones Internas"
            }
        }
        
        self.setup_ui()
        self.animate_background()

    def setup_ui(self):
        """Estructura visual centrada con fondo dinámico."""
        # Canvas para el fondo con movimiento sutil
        self.canvas = ttk.Canvas(self, highlightthickness=0)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)

        # Contenedor principal centrado
        self.main_frame = ttk.Frame(self, bootstyle=DEFAULT)
        self.main_frame.place(relx=0.5, rely=0.5, anchor=CENTER, relwidth=0.9)

        # Selector de idioma (Dropdown/Combobox)
        lang_frame = ttk.Frame(self)
        lang_frame.place(relx=0.98, rely=0.02, anchor=NE)
        
        self.combo_lang = ttk.Combobox(lang_frame, values=["English", "Español"], state="readonly", width=12)
        self.combo_lang.current(0)
        self.combo_lang.pack()
        self.combo_lang.bind("<<ComboboxSelected>>", self.update_language)

        self.render_content()

    def render_content(self):
        """Genera los componentes visuales alineados al centro."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        t = self.texts[self.current_lang]

        # Header Principal
        ttk.Label(self.main_frame, text=t["welcome"], font=("Helvetica", 28, "bold"), 
                  anchor=CENTER).pack(pady=(0, 5))
        ttk.Label(self.main_frame, text=t["subtitle"], font=("Helvetica", 12), 
                  bootstyle=SECONDARY, anchor=CENTER).pack(pady=(0, 50))

        # Grid de tarjetas centrado
        card_container = ttk.Frame(self.main_frame)
        card_container.pack(fill=X)

        services = [
            (t["room"], t["room_desc"], "info"),
            (t["equip"], t["equip_desc"], "primary"),
            (t["consult"], t["consult_desc"], "success")
        ]

        for i, (title, desc, color) in enumerate(services):
            card = ttk.Labelframe(card_container, text=f" 0{i+1} ", padding=30, bootstyle=color)
            card.grid(row=0, column=i, padx=15, sticky=NSEW)
            card_container.columnconfigure(i, weight=1)

            ttk.Label(card, text=title, font=("Helvetica", 14, "bold"), wraplength=200).pack(pady=10)
            ttk.Label(card, text=desc, font=("Helvetica", 10), wraplength=200, justify=CENTER).pack(pady=10)
            ttk.Button(card, text=t["manage"], bootstyle=color, width=20).pack(pady=15)

        # Footer
        ttk.Label(self.main_frame, text=t["footer"], font=("Helvetica", 9), 
                  bootstyle=SECONDARY).pack(pady=(60, 0))

    def update_language(self, event):
        """Maneja el cambio de idioma de toda la plataforma."""
        selection = self.combo_lang.get()
        self.current_lang = "en" if selection == "English" else "es"
        self.render_content()

    def animate_background(self):
        """Crea un efecto de gradiente en movimiento muy suave."""
        self.angle += 0.02
        # Colores sutiles que oscilan
        color_val = int(240 + 10 * math.sin(self.angle))
        color_hex = f'#{color_val:02x}{color_val:02x}{color_val+5:02x}'
        self.canvas.config(bg=color_hex)
        self.after(50, self.animate_background)

if __name__ == "__main__":
    app = SoftwareFJ_GUI()
    app.mainloop()