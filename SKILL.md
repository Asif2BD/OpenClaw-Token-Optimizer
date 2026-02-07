---
name: token-optimizer
description: Reduce OpenClaw token usage and API costs by 85-95% through smart model routing, lazy context loading, heartbeat optimization, multi-provider support, Supports Anthropic, OpenAI, Google, and OpenRouter.
version: 1.2.4
homepage: https://github.com/Asif2BD/OpenClaw-Token-Optimizer
metadata: {"openclaw":{"emoji":"🪙","homepage":"https://github.com/Asif2BD/OpenClaw-Token-Optimizer","requires":{"bins":["python3"]}}}
---

# 🪙 Token Optimizer

**Reduce OpenClaw token usage and API costs by 85-95%**

## One-Line Installation

```bash
git clone https://github.com/Asif2BD/OpenClaw-Token-Optimizer.git ~/.openclaw/skills/token-optimizer
```

**That's it!** The skill is now available. Tell your agent:
> "I have the token-optimizer skill installed. Use it to optimize my token usage."

Or manually run the scripts to start saving immediately.

---

## What This Skill Does

| Feature | Savings | Command |
|---------|---------|---------|
| **Context Optimization** | 70-90% | Loads only needed files, not everything |
| **Model Routing** | 60-98% | Uses cheap models for simple tasks |
| **Heartbeat Optimization** | 90-95% | Smart intervals, quiet hours |
| **Multi-Provider** | Variable | Falls back to cheaper providers |
| **Local Fallback** | 100% | Zero cost when cloud APIs fail |

## Quick Start Commands

### 1. Generate Optimized AGENTS.md (Biggest Win!)
```bash
python3 ~/.openclaw/skills/token-optimizer/scripts/context_optimizer.py generate-agents
# Review AGENTS.md.optimized and replace your current AGENTS.md
```

### 2. Route Tasks to Appropriate Models
```bash
# Simple greeting → Use cheap model (Haiku/Nano/Flash)
python3 ~/.openclaw/skills/token-optimizer/scripts/model_router.py "thanks!"

# Complex task → Use smart model (Opus/GPT-4.1/Pro)  
python3 ~/.openclaw/skills/token-optimizer/scripts/model_router.py "design a microservices architecture"
```

### 3. Install Optimized Heartbeat
```bash
cp ~/.openclaw/skills/token-optimizer/assets/HEARTBEAT.template.md ~/.openclaw/workspace/HEARTBEAT.md
```

### 4. Check Token Budget
```bash
python3 ~/.openclaw/skills/token-optimizer/scripts/token_tracker.py check
```

---

## ⚠️ Model Availability

**Not all users have access to all model tiers.** Some configurations only support Sonnet and Opus (no Haiku).

### Sonnet/Opus Only Setup

If you only have Sonnet and Opus available:

```bash
# Set environment variable
export AVAILABLE_TIERS="balanced,smart"

# Or create config file at ~/.openclaw/token-optimizer.json:
{
  "available_tiers": ["balanced", "smart"]
}
```

The router will automatically:
- Skip suggestions for `cheap` tier (Haiku)
- Upgrade simple tasks to `balanced` tier (Sonnet)
- Explain when a tier fallback occurred

### Why Haiku Might Not Work

Common reasons:
- API key doesn't include Haiku access
- Using a provider that doesn't offer Haiku-tier models
- Rate limits on cheaper models

### Fallback Behavior

| Requested | Available Tiers | Actual |
|-----------|-----------------|--------|
| cheap | balanced, smart | balanced |
| balanced | balanced, smart | balanced |
| smart | balanced, smart | smart |
| cheap | smart only | smart |

---

## Scripts Reference

### context_optimizer.py

Recommends minimal context files based on prompt complexity.

```bash
# Recommend context for a prompt
context_optimizer.py recommend "hi"
# → Load only: SOUL.md, IDENTITY.md (savings: ~80%)

context_optimizer.py recommend "analyze our codebase"
# → Load: SOUL.md, IDENTITY.md, MEMORY.md, memory/TODAY.md (savings: ~30%)

# Generate optimized AGENTS.md
context_optimizer.py generate-agents
# Creates AGENTS.md.optimized with lazy loading instructions

# View usage statistics
context_optimizer.py stats
```

### model_router.py

Routes tasks to appropriate model tiers. Supports multiple providers.

```bash
# Auto-detect provider and route
model_router.py "read the config file"
# → cheap tier (Haiku/Nano/Flash)

model_router.py "write a Python function"
# → balanced tier (Sonnet/Mini/Flash)

model_router.py "design system architecture"
# → smart tier (Opus/GPT-4.1/Pro)

# Force specific provider
model_router.py "thanks" --provider openai
# → openai/gpt-4.1-nano

# Compare all providers
model_router.py compare

# List providers
model_router.py providers
```

**Supported Providers:**

| Provider | Cheap | Balanced | Smart |
|----------|-------|----------|-------|
| Anthropic | claude-haiku-4 | claude-sonnet-4-5 | claude-opus-4 |
| OpenAI | gpt-4.1-nano | gpt-4.1-mini | gpt-4.1 |
| Google | gemini-2.0-flash | gemini-2.5-flash | gemini-2.5-pro |
| OpenRouter | gemini-2.0-flash | claude-sonnet-4-5 | claude-opus-4 |

### heartbeat_optimizer.py

Manages heartbeat check intervals with quiet hours.

```bash
# Plan which checks should run now
heartbeat_optimizer.py plan

# Check if specific type should run
heartbeat_optimizer.py check email
heartbeat_optimizer.py check calendar

# Record that a check was performed
heartbeat_optimizer.py record email

# Adjust interval (seconds)
heartbeat_optimizer.py interval email 7200  # 2 hours

# Reset all state
heartbeat_optimizer.py reset
```

**Default Intervals:**
- Email: 60 minutes
- Calendar: 2 hours
- Weather: 4 hours
- Social: 2 hours
- Monitoring: 30 minutes

**Quiet Hours:** 23:00-08:00 (skips non-urgent checks)

### token_tracker.py

Monitors daily token budget and usage.

```bash
# Check current usage
token_tracker.py check

# Get model suggestions for task type
token_tracker.py suggest general

# Reset daily tracking
token_tracker.py reset
```

**Status Levels:**
- `ok` — Below 80% of daily limit
- `warning` — 80-99% of daily limit
- `exceeded` — Over limit, switch to cheaper models

---

## Configuration

### Environment Variables

Set your preferred provider's API key:

```bash
# Anthropic (default)
export ANTHROPIC_API_KEY="sk-ant-..."

# OpenAI
export OPENAI_API_KEY="sk-proj-..."

# Google
export GOOGLE_API_KEY="AIza..."

# OpenRouter (unified API)
export OPENROUTER_API_KEY="sk-or-v1-..."
```

The model router auto-detects which provider to use based on available keys.

### Customization

Edit patterns in `scripts/model_router.py`:
- `COMMUNICATION_PATTERNS` — Patterns that always use cheap tier
- `BACKGROUND_TASK_PATTERNS` — Heartbeat/cron patterns
- `ROUTING_RULES` — Task classification rules
- `PROVIDER_MODELS` — Model mappings per provider

---

## Integration Patterns

### Before Every Response

```python
# 1. Get context recommendation
from context_optimizer import recommend_context_bundle
rec = recommend_context_bundle(user_prompt)

# 2. Load only recommended files
if rec["context_level"] == "minimal":
    load_only(["SOUL.md", "IDENTITY.md"])
    # Skip everything else!

# 3. Get model recommendation
from model_router import route_task
routing = route_task(user_prompt)

# 4. Use recommended model
model = routing["recommended_model"]
```

### In HEARTBEAT.md

```bash
# Check if we should run any checks
result=$(python3 scripts/heartbeat_optimizer.py plan)
should_run=$(echo $result | jq -r .should_run)

if [ "$should_run" = "false" ]; then
    echo "HEARTBEAT_OK"
    exit 0
fi

# Run only planned checks
# ...
```

### In Cronjobs

Always specify the cheapest model that can handle the task:

```bash
# Good: Use Haiku for routine tasks
cron add --schedule "0 * * * *" \
  --payload '{"kind":"agentTurn","message":"Check server health","model":"anthropic/claude-haiku-4"}' \
  --sessionTarget isolated

# Bad: Using Opus for simple checks (60x more expensive!)
```

---

## Expected Savings

### Why 85-95% Savings? (v1.2.0 Analysis)

**Combined effect is multiplicative:**
- Context reduction: ~78% (loads 22% of original)
- Model cost reduction: ~64% (pays 36% of original rate)
- Combined: 1 - (0.22 × 0.36) = **92% savings**

### Example: 100K tokens/day workload

| Strategy | Context | Model | Monthly Cost | Savings |
|----------|---------|-------|--------------|---------|
| Baseline (no optimization) | 50K | Sonnet | $9.00 | 0% |
| Context optimization only | 11K | Sonnet | $2.00 | 78% |
| Model routing only | 50K | Mixed | $3.20 | 64% |
| **Both (this skill)** | **11K** | **Mixed** | **$0.72** | **92%** |
| + Local fallback (offline) | Any | Local | $0.00 | **100%** |

### Cronjob Savings

Using Haiku instead of Opus for 10 daily cronjobs:
- Opus: 10 × 5K tokens × $15/MTok = $0.75/day = **$22.50/month**
- Haiku: 10 × 5K tokens × $0.25/MTok = $0.0125/day = **$0.38/month**
- **Savings: $22/month per agent (98% reduction)**

---

## Troubleshooting

**Scripts fail with "module not found"**
→ Ensure Python 3.7+ is installed. Scripts use stdlib only.

**State files not persisting**
→ Check `~/.openclaw/workspace/memory/` exists and is writable.

**Routing suggests wrong tier**
→ Customize patterns in `scripts/model_router.py`.

**Budget shows $0.00**
→ Token tracker needs manual usage recording or integration with session_status.

---

## Files Included

```
token-optimizer/
├── SKILL.md              # This file
├── README.md             # Quick start guide
├── CHANGELOG.md          # Version history
├── LICENSE               # MIT License
├── scripts/
│   ├── context_optimizer.py   # Context loading optimization
│   ├── model_router.py        # Multi-provider model routing
│   ├── heartbeat_optimizer.py # Heartbeat interval management
│   └── token_tracker.py       # Budget monitoring
├── assets/
│   ├── HEARTBEAT.template.md  # Drop-in heartbeat template
│   ├── cronjob-model-guide.md # Cronjob model selection guide
│   └── config-patches.json    # Advanced config examples
├── docs/
│   └── RESEARCH-NOTES.md      # Research and methodology
└── references/
    └── PROVIDERS.md           # Provider comparison guide
```

---

## Requirements

- Python 3.7+ (stdlib only, no external dependencies)
- OpenClaw installation
- Write access to `~/.openclaw/workspace/memory/`

---

## Credits

Part of the **SuperSkills** collection for OpenClaw.

Created by:
- **Oracle** — Research, analysis, and documentation
- **Morpheus** — Code review and publication

---

*"The best token is the one you don't spend."* 🪙
