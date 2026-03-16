import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


class APIClient:

    @staticmethod
    def analyze_stock(symbol: str, period: str = "1y") -> dict:
        try:
            r = requests.post(
                f"{API_BASE_URL}/api/stocks/analyze",
                json={"symbol": symbol, "period": period},
                timeout=40,
            )
            r.raise_for_status()
            return r.json()
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_price(symbol: str) -> dict:
        try:
            r = requests.get(
                f"{API_BASE_URL}/api/stocks/price/{symbol}",
                timeout=10,
            )
            r.raise_for_status()
            return r.json()
        except Exception as e:
            return {"error": str(e)}