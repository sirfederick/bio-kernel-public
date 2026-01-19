from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

import yaml
from jsonschema import validate

DEFAULT_CONFIG = Path("kernel_unknown_engine/reverse_engineering/reveng_config.yaml")
SUPPORTED_TOOLS = {"lief", "ghidra", "radare2"}


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    schema_file = data.get("validation", {}).get("schema_file")
    if not schema_file:
        raise ValueError("Missing validation.schema_file in config")
    schema_path = path.parent / schema_file
    with schema_path.open("r", encoding="utf-8") as f:
        schema = json.load(f)
    validate(data, schema)
    return data


def ensure_dirs(base: Path) -> None:
    for name in ("reports", "inputs"):
        (base / name).mkdir(parents=True, exist_ok=True)


def simulate_analysis(binary: Path, tool: str, report_dir: Path) -> Path:
    timestamp = datetime.utcnow().isoformat()
    report_path = report_dir / f"{binary.name}.analysis.txt"
    content = (
        f"Tool: {tool}\n"
        f"File: {binary.resolve()}\n"
        f"Timestamp: {timestamp}\n"
        f"Status: OK (simulated)\n"
        f"Salida: {report_path.resolve()}\n"
    )
    report_path.write_text(content, encoding="utf-8")
    return report_path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simulated binary analysis")
    parser.add_argument(
        "--config",
        type=str,
        default=str(DEFAULT_CONFIG),
        help="Ruta del YAML de configuración",
    )
    parser.add_argument("--input", type=str, required=True, help="Binario o carpeta a analizar")
    parser.add_argument(
        "--tool",
        choices=sorted(SUPPORTED_TOOLS),
        help="Herramienta a utilizar",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    config_path = Path(args.config)
    cfg = load_config(config_path)
    tool = args.tool or cfg.get("parameters", {}).get("analysis_tools", ["lief"])[0]
    base_dir = config_path.parent
    ensure_dirs(base_dir)

    input_path = Path(args.input)
    reports_dir = base_dir / "reports"

    if input_path.is_dir():
        for f in input_path.iterdir():
            if f.is_file():
                simulate_analysis(f, tool, reports_dir)
    else:
        simulate_analysis(input_path, tool, reports_dir)

    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
