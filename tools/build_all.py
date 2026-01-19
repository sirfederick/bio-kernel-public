import subprocess
from pathlib import Path
import json
import sys

BASE_DIR = Path(__file__).resolve().parents[1]

CONFIGS = list(BASE_DIR.glob('kernel_unknown_engine/**/*.yaml'))
SCHEMAS = {
    c: c.with_name(c.stem + '-schema.json') for c in CONFIGS
}


def validate_configs() -> None:
    for cfg, schema in SCHEMAS.items():
        if not schema.exists():
            continue
        try:
            subprocess.run(
                [sys.executable, '-m', 'jsonschema', str(cfg), str(schema)],
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError as exc:
            print(exc.stderr.decode(), file=sys.stderr)
            raise


def run_cmd(cmd: list[str]) -> None:
    print(' '.join(cmd))
    subprocess.run(cmd, check=True)


def main() -> None:
    validate_configs()
    run_cmd(['ruff', 'check', str(BASE_DIR)])
    run_cmd(['black', str(BASE_DIR)])
    run_cmd(['pytest', '-q'])


if __name__ == '__main__':
    main()
