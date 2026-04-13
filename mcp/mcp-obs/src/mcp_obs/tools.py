"""Tool schemas, handlers, and registry for the observability MCP server."""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Sequence
from dataclasses import dataclass

from mcp.types import Tool
from pydantic import BaseModel, Field

from mcp_obs.client import ObsClient


class LogsSearchArgs(BaseModel):
    query: str = Field(
        description="LogsQL query, e.g. '_time:10m service.name:\"Learning Management Service\" severity:ERROR'"
    )
    limit: int = Field(
        default=50, ge=1, le=1000, description="Max log entries to return (default 50)."
    )


class LogsErrorCountArgs(BaseModel):
    service: str = Field(
        description='Service name, e.g. "Learning Management Service".'
    )
    time_window: str = Field(
        default="1h",
        description="Time window, e.g. '10m', '1h', '24h'.",
    )


class TracesListArgs(BaseModel):
    service: str = Field(
        description='Service name, e.g. "Learning Management Service".'
    )
    limit: int = Field(
        default=10, ge=1, le=100, description="Max traces to return (default 10)."
    )


class TracesGetArgs(BaseModel):
    trace_id: str = Field(description="Trace ID to fetch, e.g. 'fbfc25966777426ac9bbc0b1a382a53d'.")


ToolPayload = BaseModel | Sequence[BaseModel]
ToolHandler = Callable[[ObsClient, BaseModel], Awaitable[ToolPayload]]


@dataclass(frozen=True, slots=True)
class ToolSpec:
    name: str
    description: str
    model: type[BaseModel]
    handler: ToolHandler

    def as_tool(self) -> Tool:
        schema = self.model.model_json_schema()
        schema.pop("$defs", None)
        schema.pop("title", None)
        return Tool(name=self.name, description=self.description, inputSchema=schema)


async def _logs_search(client: ObsClient, args: BaseModel) -> ToolPayload:
    a = args if isinstance(args, LogsSearchArgs) else LogsSearchArgs.model_validate(args.model_dump())
    return await client.query_logs(a.query, a.limit)


async def _logs_error_count(client: ObsClient, args: BaseModel) -> ToolPayload:
    a = args if isinstance(args, LogsErrorCountArgs) else LogsErrorCountArgs.model_validate(args.model_dump())
    return await client.count_errors(a.service, a.time_window)


async def _traces_list(client: ObsClient, args: BaseModel) -> ToolPayload:
    a = args if isinstance(args, TracesListArgs) else TracesListArgs.model_validate(args.model_dump())
    return await client.list_traces(a.service, a.limit)


async def _traces_get(client: ObsClient, args: BaseModel) -> ToolPayload:
    a = args if isinstance(args, TracesGetArgs) else TracesGetArgs.model_validate(args.model_dump())
    return await client.get_trace(a.trace_id)


TOOL_SPECS = (
    ToolSpec(
        "logs_search",
        "Search VictoriaLogs by LogsQL query and/or time range. Use to find specific log entries or errors.",
        LogsSearchArgs,
        _logs_search,
    ),
    ToolSpec(
        "logs_error_count",
        "Count error-level log entries for a service over a time window. Use to check if there are recent errors.",
        LogsErrorCountArgs,
        _logs_error_count,
    ),
    ToolSpec(
        "traces_list",
        "List recent traces for a service from VictoriaTraces. Returns trace IDs and operation names.",
        TracesListArgs,
        _traces_list,
    ),
    ToolSpec(
        "traces_get",
        "Fetch a specific trace by ID from VictoriaTraces. Shows the full span hierarchy and timing.",
        TracesGetArgs,
        _traces_get,
    ),
)
TOOLS_BY_NAME = {spec.name: spec for spec in TOOL_SPECS}
