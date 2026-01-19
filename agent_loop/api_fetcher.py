from __future__ import annotations

"""Batch API downloader with quota enforcement."""

# ruff: noqa: E402

import asyncio
from pathlib import Path
from typing import Iterable, List

import httpx

from kernel_quantum.shared.helpers import ensure_dir
from kernel_quantum.shared.secrets_manager import SecretsManager
from kernel_quantum.shared.quota_guardian import QuotaGuardian
from kernel_unknown_engine.security_layer import log_security_event
from .security_orchestrator import SecurityOrchestrator


class APIFetcher:
    """Download files from URLs respecting bandwidth quotas."""

    def __init__(
        self, service_name: str, secrets_path: str | Path = "secrets_config.yaml"
    ) -> None:
        self.service_name = service_name
        SecretsManager(secrets_path)  # ensure file exists for backward compat
        self.quota = QuotaGuardian(secrets_path)

    async def fetch_batch(
        self,
        urls: Iterable[str],
        dest_dir: str | Path = "downloads",
        security: SecurityOrchestrator | None = None,
    ) -> List[Path]:
        """Download multiple URLs sequentially."""
        dest = ensure_dir(dest_dir)
        results: List[Path] = []
        async with httpx.AsyncClient() as client:
            for url in urls:
                log_security_event(
                    {"component": "api_fetcher", "event": "request", "url": url}
                )
                resp = await client.get(url)
                size = len(resp.content)
                if not self.quota.register_usage(self.service_name, size):
                    raise RuntimeError(f"Quota exceeded for {self.service_name}")
                fname = dest / Path(url).name
                fname.write_bytes(resp.content)
                if security and security.enabled:
                    security.scan(fname)
                results.append(fname)
                await asyncio.sleep(0)
        return results
