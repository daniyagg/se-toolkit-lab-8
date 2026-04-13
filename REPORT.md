# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

### "What is the agentic loop?"

```
The agentic loop is the iterative cycle that an AI agent follows to accomplish tasks. Unlike a simple chatbot that gives a one-shot response, an agent repeatedly reasons, acts, and
observes until it reaches a goal.

The Core Loop

 ┌─────────────┐
 │   Observe   │ ← Receive input / environment state
 └──────┬──────┘
        ▼
 ┌─────────────┐
 │   Reason    │ ← Plan next step (think about what to do)
 └──────┬──────┘
        ▼
 ┌─────────────┐
 │    Act      │ ← Use a tool, call an API, execute code
 └──────┬──────┘
        ▼
 ┌─────────────┐
 │  Observe    │ ← Get the result of the action
 └──────┬──────┘
        ▼
   (repeat until goal is reached)

Key Components

 1 Observe — Perceive the current state (user input, tool outputs, environment)
 2 Reason — Decide what to do next based on the goal and current state
 3 Act — Execute an action (call a tool, run code, make an API call)
 4 Evaluate — Check if the goal is met or if more steps are needed

Example (what I just did with you)

When you asked "What is the agentic loop?", I went through this loop:

 • Observe: Read your question
 • Reason: Determine I can answer from my knowledge, no tools needed
 • Act: Generate this response
 • Evaluate: The answer is complete → done

For a more complex task (like "find the weather in Tokyo and save it to a file"), the loop would iterate multiple times — calling the weather tool, then the file tool, checking
results at each step.

Why It Matters

The agentic loop is what enables agents to:

 • Handle multi-step tasks autonomously
 • Recover from errors (retry, try alternative approaches)
 • Adapt based on intermediate results
 • Use tools dynamically rather than following a fixed script

This is essentially the pattern I'm running right now! 🐈
```

### "What labs are available in our LMS?"

```
Based on the LMS project structure, here's what's available:

Lab 8 — "The Agent is the Interface"

This is the current lab in your system. It focuses on deploying an AI agent (nanobot) as a conversational interface for the LMS.

Required Tasks

 Task    Title                                          Description
 ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 Task 1  Set Up the Agent                               Install nanobot, connect to Qwen API & LMS backend via MCP, write skill prompts
 Task 2  Deploy the Agent & Add a Web Client            Dockerize nanobot, add WebSocket channel, serve Flutter web client via Caddy
 Task 3  Give the Agent New Eyes (Observability)        Explore structured logs & traces, write MCP tools for VictoriaLogs/Traces
 Task 4  Diagnose a Failure & Make the Agent Proactive  Multi-step failure investigation, scheduled health checks via cron, fix planted bug

Optional Task

 Task             Title                      Description
 ──────────────────────────────────────────────────────────────────────────────────────────────────────
 Optional Task 1  Add a Telegram Bot Client  Wire up a Telegram bot as another client to the same agent

Key Concepts Covered

 • AI agents vs traditional clients — reasoning over hardcoded logic
 • MCP (Model Context Protocol) — reusable tool definitions
 • VictoriaLogs & VictoriaTraces — structured observability
 • Cron scheduling — proactive agent behavior

The lab files are located at /root/se-toolkit-lab-8/lab/tasks/ with the full plan in /root/se-toolkit-lab-8/instructors/lab-plan.md.
```

The agent explored local repo files (task files, lab-plan.md) and answered from documentation. It did **not** return real LMS backend data — confirming that without MCP tools, the agent has no live backend access.

---

## Task 1B — Agent with LMS tools

### "What labs are available?"

```
Here are the available labs:

 1 Lab 01 – Products, Architecture & Roles
 2 Lab 02 — Run, Fix, and Deploy a Backend Service
 3 Lab 03 — Backend API: Explore, Debug, Implement, Deploy
 4 Lab 04 — Testing, Front-end, and AI Agents
 5 Lab 05 — Data Pipeline and Analytics Dashboard
 6 Lab 06 — Build Your Own Agent
 7 Lab 07 — Build a Client with an AI Coding Agent
 8 lab-08

Let me know if you'd like stats, completion rates, or help with any specific lab! 🐈
```

The agent called `mcp_lms_lms_labs` and returned **real lab names** from the backend.

### "Is the LMS backend healthy?"

```
Yes, the LMS backend is healthy! ✅

 • Status: Healthy
 • Item count: 56
 • Errors: None
```

The agent called `mcp_lms_lms_health` and reported real health data from the backend.

---

## Task 1C — Skill prompt

### "Show me the scores"

```
Here are the available labs. Which one would you like to see the scores for?

 1 Lab 01 – Products, Architecture & Roles
 2 Lab 02 – Run, Fix, and Deploy a Backend Service
 3 Lab 03 – Backend API: Explore, Debug, Implement, Deploy
 4 Lab 04 – Testing, Front-end, and AI Agents
 5 Lab 05 – Data Pipeline and Analytics Dashboard
 6 Lab 06 – Build Your Own Agent
 7 Lab 07 – Build a Client with an AI Coding Agent
 8 Lab 08 – lab-08
```

The agent followed the skill strategy: called `lms_labs` first, listed all labs with full titles, and asked the user to choose one instead of guessing.

## Task 2A — Deployed agent

```
NAME                                IMAGE                                                                                         COMMAND                  SERVICE          CREATED       STATUS                 PORTS
se-toolkit-lab-8-backend-1          se-toolkit-lab-8-backend                                                                      "opentelemetry-instr…"   backend          9 hours ago   Up 9 hours             127.0.0.1:42001->8000/tcp
se-toolkit-lab-8-caddy-1            harbor.pg.innopolis.university/docker-hub-cache/caddy:2.11-alpine                             "caddy run --config …"   caddy            6 hours ago   Up 6 hours             443/tcp, 2019/tcp, 443/udp, 0.0.0.0:42002->80/tcp
se-toolkit-lab-8-nanobot-1          se-toolkit-lab-8-nanobot                                                                      "python /app/nanobot…"   nanobot          6 hours ago   Up 6 hours
se-toolkit-lab-8-otel-collector-1   harbor.pg.innopolis.university/docker-hub-cache/otel/opentelemetry-collector-contrib:latest   "/otelcol-contrib --…"   otel-collector   9 hours ago   Up 9 hours             4317-4318/tcp, 55679/tcp
se-toolkit-lab-8-pgadmin-1          harbor.pg.innopolis.university/docker-hub-cache/dpage/pgadmin4:latest                         "/entrypoint.sh"         pgadmin          9 hours ago   Up 9 hours             443/tcp, 127.0.0.1:42003->80/tcp
se-toolkit-lab-8-postgres-1         harbor.pg.innopolis.university/docker-hub-cache/postgres:18.3-alpine                          "docker-entrypoint.s…"   postgres         9 hours ago   Up 9 hours (healthy)   127.0.0.1:42004->5432/tcp
se-toolkit-lab-8-qwen-code-api-1    se-toolkit-lab-8-qwen-code-api                                                                "docker-entrypoint.s…"   qwen-code-api    9 hours ago   Up 9 hours (healthy)   127.0.0.1:42005->8080/tcp
se-toolkit-lab-8-victorialogs-1     harbor.pg.innopolis.university/docker-hub-cache/victoriametrics/victoria-logs:latest          "/victoria-logs-prod…"   victorialogs     9 hours ago   Up 9 hours             127.0.0.1:42010->9428/tcp
se-toolkit-lab-8-victoriatraces-1   harbor.pg.innopolis.university/docker-hub-cache/victoriametrics/victoria-traces:latest        "/victoria-traces-pr…"   victoriatraces   9 hours ago   Up 9 hours             127.0.0.1:42011->10428/tcp
```

**Nanobot startup log excerpt:**

```
Using config: /app/nanobot/config.resolved.json
🐈 Starting nanobot gateway version 0.1.4.post5 on port 18790...
✓ Channels enabled: webchat
Starting webchat channel...
WebChat relay listening on 127.0.0.1:8766
WebChat starting on 0.0.0.0:8765
MCP server 'lms': connected, 9 tools registered
MCP: registered tool 'mcp_webchat_ui_message' from server 'webchat'
MCP server 'webchat': connected, 1 tools registered
Agent loop started
```

All services started cleanly. Webchat channel enabled, both MCP servers (lms + webchat) connected.

## Task 2B — Web client
<img width="1919" height="964" alt="image" src="https://github.com/user-attachments/assets/2f180207-c175-41c4-918c-82d468cbc98d" />

### WebSocket endpoint test

```
$ echo '{"content":"What labs are available?"}' | websocat "ws://localhost:42002/ws/chat?access_key=my-secret-key"

Response:
Here are the available labs:
1. Lab 01 – Products, Architecture & Roles
2. Lab 02 – Run, Fix, and Deploy a Backend Service
3. Lab 03 – Backend API: Explore, Debug, Implement, Deploy
4. Lab 04 – Testing, Front-end, and AI Agents
5. Lab 05 – Data Pipeline and Analytics Dashboard
6. Lab 06 – Build Your Own Agent
7. Lab 07 – Build a Client with an AI Coding Agent
8. Lab 08 – lab-08
```

### Flutter web client tests

**"What can you do in this system?"** — agent responded with capabilities description.

**"How is the backend doing?"** — real LMS data:
```
The backend is healthy 🟢 — currently holding 56 items. Everything looks good!
```

**"Show me the scores"** — structured UI choice rendered (not raw JSON):
```
Type: choice
Options:
  - Lab 01 – Products, Architecture & Roles (lab-01)
  - Lab 02 – Run, Fix, and Deploy a Backend Service (lab-02)
  - Lab 03 – Backend API: Explore, Debug, Implement, Deploy (lab-03)
  - ... (8 labs total)

Agent follow-up: "I've sent you a list of available labs — please pick which one you'd like to see the scores for! 📊"
```

The Flutter client at `http://<vm-ip>:42002/flutter` loads the login screen, accepts the access key, and renders structured choice prompts instead of raw JSON.

## Task 3A — Structured logging

### Happy-path log excerpt (request_started → request_completed, status 200)

```
backend-1  | 2026-04-13 19:17:01,835 INFO [lms_backend.main] [main.py:62] [trace_id=fbfc25966777426ac9bbc0b1a382a53d span_id=271a3928f5ebf037 resource.service.name=Learning Management Service trace_sampled=True] - request_started
backend-1  | 2026-04-13 19:17:01,837 INFO [lms_backend.auth] [auth.py:30] [trace_id=fbfc25966777426ac9bbc0b1a382a53d span_id=271a3928f5ebf037 resource.service.name=Learning Management Service trace_sampled=True] - auth_success
backend-1  | 2026-04-13 19:17:01,838 INFO [lms_backend.db.items] [items.py:16] [trace_id=fbfc25966777426ac9bbc0b1a382a53d span_id=271a3928f5ebf037 resource.service.name=Learning Management Service trace_sampled=True] - db_query
backend-1  | 2026-04-13 19:17:01,845 INFO [lms_backend.main] [main.py:74] [trace_id=fbfc25966777426ac9bbc0b1a382a53d span_id=271a3928f5ebf037 resource.service.name=Learning Management Service trace_sampled=True] - request_completed
backend-1  | INFO:     172.21.0.9:52712 - "GET /items/ HTTP/1.1" 200 OK
```

All four structured events share the same `trace_id` — showing the full request lifecycle.

### Error-path log excerpt (PostgreSQL stopped)

```
backend-1  | 2026-04-13 19:36:27,200 INFO [lms_backend.main] [main.py:74] [trace_id=7d1e7169d1ce87545bacd8e4c1346220 span_id=2a2ea3b2ddc6db9f resource.service.name=Learning Management Service trace_sampled=True] - request_completed
backend-1  | INFO:     172.21.0.9:40256 - "GET /items/ HTTP/1.1" 404 Not Found
backend-1  | INFO:     172.21.0.9:40256 - "GET /items/ HTTP/1.1" 404
```

After stopping PostgreSQL, the request completes with `404 Not Found` instead of `200 OK`. The `db_query` event is missing — the database connection failed so the query never executed.

### VictoriaLogs UI query

<!-- Screenshot: VictoriaLogs query result for _time:1h service.name:"Learning Management Service" severity:ERROR -->
<img width="1280" height="679" alt="image" src="https://github.com/user-attachments/assets/6a5b4682-5aec-4113-abd5-34f9d247246e" />


## Task 3B — Traces

### Healthy trace (PostgreSQL running)

**TraceID:** `3d30b21f3af95684965afd7292ed0bee`

Command used:
```bash
curl -s "http://localhost:42011/select/jaeger/api/traces/3d30b21f3af95684965afd7292ed0bee"
```

**Span hierarchy (8 spans, total ~94ms):**

```
GET /items/ [server] — 94,114us — status=200
  ├── connect [client, sqlalchemy] — 58,104us — postgres:5432
  ├── SELECT db-lab-8 [client, sqlalchemy] — 26,631us — "SELECT item.id, item.type, ... FROM item"
  ├── BEGIN; [client, asyncpg] — 5,415us
  ├── ROLLBACK; [client, asyncpg] — 365us
  └── GET /items/ http send [internal, fastapi] — 109us — status=200 (http.response.start)
      ├── GET /items/ http send — 35us — http.response.body
      └── GET /items/ http send — 26us — http.response.body
```

The healthy trace shows a clean request lifecycle: FastAPI receives `GET /items/`, SQLAlchemy connects to PostgreSQL (58ms), executes the SELECT query (27ms), wraps in a transaction (BEGIN → ROLLBACK), and returns HTTP 200.

<!-- Screenshot: VictoriaTraces UI showing the span hierarchy for trace 3d30b21f3af95684965afd7292ed0bee -->
<img width="1280" height="578" alt="image" src="https://github.com/user-attachments/assets/84f62388-1025-4584-9d1a-947f5139d7e5" />

### Error trace (PostgreSQL stopped)

**TraceID:** `7d1e7169d1ce87545bacd8e4c1346220`

Command used:
```bash
curl -s "http://localhost:42011/select/jaeger/api/traces/7d1e7169d1ce87545bacd8e4c1346220"
```

**Span hierarchy (6 spans, error on connect):**

```
GET /items/ [server] — 237,446us — status=404
  ├── connect [client, sqlalchemy] — 229,808us — ERROR: [Errno -2] Name or service not known
  │   └── exception log: "Name or service not known" at sqlalchemy/engine/base.py:3293
  └── GET /items/ http send [internal, fastapi] — 74us — status=404 (http.response.start)
      ├── GET /items/ http send — 52us — http.response.body
      └── GET /items/ http send — 42us — http.response.body
```

The error trace shows the failure point clearly: the `connect` span (229ms) throws `[Errno -2] Name or service not known` — a DNS resolution failure because PostgreSQL is stopped. No `SELECT` or `BEGIN` spans appear because the database connection never succeeded. The request returns HTTP 404 instead of 200.

Key difference from healthy trace:
| Span | Healthy | Error |
|------|---------|-------|
| `connect` | 58ms ✅ | 229ms ❌ DNS failure |
| `SELECT` | 27ms ✅ | missing |
| `BEGIN` | 5ms ✅ | missing |
| HTTP status | 200 | 404 |

<!-- Screenshot: VictoriaTraces UI showing error trace with exception log on connect span -->
<img width="1662" height="742" alt="image" src="https://github.com/user-attachments/assets/4c1048c7-1e8a-42cb-899f-a4d16a205825" />

## Task 3C — Observability MCP tools

### Normal conditions (PostgreSQL running)

**Question:** "Any LMS backend errors in the last 10 minutes?"

**Response:**
> No errors found in the LMS backend in the last 10 minutes. The system appears to be running cleanly.

### Failure conditions (PostgreSQL stopped)

**Question:** "Any LMS backend errors in the last 10 minutes?"

**Response:**
> There was **1 error** in the Learning Management Service in the last 10 minutes. Let me pull the details.
>
> Found the issue! There are **2 recent errors** in the Learning Management Service. Both are **DNS resolution failures** during database queries:
>
> - **Error**: `[Errno -2] Name or service not known`
> - **Operation**: `SELECT` on the `item` table
> - **Time**: ~20:24–20:25 UTC
>
> This means the LMS backend **can't resolve the database hostname** — it's a DNS/network connectivity issue, not a code problem. This explains the HTTP 404 we saw earlier when trying to fetch labs.
>
> ## Summary
>
> **Yes, there are LMS backend errors in the last 10 minutes.** The issue is a **DNS resolution failure** — the LMS backend can't resolve the database hostname (`[Errno -2] Name or service not known`) when trying to query the `item` table. This is why the `/items/` endpoint returns HTTP 404.
>
> **Root cause**: Network/DNS configuration issue between the LMS backend and the database. The database hostname is unresolvable from the backend container.
>
> **Recommended fix**: Check that the database service is running and that the hostname (likely something like `postgres` or `db`) is correctly configured in the LMS backend's environment variables and resolvable within the Docker/network setup.

## Task 4A — Multi-step investigation

**Agent's response to "What went wrong?"** (with PostgreSQL stopped):

> Here's what went wrong:
>
> **Root cause: DNS resolution failure for the PostgreSQL database.**
>
> The trace shows the full request path:
>
> 1. **MCP-LMS** → sent `GET http://backend:8000/items/`
> 2. **Learning Management Service** → received the request, tried to query the `item` table
> 3. **Database connection failed** → `socket.gaierror: [Errno -2] Name or service not known`
>    - Target: `postgres:5432`, database `db-lab-8`
> 4. **404 returned** → the LMS returned a 404 because it couldn't reach the database
>
> **The LMS backend can't resolve the hostname `postgres`.** This typically means:
> - The PostgreSQL container is **down** or **restarting**
> - The `postgres` container is **not on the same Docker network** as the backend
> - The database hostname in the LMS configuration is **incorrect**
>
> Would you like me to check if there are any other recent errors, or is this something you need to fix on the infrastructure side?

**MCP tool calls observed** (from nanobot logs):

```
mcp_obs_logs_error_count({"service": "Learning Management Service", "time_window": "10m"})
mcp_obs_logs_search({"query": "_time:10m service.name:\"Learning Management Service\" severity:ERROR", "limit": 10})
mcp_obs_traces_get({"trace_id": "4f18a3dae8b1b9a281a30810a9ea42d9"})
```

The agent chained all three observability tools in the correct order: error count → log search → trace fetch → summary.

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->
<img width="1280" height="679" alt="image" src="https://github.com/user-attachments/assets/69407f39-9ecd-446b-9441-b6f1da64a3c0" />


## Task 4C — Bug fix and recovery

### 1. Root cause

The planted bug was in `backend/src/lms_backend/routers/items.py`, lines 18–30:

```python
@router.get("/", response_model=list[ItemRecord])
async def get_items(session: AsyncSession = Depends(get_session)):
    try:
        return await read_items(session)
    except Exception as exc:
        logger.warning("items_list_failed_as_not_found", ...)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Items not found",
        ) from exc
```

A broad `except Exception` block caught **all** errors (including PostgreSQL connection failures) and returned a misleading `404 Items not found`. The real cause — DNS resolution failure for `postgres:5432` — was hidden.

### 2. Fix

Removed the `try/except` wrapper so that database errors propagate to the global exception handler in `main.py`, which returns `500 Internal Server Error` with the real error details:

```python
@router.get("/", response_model=list[ItemRecord])
async def get_items(session: AsyncSession = Depends(get_session)):
    """Get all items."""
    return await read_items(session)
```

### 3. Post-fix failure check

After redeploy, with PostgreSQL stopped, asking **"What went wrong?"** now shows:

> The LMS backend is **still unable to connect to its PostgreSQL database**. Here's the summary:
>
> | Issue | Detail |
> |-------|--------|
> | **Error** | `socket.gaierror: [Errno -2] Name or service not known` |
> | **Root Cause** | The backend container cannot resolve the hostname `postgres` |
> | **Target** | `postgres:5432`, database `db-lab-8` |
> | **Symptom** | `GET /items/` returns **500 Internal Server Error** |
> | **Impact** | All lab data queries fail — no labs, learners, or scores can be fetched |

**Key change:** Before the fix → `404 Items not found`. After the fix → `500 Internal Server Error` with the real PostgreSQL connection failure.

### 4. Healthy follow-up

After restarting PostgreSQL, the backend recovered:

> The backend is **fully recovered** and healthy! ✅
> - Status: Healthy
> - Items: 56
> - No errors in the last 2 minutes

<!-- Screenshot: healthy health report from Flutter chat -->
<img width="1918" height="1021" alt="image" src="https://github.com/user-attachments/assets/9e782500-c078-4429-9326-7714cc42b29a" />


A new health check (job `62f856ad`) now runs every 15 minutes and reports the system as healthy.
