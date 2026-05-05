import yfinance as yf
import pandas as pd
# pandas_ta removed to fix installation issues
import time
from colorama import init, Fore, Style
from datetime import datetime
import warnings

# Ignore warnings for cleaner output
warnings.filterwarnings("ignore")
init(autoreset=True)

# Ticker for Nifty 50 Index on Yahoo Finance
TICKER_SYMBOL = "^NSEI"
INTERVAL = "5m"

def fetch_data():
    try:
        # yfinance caching can sometimes return bad data, we can try to repair it
        ticker = yf.Ticker(TICKER_SYMBOL)
        data = ticker.history(period="5d", interval=INTERVAL, repair=True)
        return data
    except Exception as e:
        print(f"{Fore.RED}Error fetching data: {e}")
        return None

def analyze_and_print_signal():
    data = fetch_data()
    if data is None:
        return
    if data.empty:
        return

    # Calculate EMAs for crossover logic using pandas
    data['EMA_9'] = data['Close'].ewm(span=9, adjust=False).mean()
    data['EMA_15'] = data['Close'].ewm(span=15, adjust=False).mean()
    
    # Calculate 200 EMA to identify the major trend 
    data['EMA_200'] = data['Close'].ewm(span=200, adjust=False).mean()
    
    # Calculate RSI manually using pandas (Wilder's Smoothing)
    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.ewm(alpha=1/14, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/14, adjust=False).mean()
    rs = avg_gain / avg_loss
    data['RSI'] = 100 - (100 / (1 + rs))

    # Drop intermediate NaN values caused by indicator calculation intervals
    data.dropna(inplace=True)
    if len(data) < 2:
        return

    latest = data.iloc[-1]
    prev = data.iloc[-2]

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    close = latest['Close']

    # Higher timeframe trend confirmation
    trend_up = close > latest['EMA_200']
    trend_down = close < latest['EMA_200']

    # Short term crossover
    cross_up = latest['EMA_9'] > latest['EMA_15'] and prev['EMA_9'] <= prev['EMA_15']
    cross_down = latest['EMA_9'] < latest['EMA_15'] and prev['EMA_9'] >= prev['EMA_15']

    if cross_up:
        # High probability setup: Trend is UP, Short term shows momentum UP, market not extremely overbought (RSI < 75)
        if trend_up and latest['RSI'] < 75:
            print(f"[{current_time}] {Fore.GREEN}{Style.BRIGHT}🚀 HIGH PROBABILITY BUY CALL SIGNAL! Nifty at {close:.2f} | Targets: +10/+20 pts, SL: -10 pts")
        else:
            print(f"[{current_time}] {Fore.YELLOW}⚠️ Weak BUY CALL Signal (Counter-trend or RSI high). Nifty at {close:.2f}")

    elif cross_down:
        # High probability setup: Trend is DOWN, Short term momentum DOWN, market not oversold (RSI > 25)
        if trend_down and latest['RSI'] > 25:
            print(f"[{current_time}] {Fore.RED}{Style.BRIGHT}📉 HIGH PROBABILITY BUY PUT SIGNAL! Nifty at {close:.2f} | Targets: +10/+20 pts, SL: -10 pts")
        else:
            print(f"[{current_time}] {Fore.YELLOW}⚠️ Weak BUY PUT Signal (Counter-trend or RSI low). Nifty at {close:.2f}")
    else:
        trend_str = "UP" if latest['EMA_9'] > latest['EMA_15'] else "DOWN"
        rsi_val = latest['RSI']
        print(f"[{current_time}] Nifty: {close:.2f} | Momentum: {trend_str} | RSI: {rsi_val:.1f} | Scanning for perfect setup...")

def main():
    print(f"{Fore.CYAN}{Style.BRIGHT}==========================================")
    print(f"{Fore.CYAN}{Style.BRIGHT}  NIFTY 50 LIVE SCALPING SCANNER v1.0")
    print(f"{Fore.CYAN}{Style.BRIGHT}==========================================")
    print("Strategy: 9/15 EMA Crossover + 200 EMA Trend Filter + RSI Filter")
    print(f"Interval: 5 Minutes {Fore.LIGHTBLACK_EX}(Updating every 30 seconds){Style.RESET_ALL}")
    print("Press Ctrl+C to stop.")
    print("-" * 50)
    
    while True:
        try:
            analyze_and_print_signal()
            # Wait 30 seconds before polling again to ensure we catch 1-minute candle closes in real-time
            time.sleep(30) 
        except KeyboardInterrupt:
            print(f"\n{Fore.CYAN}Stopping Scalper. Goodbye!")
            break
        except Exception as e:
            print(f"{Fore.RED}Unexpected error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()
