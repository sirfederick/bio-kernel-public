# dashboard

## Purpose
Lightweight interfaces for monitoring metrics and visualizing offline logs.

## Components
- `realtime_dashboard.py` exposes HTTP endpoints and WebSockets
- `notebook_viewer.py` renders metrics from NDJSON files

## Usage
### Real-time dashboard
```bash
python -m dashboard.realtime_dashboard
```
### Notebook viewer
```bash
python -m dashboard.notebook_viewer --plot-rewards
```
### Docker
```bash
docker-compose up dashboard
```
### Kubernetes
Apply `kubernetes/dashboard.yaml`.

## Maintainers
`dev-team@bio-kernel.local`
