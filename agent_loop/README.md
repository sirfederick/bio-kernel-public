# agent_loop

## Purpose
Central coordinator that publishes cycle events and manages local agents.

## Features
- ZeroMQ publisher for system-wide events
- Optional in-process mock messaging for tests
- Hosts the main RL agent and resource scheduler

## Usage
### Local
```bash
python -m agent_loop.orchestrator
```
### Via local_runner
```bash
python -m local_runner --only agent_loop
```
### Docker
```bash
docker-compose up agent_loop
```
### Kubernetes
Apply the manifest in `kubernetes/agent_loop.yaml`.

## Environment Variables
- `BK_DEVICE` selects GPU device.
- `BK_MOCK_MESSAGING=1` enables mock sockets.

## Maintainers
`dev-team@bio-kernel.local`
