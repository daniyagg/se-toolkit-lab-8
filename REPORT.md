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

<!-- Paste a short nanobot startup log excerpt showing the gateway started inside Docker -->

## Task 2B — Web client

<!-- Screenshot of a conversation with the agent in the Flutter web app -->

## Task 3A — Structured logging

<!-- Paste happy-path and error-path log excerpts, VictoriaLogs query screenshot -->

## Task 3B — Traces

<!-- Screenshots: healthy trace span hierarchy, error trace -->

## Task 3C — Observability MCP tools

<!-- Paste agent responses to "any errors in the last hour?" under normal and failure conditions -->

## Task 4A — Multi-step investigation

<!-- Paste the agent's response to "What went wrong?" showing chained log + trace investigation -->

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->

## Task 4C — Bug fix and recovery

<!-- 1. Root cause identified
     2. Code fix (diff or description)
     3. Post-fix response to "What went wrong?" showing the real underlying failure
     4. Healthy follow-up report or transcript after recovery -->
