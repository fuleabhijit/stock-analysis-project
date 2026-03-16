import yfinance as yf
import pandas as pd
from typing import Tuple

class YahooFinanceService:

    @staticmethod
    def get_stock_data(symbol: str, period: str = "1y") -> Tuple[pd.DataFrame, dict]:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)

        if hist.empty:
            raise ValueError(f"No data found for symbol '{symbol}'")

        info = ticker.info
        current_price = hist["Close"].iloc[-1]
        open_price    = hist["Close"].iloc[0]
        price_change  = current_price - open_price
        pct_change    = (price_change / open_price * 100) if open_price else 0

        metadata = {
            "symbol":            symbol.upper(),
            "company_name":      info.get("longName", symbol.upper()),
            "current_price":     round(float(current_price), 2),
            "price_change":      round(float(price_change), 2),
            "percentage_change": round(float(pct_change), 2),
            "market_cap":        info.get("marketCap", 0),
            "pe_ratio":          info.get("trailingPE", 0) or 0,
            "dividend_yield":    info.get("dividendYield", 0) or 0,
            "52w_high":          info.get("fiftyTwoWeekHigh", 0) or 0,
            "52w_low":           info.get("fiftyTwoWeekLow", 0) or 0,
            "avg_volume":        info.get("averageVolume", 0) or 0,
            "sector":            info.get("sector", "N/A"),
        }
        return hist, metadata

    @staticmethod
    def get_latest_price(symbol: str) -> float:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1d")
        if hist.empty:
            raise ValueError(f"No price data for '{symbol}'")
        return round(float(hist["Close"].iloc[-1]), 2)