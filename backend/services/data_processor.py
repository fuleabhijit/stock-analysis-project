import pandas as pd
from typing import Dict, Any, List

class DataProcessor:

    @staticmethod
    def prepare_chart_data(df: pd.DataFrame) -> Dict[str, Any]:
        df = df.copy()
        df.index = pd.to_datetime(df.index)
        return {
            "dates":   df.index.strftime("%Y-%m-%d").tolist(),
            "opens":   [round(v, 2) for v in df["Open"].tolist()],
            "highs":   [round(v, 2) for v in df["High"].tolist()],
            "lows":    [round(v, 2) for v in df["Low"].tolist()],
            "closes":  [round(v, 2) for v in df["Close"].tolist()],
            "volumes": [int(v) for v in df["Volume"].tolist()],
        }

    @staticmethod
    def calculate_moving_averages(df: pd.DataFrame,
                                  windows: List[int] = [20, 50, 200]) -> Dict[str, List]:
        result = {}
        for w in windows:
            if len(df) >= w:
                ma = df["Close"].rolling(window=w).mean()
                result[f"MA{w}"] = [None if pd.isna(v) else round(v, 2) for v in ma.tolist()]
        return result

    @staticmethod
    def calculate_rsi(df: pd.DataFrame, period: int = 14) -> List:
        delta = df["Close"].diff()
        gain  = delta.where(delta > 0, 0).rolling(window=period).mean()
        loss  = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs    = gain / loss
        rsi   = 100 - (100 / (1 + rs))
        return [None if pd.isna(v) else round(v, 2) for v in rsi.tolist()]

    @staticmethod
    def calculate_bollinger_bands(df: pd.DataFrame, window: int = 20) -> Dict[str, List]:
        ma  = df["Close"].rolling(window=window).mean()
        std = df["Close"].rolling(window=window).std()
        return {
            "bb_upper": [None if pd.isna(v) else round(v, 2) for v in (ma + std * 2).tolist()],
            "bb_mid":   [None if pd.isna(v) else round(v, 2) for v in ma.tolist()],
            "bb_lower": [None if pd.isna(v) else round(v, 2) for v in (ma - std * 2).tolist()],
        }