# 🪙 Token Optimizer

**Reduce OpenClaw token usage and API costs by 50-80%**

An OpenClaw skill that implements smart model routing, lazy context loading, optimized heartbeats, and budget tracking.

[![ClawHub](https://img.shields.io/badge/ClawHub-Ready-blue)](https://github.com/Asif2BD/OpenClaw-Token-Optimizer)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-purple)](https://openclaw.dev)

## 🎯 Quick Start

```bash
# Clone to your OpenClaw skills directory
git clone https://github.com/Asif2BD/OpenClaw-Token-Optimizer.git ~/.openclaw/skills/token-optimizer

# Generate optimized AGENTS.md (biggest win!)
python3 scripts/context_optimizer.py generate-agents

# Check model routing for a prompt
python3 scripts/model_router.py "thanks!"
# → Output: Use Haiku, not Opus!

# Install optimized heartbeat
cp assets/HEARTBEAT.template.md ~/.openclaw/workspace/HEARTBEAT.md

# Check token budget
python3 scripts/token_tracker.py check
```

**Expected savings:** 50-80% reduction in token costs for typical workloads.

## 📦 What's Included

### Scripts

| Script | Purpose |
|--------|---------|
| `context_optimizer.py` | Lazy context loading — only load files you actually need |
| `model_router.py` | Smart model selection based on task complexity |
| `heartbeat_optimizer.py` | Efficient heartbeat scheduling with check intervals |
| `token_tracker.py` | Budget monitoring and usage alerts |

### Assets

| File | Purpose |
|------|---------|
| `HEARTBEAT.template.md` | Drop-in optimized heartbeat template |
| `cronjob-model-guide.md` | Complete guide for choosing models in cronjobs |
| `config-patches.json` | Advanced configuration examples |

### References

| File | Purpose |
|------|---------|
| `PROVIDERS.md` | Alternative AI providers, pricing, and routing strategies |

## 💡 Core Optimization Strategies

### 1. Context Optimization (Biggest Win!)

**Problem:** Default OpenClaw loads ALL context files every session — often 50K+ tokens before the user even speaks.

**Solution:** Load only what's needed based on prompt complexity.

```bash
# Simple greeting → minimal context
python3 scripts/context_optimizer.py recommend "hi"
# → Load only: SOUL.md, IDENTITY.md (savings: ~80%)

# Standard work → selective loading
python3 scripts/context_optimizer.py recommend "write a function"
# → Load: SOUL.md, IDENTITY.md, memory/TODAY.md (savings: ~50%)

# Complex task → full context
python3 scripts/context_optimizer.py recommend "analyze architecture"
# → Load: SOUL.md, IDENTITY.md, MEMORY.md, + relevant docs (savings: ~30%)
```

### 2. Smart Model Routing

**Problem:** Using Opus ($15/MTok) for "thanks!" is a waste.

**Solution:** Route to appropriate model tier based on task.

```bash
# Communication → ALWAYS Haiku
python3 scripts/model_router.py "thanks!"
# → anthropic/claude-haiku-4 (NEVER Sonnet/Opus for casual chat)

# Simple task → Haiku
python3 scripts/model_router.py "read the log file"
# → anthropic/claude-haiku-4

# Medium task → Sonnet
python3 scripts/model_router.py "write a function to parse JSON"
# → anthropic/claude-sonnet-4-5

# Complex task → Opus (only when needed)
python3 scripts/model_router.py "design a microservices architecture"
# → anthropic/claude-opus-4
```

### 3. Heartbeat Optimization

**Problem:** Checking email every 5 minutes at 3 AM wastes tokens.

**Solution:** Smart intervals + quiet hours + batched checks.

```bash
# Plan which checks should run now
python3 scripts/heartbeat_optimizer.py plan

# Check if email should be checked (based on interval)
python3 scripts/heartbeat_optimizer.py check email

# Record that you just checked email
python3 scripts/heartbeat_optimizer.py record email

# Adjust interval (seconds)
python3 scripts/heartbeat_optimizer.py interval email 7200  # 2 hours
```

**Default intervals:**
- Email: 60 minutes
- Calendar: 2 hours
- Weather: 4 hours
- Monitoring: 30 minutes

**Quiet hours:** 23:00-08:00 — skips all non-urgent checks.

### 4. Budget Tracking

```bash
# Check daily usage
python3 scripts/token_tracker.py check

# Get model suggestions for task type
python3 scripts/token_tracker.py suggest general

# Reset daily tracking
python3 scripts/token_tracker.py reset
```

**Status levels:**
- `ok`: Below 80% of daily limit
- `warning`: 80-99% of daily limit
- `exceeded`: Over daily limit — switch to cheaper models

## 📊 Cost Savings Examples

### Example: 100K tokens/day workload

| Strategy | Context | Model | Daily Cost | Monthly | Savings |
|----------|---------|-------|------------|---------|---------|
| Baseline (no optimization) | 50K | Sonnet | $0.30 | $9.00 | 0% |
| Context optimization only | 10K | Sonnet | $0.18 | $5.40 | 40% |
| Model routing only | 50K | Mixed | $0.18 | $5.40 | 40% |
| **Both (this skill)** | **10K** | **Mixed** | **$0.09** | **$2.70** | **70%** |

### Example: Cronjobs

Using Haiku instead of Opus for 10 daily cronjobs = **$17.70/month saved**.

## 🚀 Deployment Patterns

### Personal Use
1. Install optimized `HEARTBEAT.md`
2. Run budget checks before expensive operations
3. Manually route complex tasks to Opus only when needed
4. **Expected savings: 20-30%**

### Managed Hosting (xCloud, etc.)
1. Default all agents to Haiku
2. Route user interactions to Sonnet
3. Reserve Opus for explicitly complex requests
4. Use Gemini Flash for background operations
5. **Expected savings: 40-60%**

### High-Volume Deployments
1. Use multi-provider fallback (OpenRouter + Together.ai)
2. Aggressive routing (80% Gemini, 15% Haiku, 5% Sonnet)
3. Batch heartbeat checks (every 2-4 hours, not 30 min)
4. **Expected savings: 70-90%**

## 🔧 Requirements

- Python 3.7+ (uses stdlib only, no dependencies)
- OpenClaw installation
- Write access to `~/.openclaw/workspace/memory/`

## 📁 Installation

### From GitHub

```bash
# Clone to your skills directory
git clone https://github.com/Asif2BD/OpenClaw-Token-Optimizer.git ~/.openclaw/skills/token-optimizer
```

### From ClawHub

```bash
# Coming soon to ClawHub
claw install token-optimizer
```

## 📖 Full Documentation

See [SKILL.md](SKILL.md) for complete documentation including:
- All script options and examples
- Integration patterns
- Workflow examples
- Troubleshooting guide
- Maintenance tips

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

**Ideas for extending this skill:**
1. Auto-routing integration with OpenClaw message pipeline
2. Real-time usage tracking via session_status parsing
3. Cost forecasting based on recent usage
4. Provider health monitoring
5. A/B testing for routing strategies

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

## 🙏 Credits

Created by the OpenClaw agent team:
- **Oracle** — Research, analysis, and documentation
- **Morpheus** — Code review and publication

Part of the **SuperSkills** collection for OpenClaw.

---

*"The best token is the one you don't spend."* 🪙
