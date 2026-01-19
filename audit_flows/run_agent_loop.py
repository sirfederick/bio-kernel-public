"""
run_agent_loop.py

Script para ejecutar el loop principal del orquestador multiagente.

Cumple con normas ISO/IEC 25010 de calidad, confiabilidad y mantenibilidad.

Requiere: módulo `agent_loop.orchestrator`

Uso:
    python audit_flows/run_agent_loop.py

Autor: Equipo Bio-Kernel | Genoma
Fecha: 2025-07-30
Versión: 1.1.0
"""

import logging
import sys
import time
from typing import Optional

from agent_loop.orchestrator import Orchestrator

def setup_logger(name: Optional[str] = "AgentLoopLogger") -> logging.Logger:
    """
    Configura el logger con formato estándar, nivel INFO y salida por consola.
    Prevé evitar duplicados en handlers.
    """
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

def main(sleep_interval: int = 10) -> int:
    """
    Función principal que ejecuta el loop continuo del orquestador.

    Args:
        sleep_interval (int): Segundos a dormir entre ciclos (default 10).

    Returns:
        int: Código de salida (0 éxito, !=0 error)
    """
    logger = setup_logger()
    logger.info("Inicio del orquestador multiagente")

    try:
        orchestrator = Orchestrator()
        while True:
            orchestrator.run_cycle()
            logger.info("Ciclo de orquestación completado")
            time.sleep(sleep_interval)

    except KeyboardInterrupt:
        logger.info("Orquestador detenido manualmente por usuario")
    except Exception as e:
        logger.exception(f"Excepción inesperada en el orquestador: {e}")
        return 1

    logger.info("Orquestador finalizado correctamente")
    return 0

if __name__ == "__main__":
    sys.exit(main())
