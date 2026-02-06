# 🪙 Token Optimizer

**Reduce OpenClaw token usage and API costs by 50-80%**

An OpenClaw skill that implements smart model routing, lazy context loading, optimized heartbeats, and multi-provider support.

[![ClawHub](https://img.shields.io/badge/ClawHub-Ready-blue)](https://clawhub.ai)
[![Version](https://img.shields.io/badge/version-1.1.0-green)](https://github.com/Asif2BD/OpenClaw-Token-Optimizer/blob/main/CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-purple)](https://openclaw.ai)

---

## 🚀 One-Line Installation

```bash
git clone https://github.com/Asif2BD/OpenClaw-Token-Optimizer.git ~/.openclaw/skills/token-optimizer
```

**Done!** Your agent now has access to token optimization tools.

### Alternative: Tell Your Agent

> "Install the token-optimizer skill from github.com/Asif2BD/OpenClaw-Token-Optimizer"

Your agent will clone it to the skills directory automatically.

---

## 🎯 Quick Start

### 1. Generate Optimized AGENTS.md (Biggest Win!)

```bash
python3 ~/.openclaw/skills/token-optimizer/scripts/context_optimizer.py generate-agents
# Creates AGENTS.md.optimized — review and replace your current AGENTS.md
```

This teaches your agent to load only the context it needs (50-80% savings!).

### 2. Route Tasks to Appropriate Models

```bash
# Check what model to use for a prompt
python3 ~/.openclaw/skills/token-optimizer/scripts/model_router.py "thanks!"
# → Output: Use cheap tier (Haiku/Nano/Flash), not Opus!

python3 ~/.openclaw/skills/token-optimizer/scripts/model_router.py "design a microservices architecture"
# → Output: Use smart tier (Opus/GPT-4.1/Pro)
```

### 3. Install Optimized Heartbeat

```bash
cp ~/.openclaw/skills/token-optimizer/assets/HEARTBEAT.template.md ~/.openclaw/workspace/HEARTBEAT.md
```

### 4. Check Token Budget

```bash
python3 ~/.openclaw/skills/token-optimizer/scripts/token_tracker.py check
```

**Expected savings:** 50-80% reduction in token costs for typical workloads.

---

## 📦 What's Included

### Scripts

| Script | Purpose | Savings |
|--------|---------|---------|
| `context_optimizer.py` | Lazy context loading — only load needed files | 50-80% |
| `model_router.py` | Smart model selection with multi-provider support | 40-60% |
| `heartbeat_optimizer.py` | Efficient heartbeat scheduling | 50% |
| `token_tracker.py` | Budget monitoring and alerts | Prevents overruns |

### Assets

| File | Purpose |
|------|---------|
| `HEARTBEAT.template.md` | Drop-in optimized heartbeat template |
| `cronjob-model-guide.md` | Guide for choosing models in cronjobs |
| `config-patches.json` | Advanced configuration examples |

### References

| File | Purpose |
|------|---------|
| `PROVIDERS.md` | Alternative AI providers, pricing, routing strategies |

---

## 🌐 Multi-Provider Support

The skill supports multiple AI providers with automatic detection:

| Provider | Cheap Tier | Balanced Tier | Smart Tier |
|----------|------------|---------------|------------|
| **Anthropic** | claude-haiku-4 | claude-sonnet-4-5 | claude-opus-4 |
| **OpenAI** | gpt-4.1-nano | gpt-4.1-mini | gpt-4.1 |
| **Google** | gemini-2.0-flash | gemini-2.5-flash | gemini-2.5-pro |
| **OpenRouter** | gemini-2.0-flash | claude-sonnet-4-5 | claude-opus-4 |

Set your preferred provider via environment variable:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."   # Default
export OPENAI_API_KEY="sk-proj-..."     # For OpenAI routing
export GOOGLE_API_KEY="AIza..."         # For Google routing
export OPENROUTER_API_KEY="sk-or-..."   # For unified API
```

The model router auto-detects which provider to use based on available keys.

```bash
# Compare models across all providers
python3 scripts/model_router.py compare

# Force specific provider
python3 scripts/model_router.py "thanks" --provider openai
```

---

## 💡 Core Optimization Strategies

### 1. Context Optimization (Biggest Win!)

**Problem:** Default OpenClaw loads ALL context files — often 50K+ tokens before the user speaks.

**Solution:** Load only what's needed based on prompt complexity.

```bash
# Simple greeting → minimal context (2 files only!)
python3 scripts/context_optimizer.py recommend "hi"
# → Load: SOUL.md, IDENTITY.md (savings: ~80%)

# Complex task → full context
python3 scripts/context_optimizer.py recommend "analyze architecture"
# → Load: SOUL.md, IDENTITY.md, MEMORY.md, etc. (savings: ~30%)
```

### 2. Smart Model Routing

**Problem:** Using Opus ($15/MTok) for "thanks!" is wasteful.

**Solution:** Route to appropriate tier based on task.

```bash
# Communication → ALWAYS cheap tier
python3 scripts/model_router.py "thanks!"
# → anthropic/claude-haiku-4 (or openai/gpt-4.1-nano)

# Complex task → smart tier (only when needed)
python3 scripts/model_router.py "design a microservices architecture"
# → anthropic/claude-opus-4
```

### 3. Heartbeat Optimization

**Problem:** Checking email every 5 minutes at 3 AM wastes tokens.

**Solution:** Smart intervals + quiet hours.

```bash
python3 scripts/heartbeat_optimizer.py plan
# → Checks what needs checking, skips during quiet hours
```

---

## 📊 Cost Savings Examples

### 100K tokens/day workload

| Strategy | Context | Model | Monthly Cost | Savings |
|----------|---------|-------|--------------|---------|
| No optimization | 50K | Sonnet | $9.00 | 0% |
| Context only | 10K | Sonnet | $5.40 | 40% |
| Routing only | 50K | Mixed | $5.40 | 40% |
| **Both** | **10K** | **Mixed** | **$2.70** | **70%** |
| Aggressive | 10K | Gemini | $0.90 | **90%** |

### Cronjobs

Using Haiku instead of Opus for 10 daily cronjobs = **$22/month saved**.

---

## 📋 Changelog

See [CHANGELOG.md](CHANGELOG.md) for full version history.

### v1.1.0 (2026-02-06)
- ✨ **Multi-provider support**: OpenAI, Google, OpenRouter
- 🏷️ Provider-agnostic tier system (cheap/balanced/smart)
- 📦 ClawHub-ready SKILL.md with proper metadata
- 📝 One-line installation instructions

### v1.0.0 (2026-02-05)
- 🎉 Initial release
- Context optimizer, model router, heartbeat optimizer, token tracker
- Comprehensive documentation and examples

---

## 🔧 Requirements

- Python 3.7+ (stdlib only, no external dependencies)
- OpenClaw installation
- Write access to `~/.openclaw/workspace/memory/`

---

## 📁 Project Structure

```
token-optimizer/
├── SKILL.md              # Skill definition (ClawHub-ready)
├── README.md             # This file
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
└── references/
    └── PROVIDERS.md           # Provider comparison guide
```

---

## 📖 Full Documentation

See [SKILL.md](SKILL.md) for complete documentation including:
- All script options and examples
- Integration patterns
- Workflow examples
- Troubleshooting guide

---

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

**Ideas for extending this skill:**
1. Auto-routing integration with OpenClaw message pipeline
2. Real-time usage tracking via session_status parsing
3. Cost forecasting based on recent usage
4. Provider health monitoring
5. A/B testing for routing strategies

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Credits

Part of the **SuperSkills** collection for OpenClaw.

Created by:
- **Oracle** — Research, analysis, and documentation
- **Morpheus** — Code review and publication

---

*"The best token is the one you don't spend."* 🪙
