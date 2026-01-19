"""Kernel Quantum Orchestrator
==============================

Este módulo coordina la ejecución de todos los pipelines de kernel_quantum,
incluyendo:

    * Validación (sanity checks)
    * Recolección de datos
    * Construcción de módulos (builder)
    * Integración con módulos descubiertos dinámicamente
    * Colaboración con kernel_unknown_engine

Características principales:
    - Decisión de ejecución basada en agentes de aprendizaje por refuerzo (RL).
    - Ejecución cooperativa y negociada entre módulos usando ZeroMQ.
    - Generación de reportes estructurados en JSON.
    - Descubrimiento automático de tareas modulares.
    - Compatibilidad con ejecución paralela (ThreadPool) o secuencial.

Estándares y buenas prácticas:
    - Logging estructurado en JSON.
    - Documentación alineada a ISO/IEC 25010.
    - Arquitectura preparada para sistemas distribuidos y extensibles.

Autor:
    Bio-Kernel Team
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import importlib
import json
import os
from pathlib import Path
import pkgutil
from time import perf_counter
from typing import Callable, Dict, List, cast

from kernel_quantum.messaging import ZMQPusher, ZMQRequester, ZMQSubscriber, _load_config
from kernel_quantum.rl_agent import RLAgent
from kernel_quantum.shared.helpers import ensure_dir, timestamp_now
from kernel_quantum.shared.logging_utils import get_logger

# Integración opcional con kernel_unknown_engine
try:  # pragma: no cover
    import kernel_unknown_engine
except ImportError:  # pragma: no cover
    kernel_unknown_engine = None

# Rutas y configuración
ROOT = Path(__file__).resolve().parents[1]
LOG_PATH = ensure_dir(ROOT / "logs") / "orchestrator.log"
REPORT_PATH = ensure_dir(ROOT / "reports") / "master_report.json"
LOGGER = get_logger("orchestrator")

# Soporte para orquestadores antiguos
_pkg_dir = Path(__file__).with_name("orchestrator")
if _pkg_dir.is_dir():
    __path__ = [str(_pkg_dir)]


class ModuleTask:
    """Encapsula una tarea ejecutable representada por una función."""

    def __init__(self, name: str, func: Callable[[], None]):
        self.name = name
        self.func = func

    def run(self) -> Dict[str, object]:
        """
        Ejecuta la función asociada y retorna un reporte con métricas.

        Returns:
            dict con nombre, estado, duración y error (si aplica).
        """
        LOGGER.info(json.dumps({"event": "start", "module": self.name}))
        start = perf_counter()
        status, error = "ok", None
        try:
            self.func()
        except Exception as exc:  # pragma: no cover
            status, error = "fail", str(exc)
            LOGGER.exception("%s execution failed", self.name)
        runtime = perf_counter() - start
        data = {
            "name": self.name,
            "status": status,
            "runtime_seconds": round(runtime, 4),
            "error": error,
        }
        LOGGER.info(json.dumps({"event": "finish", **data}))
        return data


# ----------------------------------------------------------------------
# Funciones principales de los pipelines
# ----------------------------------------------------------------------
def _run_sanity() -> None:
    """Ejecuta la validación de integridad (sanity checks)."""
    import sys
    from kernel_quantum.sanity_pipeline import run_all_validations

    sys.argv = ["run_all_validations"]
    run_all_validations.main()


def _run_collector() -> None:
    """Ejecuta el pipeline de recolección de datos (collector)."""
    from kernel_quantum.collector import collector as collector_mod

    if os.getenv("BK_TEST_MODE"):
        test_cfg = {
            "sources": {
                "dummy": {
                    "enabled": True,
                    "endpoint": "https://example.com",
                    "auth": None,
                    "params": {},
                }
            }
        }
        orig_load = collector_mod.load_config
        collector_mod.load_config = lambda *_a, **_k: test_cfg
        import requests  # type: ignore

        class DummyResponse:
            status_code = 200
            content = b"{}"
            def raise_for_status(self) -> None:
                return None

        orig_get = requests.get
        requests.get = lambda *_args, **_kwargs: DummyResponse()  # type: ignore
        try:
            results = collector_mod.run()
        finally:
            collector_mod.load_config = orig_load
            requests.get = orig_get
    else:
        results = collector_mod.run()

    (REPORT_PATH.parent / "collector_report.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8"
    )


def _run_builder() -> None:
    """Ejecuta el pipeline builder con configuración opcional."""
    import kernel_builder_gen.builder as builder
    cfg_path = os.getenv("BK_BUILDER_CONFIG")
    if cfg_path:
        from kernel_quantum.shared.config_loader import load_config
        orig_load = builder.load_module_config
        builder.load_module_config = lambda: load_config(cfg_path)
        try:
            builder.main()
        finally:
            builder.load_module_config = orig_load
    else:
        builder.main()


# ----------------------------------------------------------------------
# Descubrimiento dinámico de módulos adicionales
# ----------------------------------------------------------------------
def _discover_additional() -> List[ModuleTask]:
    """
    Descubre dinámicamente módulos adicionales y los prepara como tareas.

    Returns:
        Lista de tareas (ModuleTask).
    """
    tasks: List[ModuleTask] = []
    for pkg_name in ["kernel_quantum", "kernel_builder_gen"]:
        try:
            pkg = importlib.import_module(pkg_name)
        except Exception:
            continue
        for mod in pkgutil.walk_packages(getattr(pkg, "__path__", []), pkg.__name__ + "."):
            mod_name = mod.name
            try:
                module = importlib.import_module(mod_name)
            except Exception:
                continue
            func = getattr(module, "main", None)
            if callable(func) and mod_name not in {
                "kernel_quantum.sanity_pipeline.run_all_validations",
                "kernel_quantum.collector.fetch_manager",
                "kernel_builder_gen.builder",
            }:
                tasks.append(ModuleTask(mod_name, func))
    return tasks


# ----------------------------------------------------------------------
# Lógica principal del orquestador
# ----------------------------------------------------------------------
def run_all(mode: str = "sequential") -> Dict[str, object]:
    """
    Ejecuta todas las tareas orquestadas y genera un reporte consolidado.

    Args:
        mode: Modo de ejecución ("parallel" o "sequential").

    Returns:
        dict con resultados y resumen.
    """
    LOGGER.info(json.dumps({"event": "orchestrator_start", "mode": mode}))

    # Subscribirse a eventos de agent_loop
    sub = ZMQSubscriber(topics=["cycle.started"])
    event = sub.receive(timeout=100)
    if event:
        LOGGER.info(json.dumps({"event": "received", "topic": event[0], "payload": event[1]}))

    # Configuración de ZeroMQ
    cfg = _load_config()
    metrics_addr = cfg.get("metrics", {}).get("address")
    metrics_pusher = ZMQPusher(address=metrics_addr) if metrics_addr else None
    coop_addr = cfg.get("cooperation", {}).get("address")
    coop_req = ZMQRequester(address=coop_addr) if coop_addr else None

    rl_agent = RLAgent(
        state_dim=2,
        action_dim=2,
        module_name="kernel_quantum",
        metrics_pusher=metrics_pusher,
    )

    # Definición de tareas base
    tasks = [
        ModuleTask("kernel_quantum.sanity_pipeline", _run_sanity),
        ModuleTask("kernel_quantum.collector", _run_collector),
        ModuleTask("kernel_builder_gen", _run_builder),
    ]
    tasks.extend(_discover_additional())

    # Decisión de ejecución cooperativa
    state = [float(len(tasks)), 1.0 if mode == "parallel" else 0.0]
    action = rl_agent.act(state)

    if coop_req is not None:
        resp = coop_req.request({"module": "kernel_quantum", "priority": len(tasks)}, timeout=100)
        if resp and not resp.get("execute", True):
            if metrics_pusher is not None:
                metrics_pusher.send(
                    {"kind": "cooperative", "module": "kernel_quantum", "decision": "deferred"}
                )
            return {
                "timestamp": timestamp_now(),
                "mode": mode,
                "results": [],
                "summary": {"total_runtime_seconds": 0.0, "error_count": 0, "failed_modules": []},
            }

    mode = "parallel" if action == 1 else "sequential"

    # Ejecución de tareas
    if mode == "parallel":
        with ThreadPoolExecutor() as exc:
            results = list(exc.map(lambda t: t.run(), tasks))
    else:
        results = [t.run() for t in tasks]

    # Resumen
    total_runtime = round(sum(cast(float, r["runtime_seconds"]) for r in results), 4)
    failures = [r["name"] for r in results if r["status"] != "ok"]

    report = {
        "timestamp": timestamp_now(),
        "mode": mode,
        "results": results,
        "summary": {
            "total_runtime_seconds": total_runtime,
            "error_count": len(failures),
            "failed_modules": failures,
        },
    }

    # Integración con reportes externos
    ZMQRequester().request({"cmd": "sync_report", "summary": report["summary"]}, timeout=100)
    _merge_collector_report(report)
    _merge_unknown_genes_report(report)

    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")

    if kernel_unknown_engine:
        try:
            kernel_unknown_engine.main.run()
        except Exception:
            LOGGER.exception("kernel_unknown_engine execution failed")

    # Feedback RL
    reward = 1.0 if not failures else -1.0
    rl_agent.remember(state, action, reward, [0.0, 0.0], True)
    rl_agent.train_step()

    LOGGER.info(json.dumps({"event": "orchestrator_end", **report["summary"]}))
    return report


def _merge_collector_report(report: dict) -> None:
    """Integra el reporte de collector si existe."""
    collector_file = REPORT_PATH.parent / "collector_report.json"
    if collector_file.exists():
        try:
            report["collector"] = json.loads(collector_file.read_text())
        except Exception:
            report["collector"] = {"error": "invalid collector report"}


def _merge_unknown_genes_report(report: dict) -> None:
    """Integra el reporte de unknown_genes si existe."""
    unknown_path = ROOT / "kernel_builder_gen" / "reports" / "unknown_genes.ndjson"
    if unknown_path.exists():
        try:
            lines = [
                json.loads(line)
                for line in unknown_path.read_text().splitlines()
                if line.strip()
            ]
            if lines:
                scores = [r.get("unknown_score", 0.0) for r in lines]
                report["unknown_genes"] = {
                    "count": len(lines),
                    "avg_score": round(sum(scores) / len(scores), 3),
                }
        except Exception:
            report["unknown_genes"] = {"error": "invalid unknown genes report"}


def main(mode: str = "sequential") -> None:
    """Punto de entrada CLI del orquestador."""
    if kernel_unknown_engine:
        LOGGER.info("kernel_unknown_engine detectado. Integrando orquestación.")
    run_all(mode=mode)
