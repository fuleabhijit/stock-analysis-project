import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")


def _client():
    return Groq(api_key=GROQ_API_KEY)


def analyze_stock(symbol: str, current_price: float,
                  price_change: float, pct_change: float,
                  metadata: dict) -> dict:

    if not GROQ_API_KEY:
        return {
            "technical_analysis": "Set GROQ_API_KEY in .env to enable AI analysis.",
            "trend": "N/A",
            "risk": "N/A",
            "recommendation": "N/A",
            "support_resistance": "N/A",
        }

    prompt = f"""
You are a professional stock analyst. Analyze {symbol}:
- Current price: ${current_price}
- Change: ${price_change} ({pct_change:.2f}%)
- Sector: {metadata.get('sector', 'N/A')}
- P/E ratio: {metadata.get('pe_ratio', 'N/A')}
- 52-week high: ${metadata.get('52w_high')} / low: ${metadata.get('52w_low')}

Return ONLY a valid JSON object with exactly these keys:
technical_analysis, trend, risk, recommendation, support_resistance

Each value must be a plain string under 60 words. No markdown, no code fences.
"""

    try:
        resp = _client().chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.3,
        )
        text = resp.choices[0].message.content.strip()

        # Clean up any accidental markdown fences
        if "```" in text:
            parts = text.split("```")
            for part in parts:
                part = part.strip()
                if part.startswith("json"):
                    part = part[4:].strip()
                if part.startswith("{"):
                    text = part
                    break

        return json.loads(text)

    except json.JSONDecodeError:
        return {
            "technical_analysis": text if "text" in dir() else "Parse error",
            "trend": "N/A",
            "risk": "N/A",
            "recommendation": "HOLD",
            "support_resistance": "N/A",
        }
    except Exception as e:
        return {
            "technical_analysis": f"Analysis error: {str(e)}",
            "trend": "N/A",
            "risk": "N/A",
            "recommendation": "N/A",
            "support_resistance": "N/A",
        }


def get_news_summary(symbol: str, company_name: str) -> str:
    if not GROQ_API_KEY:
        return "Set GROQ_API_KEY in .env to enable news summaries."

    prompt = (
        f"In 3-4 sentences, summarise the current market sentiment, "
        f"recent developments, and analyst outlook for {company_name} ({symbol}). "
        f"Be concise and factual. No markdown formatting."
    )

    try:
        resp = _client().chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.3,
        )
        return resp.choices[0].message.content.strip()

    except Exception as e:
        return f"News summary unavailable: {str(e)}"