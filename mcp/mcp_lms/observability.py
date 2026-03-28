"""VictoriaLogs and VictoriaTraces HTTP API clients."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

import httpx


@dataclass
class LogEntry:
    """A single log entry from VictoriaLogs."""

    timestamp: str
    message: str
    level: str
    service: str
    trace_id: str = ""
    span_id: str = ""
    raw: dict[str, Any] | None = None


@dataclass
class TraceSummary:
    """Summary of a trace."""

    trace_id: str
    service: str
    start_time: str
    duration_ms: int
    span_count: int
    has_error: bool


class VictoriaLogsClient:
    """Client for VictoriaLogs HTTP API."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def _client(self) -> httpx.Client:
        return httpx.Client(timeout=30.0)

    def search(
        self,
        query: str = "*",
        limit: int = 100,
        start_time: str | None = None,
        end_time: str | None = None,
    ) -> list[LogEntry]:
        """Search logs using LogsQL query."""
        url = f"{self.base_url}/select/logsql/query"
        params: dict[str, Any] = {"query": query, "limit": limit}

        if start_time:
            params["start"] = start_time
        if end_time:
            params["end"] = end_time

        try:
            with self._client() as c:
                r = c.get(url, params=params)
                r.raise_for_status()
                lines = r.text.strip().split("\n") if r.text else []
                entries = []
                for line in lines:
                    if not line.strip():
                        continue
                    try:
                        data = httpx.Response(line).json() if line.startswith("{") else eval(line)
                    except:
                        import json
                        try:
                            data = json.loads(line)
                        except:
                            continue

                    entries.append(
                        LogEntry(
                            timestamp=data.get("_time", ""),
                            message=data.get("_msg", ""),
                            level=data.get("severity", data.get("level", "INFO")),
                            service=data.get("service.name", data.get("service", "unknown")),
                            trace_id=data.get("trace_id", data.get("otelTraceID", "")),
                            span_id=data.get("span_id", data.get("otelSpanID", "")),
                            raw=data,
                        )
                    )
                return entries
        except httpx.ConnectError:
            return []
        except httpx.HTTPStatusError:
            return []
        except Exception:
            return []

    def count_errors(
        self,
        service: str | None = None,
        hours: int = 1,
    ) -> dict[str, int]:
        """Count errors per service over a time window."""
        end_time = "now"
        start_time = f"now-{hours}h"

        query = "severity:ERROR"
        if service:
            query = f'_stream:{{service="{service}"}} AND severity:ERROR'

        entries = self.search(query=query, limit=10000, start_time=start_time, end_time=end_time)

        # Count by service
        counts: dict[str, int] = {}
        for entry in entries:
            svc = entry.service
            counts[svc] = counts.get(svc, 0) + 1

        return counts


class VictoriaTracesClient:
    """Client for VictoriaTraces HTTP API (Jaeger-compatible)."""

    def __init__(self, base_url: str):
        # VictoriaTraces Jaeger API is at /select/jaeger/api/*
        self.base_url = base_url.rstrip("/") + "/select/jaeger/api"

    def _client(self) -> httpx.Client:
        return httpx.Client(timeout=30.0)

    def list_traces(
        self,
        service: str | None = None,
        limit: int = 20,
        lookback_hours: int = 1,
    ) -> list[TraceSummary]:
        """List recent traces."""
        # VictoriaTraces Jaeger API requires service parameter
        # Default to "Learning Management Service" if not specified
        if not service:
            service = "Learning Management Service"
        
        url = f"{self.base_url}/traces"
        params: dict[str, Any] = {"limit": limit, "service": service}

        try:
            with self._client() as c:
                r = c.get(url, params=params)
                if r.status_code != 200:
                    return []
                data = r.json()
                traces_data = data.get("data", [])

                results = []
                for trace in traces_data:
                    trace_id = trace.get("traceID", "")
                    spans = trace.get("spans", [])
                    processes = trace.get("processes", {})

                    if not spans:
                        continue

                    # Find min/max timestamps
                    timestamps = [s.get("startTime", 0) for s in spans]
                    min_ts = min(timestamps) if timestamps else 0
                    max_ts = max(timestamps) if timestamps else 0
                    duration_ms = max_ts - min_ts

                    # Check for errors
                    has_error = any(
                        any(t.get("key") == "error" for t in s.get("tags", [])) for s in spans
                    )

                    # Get service name from processes
                    service_name = "unknown"
                    for proc_id, proc in processes.items():
                        if proc.get("serviceName"):
                            service_name = proc.get("serviceName", "unknown")
                            break

                    results.append(
                        TraceSummary(
                            trace_id=trace_id,
                            service=service_name,
                            start_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(min_ts / 1000)),
                            duration_ms=int(duration_ms / 1000),
                            span_count=len(spans),
                            has_error=has_error,
                        )
                    )
                return results
        except Exception:
            return []

    def get_trace(self, trace_id: str) -> dict[str, Any] | None:
        """Get full trace details by ID."""
        url = f"{self.base_url}/traces/{trace_id}"

        try:
            with self._client() as c:
                r = c.get(url)
                if r.status_code != 200:
                    return None
                data = r.json()
                traces_data = data.get("data", [])
                return traces_data[0] if traces_data else None
        except Exception:
            return None
