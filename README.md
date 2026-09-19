# OpenClaw Token Optimizer — AI Cost Audit & Model Routing

[![Version](https://img.shields.io/badge/version-4.0.2-brightgreen.svg)](CHANGELOG.md)
[![MissionDeck](https://img.shields.io/badge/MissionDeck-ai-blueviolet)](https://missiondeck.ai)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE.txt)

Built by [MissionDeck.ai](https://missiondeck.ai) · [GitHub](https://github.com/Asif2BD/OpenClaw-Token-Optimizer) · [ClawHub](https://clawhub.ai/asif2bd/skills/openclaw-token-optimizer)

**Find potential token waste in your OpenClaw agents with read-only audits of AI model routing, context size and scheduled automations.**

OpenClaw Token Optimizer inspects your actual model catalog and agent configuration,
then produces local, evidence-based recommendations. It does not silently switch
models, rewrite instructions, change schedules or promise a percentage saving.

## What does OpenClaw Token Optimizer do?

- **AI model routing:** select an eligible candidate from your own ordered model policy,
  checking catalog availability, allowlists and required capabilities.
- **Token context analysis:** rank explicitly selected files by size and identify duplicate
  contents. Approximate token counts help prioritize a deeper native context review.
- **Cron and automation auditing:** review agent-turn models, timeouts, delivery intent,
  frequency and lightContext candidates without modifying jobs.
- **Native heartbeat support:** recognize heartbeat and systemEvent payloads without
  incorrectly applying agent-turn checks or labeling them unknown.
- **Honest cost reporting:** missing usage stays unknown—not zero. No hard-coded pricing
  or unverified cost-saving estimates.
- **Local text and JSON reports:** use offline JSON exports or the installed OpenClaw CLI.

Useful for multi-agent systems, recurring AI tasks and large instruction workspaces.

## Install from ClawHub

```bash
clawhub install openclaw-token-optimizer --version 4.0.2
```

Run commands from the installed skill directory. Requires **Python 3.10+**, with no
third-party Python dependencies. Offline mode does not require OpenClaw. The live adapter
is verified against **OpenClaw 2026.9.4**; other versions are labeled unverified.

For a manual installation, use the [versioned GitHub release](https://github.com/Asif2BD/OpenClaw-Token-Optimizer/releases/tag/v4.0.2).

## Quick start: audit your OpenClaw agent

```bash
python3 scripts/optimizer.py audit --live --agent YOUR_AGENT --json
```

Replace `YOUR_AGENT` with your actual agent ID. To include config-level findings, provide
an explicit local JSON file with `--config /path/to/config.json`. Its contents are not echoed.

Generate a review plan with the same inputs:

```bash
python3 scripts/optimizer.py plan --live --agent YOUR_AGENT --json
```

The plan contains review actions, not automatic fixes. Model absence and missing metadata
are reasons to investigate—not proof that a model or job is broken.

## Choose a model using your policy

```bash
python3 scripts/optimizer.py route --live --agent YOUR_AGENT \
  --policy assets/config.example.json --tier research --json
```

The bundled policy illustrates routine, balanced, research, coding and background tiers.
Adapt it to your available providers and quality/cost preferences. It is not a universal
ranking or live pricing database. Recommendations never activate a model.

Add `--image`, `--tools` or `--context-tokens 8000` when the task requires those capabilities.
Unknown capability metadata blocks the recommendation. In particular, many native catalogs
do not expose `supportsTools`; lack of that field does not mean the model lacks tools.
A separately authorized exact-route canary is needed before activation.

## Inspect context size and duplicate instructions

```bash
python3 scripts/optimizer.py context /path/to/SOUL.md /path/to/AGENTS.md --json
```

Only explicitly named files are read. Reports show character counts, approximate tokens
(character count divided by four), and duplicate content. They do not print file contents.
Use OpenClaw's native `/context list` and `/context detail` to establish actual injected
context. Do not remove essential agent instructions based on file size alone.

## Check supplied usage without false zeros

```bash
python3 scripts/optimizer.py budget --json
python3 scripts/optimizer.py budget --usage usage.json --limit 10 --json
```

`usage.json` accepts an aggregate such as `{"costUSD":2.5,"complete":false}`.
Without data, the result is unknown/null. **Automatic native usage ingestion, daily/weekly
alerts and measured billing comparisons are not included in v4.0.2.**

## Offline audit and input formats

```bash
python3 scripts/optimizer.py audit --catalog catalog.json --status status.json \
  --config config.json --jobs jobs.json --json
```

Native JSON shapes:

- Catalog: `{ "models": [{ "key": "provider/model", "available": true, "input": "text+image", "contextWindow": 32000 }] }`
- Status: `{ "allowed": ["provider/model"], "auth": { "missingProvidersInUse": [], "modelRouteIssues": [] } }`
- Config: `{ "agents": { "defaults": { "model": "provider/model" }, "entries": {} } }`
- Automations: `{ "jobs": [] }`
- Optional normalized sessions via `--sessions`: `{ "sessions": [{ "agentId": "example", "model": "provider/model" }] }`

Inputs must be JSON, not JSON5. Missing inputs and paginated automation responses are
explicitly marked as incomplete coverage. Tool capability may be supplied as
`supportsTools: true` only when backed by trustworthy metadata.

## Safety and operational limits

The pure analysis core has no I/O. Explicit live mode invokes fixed native read commands:

- `openclaw --version`
- `openclaw models list --agent ID --all --json`
- `openclaw models status --agent ID --json`
- `openclaw cron list --all --json` (audit/plan only)

These commands may contact your configured Gateway or providers and update native caches.
The optimizer does not run paid inference probes, upload reports, install other software,
or write your configuration. Native reads have a 45-second timeout; inputs have an 8 MiB
size limit. Selected identifiers and basenames can still be private—review reports before sharing.

Exit **0** means analysis completed, not that no issues exist. Exit **2** means invalid
input or a failed native read. Reports go to stdout; `--json` supports downstream tooling.
`plan` intentionally emits no schema-blind patches. See [SECURITY.md](SECURITY.md).

## What's fixed in v4.0.2?

Native **heartbeat** and **systemEvent** jobs are now recognized. The optimizer no longer
reports them as unknown or subjects them to agent-turn-only model/timeout/context checks.
Unknown future payload kinds remain visible. Recognition is not a full audit of those
jobs' effective runtime settings.

## Frequently asked questions

### Does this automatically reduce OpenClaw API costs?

No. It identifies review candidates. Savings depend on which changes you safely apply
and must be measured on comparable workloads. There is no guaranteed savings percentage.

### Does it work with OpenAI, Anthropic and other model providers?

Routing uses your supplied/native catalog and policy instead of a fixed vendor list.
Eligibility depends on your model availability, allowlist and capability evidence.
Catalog availability alone is not proof that an exact authentication route will succeed.

### Will it change my models, cron jobs or heartbeat schedule?

No. All v4 commands are diagnostic. No restart is required to run the CLI.

### Is the ClawHub package verifiable?

Yes. From the extracted package directory:

```bash
sha256sum -c SHA256SUMS.txt
```

`LICENSE.txt` and `SHA256SUMS.txt` survive registry clients that filter extensionless files.
Hashes verify integrity, not safety. Check the version-specific ClawHub security review too.

## Development and migration

```bash
python3 -m unittest discover -s tests -v
python3 -m py_compile scripts/*.py
```

Tests are in the GitHub source, not the installed skill bundle. CI covers Python
3.10/3.12/3.13. From v3, use the new CLI arguments: old script names are migration shims,
not the former prompt classifiers or template installers. Existing state files are left
untouched. MIT licensing is retained. See [CHANGELOG.md](CHANGELOG.md).

## MissionDeck.ai — Your Agent Command Center

[MissionDeck.ai](https://missiondeck.ai) is the related multi-agent coordination dashboard.
This optimizer runs locally, requires no MissionDeck account and has no cloud upload integration.

## More by Asif2BD

Browse [Asif2BD on ClawHub](https://clawhub.ai/asif2bd) for other OpenClaw skills.

[MissionDeck.ai](https://missiondeck.ai) · [OpenClaw documentation](https://docs.openclaw.ai/) · [Source code](https://github.com/Asif2BD/OpenClaw-Token-Optimizer)
