"""HTTP client for VictoriaLogs and VictoriaTraces APIs."""

from __future__ import annotations

import httpx


class ObsClient:
    """Thin wrapper around VictoriaLogs and VictoriaTraces HTTP APIs."""

    def __init__(self, victorialogs_url: str, victoriatraces_url: str) -> None:
        self.victorialogs_url = victorialogs_url.rstrip("/")
        self.victoriatraces_url = victoriatraces_url.rstrip("/")
        self._http = httpx.AsyncClient(timeout=30.0)

    async def close(self) -> None:
        await self._http.aclose()

    async def __aenter__(self) -> "ObsClient":
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self.close()

    # --- VictoriaLogs ---

    async def query_logs(self, query: str, limit: int = 100) -> str:
        """Execute a LogsQL query against VictoriaLogs."""
        url = f"{self.victorialogs_url}/select/logsql/query"
        params = {"query": query, "limit": limit}
        resp = await self._http.get(url, params=params)
        resp.raise_for_status()
        return resp.text

    async def count_errors(self, service: str, time_window: str = "1h") -> str:
        """Count error-level log entries for a service over a time window."""
        query = f'_time:{time_window} service.name:"{service}" severity:ERROR'
        url = f"{self.victorialogs_url}/select/logsql/query"
        params = {"query": query, "limit": 10000}
        resp = await self._http.get(url, params=params)
        resp.raise_for_status()
        # Count lines (each line is one log entry)
        lines = [line for line in resp.text.strip().split("\n") if line.strip()]
        return str(len(lines))

    # --- VictoriaTraces (Jaeger-compatible API) ---

    async def list_traces(self, service: str, limit: int = 10) -> str:
        """List recent traces for a service."""
        url = f"{self.victoriatraces_url}/select/jaeger/api/traces"
        params = {"service": service, "limit": limit}
        resp = await self._http.get(url, params=params)
        resp.raise_for_status()
        return resp.text

    async def get_trace(self, trace_id: str) -> str:
        """Fetch a specific trace by ID."""
        url = f"{self.victoriatraces_url}/select/jaeger/api/traces/{trace_id}"
        resp = await self._http.get(url)
        resp.raise_for_status()
        return resp.text
