# Nifty 50 Live Scalping Scanner

A highly optimized live scalping scanner for Nifty 50, focusing on high probability setups using EMAs and basic Price Action.

## Features
- **Live Data Fetching**: Uses `yfinance` to get 1-minute real-time data for Nifty 50 (`^NSEI`).
- **High Accuracy Indicators**:
  - `9 EMA` & `15 EMA` crossovers for short-term momentum shifts.
  - `200 EMA` for major trend confirmation.
  - `RSI (14)` to filter out overbought/oversold traps.
- **Color-Coded Console Output**: Provides clear, instant buy/sell signals with visual cues.

## Installation

1. Make sure you have Python 3 installed.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Simply run the script to start scanning:

```bash
python live_scanner.py
```

The script will fetch live market data every 30 seconds and print out high-probability Buy Call or Buy Put setups based on the crossover strategy. Press `Ctrl+C` to stop the scanner.

## Strategy Details
To hit a high win-rate, the scanner looks for:
- **BUY CALL**: `9 EMA` crosses above `15 EMA` + `Price > 200 EMA` (Uptrend) + `RSI < 75` (Not overbought).
- **BUY PUT**: `9 EMA` crosses below `15 EMA` + `Price < 200 EMA` (Downtrend) + `RSI > 25` (Not oversold).

*(Note: 99% accuracy is scientifically impossible in live markets, but combining EMA crossovers with Higher Timeframe Trends and RSI greatly increases probability)*.
