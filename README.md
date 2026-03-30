# KairuAI

> **Autonomous AI Trading Agent**
> Predict markets. Analyze sentiment. Execute trades. All from one agent system.

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![TypeScript](https://img.shields.io/badge/typescript-5.4+-blue.svg)](https://typescriptlang.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Solana](https://img.shields.io/badge/chain-Solana-purple.svg)](https://solana.com)
[![Token](https://img.shields.io/badge/token-%24KAIRUAI-orange.svg)](https://pump.fun)
[![Contributing](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## What is KairuAI?

KairuAI is an open-source autonomous AI trading agent built on Solana. It combines LLM-powered price prediction, real-time sentiment analysis, on-chain trade execution, and prediction market intelligence — all under one unified system.

> *"Most AI tokens ship a roadmap. KairuAI ships working agents."*

---

## Agents

| Agent | Language | Description |
|-------|----------|-------------|
| **Prediction Agent** | Python | LLM + technical analysis for price forecasting |
| **Signal Agent** | Python | Sentiment from Twitter/X + news → BUY/SELL/HOLD signals |
| **Trading Agent** | TypeScript | Execute token swaps on Solana via Jupiter Aggregator |
| **Polymarket Agent** | TypeScript | Monitor prediction markets, surface high-value opportunities |

---

## Quickstart

### 1. Clone

```bash
git clone https://github.com/KairuAI/kairuai
cd kairuai
```

### 2. Install

```bash
# Install everything
make install

# Or manually:
pip install -r requirements.txt
npm install
```

### 3. Configure

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 4. Run

```bash
# Interactive menu
python kairu.py

# Or run specific agents:
make predict      # Prediction Agent
make signal       # Signal Agent
make trading      # Trading Agent (TypeScript)
make polymarket   # Polymarket Agent (TypeScript)
```

---

## Usage

### Prediction Agent
```
KairuAI Prediction: SOL
─────────────────────────────
PREDICTION: BULLISH
Confidence: 78/100
Current: $142.30
Target: $158.00
Key risk: Market-wide correction
```

### Signal Agent
```
Signal: $SOL
─────────────────────────────
Sentiment: BULLISH
Signal: BUY
Confidence: 72/100
Themes: ecosystem growth, validator activity
```

### Trading Agent (TypeScript)
```bash
cd agents/trading && npm run dev
# → Connects to Solana RPC
# → Fetches live prices
# → Gets swap quote via Jupiter
# → Executes on confirmation
```

### Polymarket Agent (TypeScript)
```bash
cd agents/polymarket && npm run dev
# → Fetches top markets by volume
# → Identifies high-confidence opportunities
# → Displays market analysis
```

---

## Project Structure

```
kairuai/
├── kairu.py                      ← Python CLI entry point
├── agents/
│   ├── prediction_agent.py       ← LLM price prediction
│   ├── signal_agent.py           ← Sentiment → signals
│   ├── trading/                  ← TypeScript Solana DEX
│   │   └── src/index.ts
│   └── polymarket/               ← TypeScript prediction markets
│       └── src/index.ts
├── sdk/
│   └── src/index.ts              ← Shared TypeScript SDK
├── .github/workflows/ci.yml      ← CI pipeline
├── Makefile
├── install.sh
├── requirements.txt
├── package.json
└── .env.example
```

---

## API Keys

| Key | Source | Used by |
|-----|--------|---------|
| `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com) | Prediction + Signal |
| `SOLANA_PRIVATE_KEY` | Your Solana wallet | Trading Agent |
| `TWITTER_BEARER_TOKEN` | [developer.twitter.com](https://developer.twitter.com) | Signal Agent |
| `POLYMARKET_API_KEY` | [polymarket.com](https://polymarket.com) | Polymarket Agent |
| `SOLANA_RPC_URL` | [helius.dev](https://helius.dev) or public RPC | Trading Agent |

---

## Disclaimer

KairuAI is experimental software. AI predictions are **not financial advice**. Trading involves significant risk. Always test with small amounts. Never share your private key.

---

## Roadmap

### v1.0.0 (current)
- [x] Prediction Agent — LLM price forecasting
- [x] Signal Agent — sentiment analysis
- [x] Trading Agent — Solana DEX execution (TypeScript)
- [x] Polymarket Agent — prediction markets (TypeScript)
- [x] TypeScript SDK
- [x] GitHub Actions CI

### v1.1.0
- [ ] Persistent agent memory
- [ ] Auto-trading mode with risk limits
- [ ] Telegram alerts

### v2.0.0
- [ ] Web dashboard
- [ ] Multi-chain support
- [ ] Agent coordination

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) — contributions welcome.

---

## License

MIT — see [LICENSE](LICENSE)

---

<div align="center">
  <strong>KairuAI</strong> · Autonomous AI Trading Agent<br>
  <code>$KAIRUAI</code> · Built on Solana
</div>
