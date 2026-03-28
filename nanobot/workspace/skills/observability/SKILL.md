# Observability Skill

You have access to **VictoriaLogs** and **VictoriaTraces** — the observability stack for this system. Use these tools to investigate errors, trace request flows, and answer questions about system health.

## Available Tools

### Log Tools (VictoriaLogs)

- **`logs_search`** — Search logs using LogsQL queries
  - Use when: User asks about specific events, errors, or time periods
  - Example queries: `"level:error"`, `"_stream:{service=\"backend\"}"`, `"event:request_started"`
  - Time range: Use `start="-1h"` for last hour, `start="-24h"` for last day

- **`logs_error_count`** — Count errors per service over a time window
  - Use when: User asks "any errors?", "is the system healthy?", or "what's broken?"
  - Returns: Error counts grouped by service with sample error messages

### Trace Tools (VictoriaTraces)

- **`traces_list`** — List recent traces for a service
  - Use when: You need to find trace IDs for investigation
  - Returns: Trace summaries with duration, span count, and error indicators

- **`traces_get`** — Fetch detailed trace by ID
  - Use when: You have a trace ID and need to see the full span hierarchy
  - Returns: Span tree showing operation names, durations, and error markers

## Investigation Patterns

### Pattern 1: Quick Health Check

When asked "any errors in the last hour?" or "is the system healthy?":

1. Call `logs_error_count` with `start="-1h"` to get error counts by service
2. If errors found, call `logs_search` with `query="level:error"` and `start="-1h"` to see details
3. Summarize: which services have errors, how many, and what the errors are

### Pattern 2: Deep Dive on Specific Error

When logs show an error with a trace ID, or user asks about a specific failure:

1. Call `logs_search` to find the error details and any trace IDs
2. If trace ID found, call `traces_get` with that ID
3. Examine the span hierarchy — look for spans marked `[ERROR]`
4. Report: which operation failed, how long it took, and what came before/after

### Pattern 3: Request Flow Investigation

When user asks "what happened when a user requested X?":

1. Call `logs_search` with `query="event:request_started"` and relevant filters
2. Find the trace ID from log entries
3. Call `traces_get` to see the full flow
4. Report: which services were involved, how long each step took, where it succeeded or failed

## Response Style

- **Be concise** — summarize findings, don't dump raw JSON
- **Highlight errors** — if you find errors, say which service and what the error is
- **Include time context** — "in the last hour", "since 2pm UTC", etc.
- **Offer next steps** — "Want me to fetch the full trace?" or "Should I check the last 24 hours?"

## Example Queries

**"Any errors in the last hour?"**
→ Call `logs_error_count(start="-1h")` → Report counts by service

**"Show me backend errors"**
→ Call `logs_search(query="level:error AND _stream:{service=\"backend\"}", start="-1h")`

**"What's the trace for request XYZ?"**
→ Call `traces_get(trace_id="XYZ")` → Show span hierarchy

**"Is the LMS backend healthy?"**
→ Call `logs_error_count(service="backend", start="-1h")` → Report if any errors found

## Important Notes

- VictoriaLogs URL: configured via `VICTORIALOGS_URL` (default: `http://localhost:9428`)
- VictoriaTraces URL: configured via `VICTORIATRACES_URL` (default: `http://localhost:10428`)
- In Docker Compose, use service names: `victorialogs:9428` and `victoriatrace:10428`
- LogsQL syntax: `_stream:{service="backend"}` filters by service, `level:error` filters by level
- Trace IDs are long hex strings — you may see them in log entries as `trace_id` field
