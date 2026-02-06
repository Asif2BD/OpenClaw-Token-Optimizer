# 🛸 Local Model Fallback (Emergency Fuel Mode)

**Zero-cost resilience with local AI models**

When cloud APIs fail — rate limits, billing issues, network outages — your agent doesn't have to stop. It can automatically fall back to locally-running models.

---

## 🚨 What is Emergency Fuel Mode?

Emergency Fuel Mode is automatic failover to local models when cloud providers are unavailable.

**When it activates:**
- Cloud API returns rate limit errors (429)
- Billing/quota exceeded
- Network connectivity issues
- API timeout

**What happens:**
1. OpenClaw detects the API failure
2. Automatically switches to configured fallback model
3. Agent announces: `🛸 Emergency fuel mode — running on local backup`
4. Full functionality continues with local model
5. When cloud recovers, normal operation resumes

---

## 💻 Setup Instructions

### Step 1: Install Ollama

Ollama is the easiest way to run local models.

```bash
# Linux/macOS
curl -fsSL https://ollama.ai/install.sh | sh

# Verify installation
ollama --version
```

### Step 2: Pull Recommended Models

```bash
# General purpose - great for most tasks (1.9GB)
ollama pull qwen2.5:3b

# Coding tasks (3.8GB) - Note: limited tool support
ollama pull deepseek-coder:6.7b

# Alternative: Llama 3.2 (good balance)
ollama pull llama3.2:3b
```

**Model recommendations:**

| Model | Size | Best For | Tool Support |
|-------|------|----------|--------------|
| `qwen2.5:3b` | 1.9GB | General tasks, chat, simple coding | ✅ Good |
| `qwen2.5:7b` | 4.4GB | Better quality general tasks | ✅ Good |
| `llama3.2:3b` | 2.0GB | General tasks, reasoning | ✅ Good |
| `deepseek-coder:6.7b` | 3.8GB | Coding, code review | ⚠️ Limited |
| `codestral:22b` | 12GB | Advanced coding (needs GPU) | ⚠️ Limited |

### Step 3: Verify Ollama is Running

```bash
# Start Ollama service (if not auto-started)
ollama serve &

# Test the model
ollama run qwen2.5:3b "Hello, can you help me?"

# Check API endpoint
curl http://localhost:11434/api/tags
```

### Step 4: Configure OpenClaw

Add to your OpenClaw config (`~/.openclaw/config.json`):

```json
{
  "models": {
    "providers": {
      "ollama": {
        "baseUrl": "http://localhost:11434/v1",
        "apiKey": "ollama-local",
        "api": "openai-completions",
        "models": [
          {"id": "qwen2.5:3b", "name": "Qwen 2.5 3B (Local)"},
          {"id": "qwen2.5:7b", "name": "Qwen 2.5 7B (Local)"},
          {"id": "llama3.2:3b", "name": "Llama 3.2 3B (Local)"},
          {"id": "deepseek-coder:6.7b", "name": "DeepSeek Coder 6.7B (Local)"}
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "fallbacks": ["ollama/qwen2.5:3b"]
      }
    }
  }
}
```

### Step 5: Test the Fallback

```bash
# Simulate API failure by temporarily blocking the API
# Your agent should automatically switch to local model
```

---

## 🎯 Benefits

### 💰 Zero API Costs
When running on local models, you pay nothing for tokens. Great for:
- Development and testing
- After-hours batch processing
- High-volume tasks during budget crunches

### 🚫 No Rate Limits
Local models don't have rate limits. Process as many requests as your hardware allows.

### 📡 Works Offline
Network down? Agent keeps working. Perfect for:
- Travel (airplane mode)
- Remote locations
- Network outages

### 🔒 Privacy
Everything stays local. Your data never leaves your machine. Ideal for:
- Sensitive information
- Compliance requirements
- Personal privacy

---

## ⚙️ Advanced Configuration

### Multiple Fallback Layers

Configure a chain of fallbacks:

```json
{
  "agents": {
    "defaults": {
      "model": {
        "model": "anthropic/claude-sonnet-4-5",
        "fallbacks": [
          "openai/gpt-4.1-mini",
          "google/gemini-2.0-flash",
          "ollama/qwen2.5:7b",
          "ollama/qwen2.5:3b"
        ]
      }
    }
  }
}
```

This tries each provider in order:
1. Claude Sonnet (primary)
2. GPT-4.1 Mini (if Anthropic fails)
3. Gemini Flash (if OpenAI fails)
4. Qwen 7B local (if all cloud fails)
5. Qwen 3B local (last resort)

### Per-Agent Fallbacks

Different agents can have different fallbacks:

```json
{
  "agents": {
    "agents": {
      "morpheus": {
        "model": {
          "model": "anthropic/claude-opus-4",
          "fallbacks": ["ollama/qwen2.5:7b"]
        }
      },
      "oracle": {
        "model": {
          "model": "anthropic/claude-sonnet-4-5",
          "fallbacks": ["ollama/llama3.2:3b"]
        }
      }
    }
  }
}
```

### Remote Ollama Server

If you have a powerful machine elsewhere:

```json
{
  "models": {
    "providers": {
      "ollama-remote": {
        "baseUrl": "http://192.168.1.100:11434/v1",
        "apiKey": "ollama-local",
        "api": "openai-completions",
        "models": [
          {"id": "codestral:22b", "name": "Codestral 22B (Remote GPU)"}
        ]
      }
    }
  }
}
```

---

## 📊 Performance Expectations

### Local Model Capabilities

| Capability | Cloud (Sonnet) | Local (Qwen 3B) | Notes |
|------------|----------------|-----------------|-------|
| Simple chat | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Nearly identical |
| Tool calling | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Works but less reliable |
| Complex reasoning | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Noticeable quality drop |
| Coding | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Good for simple tasks |
| Long context | ⭐⭐⭐⭐⭐ | ⭐⭐ | Limited context window |

### Response Time

| Model | Typical Response Time | Hardware |
|-------|----------------------|----------|
| Cloud (Sonnet) | 1-3 seconds | N/A |
| Qwen 3B (CPU) | 5-15 seconds | 8GB RAM |
| Qwen 3B (GPU) | 1-3 seconds | RTX 3060+ |
| Qwen 7B (GPU) | 2-5 seconds | RTX 3070+ |

---

## 🔧 Troubleshooting

### "Connection refused" to Ollama

```bash
# Check if Ollama is running
pgrep ollama

# Start it
ollama serve

# Or as a service
systemctl start ollama
```

### Model not found

```bash
# List installed models
ollama list

# Pull if missing
ollama pull qwen2.5:3b
```

### Out of memory

```bash
# Use smaller model
ollama pull qwen2.5:1.5b

# Or increase swap
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Slow responses

- Use GPU if available (CUDA/ROCm)
- Try smaller models (3B instead of 7B)
- Close other memory-intensive applications

---

## 🧪 Testing Your Setup

### Quick Test Script

```bash
#!/bin/bash
# test-local-fallback.sh

echo "Testing Ollama connection..."
curl -s http://localhost:11434/api/tags | jq '.models[].name'

echo -e "\nTesting model response..."
curl -s http://localhost:11434/api/generate \
  -d '{"model": "qwen2.5:3b", "prompt": "Say hello!", "stream": false}' \
  | jq -r '.response'

echo -e "\nLocal fallback ready! ✅"
```

### Simulate Failover

To test that failover works:
1. Temporarily rename/disable your API key
2. Send a message to your agent
3. Verify it switches to local model
4. Restore API key

---

## 📝 Best Practices

1. **Always have a local fallback** — Even if you never use it, peace of mind is valuable

2. **Test regularly** — Run the test script monthly to ensure local models work

3. **Keep models updated** — `ollama pull qwen2.5:3b` to get latest versions

4. **Match capabilities** — Use coding models for coding agents, general models for chat

5. **Monitor disk space** — Models are large; keep 20GB+ free

6. **Document your setup** — Note which models work best for your workflows

---

## 🚀 Future Enhancements

Planned improvements for local fallback:

- [ ] Automatic model selection based on task type
- [ ] Quality estimation to warn when local quality might be insufficient
- [ ] Hybrid mode: Use local for simple tasks, cloud for complex
- [ ] Model download assistant in skill scripts

---

*"When the cloud fails, the local machine saves the day."* 🛸
