# Contributing to KairuAI

Thanks for your interest in contributing. All contributions are welcome.

## Getting Started

1. Fork the repository
2. Clone: `git clone https://github.com/YOUR_USERNAME/kairuai`
3. Create a branch: `git checkout -b feat/your-feature`
4. Install deps: `make install`
5. Copy env: `cp .env.example .env`

## Project Structure

```
kairu.py                    ← Python CLI entry point
agents/
  prediction_agent.py       ← Python: LLM price prediction
  signal_agent.py           ← Python: sentiment analysis
  trading/src/index.ts      ← TypeScript: Solana DEX trading
  polymarket/src/index.ts   ← TypeScript: prediction markets
sdk/src/index.ts            ← TypeScript: shared SDK
```

## Adding a New Agent

**Python agent:**
1. Create `agents/your_agent.py` with a `run()` function
2. Register it in `kairu.py`

**TypeScript agent:**
1. Create `agents/your_agent/src/index.ts`
2. Add `package.json` and `tsconfig.json`
3. Add to workspace in root `package.json`

## Pull Request Guidelines

- One feature or fix per PR
- Clear commit messages
- Update README if behavior changes

## Reporting Issues

Open a GitHub issue with:
- What you expected
- What happened
- Steps to reproduce
- OS, Python/Node version

---

MIT License — contributions are welcome.
