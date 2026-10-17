# crypto-signal-aggregator

A multi-source crypto futures signal generator that fuses 10 independent analytical bots into a single unified recommendation. Designed as a modular aggregator with wrappers for each analytical dimension.

*English summary below; the original Persian (فارسی) overview is in [README_FA.md](README_FA.md).*

## The 10 analytical wrappers

Each lives under `bots/` and produces signals that the aggregator combines:

| Wrapper | Focus |
|---------|-------|
| `wrapper_technical_basic` | Classical TA (RSI, MACD, MA crosses) |
| `wrapper_technical_advanced` | Advanced patterns, structure, divergence |
| `wrapper_volume` | Volume profile, imbalance, anomaly |
| `wrapper_volatility` | ATR-based regime + breakout detection |
| `wrapper_ml_prediction` | ML price/direction forecasts |
| `wrapper_onchain` | On-chain token flow + whale activity |
| `wrapper_sentiment` | Reddit + Twitter sentiment |
| `wrapper_macro` | Macro/economic context |
| `wrapper_correlation` | Cross-asset correlation diagnostics |
| `wrapper_ai` | GPT-4 synthesis over the other signals |

## Layout

```
crypto-signal-aggregator/
├── main.py                # Entry point
├── start.py               # Process orchestrator
├── aggregator/            # Cross-wrapper signal fusion
├── bots/                  # The 10 analytical wrappers
│   ├── crypto_signal_base # Shared base classes
│   └── ta_lib             # TA-Lib wrappers
├── data_fetchers/         # Market data adapters
├── database/              # Persistence layer
├── tg_bot/                # Telegram delivery
├── config/                # Config files
├── utils/                 # Shared utilities
├── tests/                 # Unit tests
├── Dockerfile
├── docker-compose.yml
└── requirements*.txt
```

## Quick start

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set credentials in environment (Telegram, OpenAI, exchange keys, etc.)
# Avoid committing .env — it is gitignored.

python main.py
```

Docker:

```bash
docker-compose up -d
```

## Requirements files

- `requirements.txt` — core runtime
- `requirements-min.txt` — minimal slice
- `requirements-optional.txt` — optional extras (ML, on-chain, etc.)
- `requirements-dev.txt` — dev / test

## Credits and third-party code

This repository vendors two MIT-licensed open-source projects. Their original licenses are kept in place, and all credit for that code goes to the original authors:

- **`bots/crypto_signal_base/`**: [Crypto-Signal](https://github.com/CryptoSignal/Crypto-Signal), Copyright (c) 2017 Abenezer Mamo, MIT License (see `bots/crypto_signal_base/LICENSE`).
- **`bots/ta_lib/`**: [ta — Technical Analysis Library in Python](https://github.com/bukosabino/ta) v0.11.0, Copyright 2020 Darío López Padial (Bukosabino), MIT License (see `bots/ta_lib/LICENSE`).

Everything outside those two folders (e.g. `bots/wrapper_*.py`, `aggregator/`, `data_fetchers/`, `tg_bot/`) is covered by the root `LICENSE`.

## ⚠️ Disclaimer

This software is provided **for educational and research purposes only** and is **not** financial advice. Aggregated signals are algorithmic opinions drawn from public data and may be wrong. Trading cryptocurrency futures carries substantial risk of loss including leveraged liquidation. The author assumes no liability for losses arising from use of this software.
