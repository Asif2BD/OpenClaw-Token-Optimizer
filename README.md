# OpenClaw Token Optimizer

[![Version](https://img.shields.io/badge/version-4.0.0-brightgreen.svg)](CHANGELOG.md)
[![MissionDeck](https://img.shields.io/badge/MissionDeck-ai-blueviolet)](https://missiondeck.ai)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Built by [MissionDeck.ai](https://missiondeck.ai) · [GitHub](https://github.com/Asif2BD/OpenClaw-Token-Optimizer)

> Read-only, evidence-based audits of your real model catalog, context, and automations.

## Overview

v4 combines the compatibility refresh and native-aware core. No more static model
ranking, blanket cache-warming schedules, or zero-cost reports when usage is missing.
It does not silently modify your agent or promise a percentage saving.

## Setup modes

- **OpenClaw agent:** install `clawhub install openclaw-token-optimizer`.
- **Self-hosted/offline:** clone this repo and run Python 3.10+; no dependencies.
- **MissionDeck Cloud:** [missiondeck.ai](https://missiondeck.ai) is the related agent
  coordination product; this CLI remains local and has no cloud upload integration.

## Quick start

```bash
python3 scripts/optimizer.py audit --live --agent oracle --json
python3 scripts/optimizer.py plan --live --agent oracle --json
python3 scripts/optimizer.py route --live --agent oracle --policy assets/config.example.json --tier research --json
python3 scripts/optimizer.py context SOUL.md AGENTS.md --json
python3 scripts/optimizer.py budget --json
```

Replace `oracle` with your agent ID. `--live` runs only fixed read commands:
`openclaw --version`, `openclaw models list --agent ID --all --json`, `openclaw models status --agent ID --json`,
and (audit/plan only) `openclaw cron list --all --json`. These may contact configured
Gateway/provider services through OpenClaw. No automatic auth probe or inference call.

Offline equivalent:

```bash
python3 scripts/optimizer.py audit --catalog catalog.json --status status.json --config config.json --jobs jobs.json --json
python3 scripts/optimizer.py route --catalog catalog.json --status status.json --policy assets/config.example.json --tier routine --image --context-tokens 8000 --json
```

Inputs use native JSON shapes: catalog `{models:[{key,available,input,contextWindow}]}`,
status `{allowed:[],auth:{missingProvidersInUse:[],modelRouteIssues:[]}}`, config
`{agents:{defaults:{model:...},entries:{...}}}`, jobs `{jobs:[...]}`.
Optional normalized sessions: `{sessions:[{agentId,model}]}` via `--sessions`.
For tool routing, `--tools` requires explicit `supportsTools: true` in trusted catalog data.
Native catalogs may omit that field; do not assume support.

## Commands and limits

- **audit:** catalog/allowlist references, unknown availability, native route issues,
  shared-provider fallbacks, session/default differences, frequent agent jobs,
  timeout/model/lightContext/delivery review. Reports coverage and limitations.
- **plan:** ranked review actions as JSON or text. `patches` is intentionally empty:
  no schema-blind or automatic config changes. Apply changes separately after validation.
- **route:** first eligible candidate in user preference order. Availability and allowlist
  required. Optional image/tool/context checks are fail-closed. No price/quality inference.
  A separate exact-model canary remains required before activation.
- **context:** explicit files only; character counts, approximate tokens, exact duplicate
  content detection. No recursive workspace scan, raw contents in output, or file edits.
- **budget:** missing data is unknown, not zero. `--usage usage.json --limit 10` accepts
  `{costUSD:2.5,complete:false}`. Automated native usage ingestion/alerts are deferred to v4.1.

All commands print to stdout. Exit 0 means analysis completed, not that the configuration
is fault-free. Exit 2 means invalid inputs/native read failure. `--json` is machine-readable.
Reports are local; selected identifiers and file basenames can still be sensitive.
Inputs are JSON, not JSON5, and limited to 8 MiB each. Native reads have a 45-second timeout.
No prices or savings estimates are invented. Automation pagination is explicitly flagged.

## Migration from v3

This is a breaking major release. Legacy script names delegate to v4 subcommands, so
old positional prompts, template installs, and state-writing commands are no longer supported.
Use `optimizer.py --help` and the examples above. Existing state files are left untouched.
The skill slug/frontmatter is consistently `openclaw-token-optimizer`. MIT LICENSE is retained.
Do not replace your AGENTS.md or HEARTBEAT.md with generated templates.

## Verification

```bash
python3 -m unittest discover -s tests -v
python3 -m py_compile scripts/*.py
sha256sum -c .clawhubsafe
```

CI runs tests on Python 3.10/3.12/3.13. The native adapter is tested locally against
OpenClaw 2026.9.4; future schemas must be verified. Checksums attest integrity, not security
approval. ClawHub's independent review status must be checked after publishing.

## Security

See [SECURITY.md](SECURITY.md). The pure core has no I/O; the optional live adapter uses
fixed native read commands without a shell. No installation hooks or third-party dependencies.
Package preparation excludes tests, CI, internal notes, caches and credentials.

## MissionDeck.ai — Your Agent Command Center

[MissionDeck.ai](https://missiondeck.ai) provides a dashboard for multi-agent coordination.
The optimizer does not require a MissionDeck account and never uploads audit data there.

## More by Asif2BD

```bash
clawhub install jarvis-mission-control
clawhub search Asif2BD
```

[MissionDeck.ai](https://missiondeck.ai) · [OpenClaw 2026.9.4](https://docs.openclaw.ai/releases/2026.9.4)
