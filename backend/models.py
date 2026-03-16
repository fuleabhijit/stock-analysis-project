from pydantic import BaseModel

class StockRequest(BaseModel):
    symbol: str
    period: str = "1y"   # Options: 1d | 5d | 1mo | 3mo | 6mo | 1y | 2y | 5y