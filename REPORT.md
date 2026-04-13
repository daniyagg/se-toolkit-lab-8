# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

### "What is the agentic loop?"

The agentic loop is the iterative cycle that an AI agent follows to accomplish tasks. Unlike a simple chatbot that gives a one-shot response, an agent repeatedly reasons, acts, and observes until it reaches a goal.

**The Core Loop:**

```
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
```

**Key Components:**
1. **Observe** — Perceive the current state (user input, tool outputs, environment)
2. **Reason** — Decide what to do next based on the goal and current state
3. **Act** — Execute an action (call a tool, run code, make an API call)
4. **Evaluate** — Check if the goal is met or if more steps are needed

The agent answered with a diagram and explained that this is the pattern it's running right now.

### "What labs are available in our LMS?"

The agent could **not** return real LMS backend data. Instead, it explored local repo files (task files, lab-plan.md) and answered from documentation — listing Lab 8 tasks and their descriptions. This confirms that without MCP tools, the agent has no live backend access.

---

## Task 1B — Agent with LMS tools

### "What labs are available?"

The agent called `mcp_lms_lms_labs` and returned real lab names from the backend:

1. Lab 01 – Products, Architecture & Roles
2. Lab 02 — Run, Fix, and Deploy a Backend Service
3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
4. Lab 04 — Testing, Front-end, and AI Agents
5. Lab 05 — Data Pipeline and Analytics Dashboard
6. Lab 06 — Build Your Own Agent
7. Lab 07 — Build a Client with an AI Coding Agent
8. lab-08

### "Is the LMS backend healthy?"

The agent called `mcp_lms_lms_health` and reported:
- **Status**: Healthy
- **Item count**: 56
- **Errors**: None

---

## Task 1C — Skill prompt

### "Show me the scores"

The agent followed the skill strategy:
1. Called `lms_labs` to discover available labs
2. Listed all 8 labs with full titles
3. Asked the user to choose one instead of guessing

Response: "Here are the available labs. Which one would you like to see the scores for?" followed by the numbered list of labs.

This confirms the skill prompt successfully teaches the agent to ask for clarification when a lab parameter is required but not provided.

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
