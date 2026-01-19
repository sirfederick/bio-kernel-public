from __future__ import annotations

"""Simple resource scheduler for multi-node deployments."""

import time
from typing import Any, Dict

from kernel_quantum.messaging import ZMQPublisher, ZMQPuller, ZMQPusher, _load_config


class Scheduler:
    """Collect resource info and publish cluster metrics."""

    def __init__(self, interval: float = 1.0) -> None:
        cfg = _load_config()
        sched_cfg = cfg.get("scheduler", {})
        self._pull = ZMQPuller(address=sched_cfg.get("pull_address"))
        self._pub = ZMQPublisher(address=sched_cfg.get("pub_address"))
        metrics_addr = cfg.get("metrics", {}).get("address")
        self._metrics = ZMQPusher(address=metrics_addr) if metrics_addr else None
        self.interval = interval
        self.nodes: Dict[str, Dict[str, Any]] = {}

    def poll_once(self) -> None:
        while True:
            msg = self._pull.receive(timeout=100)
            if msg is None:
                break
            node = msg.get("node", f"node{len(self.nodes)}")
            self.nodes[node] = msg
        if self._metrics is not None:
            self._metrics.send({"kind": "cluster", "nodes": self.nodes})
        self._pub.publish("cluster.metrics", {"nodes": self.nodes})

    def run(self) -> None:  # pragma: no cover - long running loop
        while True:
            self.poll_once()
            time.sleep(self.interval)


if __name__ == "__main__":  # pragma: no cover - manual execution
    Scheduler().run()
