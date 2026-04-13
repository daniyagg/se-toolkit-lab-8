---
name: lms
description: Use LMS MCP tools for live course data
always: true
---

# LMS Skill

You have access to the LMS backend via MCP tools. Use them to answer questions about labs, learners, scores, and performance.

## Available tools

| Tool | What it does | Parameters |
|------|-------------|------------|
| `lms_health` | Check backend health and item count | none |
| `lms_labs` | List all available labs | none |
| `lms_learners` | List all registered learners | none |
| `lms_pass_rates` | Get average score and attempt count per task for a lab | `lab` (required) |
| `lms_timeline` | Get submission timeline (date + count) for a lab | `lab` (required) |
| `lms_groups` | Get group performance (avg score + student count) for a lab | `lab` (required) |
| `lms_top_learners` | Get top learners by average score for a lab | `lab` (required), `limit` (optional, default 5) |
| `lms_completion_rate` | Get completion rate (passed / total) for a lab | `lab` (required) |
| `lms_sync_pipeline` | Trigger the LMS sync pipeline | none |

## Strategy

- If the user asks for scores, pass rates, completion, groups, timeline, or top learners **without naming a lab**, call `lms_labs` first to see what's available.
- When a lab parameter is needed and not provided, **ask the user which lab** they want. Use the `structured-ui` skill to present lab choices on supported channels.
- When presenting lab choices, use the full lab title as the user-facing label (e.g. "Lab 01 – Products, Architecture & Roles") and the short ID as the value (e.g. "lab-01").
- If multiple labs are available, let the user pick one before calling lab-specific tools.
- Format numeric results clearly: percentages as `XX%`, counts as plain numbers.
- Keep responses concise — state the key numbers, don't dump raw JSON.
- When the user asks "what can you do?", explain your current LMS tools and that you can query live data from the LMS backend.

## Example flow for "Show me the scores"

1. Call `lms_labs` to discover available labs.
2. If multiple labs exist, ask the user which one (use structured-ui choice).
3. Once a lab is selected, call `lms_pass_rates` with that lab ID.
4. Present the results as a formatted summary.

## Error handling

- If a tool returns an error, explain what went wrong in plain language.
- If the backend is unreachable, suggest the user check `lms_health` first.
- If a lab has no data, say so clearly instead of returning empty results silently.
