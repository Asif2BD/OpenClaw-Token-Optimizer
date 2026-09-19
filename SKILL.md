---
name: openclaw-token-optimizer
description: "Audit OpenClaw model routes, context and automations; produce read-only, evidence-based optimization plans without guessing savings or changing configuration."
version: 4.0.0
author: Asif2BD
homepage: https://missiondeck.ai
source: https://github.com/Asif2BD/OpenClaw-Token-Optimizer
license: MIT
openclaw: ">=2026.9.4"
metadata: {"openclaw":{"emoji":"💰","requires":{"bins":["python3"]}}}
---

# OpenClaw Token Optimizer

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
   accepts an explicit aggregate; native usage ingestion and alerts are not part of v4.0.

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

Python 3.10+, standard library only. OpenClaw is optional for offline mode; live adapter
verified against 2026.9.4. No claim of compatibility with every future schema.
[GitHub](https://github.com/Asif2BD/OpenClaw-Token-Optimizer) ·
[MissionDeck.ai Cloud](https://missiondeck.ai) · See SECURITY.md for the trust boundary.
