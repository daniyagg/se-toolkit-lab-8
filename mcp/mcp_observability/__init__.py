"""Observability MCP server exposing VictoriaLogs and VictoriaTraces as typed tools."""

from __future__ import annotations

import asyncio
import json
import os
from collections.abc import Awaitable, Callable
from typing import Any
from urllib.parse import quote

import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel, Field

server = Server("observability")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

_VICTORIALOGS_URL: str = ""
_VICTORIATRACES_URL: str = ""

# ---------------------------------------------------------------------------
# Input models
# ---------------------------------------------------------------------------


class _LogsSearchArgs(BaseModel):
    query: str = Field(
        description="LogsQL query string, e.g. 'level:error' or '_stream:{service=\"backend\"}'"
    )
    limit: int = Field(
        default=100, ge=1, le=1000, description="Max entries to return (default 100)"
    )
    start: str = Field(
        default="-1h",
        description="Start time for search (e.g., '-1h', '-24h', '2024-01-01T00:00:00Z')",
    )
    end: str = Field(
        default="now", description="End time (e.g., 'now' or specific timestamp)"
    )


class _LogsErrorCountArgs(BaseModel):
    service: str = Field(
        default="*", description="Service name to filter (use '*' for all services)"
    )
    start: str = Field(
        default="-1h", description="Start time window (e.g., '-1h', '-24h')"
    )
    end: str = Field(default="now", description="End time (e.g., 'now')")


class _TracesListArgs(BaseModel):
    service: str = Field(description="Service name to list traces for")
    limit: int = Field(
        default=20, ge=1, le=100, description="Max traces to return (default 20)"
    )
    start: str = Field(
        default="-1h", description="Start time window (e.g., '-1h', '-24h')"
    )


class _TracesGetArgs(BaseModel):
    trace_id: str = Field(description="The trace ID to fetch details for")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _text(data: Any) -> list[TextContent]:
    """Serialize data to a JSON text block."""
    return [TextContent(type="text", text=json.dumps(data, ensure_ascii=False, indent=2))]


def _format_log_entry(entry: dict) -> str:
    """Format a log entry for human readability."""
    timestamp = entry.get("timestamp", entry.get("_timestamp", "unknown"))
    level = entry.get("level", "unknown")
    service = entry.get("service", entry.get("_stream", "unknown"))
    message = entry.get("message", entry.get("msg", str(entry)))
    return f"[{timestamp}] [{level.upper()}] {service}: {message}"


def _format_trace_summary(trace: dict) -> str:
    """Format a trace summary for human readability."""
    trace_id = trace.get("traceID", "unknown")
    service = trace.get("serviceName", "unknown")
    duration = trace.get("duration", 0) / 1_000_000  # Convert to seconds
    spans = len(trace.get("spans", []))
    errors = sum(1 for s in trace.get("spans", []) if s.get("tags", {}).get("error"))
    return f"Trace {trace_id[:16]}... | {service} | {duration:.3f}s | {spans} spans | {errors} errors"


# ---------------------------------------------------------------------------
# VictoriaLogs tools
# ---------------------------------------------------------------------------


async def _logs_search(args: _LogsSearchArgs) -> list[TextContent]:
    """Search VictoriaLogs using LogsQL query."""
    if not _VICTORIALOGS_URL:
        return _text({"error": "VictoriaLogs URL not configured"})

    url = f"{_VICTORIALOGS_URL}/select/logsql/query"
    params = {
        "query": args.query,
        "limit": args.limit,
        "start": args.start,
        "end": args.end,
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            # VictoriaLogs returns data in various formats depending on query type
            if isinstance(data, dict):
                entries = data.get("entries", data.get("data", []))
            elif isinstance(data, list):
                entries = data
            else:
                entries = [data]

            # Format for readability
            formatted = [_format_log_entry(e) if isinstance(e, dict) else str(e) for e in entries[:20]]
            result = {
                "query": args.query,
                "total_found": len(entries),
                "showing": min(20, len(entries)),
                "entries": formatted,
                "raw_data": entries[:50],  # Include some raw data for programmatic use
            }
            return _text(result)
    except httpx.HTTPError as e:
        return _text({"error": f"HTTP error: {e}", "status_code": getattr(e, "status_code", None)})
    except Exception as e:
        return _text({"error": f"Error: {type(e).__name__}: {e}"})


async def _logs_error_count(args: _LogsErrorCountArgs) -> list[TextContent]:
    """Count errors per service over a time window."""
    if not _VICTORIALOGS_URL:
        return _text({"error": "VictoriaLogs URL not configured"})

    # Build LogsQL query for error counting
    if args.service == "*":
        query = 'level:error OR level:ERROR OR level:"error"'
    else:
        query = f'_stream:{{service="{args.service}"}} AND (level:error OR level:ERROR OR level:"error")'

    url = f"{_VICTORIALOGS_URL}/select/logsql/query"
    params = {
        "query": query,
        "limit": 1000,
        "start": args.start,
        "end": args.end,
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if isinstance(data, dict):
                entries = data.get("entries", data.get("data", []))
            elif isinstance(data, list):
                entries = data
            else:
                entries = [data]

            # Count errors by service
            error_counts: dict[str, int] = {}
            error_types: dict[str, list[str]] = {}

            for entry in entries:
                if isinstance(entry, dict):
                    service = entry.get("service", entry.get("_stream", "unknown"))
                    error_msg = entry.get("error", entry.get("message", entry.get("msg", "unknown error")))
                    error_counts[service] = error_counts.get(service, 0) + 1
                    if service not in error_types:
                        error_types[service] = []
                    if len(error_types[service]) < 5:  # Keep sample of error messages
                        error_types[service].append(error_msg)

            result = {
                "query": query,
                "time_range": {"start": args.start, "end": args.end},
                "total_errors": sum(error_counts.values()),
                "errors_by_service": error_counts,
                "sample_errors": error_types,
            }
            return _text(result)
    except httpx.HTTPError as e:
        return _text({"error": f"HTTP error: {e}", "status_code": getattr(e, "status_code", None)})
    except Exception as e:
        return _text({"error": f"Error: {type(e).__name__}: {e}"})


# ---------------------------------------------------------------------------
# VictoriaTraces tools
# ---------------------------------------------------------------------------


async def _traces_list(args: _TracesListArgs) -> list[TextContent]:
    """List recent traces for a service."""
    if not _VICTORIATRACES_URL:
        return _text({"error": "VictoriaTraces URL not configured"})

    # VictoriaTraces Jaeger API endpoint
    url = f"{_VICTORIATRACES_URL}/jaeger/api/traces"
    params = {
        "service": args.service,
        "limit": args.limit,
        "start": args.start,
        "end": "now",
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            # Jaeger API returns {"data": [...]}
            traces = data.get("data", []) if isinstance(data, dict) else data

            # Format summaries
            summaries = [_format_trace_summary(t) for t in traces[:20]]

            result = {
                "service": args.service,
                "time_range": {"start": args.start, "end": "now"},
                "total_traces": len(traces),
                "showing": min(20, len(traces)),
                "traces": summaries,
                "trace_ids": [t.get("traceID") for t in traces[:20]],
            }
            return _text(result)
    except httpx.HTTPError as e:
        return _text({"error": f"HTTP error: {e}", "status_code": getattr(e, "status_code", None)})
    except Exception as e:
        return _text({"error": f"Error: {type(e).__name__}: {e}"})


async def _traces_get(args: _TracesGetArgs) -> list[TextContent]:
    """Fetch a specific trace by ID."""
    if not _VICTORIATRACES_URL:
        return _text({"error": "VictoriaTraces URL not configured"})

    url = f"{_VICTORIATRACES_URL}/jaeger/api/traces/{quote(args.trace_id)}"

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

            # Jaeger API returns {"data": [trace]}
            traces = data.get("data", []) if isinstance(data, dict) else data
            trace = traces[0] if traces else None

            if not trace:
                return _text({"error": f"Trace not found: {args.trace_id}"})

            # Build span hierarchy summary
            spans = trace.get("spans", [])
            span_summary = []
            for span in spans:
                indent = "  " * (span.get("depth", 0))
                operation = span.get("operationName", "unknown")
                duration = span.get("duration", 0) / 1_000_000  # Convert to seconds
                tags = span.get("tags", [])
                error_tag = any(t.get("key") == "error" for t in tags)
                error_marker = " [ERROR]" if error_tag else ""
                span_summary.append(f"{indent}{operation}: {duration:.3f}s{error_marker}")

            result = {
                "trace_id": trace.get("traceID"),
                "service": trace.get("serviceName"),
                "duration_seconds": trace.get("duration", 0) / 1_000_000,
                "span_count": len(spans),
                "has_errors": any(
                    any(t.get("key") == "error" for t in span.get("tags", []))
                    for span in spans
                ),
                "span_hierarchy": span_summary,
            }
            return _text(result)
    except httpx.HTTPError as e:
        return _text({"error": f"HTTP error: {e}", "status_code": getattr(e, "status_code", None)})
    except Exception as e:
        return _text({"error": f"Error: {type(e).__name__}: {e}"})


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

_Registry = tuple[type[BaseModel], Callable[..., Awaitable[list[TextContent]]], Tool]

_TOOLS: dict[str, _Registry] = {}


def _register(
    name: str,
    description: str,
    model: type[BaseModel],
    handler: Callable[..., Awaitable[list[TextContent]]],
) -> None:
    schema = model.model_json_schema()
    schema.pop("$defs", None)
    schema.pop("title", None)
    _TOOLS[name] = (model, handler, Tool(name=name, description=description, inputSchema=schema))


_register(
    "logs_search",
    "Search VictoriaLogs using LogsQL. Use for finding specific log entries, errors, or events. "
    "Examples: 'level:error', '_stream:{service=\"backend\"}', 'event:request_started'",
    _LogsSearchArgs,
    _logs_search,
)

_register(
    "logs_error_count",
    "Count errors per service over a time window. Use for quick health checks and error summaries.",
    _LogsErrorCountArgs,
    _logs_error_count,
)

_register(
    "traces_list",
    "List recent traces for a service. Use to find trace IDs for detailed investigation.",
    _TracesListArgs,
    _traces_list,
)

_register(
    "traces_get",
    "Fetch detailed information about a specific trace by ID. Shows span hierarchy, durations, and errors.",
    _TracesGetArgs,
    _traces_get,
)


# ---------------------------------------------------------------------------
# MCP handlers
# ---------------------------------------------------------------------------


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [entry[2] for entry in _TOOLS.values()]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
    entry = _TOOLS.get(name)
    if entry is None:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]

    model_cls, handler, _ = entry
    try:
        args = model_cls.model_validate(arguments or {})
        return await handler(args)
    except Exception as exc:
        return [TextContent(type="text", text=f"Error: {type(exc).__name__}: {exc}")]


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


async def main(
    victorialogs_url: str | None = None,
    victoriatrace_url: str | None = None,
) -> None:
    global _VICTORIALOGS_URL, _VICTORIATRACES_URL
    _VICTORIALOGS_URL = victorialogs_url or os.environ.get("VICTORIALOGS_URL", "http://localhost:9428")
    _VICTORIATRACES_URL = victoriatrace_url or os.environ.get("VICTORIATRACES_URL", "http://localhost:10428")
    async with stdio_server() as (read_stream, write_stream):
        init_options = server.create_initialization_options()
        await server.run(read_stream, write_stream, init_options)


if __name__ == "__main__":
    asyncio.run(main())
