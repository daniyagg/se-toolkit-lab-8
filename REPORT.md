# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

**Test command:**
```bash
cd nanobot
uv run nanobot agent -c ./config.json -m "What is the agentic loop?"
```

**Response:**
The agent provided a detailed explanation of the agentic loop:

> "The agentic loop (or AI agent loop) is the core architectural pattern that enables AI agents to act autonomously and complete multi-step tasks."
>
> **The 5-Stage Loop:**
> 1. **Perceive** - Gather context from the environment, inputs, and previous results
> 2. **Reason** - Use the LLM to analyze the situation and consider available options
> 3. **Plan** - Determine the next action or sequence of actions to take
> 4. **Act** - Execute the chosen action (call tools, APIs, make decisions)
> 5. **Observe** - Collect the outcome/result of the action
>
> Then it repeats until the task is complete or a stopping condition is reached.

**Test command (no tools):**
```bash
uv run nanobot agent -c ./config.json -m "What labs are available in our LMS?"
```

**Response:**
The agent successfully called the MCP tools and returned real lab data:

```
Here are the labs available in your LMS:

 ID  Title                                                   
 ─────────────────────────────────────────────────────────── 
 1   Lab 01 – Products, Architecture & Roles                 
 2   Lab 02 — Run, Fix, and Deploy a Backend Service         
 3   Lab 03 — Backend API: Explore, Debug, Implement, Deploy 
 4   Lab 04 — Testing, Front-end, and AI Agents              
 5   Lab 05 — Data Pipeline and Analytics Dashboard          
 6   Lab 06 — Build Your Own Agent                           
 7   Lab 07 — Build a Client with an AI Coding Agent         
 8   lab-08                                                  
```

---

## Task 1B — Agent with LMS tools

**Test command:**
```bash
cd nanobot
uv run nanobot agent -c ./config.json -m "What labs are available?"
```

**Response:**
The agent successfully called the `lms_labs` MCP tool and returned real backend data showing 8 labs available in the system.

**Test command (architecture question):**
```bash
uv run nanobot agent -c ./config.json -m "Describe the architecture of the LMS system"
```

**Response:**
The agent can describe the LMS architecture using its MCP tools. The system includes:
- **Backend** (FastAPI) - serves the API endpoints
- **PostgreSQL** - stores lab data, learners, submissions
- **Caddy** - reverse proxy serving all traffic on port 80
- **Qwen Code API** - provides LLM access for the agent
- **VictoriaLogs/VictoriaTraces** - observability data collection
- **OpenTelemetry Collector** - collects and forwards telemetry

---

## Task 1C — Skill prompt

**Skill prompt location:** `nanobot/workspace/skills/lms/SKILL.md`

**Test command:**
```bash
cd nanobot
set NANOBOT_LMS_BACKEND_URL=http://localhost:42002
set NANOBOT_LMS_API_KEY=my-secret-api-key
uv run nanobot agent -c ./config.json -m "Show me the scores"
```

**Response:**
With the skill prompt, the agent correctly identified that no lab was specified and provided a comprehensive overview of all labs with their completion rates:

```
Here are the scores and completion rates for all labs:

 Lab     Title              Completion Rate  Passed  Total  Avg Score  Attempts 
 ────────────────────────────────────────────────────────────────────────────── 
 lab-01  Lab 01 –           0.0%             0       0      -          -        
         Products,                                                              
         Architecture &                                                         
         Roles                                                                  
 ... (all 8 labs listed)

Summary: All labs currently have no submissions yet (0 total learners).
```

The agent:
- Listed all available labs
- Formatted numeric results as percentages
- Explained why data is empty (no submissions yet)
- Offered to check learners or submission timeline

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
