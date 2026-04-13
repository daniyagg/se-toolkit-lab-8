---
name: observability
description: Use observability MCP tools to investigate logs and traces
always: true
---

# Observability Skill

You have access to VictoriaLogs and VictoriaTraces via MCP tools. Use them to investigate errors, trace request failures, and diagnose system health.

## Available tools

| Tool | What it does | Parameters |
|------|-------------|------------|
| `logs_search` | Search VictoriaLogs by LogsQL query | `query` (required), `limit` (optional, default 50) |
| `logs_error_count` | Count errors for a service over a time window | `service` (required), `time_window` (optional, default "1h") |
| `traces_list` | List recent traces for a service | `service` (required), `limit` (optional, default 10) |
| `traces_get` | Fetch a specific trace by ID | `trace_id` (required) |

## Strategy

- **When the user asks about errors or failures:**
  1. First call `logs_error_count` to check if there are recent errors for the relevant service.
  2. If errors exist, call `logs_search` with a scoped query (e.g., `_time:10m service.name:"Learning Management Service" severity:ERROR`) to inspect the details and extract a `trace_id`.
  3. If you find a `trace_id` in the logs, call `traces_get` to fetch the full trace and identify where the failure occurred.
  4. Summarize findings concisely — don't dump raw JSON.

- **When the user asks "is the system healthy?":**
  1. Call `logs_error_count` with a short time window (e.g., "10m") for key services.
  2. Report whether there are recent errors or not.

- **When investigating a specific issue:**
  1. Use `logs_search` with a time-scoped query to find relevant log entries.
  2. Extract `trace_id` from log entries if available.
  3. Use `traces_get` to inspect the full request path.

## Query patterns

- Search for LMS errors in the last 10 minutes:
  ```
  _time:10m service.name:"Learning Management Service" severity:ERROR
  ```

- Search for all errors in the last hour:
  ```
  _time:1h severity:ERROR
  ```

- The most useful fields are: `service.name`, `severity`, `event`, `trace_id`.

## Response guidelines

- Summarize findings in plain language: "There were 3 errors in the LMS backend in the last 10 minutes. The failures occurred during database queries — PostgreSQL connection refused."
- If you find a trace, explain the span hierarchy briefly: "The request failed at the db_query span after 2ms — the database was unreachable."
- Don't dump raw JSON or long log outputs unless the user explicitly asks for them.
- If no errors are found, say so clearly: "No errors found in the LMS backend in the last 10 minutes."

## Error handling

- If the observability tools are unreachable, explain that the logging infrastructure may be down.
- If a query returns empty results, say "No matching entries found" rather than returning empty output.
- If a trace ID is invalid or not found, explain that the trace may have expired or the ID is incorrect.
