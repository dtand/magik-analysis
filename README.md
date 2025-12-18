# magik-analysis

**MAGE** (Massive Gains Analysis Engine) - A Python-based framework for backtesting and analyzing trading strategies on historical market data.

> ⚠️ **Disclaimer**: I have no alpha. This is an educational/experimental project for testing trading strategies. Use at your own risk.

## 📋 Overview

MAGE enables you to:
- Define complex trading strategies using JSON configuration
- Backtest strategies on historical market data (futures, crypto, equities)
- Run multiple sampling strategies (sequential, random, Monte Carlo-style)
- Generate comprehensive performance reports with trade logs and metrics
- Utilize technical indicators (RSI, SMA, custom indicators)
- Implement session-based trading logic (pre-market, trading sessions)

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd magik-analysis

# Install dependencies
pip install -e .
```

## 📖 Quick Start

### Basic Usage

```python
from mage.src.Services.BacktestEngine import BacktestEngine
from mage.src.Services.BacktestService import BacktestService
from mage.src.Services.DTO.BacktestConfig import BacktestConfig

# Configure backtest
backtest_config = BacktestConfig(
    symbols=['6B.FUT'],                    # Symbols to test
    total_runs=50,                          # Number of runs (for random sampling)
    sample_size='3M',                       # Sample size (3 months)
    enable_reports=True,                    # Generate reports
    sampling_type='RANDOM',                 # RANDOM, SEQUENTIAL, or NONE
    strategy_json='./Strategies/resources/DeltaRSIThresholdLong.json',
    testing_period=[None, None]             # Optional: ['2024-01-01', '2024-12-31']
)

# Run backtest
backtest = BacktestService()
backtest.config = backtest_config
backtest.engine = BacktestEngine()
backtest.run()
```

### Run from main.py

Edit [mage/src/main.py](mage/src/main.py) and run:

```bash
python -m mage.src.main
```

## 📝 Creating a Strategy

Strategies are defined using JSON configuration files. Here's a complete example:

### Strategy JSON Structure

Create a JSON file in `mage/src/Strategies/resources/`:

```json
{
    "name": "My Strategy",
    "description": "Strategy description",
    "dataSpecifications": [
        {
            "symbol": "6B.FUT",
            "source": "LocalFiles",
            "marketType": "FUTURE",
            "timeSeries": "1h",
            "indicators": [
                {
                    "name": "rsi",
                    "identifier": "RSI",
                    "config": {
                        "real": "close",
                        "timeperiod": 14
                    }
                },
                {
                    "name": "sma",
                    "identifier": "SMA_50",
                    "config": {
                        "real": "close",
                        "timeperiod": 50
                    }
                }
            ]
        }
    ],
    "signals": [
        {
            "identifier": "OVERSOLD_SIGNAL",
            "criteria": {
                "var1": {
                    "symbol": "6B.FUT",
                    "var": "RSI",
                    "offset": 0
                },
                "op": "lt",
                "var2": {
                    "symbol": null,
                    "var": 30,
                    "offset": 0
                }
            }
        }
    ],
    "actions": [
        {
            "action": {
                "do": "MARKET_BUY"
            },
            "size": {
                "size": 10,
                "type": "STANDARD"
            },
            "symbol": "6B.FUT",
            "criteria": {
                "var1": {
                    "symbol": null,
                    "var": "OVERSOLD_SIGNAL",
                    "offset": 0
                },
                "op": "eq",
                "var2": {
                    "symbol": null,
                    "var": true,
                    "offset": 0
                },
                "and": [{
                    "var1": {
                        "symbol": "6B.FUT",
                        "var": "position",
                        "offset": 0
                    },
                    "op": "eq",
                    "var2": {
                        "symbol": null,
                        "var": false,
                        "offset": 0
                    }
                }]
            },
            "followUpActions": [{
                "action": {
                    "do": "SIGNAL_RESET",
                    "signal": "OVERSOLD_SIGNAL"
                }
            }]
        },
        {
            "action": {
                "do": "MARKET_SELL"
            },
            "size": {
                "size": 1.0,
                "type": "PERCENT"
            },
            "symbol": "6B.FUT",
            "criteria": {
                "var1": {
                    "symbol": "6B.FUT",
                    "var": "RSI",
                    "offset": 0
                },
                "op": "gt",
                "var2": {
                    "symbol": null,
                    "var": 70,
                    "offset": 0
                }
            }
        }
    ]
}
```

### Strategy Components

#### 1. Data Specifications
Define symbols, data sources, and indicators:

```json
"dataSpecifications": [{
    "symbol": "6B.FUT",              // Symbol identifier
    "source": "LocalFiles",           // Data source
    "marketType": "FUTURE",           // FUTURE, CRYPTO, EQUITY
    "timeSeries": "1h",               // Time resolution
    "indicators": [...]               // Technical indicators
}]
```

#### 2. Available Indicators

- **RSI** (Relative Strength Index)
  ```json
  {
      "name": "rsi",
      "identifier": "RSI",
      "config": {
          "real": "close",
          "timeperiod": 14
      }
  }
  ```

- **SMA** (Simple Moving Average)
  ```json
  {
      "name": "sma",
      "identifier": "SMA_50",
      "config": {
          "real": "close",
          "timeperiod": 50
      }
  }
  ```

- **Delta** (Calculate change between periods)
  ```json
  {
      "name": "delta",
      "identifier": "DELTA_RSI",
      "config": {
          "indicator": "RSI",
          "d1": 0,
          "d2": -6
      }
  }
  ```

- **Session-Based High/Low** (sbh)
  ```json
  {
      "name": "sbh",
      "identifier": "SBH",
      "config": {
          "pre_session": [0, 5],
          "session_a": [6, 12],
          "session_b": [13, 20]
      }
  }
  ```

#### 3. Signals
Reusable conditions that can be referenced in actions:

```json
"signals": [{
    "identifier": "SIGNAL_NAME",
    "criteria": {
        "var1": { "symbol": "6B.FUT", "var": "RSI", "offset": 0 },
        "op": "lt",
        "var2": { "symbol": null, "var": 30, "offset": 0 }
    }
}]
```

#### 4. Actions
Define buy/sell logic:

**Action Types:**
- `MARKET_BUY` - Open long position
- `MARKET_SELL` - Close long position or open short
- `SIGNAL_RESET` - Reset a signal flag

**Size Types:**
- `STANDARD` - Fixed quantity
- `PERCENT` - Percentage of position (1.0 = 100%)

**Operators:**
- `eq` - Equal to
- `gt` - Greater than
- `lt` - Less than
- `gteq` - Greater than or equal to
- `lteq` - Less than or equal to

#### 5. Criteria with Logic
Combine multiple conditions:

```json
"criteria": {
    "var1": { "symbol": "6B.FUT", "var": "RSI", "offset": 0 },
    "op": "lt",
    "var2": { "symbol": null, "var": 30, "offset": 0 },
    "and": [
        {
            "var1": { "symbol": "6B.FUT", "var": "position", "offset": 0 },
            "op": "eq",
            "var2": { "symbol": null, "var": false, "offset": 0 }
        }
    ],
    "or": [...]
}
```

## 🔍 Sampling Types

### SEQUENTIAL
Runs backtest from start to finish on full dataset:
```python
sampling_type='SEQUENTIAL'
```

### RANDOM
Runs multiple tests on random sample periods:
```python
sampling_type='RANDOM',
total_runs=50,
sample_size='3M'  # 3 months per sample
```

### NONE
Single run on full dataset:
```python
sampling_type='NONE'
```

## 📊 Understanding Results

Results are saved to `mage/src/Strategies/results/` as Excel files with multiple sheets:

### Trades Sheet
- Timestamp
- Symbol
- Action Type (MARKET_BUY, MARKET_SELL)
- Position Status (Open, Close, Add)
- Cost Basis
- Size
- P&L

### Performance Sheet
- **PnL**: Total profit/loss
- **Win / Loss Ratio**: Winning trades / losing trades
- **Avg Win**: Average profit per winning trade
- **Avg Loss**: Average loss per losing trade
- **Max Win**: Largest winning trade
- **Max Loss**: Largest losing trade
- **Longest Win Streak**: Consecutive wins
- **Longest Lose Streak**: Consecutive losses

### Data Log Sheet
Complete candle data with indicators for every epoch

## 📁 Project Structure

```
mage/src/
├── Analysis/           # Analysis framework
├── ApiClients/         # Data providers (Alpha Vantage, local files)
├── Indicators/         # Technical indicators
├── Resources/          # Historical data
│   ├── downloads/
│   └── test-data/
├── Services/           # Core engines
│   ├── BacktestEngine.py       # Main backtest orchestration
│   ├── BacktestService.py      # Service wrapper
│   ├── LogicEngine.py          # Criteria evaluation
│   ├── Portfolio.py            # Position management
│   └── TradingReport.py        # Report generation
├── Strategies/         # Strategy definitions
│   ├── resources/      # Strategy JSON files
│   └── results/        # Backtest results
└── Utils/              # Helper functions
```

## 💡 Example Strategies

See [mage/src/Strategies/resources/](mage/src/Strategies/resources/) for examples:

- **DeltaRSIThresholdLong.json** - RSI delta-based trend following
- **MACrossTrendBTD.json** - Moving average crossover
- **DeltaRSIThresholdShort.json** - Short-side RSI strategy

## 📦 Supported Data

The framework includes test data for:
- **Futures**: 6B, 6A, 6C, 6E, 6J, ES, NQ, GC, etc.
- **Crypto**: BTC, ETH, BNB, DOGE
- **Equities**: GLD, GBTC, ETHE

Data format: JSON with OHLCV + timestamp

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=mage
```

## 🤝 Contributing

Feel free to open issues or submit pull requests for improvements.

## 📄 License

MIT

## ⚠️ Risk Warning

This software is for educational and research purposes only. Past performance does not guarantee future results. Trading involves substantial risk of loss. Always conduct thorough testing and risk management before using any trading strategy with real capital.
