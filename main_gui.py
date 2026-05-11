# ============================================================
# ENTRY POINT: Sistema Integral de Gestión - Software FJ
# PROYECTO: Sistema Integral de Gestión - Software FJ
# AUTOR: César David Toro Fernández
# DESCRIPCIÓN: Punto de entrada principal del sistema. Inicializa
#              la aplicación gráfica, ejecuta las operaciones de
#              demostración requeridas y lanza el loop principal.
# ============================================================

from gui.app import SoftwareFJ_App
from models.cliente import Cliente
from models.reserva import Reserva
from models.servicios.sala import ReservaSala
from models.servicios.equipo import AlquilerEquipo
from models.servicios.asesoria import AsesoriaEspecializada
from exceptions.custom import (
    ClienteInvalidoError,
    ReservaInvalidaError,
    DuracionInvalidaError,
    ServicioNoDisponibleError,
    ParametroFaltanteError
)
from services.logger import Logger

logger = Logger()


def ejecutar_operaciones_demo(app: SoftwareFJ_App):
    """
    Simula 10 operaciones completas del sistema incluyendo registros
    válidos e inválidos de clientes, servicios y reservas, demostrando
    el manejo robusto de excepciones y la continuidad operativa del sistema.

    Args:
        app: Instancia principal de la aplicación con estado compartido.
    """

    logger.info("=" * 55)
    logger.info("INICIO DE OPERACIONES DE DEMOSTRACIÓN — SOFTWARE FJ")
    logger.info("=" * 55)

    # ── OPERACIÓN 1 — Registro válido de cliente ──────────────
    try:
        c1 = Cliente(1, "César", "Toro", "3001234567", "cesar@softwarefj.com")
        app.clientes.append(c1)
        logger.info("OP-01 ✅ Cliente válido registrado: César Toro")
    except ClienteInvalidoError as e:
        logger.error(f"OP-01 ❌ {e.mensaje}")

    # ── OPERACIÓN 2 — Registro válido de cliente ──────────────
    try:
        c2 = Cliente(2, "Ana", "Gómez", "3109876543", "ana@softwarefj.com")
        app.clientes.append(c2)
        logger.info("OP-02 ✅ Cliente válido registrado: Ana Gómez")
    except ClienteInvalidoError as e:
        logger.error(f"OP-02 ❌ {e.mensaje}")

    # ── OPERACIÓN 3 — Registro inválido de cliente ────────────
    try:
        c3 = Cliente(3, "", "Inválido", "abc", "sinformato")
        app.clientes.append(c3)
    except ClienteInvalidoError as e:
        logger.error(f"OP-03 ❌ Cliente inválido detectado correctamente: {e.mensaje}")

    # ── OPERACIÓN 4 — Registro válido de sala ─────────────────
    try:
        s1 = ReservaSala(1, 10)
        app.servicios.append(s1)
        costo = s1.calcular_costo(3)
        logger.info(f"OP-04 ✅ Sala registrada | 3h | ${costo:,.0f} COP")
    except (ServicioNoDisponibleError, DuracionInvalidaError) as e:
        logger.error(f"OP-04 ❌ {e.mensaje}")

    # ── OPERACIÓN 5 — Sala con duración inválida ──────────────
    try:
        s_test = ReservaSala(99, 5)
        s_test.calcular_costo(25)
    except DuracionInvalidaError as e:
        logger.error(f"OP-05 ❌ Duración inválida detectada correctamente: {e.mensaje}")

    # ── OPERACIÓN 6 — Registro válido de equipo ───────────────
    try:
        s2 = AlquilerEquipo(2, "laptop", 3)
        app.servicios.append(s2)
        costo = s2.calcular_costo(5)
        logger.info(f"OP-06 ✅ Equipo registrado | Laptop x3 | 5h | ${costo:,.0f} COP")
    except (ParametroFaltanteError, DuracionInvalidaError) as e:
        logger.error(f"OP-06 ❌ {e.mensaje}")

    # ── OPERACIÓN 7 — Equipo con tipo inválido ────────────────
    try:
        s_invalido = AlquilerEquipo(98, "helicoptero", 1)
        app.servicios.append(s_invalido)
    except ParametroFaltanteError as e:
        logger.error(f"OP-07 ❌ Equipo inválido detectado correctamente: {e.mensaje}")

    # ── OPERACIÓN 8 — Registro válido de asesoría ─────────────
    try:
        s3 = AsesoriaEspecializada(3, "experto", "César David Toro")
        app.servicios.append(s3)
        costo = s3.calcular_costo_con_iva(2)
        logger.info(f"OP-08 ✅ Asesoría registrada | Experto | 2h + IVA | ${costo:,.0f} COP")
    except (ParametroFaltanteError, DuracionInvalidaError) as e:
        logger.error(f"OP-08 ❌ {e.mensaje}")

    # ── OPERACIÓN 9 — Reserva válida confirmada ───────────────
    try:
        r1 = Reserva(1, app.clientes[0], app.servicios[0], 3)
        r1.confirmar()
        costo = r1.procesar(10)
        app.reservas.append(r1)
        logger.info(f"OP-09 ✅ Reserva confirmada y procesada | 10% desc | ${costo:,.0f} COP")
    except (ReservaInvalidaError, DuracionInvalidaError, ServicioNoDisponibleError) as e:
        logger.error(f"OP-09 ❌ {e.mensaje}")

    # ── OPERACIÓN 10 — Reserva inválida (duración fuera rango) ─
    try:
        r_invalida = Reserva(99, app.clientes[1], app.servicios[0], 99)
        app.reservas.append(r_invalida)
    except DuracionInvalidaError as e:
        logger.error(f"OP-10 ❌ Reserva inválida detectada correctamente: {e.mensaje}")

    logger.info("=" * 55)
    logger.info("FIN DE OPERACIONES DE DEMOSTRACIÓN — 10/10 COMPLETADAS")
    logger.info("=" * 55)


if __name__ == "__main__":
    app = SoftwareFJ_App()
    ejecutar_operaciones_demo(app)
    app.mainloop()