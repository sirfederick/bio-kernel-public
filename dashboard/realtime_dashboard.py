"""Real-time Dashboard for Bio-Kernel
====================================

Este módulo provee una interfaz REST y WebSocket para monitoreo en tiempo real
de métricas del ecosistema Bio-Kernel.

Características principales:
    * Streaming de métricas en vivo vía WebSocket.
    * Endpoints REST estructurados para consumo programático.
    * Visualización de métricas de agentes de RL, aprendizaje federado,
      cooperación y actividad ZMQ.
    * Métricas de nodos, GPU, y datos de clúster distribuidos.
    * Arquitectura extensible para integración con ReactJS u otros frameworks frontend.

Cumple normas de:
    * Diseño modular (ISO/IEC 25010).
    * Escalabilidad y extensibilidad de endpoints.
    * Preparación para UI moderna desacoplada.
"""

from __future__ import annotations

import asyncio
from collections import Counter, defaultdict
from pathlib import Path
import json
from typing import Any

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

from kernel_quantum.messaging import ZMQPuller, ZMQSubscriber, _load_config
from kernel_quantum.shared.quota_guardian import QuotaGuardian


class RealTimeDashboard:
    """
    Dashboard en tiempo real para Bio-Kernel.
    
    Proporciona métricas del sistema mediante REST y WebSocket.
    """

    def __init__(self) -> None:
        # --- Inicialización FastAPI ---
        self.app = FastAPI(
            title="Bio-Kernel Real-Time Dashboard",
            description="API de métricas en tiempo real y estadísticas de RL",
            version="1.0.0",
        )

        # --- Métricas núcleo ---
        self.pending = 0
        self.processing = 0
        self.completed = 0
        self.blocked = 0
        self.quarantined = 0
        self.api_gb_hour = 0
        self.api_gb_day = 0

        # --- Métricas avanzadas ---
        self.connections: list[WebSocket] = []
        self.rl_rewards: dict[str, list[float]] = defaultdict(list)
        self.rl_actions: dict[str, Counter[int]] = defaultdict(Counter)
        self.zmq_messages = 0
        self.zmq_latencies: list[float] = []
        self.federated_syncs = 0
        self.model_version = 0
        self.shared_experiences = 0
        self.cooperative_decisions: list[dict[str, Any]] = []
        self.cluster_nodes: dict[str, dict[str, Any]] = {}

        # --- Configuración de mensajería y rutas ---
        self._setup_routes()
        
        # Servir index.html en la raíz
        @self.app.get("/", response_class=HTMLResponse)
        async def read_root():
            index_path = Path(__file__).parent / "dashboard_tabs.html"
            content = index_path.read_text(encoding="utf-8")
            return HTMLResponse(content=content, headers={
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            })

        cfg = _load_config()
        self._subscriber = ZMQSubscriber(topics=["cycle.started", "cycle.finished"])
        metrics_addr = cfg.get("metrics", {}).get("address")
        self._metrics_puller = ZMQPuller(address=metrics_addr) if metrics_addr else None

        # --- Lanzar tareas de escucha (si hay loop) ---
        try:
            loop = asyncio.get_running_loop()
            if loop.is_running():
                loop.create_task(self._listen_events())
                loop.create_task(self._file_watcher_loop()) # [NEW] File Watcher
                if self._metrics_puller is not None:
                    loop.create_task(self._listen_metrics())
        except RuntimeError:
            # No hay loop corriendo, se deben iniciar manualmente con .start_listening()
            pass

    def start_listening(self) -> None:
        """Inicia las tareas de escucha de ZeroMQ y File Watcher."""
        asyncio.create_task(self._listen_events())
        asyncio.create_task(self._file_watcher_loop())
        if self._metrics_puller is not None:
            asyncio.create_task(self._listen_metrics())

    async def _room_broadcast(self, message: dict) -> None:
        """Envía un mensaje a todos los clientes WebSocket conectados."""
        if not self.connections:
            return
            
        disconnected = []
        for ws in self.connections:
            try:
                await ws.send_json(message)
            except Exception:
                disconnected.append(ws)
        
        for ws in disconnected:
            if ws in self.connections:
                self.connections.remove(ws)

    async def _broadcast(self, message: dict) -> None:
        """Wrapper compatible para _broadcast."""
        await self._room_broadcast(message)

    async def _file_watcher_loop(self) -> None:
        """
        [FALLBACK] Lee los archivos de logs y reportes periódicamente para actualizar la UI
        si ZeroMQ no está transmitiendo o para datos persistidos.
        """
        while True:
            try:
                # Defensive check for zombie tasks during reload
                if not hasattr(self, '_room_broadcast'):
                    await asyncio.sleep(1)
                    continue

                # 1. Leer Inteligencia Generada
                intel_reports = list(Path("intelligence_reports").glob("*.json"))
                self.completed = len(intel_reports)
                
                # 2. Leer Master Status
                master_status = Path("reports/master_report.json")
                if master_status.exists():
                     # Podríamos parsear esto para estado global
                     pass
                
                # 3. Leer Logs de Quantum para actividad reciente
                log_file = Path("logs/runtime_quantum.log.err")
                if log_file.exists():
                    self.processing = 1 # Asumimos uno activo por simplicidad si el log existe
                
                # Broadcast genérico de actualización
                await self._broadcast({
                    "type": "system_stats",
                    "data": {
                        "pending": 24 - self.completed, # Aprox
                        "processing": self.processing,
                        "completed": self.completed,
                        "blocked": 0,
                        "quarantined": 0
                    }
                })
                
                # Enviar último hallazgo si hay nuevos
                if intel_reports:
                    latest = max(intel_reports, key=lambda p: p.stat().st_mtime)
                    data = json.loads(latest.read_text())
                    findings = data.get("findings", [])
                    if findings:
                        # Tomar el último hallazgo significativa
                        # Enviar 'new_intelligence' event
                        await self._broadcast({
                            "type": "new_intelligence",
                            "data": {
                                "chromosome": data.get("chromosome"),
                                "gene": findings[0].get("gene_id"),
                                "hypothesis": findings[0].get("hypothesis")
                            }
                        })

            except Exception as e:
                print(f"File watcher error: {e}")
            
            await asyncio.sleep(2) # Polling cada 2s

    # ------------------------------------------------------------------
    # Rutas y endpoints
    # ------------------------------------------------------------------
    def _setup_routes(self) -> None:
        @self.app.get("/metrics", tags=["Core Metrics"])
        async def metrics() -> dict[str, Any]:
            """Obtiene métricas centrales del sistema."""
            return self._core_metrics()

        @self.app.get("/", tags=["UI"])
        @self.app.get("/dashboard", tags=["UI"])
        async def dashboard() -> HTMLResponse:
            """Página del Dashboard Premium."""
            index_file = Path(__file__).resolve().parent / "dashboard_tabs.html"
            if index_file.exists():
                return HTMLResponse(index_file.read_text())
            return HTMLResponse("<h1>Dashboard dashboard_tabs.html no encontrado</h1>")

        @self.app.get("/quota", tags=["Resource Quota"])
        async def quota() -> dict:
            """Obtiene el uso de cuotas de servicios."""
            guardian = QuotaGuardian()
            return {svc: guardian.current_usage(svc) for svc in guardian.config.get("services", {})}

        @self.app.get("/rl_metrics", tags=["Reinforcement Learning"])
        async def rl_metrics() -> dict[str, Any]:
            """Métricas de agentes RL."""
            return {
                "rewards": self.rl_rewards,
                "actions": {m: dict(c) for m, c in self.rl_actions.items()},
            }

        @self.app.get("/zmq_metrics", tags=["Messaging"])
        async def zmq_metrics() -> dict[str, float]:
            """Métricas de mensajería ZeroMQ."""
            avg = sum(self.zmq_latencies) / len(self.zmq_latencies) if self.zmq_latencies else 0.0
            return {"messages": self.zmq_messages, "avg_latency_ms": avg}

        @self.app.get("/federated_metrics", tags=["Federated Learning"])
        async def federated_metrics() -> dict[str, int]:
            """Métricas de aprendizaje federado."""
            return {"syncs": self.federated_syncs, "model_version": self.model_version}

        @self.app.get("/shared_experiences", tags=["Federated Learning"])
        async def shared_experiences() -> dict[str, int]:
            """Estadísticas de experiencias compartidas."""
            return {"count": self.shared_experiences}

        @self.app.get("/cooperative_decisions", tags=["Cooperation"])
        async def cooperative_decisions() -> list[dict[str, Any]]:
            """Últimas decisiones cooperativas entre nodos."""
            return self.cooperative_decisions[-10:]

        @self.app.get("/cluster_metrics", tags=["Cluster"])
        async def cluster_metrics() -> dict[str, Any]:
            """Métricas actuales de nodos en el clúster."""
            return {"nodes": self.cluster_nodes}

        @self.app.get("/genomics_stats", tags=["Genomics"])
        async def genomics_stats() -> dict[str, Any]:
            """Estadísticas actuales de binarización y análisis."""
            from pathlib import Path
            import re
            
            chroms = {}
            total_genes = 0
            verdicts = Counter()
            
            # 1. Leer conteos base de los Reportes Finales (Legacy/Base Map)
            reports_dir = Path("reports")
            for report in reports_dir.glob("CHR*_FINAL_REPORT.md"):
                try:
                    name = report.name.replace("_FINAL_REPORT.md", "").replace("CHR", "")
                    content = report.read_text(encoding="utf-8")
                    # Intentar extraer conteo de "Genes Processed: N" o similar
                    match = re.search(r"Genes Processed.*:\s*(\d+)", content, re.IGNORECASE)
                    count = int(match.group(1)) if match else 0
                    
                    # Store base stats
                    chroms[name] = {"total": count, "completed": 0} # completed updated below
                    total_genes += count
                except:
                    pass

            # 2. Leer inteligencia generada (AI Analysis)
            intel_dir = Path("intelligence_reports")
            if intel_dir.exists():
                for report in intel_dir.glob("*.json"):
                    try:
                        with open(report) as f:
                            data = json.load(f)
                            c_name = str(data.get("chromosome", "unknown"))
                            findings = data.get("findings", [])
                            
                            # Actualizar conteo de "completados" (analizados por IA)
                            if c_name in chroms:
                                chroms[c_name]["completed"] += len(findings)
                            else:
                                chroms[c_name] = {"total": len(findings), "completed": len(findings)}

                            # Actualizar veredictos
                            for f in findings:
                                verdicts[f.get("verdict", "unknown")] += 1
                    except: pass
            
            # 3. Fallback: Si no hay reportes de inteligencia, simular con datos de bin si existen
            # (No hacer nada para no inflar artificialmente, el dashboard mostrará lo real)

            return {
                "total_genes": total_genes,
                "chromosomes": chroms,
                "verdicts": dict(verdicts)
            }

        @self.app.get("/oracle_insights", tags=["Intelligence"])
        async def oracle_insights() -> list[dict[str, Any]]:
            """Retorna los últimos hallazgos del Oráculo Científico."""
            reports_dir = Path("intelligence_reports")
            if not reports_dir.exists(): return []
            
            all_findings = []
            for report_file in sorted(reports_dir.glob("*.json"), reverse=True):
                try:
                    with open(report_file) as f:
                        data = json.load(f)
                        all_findings.extend(data.get("findings", []))
                except: pass
            return all_findings[:50] # Top 50 más recientes

        @self.app.get("/gpu_metrics", tags=["Cluster"])
        async def gpu_metrics() -> dict[str, int]:
            """Uso de GPU por nodo en el clúster."""
            return {n: int(d.get("gpu", 0)) for n, d in self.cluster_nodes.items()}

        @self.app.get("/offline_metrics", tags=["Offline Logs"])
        async def offline_metrics() -> dict[str, Any]:
            """Carga métricas históricas locales."""
            def _load(path: Path) -> list[Any]:
                if not path.exists():
                    return []
                with path.open("r", encoding="utf-8") as fh:
                    return [json.loads(line) for line in fh if line.strip()]

            base = Path("logs")
            return {
                "metrics": _load(base / "local_metrics.ndjson"),
                "events": _load(base / "local_events.ndjson"),
            }

        @self.app.websocket("/ws")
        async def websocket_endpoint(ws: WebSocket) -> None:
            """Stream de métricas en tiempo real vía WebSocket."""
            await ws.accept()
            self.connections.append(ws)
            try:
                while True:
                    await ws.send_json(self._core_metrics())
                    await asyncio.sleep(1)
            except Exception:
                pass
            finally:
                self.connections.remove(ws)

    # ------------------------------------------------------------------
    # Utilidades internas
    # ------------------------------------------------------------------
    def _core_metrics(self) -> dict[str, Any]:
        """Devuelve las métricas centrales como diccionario."""
        return {
            "pending": self.pending,
            "processing": self.processing,
            "completed": self.completed,
            "blocked": self.blocked,
            "quarantined": self.quarantined,
            "api_gb_hour": self.api_gb_hour,
            "api_gb_day": self.api_gb_day,
        }

    async def broadcast(self) -> None:
        """Difunde métricas actuales a todos los clientes WebSocket."""
        data = self._core_metrics()
        for ws in list(self.connections):
            try:
                await ws.send_json(data)
            except Exception:
                self.connections.remove(ws)

    async def _listen_events(self) -> None:
        """Escucha eventos del bus ZMQ y notifica al dashboard."""
        while True:
            evt = self._subscriber.receive(timeout=100)
            if evt:
                await self.broadcast()
            await asyncio.sleep(0.1)

    async def _listen_metrics(self) -> None:
        """Escucha actualizaciones de métricas a través de ZMQ."""
        while True:
            if self._metrics_puller is None:
                await asyncio.sleep(1)
                continue
            msg = self._metrics_puller.receive(timeout=100)
            if msg:
                self._handle_metric_message(msg)
            await asyncio.sleep(0.1)

    def _handle_metric_message(self, msg: dict[str, Any]) -> None:
        """Procesa mensajes entrantes de métricas."""
        kind = msg.get("kind")
        if kind == "rl":
            mod = msg.get("module", "?")
            self.rl_rewards[mod].append(float(msg.get("reward", 0.0)))
            self.rl_actions[mod][int(msg.get("action", 0))] += 1
        elif kind == "zmq":
            self.zmq_messages += 1
            lat = msg.get("latency_ms")
            if lat is not None:
                self.zmq_latencies.append(float(lat))
        elif kind == "federated":
            self.federated_syncs += 1
            self.model_version = int(msg.get("version", self.model_version))
        elif kind == "experience_share":
            self.shared_experiences += int(msg.get("count", 0))
        elif kind == "cooperative":
            self.cooperative_decisions.append(msg)
        elif kind == "cluster":
            self.cluster_nodes = msg.get("nodes", {})

    async def notify_quarantine(self) -> None:
        """Notifica un evento de cuarentena."""
        self.quarantined += 1
        await self.broadcast()


# Lazy instance getter
_dashboard_instance = None

# Singleton global
_dashboard_instance = None

def get_dashboard_app():
    global _dashboard_instance
    if _dashboard_instance is None:
        _dashboard_instance = RealTimeDashboard()
        # Iniciar escuchas automáticamente al crear la instancia
        _dashboard_instance.start_listening()
    return _dashboard_instance.app

# Expose app for uvicorn
app_instance = get_dashboard_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("dashboard.realtime_dashboard:app_instance", host="0.0.0.0", port=8000, reload=True)
