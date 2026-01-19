"""Offline visualization utilities for Bio-Kernel metrics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, List


def _load_ndjson(path: Path) -> List[Any]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def plot_rewards() -> None:
    """Plot reward history using matplotlib if available."""

    try:
        import matplotlib.pyplot as plt
    except Exception as exc:  # pragma: no cover - dependency optional
        raise SystemExit("matplotlib is required for plotting") from exc

    data = _load_ndjson(Path("logs/local_metrics.ndjson"))
    rewards: dict[str, List[float]] = {}
    for rec in data:
        payload = rec.get("payload", {})
        module = payload.get("module")
        reward = payload.get("reward")
        if module is not None and isinstance(reward, (int, float)):
            rewards.setdefault(module, []).append(float(reward))
    for module, vals in rewards.items():
        plt.plot(vals, label=module)
    plt.legend()
    plt.xlabel("step")
    plt.ylabel("reward")
    plt.show()


def main() -> None:
    parser = argparse.ArgumentParser(description="Offline metrics viewer")
    parser.add_argument(
        "--plot-rewards",
        action="store_true",
        help="plot reward history from local logs",
    )
    args = parser.parse_args()
    if args.plot_rewards:
        plot_rewards()
    else:
        metrics = _load_ndjson(Path("logs/local_metrics.ndjson"))
        events = _load_ndjson(Path("logs/local_events.ndjson"))
        print(f"Loaded {len(metrics)} metrics and {len(events)} events")


if __name__ == "__main__":  # pragma: no cover - manual execution
    main()
