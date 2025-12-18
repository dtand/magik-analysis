# Strategy Configuration Reference

## Overview

Trading strategies in MAGE are defined using JSON configuration files. This declarative approach allows you to build complex conditional trading logic without writing code.

---

## Structure

### Basic Template

```json
{
    "name": "Strategy Name",
    "description": "Strategy description",
    "dataSpecifications": [...],
    "signals": [...],
    "actions": [...]
}
```

---

## Top-Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✓ | Strategy identifier used in reports and output files |
| `description` | string | ✓ | Human-readable explanation of the strategy logic |
| `dataSpecifications` | array | ✓ | Define symbols, data sources, and indicators |
| `signals` | array | | Reusable boolean conditions that can be referenced in actions |
| `actions` | array | ✓ | Trading instructions (buy/sell) with trigger criteria |

---

## Data Specifications

Defines the market data and technical indicators required for your strategy.

```json
{
    "symbol": "6B.FUT",
    "source": "LocalFiles",
    "marketType": "FUTURE",
    "timeSeries": "1h",
    "indicators": [...]
}
```

### Fields

| Field | Options | Description |
|-------|---------|-------------|
| `symbol` | string | Ticker symbol or `$1` as placeholder |
| `source` | `LocalFiles`, `AlphaVantage` | Data provider |
| `marketType` | `FUTURE`, `SPOT`, `CRYPTO`, `EQUITY` | Asset classification |
| `timeSeries` | `1h`, `DAILY`, etc. | Candle time resolution |
| `indicators` | array | Technical indicators to compute |

### Indicators

Each indicator calculates a technical value that can be referenced in your strategy logic.

```json
{
    "name": "rsi",
    "identifier": "RSI_14",
    "config": {
        "real": "close",
        "timeperiod": 14
    }
}
```

| Field | Description |
|-------|-------------|
| `name` | Indicator function: `rsi`, `sma`, `delta`, `sbh`, `var_change_pct` |
| `identifier` | Variable name used to reference this indicator in criteria |
| `config` | Indicator-specific parameters |

#### Common Indicators

**RSI** - Relative Strength Index
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

**SMA** - Simple Moving Average
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

**Delta** - Change between two points
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

**SBH** - Session-Based High/Low
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

---

## Signals

Optional reusable conditions that act as boolean flags. Once triggered, they remain active until reset.

```json
{
    "identifier": "BULLISH_SIGNAL",
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
```

| Field | Description |
|-------|-------------|
| `identifier` | Signal name to reference in actions |
| `criteria` | Logical condition that activates the signal |

---

## Actions

Define when and how to execute trades.

```json
{
    "action": {
        "do": "MARKET_BUY"
    },
    "symbol": "6B.FUT",
    "size": {
        "size": 10,
        "type": "STANDARD"
    },
    "criteria": {...},
    "followUpActions": [...]
}
```

### Action Types

| Type | Description |
|------|-------------|
| `MARKET_BUY` | Open or add to a long position |
| `MARKET_SELL` | Close long position or open short |
| `SIGNAL_RESET` | Reset a signal flag to inactive |

### Size Configuration

| Field | Values | Description |
|-------|--------|-------------|
| `size` | number | Quantity or percentage |
| `type` | `STANDARD`, `PERCENT` | Fixed units or % of position (1.0 = 100%) |
| `transform` | object | Optional dynamic sizing function |

### Transform Example

```json
"size": {
    "size": 10,
    "type": "STANDARD",
    "transform": {
        "method": "rsi_inverse_range",
        "configuration": {
            "symbol": "6B.FUT",
            "variables": ["RSI"],
            "rsiRange": [30, 70]
        }
    }
}
```

---

## Criteria Logic

Criteria define conditional logic using comparison operators and AND/OR chains.

### Structure

```json
{
    "var1": {
        "symbol": "6B.FUT",
        "var": "close",
        "offset": 0
    },
    "op": "gt",
    "var2": {
        "symbol": "6B.FUT",
        "var": "SMA_50",
        "offset": 0
    },
    "and": [...],
    "or": [...]
}
```

### Variable Object

| Field | Description |
|-------|-------------|
| `symbol` | Symbol to reference, or `null` for global variables |
| `var` | Variable name (see Variable Reference below) |
| `offset` | Lookback period: `0` = current, `-1` = previous bar, `-6` = 6 bars ago |

### Comparison Operators

| Operator | Meaning |
|----------|---------|
| `eq` | Equal to |
| `gt` | Greater than |
| `lt` | Less than |
| `gteq` | Greater than or equal to |
| `lteq` | Less than or equal to |

### Logical Operators

- **`and`**: Array of criteria - ALL must be true
- **`or`**: Array of criteria - ANY can be true

### Example: Complex Criteria

```json
{
    "var1": {"symbol": "6B.FUT", "var": "RSI", "offset": 0},
    "op": "lt",
    "var2": {"symbol": null, "var": 30, "offset": 0},
    "and": [
        {
            "var1": {"symbol": "6B.FUT", "var": "close", "offset": 0},
            "op": "gt",
            "var2": {"symbol": "6B.FUT", "var": "SMA_50", "offset": 0}
        },
        {
            "var1": {"symbol": "6B.FUT", "var": "position", "offset": 0},
            "op": "eq",
            "var2": {"symbol": null, "var": false, "offset": 0}
        }
    ]
}
```

This reads as: "RSI is below 30 AND close is above SMA_50 AND no position is open"

---

## Variable Reference

### Market Data

- `open`, `close`, `high`, `low`, `volume`

### Timestamps

- `timestamp.hour` - Hour of day (0-23)
- `timestamp.day` - Day of week
- `timestamp.minute` - Minute

### Indicators

Use the `identifier` defined in your data specifications:
- `RSI`, `SMA_50`, `DELTA_RSI`, etc.

### Position Data

- `position` - Boolean, true if position is open
- `position.quantity` - Current position size
- `position.pnl` - Unrealized P&L

### Signals

Reference signal `identifier` names directly:
- `BULLISH_SIGNAL`, `TREND_ACTIVE`, etc.

### Portfolio

- `portfolio` - Portfolio object with all positions

---

## Complete Example

```json
{
    "name": "RSI Oversold Long",
    "description": "Buy when RSI drops below 30 and price is above 50-day SMA",
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
                    "config": {"real": "close", "timeperiod": 14}
                },
                {
                    "name": "sma",
                    "identifier": "SMA_50",
                    "config": {"real": "close", "timeperiod": 50}
                }
            ]
        }
    ],
    "signals": [
        {
            "identifier": "OVERSOLD",
            "criteria": {
                "var1": {"symbol": "6B.FUT", "var": "RSI", "offset": 0},
                "op": "lt",
                "var2": {"symbol": null, "var": 30, "offset": 0}
            }
        }
    ],
    "actions": [
        {
            "action": {"do": "MARKET_BUY"},
            "symbol": "6B.FUT",
            "size": {"size": 10, "type": "STANDARD"},
            "criteria": {
                "var1": {"symbol": null, "var": "OVERSOLD", "offset": 0},
                "op": "eq",
                "var2": {"symbol": null, "var": true, "offset": 0},
                "and": [
                    {
                        "var1": {"symbol": "6B.FUT", "var": "close", "offset": 0},
                        "op": "gt",
                        "var2": {"symbol": "6B.FUT", "var": "SMA_50", "offset": 0}
                    },
                    {
                        "var1": {"symbol": "6B.FUT", "var": "position", "offset": 0},
                        "op": "eq",
                        "var2": {"symbol": null, "var": false, "offset": 0}
                    }
                ]
            },
            "followUpActions": [
                {
                    "action": {"do": "SIGNAL_RESET", "signal": "OVERSOLD"}
                }
            ]
        },
        {
            "action": {"do": "MARKET_SELL"},
            "symbol": "6B.FUT",
            "size": {"size": 1.0, "type": "PERCENT"},
            "criteria": {
                "var1": {"symbol": "6B.FUT", "var": "RSI", "offset": 0},
                "op": "gt",
                "var2": {"symbol": null, "var": 70, "offset": 0}
            }
        }
    ]
}
```

---

This documentation provides everything needed to create and understand JSON-based trading strategies in MAGE.
