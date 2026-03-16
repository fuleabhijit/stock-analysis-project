from fastapi import APIRouter, HTTPException
from datetime import datetime
from models import StockRequest
from services.yahoo_finance import YahooFinanceService
from services.data_processor import DataProcessor
from services import grok_analyzer

router = APIRouter(prefix="/api/stocks", tags=["stocks"])

@router.post("/analyze")
async def analyze_stock(req: StockRequest):
    try:
        hist, meta = YahooFinanceService.get_stock_data(req.symbol, req.period)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    chart_data  = DataProcessor.prepare_chart_data(hist)
    moving_avgs = DataProcessor.calculate_moving_averages(hist)
    rsi         = DataProcessor.calculate_rsi(hist)
    bbands      = DataProcessor.calculate_bollinger_bands(hist)

    analysis = grok_analyzer.analyze_stock(
        req.symbol, meta["current_price"],
        meta["price_change"], meta["percentage_change"], meta
    )
    news = grok_analyzer.get_news_summary(req.symbol, meta["company_name"])

    return {
        **meta,
        "chart_data":      chart_data,
        "moving_averages": moving_avgs,
        "rsi":             rsi,
        "bollinger":       bbands,
        "analysis":        analysis,
        "news_summary":    news,
        "timestamp":       datetime.now().isoformat(),
    }

@router.get("/price/{symbol}")
async def get_price(symbol: str):
    try:
        price = YahooFinanceService.get_latest_price(symbol)
        return {"symbol": symbol.upper(), "price": price}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))