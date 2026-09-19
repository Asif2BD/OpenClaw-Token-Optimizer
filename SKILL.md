---
name: openclaw-token-optimizer
description: "Token optimization for OpenClaw and Hermes Agent: inspect model routing, context size, cron jobs and heartbeats with read-only diagnostics and evidence-based recommendations."
version: 4.1.0
author: Asif2BD
homepage: https://missiondeck.ai
source: https://github.com/Asif2BD/OpenClaw-Token-Optimizer
license: MIT
openclaw: ">=2026.9.4"
metadata: {"openclaw":{"emoji":"💰","requires":{"bins":["python3"]}}}
---

# Token Optimizer for OpenClaw & Hermes

Find potential token waste in OpenClaw agents without changing their configuration.
Audit model availability, review automation settings, and inspect context size.

**Best for:** multi-agent setups, scheduled agent jobs, and context-heavy workspaces.
**Output:** local text or JSON recommendations; no guaranteed savings claims.

## Quick start

```bash
python3 scripts/optimizer.py audit --live --agent YOUR_AGENT --json
```

Replace YOUR_AGENT with an existing agent ID. Offline JSON analysis is also supported.

Built by [MissionDeck.ai](https://missiondeck.ai).

## Workflow

1. Explain that analysis is read-only. Never claim an audit changed runtime behavior.
2. For offline analysis, request explicit catalog/status/config/jobs JSON paths. Do not
   search for credentials. Missing inputs are reported as incomplete coverage.
3. For live reads, run `python3 scripts/optimizer.py audit --live --agent AGENT --json`.
   Optional `--config PATH` reads explicit JSON config locally; it is never written or echoed.
   Live mode invokes installed OpenClaw read commands, which may contact configured services.
4. Review findings. `plan` uses the same inputs and emits review actions, not blind patches.
5. To choose a model, use `route --live --agent AGENT --policy PATH --tier TIER --json`.
   The policy's model order is authoritative. No model is activated. Prove the exact route
   with a separately authorized canary before changing any configuration.
6. For context, run `context SOUL.md AGENTS.md --json` using explicitly chosen files.
   The character/4 estimate is approximate; confirm actual injected cost with native
   `/context list` or `/context detail`. Never remove required instructions blindly.
7. `budget --json` reports unknown without data. Optional `--usage PATH --limit USD`
   accepts an explicit aggregate; native usage ingestion and alerts are not implemented.

## Hermes runtime

Use `audit --runtime hermes --live --hermes-home /explicit/profile --json` to read only
config.yaml and cron/jobs.json. Or supply explicit `--config` and `--jobs` exports.
Never load `.env` or credentials. Never start Hermes or execute job scripts for this audit.
Model evidence follows job → cron → creation snapshot → explicit `--hermes-model-env` →
global default. Missing environment/overlay/authentication evidence stays unverified.
`no_agent` avoids Hermes inference, not necessarily all script costs. Paused jobs are skipped.
`plan` emits review actions only. Hermes `route` requires explicit normalized catalog/status;
no native discovery is available. Use shared `context` and `budget` normally.
Read references/HERMES.md for scope and pinned-source integration evidence.
Default runtime remains OpenClaw; do not guess when both are installed.

## Native automation compatibility

Recognizes agentTurn/agent, command, heartbeat and systemEvent payloads. Agent-turn
model, timeout and lightContext checks apply only to agent turns. Heartbeat/systemEvent
recognition is not a full audit of their effective execution settings. Unknown future kinds
remain visible for manual review.

## Constraints

- No automatic config edits, model switching, installs, paid probes, jobs or messages.
- No fixed savings percentages, hard-coded pricing, or universal cache TTL recommendations.
- Do not treat catalog availability as successful authentication/inference proof.
- Unknown capabilities block required image/tool/context routing.
- Reports omit raw config, auth profiles, prompts and commands. Review reports before sharing;
  selected model/agent identifiers and chosen basenames may still be sensitive.
- Do not load all skill references into every turn. Read references/PROVIDERS.md only for
  routing or cache guidance, assets/cronjob-model-guide.md only for automation analysis.
- The old script names are migration shims; use the v4 arguments documented in README.

## Requirements and provenance

Python 3.10+; standard library for OpenClaw/JSON, optional PyYAML for Hermes YAML. OpenClaw is optional for offline mode; live adapter
verified against 2026.9.4. No claim of compatibility with every future schema.
[GitHub](https://github.com/Asif2BD/OpenClaw-Token-Optimizer) ·
[MissionDeck.ai Cloud](https://missiondeck.ai) · See SECURITY.md for the trust boundary.
