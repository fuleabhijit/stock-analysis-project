import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from utils import APIClient

st.set_page_config(
    page_title="StockMind AI",
    page_icon="S",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    .stApp { background: #f8fafc; min-height: 100vh; }
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="stToolbar"] { display: none; }
    [data-testid="stDecoration"] { display: none; }

    .main .block-container {
        padding-left: 3rem;
        padding-right: 3rem;
        padding-top: 2rem;
        max-width: 100%;
    }

    /* Search input */
    .stTextInput > div > div > input {
        background: #ffffff !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 14px !important;
        color: #0f172a !important;
        font-size: 15px !important;
        padding: 14px 20px !important;
        font-family: 'Inter', sans-serif !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 4px rgba(59,130,246,0.12) !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #94a3b8 !important;
    }

    /* Search button */
    .search-btn .stButton > button {
        background: #2563eb !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        width: 100% !important;
        height: 54px !important;
        box-shadow: 0 4px 14px rgba(37,99,235,0.3) !important;
        transition: all 0.2s !important;
        white-space: nowrap !important;
    }
    .search-btn .stButton > button:hover {
        background: #1d4ed8 !important;
        box-shadow: 0 6px 20px rgba(37,99,235,0.4) !important;
    }

    /* Popular ticker buttons */
    .pop-btn .stButton > button {
        background: #ffffff !important;
        color: #1d4ed8 !important;
        border: 1.5px solid #bfdbfe !important;
        border-radius: 8px !important;
        padding: 5px 4px !important;
        font-size: 11px !important;
        font-weight: 700 !important;
        width: 100% !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        letter-spacing: 0.02em !important;
        transition: all 0.15s !important;
        background-color: #eff6ff !important;
    }
    .pop-btn .stButton > button:hover {
        background: #dbeafe !important;
        border-color: #3b82f6 !important;
        color: #1e40af !important;
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1.5px solid #e2e8f0;
        border-radius: 16px;
        padding: 20px 24px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: all 0.25s;
    }
    [data-testid="stMetric"]:hover {
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        transform: translateY(-2px);
        border-color: #bfdbfe;
    }
    [data-testid="stMetricLabel"] {
        color: #6b7280 !important;
        font-size: 11px !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 700 !important;
    }
    [data-testid="stMetricValue"] {
        color: #0f172a !important;
        font-size: 22px !important;
        font-weight: 800 !important;
    }
    [data-testid="stMetricDelta"] { font-size: 12px !important; font-weight: 600 !important; }
    [data-testid="stMetricDeltaIcon-Up"]   { color: #10b981 !important; }
    [data-testid="stMetricDeltaIcon-Down"] { color: #ef4444 !important; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #0f172a;
        border-right: 1px solid #1e293b;
    }
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background: rgba(255,255,255,0.05) !important;
        border: 1.5px solid rgba(255,255,255,0.12) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
    }
    [data-testid="stSidebar"] .stMultiSelect > div > div {
        background: rgba(255,255,255,0.05) !important;
        border: 1.5px solid rgba(255,255,255,0.12) !important;
        border-radius: 10px !important;
    }
    [data-testid="stSidebar"] .stMultiSelect span[data-baseweb="tag"] {
        background: rgba(96,165,250,0.15) !important;
        color: #93c5fd !important;
        border: 1px solid rgba(96,165,250,0.3) !important;
    }
    [data-testid="stSidebar"] .stButton > button {
        background: #2563eb !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        width: 100% !important;
    }

    hr { border-color: #e2e8f0 !important; margin: 1.5rem 0 !important; }
    .stSpinner > div { border-top-color: #3b82f6 !important; }
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:24px 0 32px;'>
        <div style='font-size:20px;font-weight:800;color:#60a5fa;letter-spacing:-0.5px;'>
            StockMind AI
        </div>
        <div style='font-size:11px;color:#475569;margin-top:4px;'>Chart settings</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.1em;font-weight:700;margin-bottom:8px;'>Time Period</div>", unsafe_allow_html=True)
    period = st.selectbox("", ["1d","5d","1mo","3mo","6mo","1y","2y","5y"],
                          index=5, label_visibility="collapsed")

    st.markdown("<div style='font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.1em;font-weight:700;margin:20px 0 8px;'>Indicators</div>", unsafe_allow_html=True)
    indicators = st.multiselect("", ["MA20","MA50","MA200","Bollinger Bands"],
                                default=["MA20","MA50"], label_visibility="collapsed")

    st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)
    sidebar_analyze = st.button("Apply & Analyze", use_container_width=True)

    st.markdown("""
    <div style='margin-top:32px;padding-top:20px;border-top:1px solid #1e293b;'>
        <div style='font-size:11px;color:#475569;line-height:1.7;'>
            Supports NYSE, NASDAQ, NSE, BSE, LSE and all major global exchanges.
            <br><br>
            Indian stocks: add .NS (e.g. TCS.NS)<br>
            UK stocks: add .L (e.g. BP.L)
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Navbar ────────────────────────────────────────────────────
st.markdown("""
<div style='display:flex;align-items:center;justify-content:space-between;margin-bottom:28px;'>
    <div>
        <span style='font-size:26px;font-weight:800;color:#0f172a;letter-spacing:-0.5px;'>StockMind</span>
        <span style='font-size:26px;font-weight:800;color:#3b82f6;letter-spacing:-0.5px;'>AI</span>
        <div style='font-size:12px;color:#94a3b8;margin-top:2px;font-weight:500;'>
            Global Market Intelligence Platform
        </div>
    </div>
    <div style='display:flex;gap:8px;'>
        <span style='background:#f0fdf4;color:#15803d;font-size:11px;font-weight:700;
                     padding:6px 14px;border-radius:20px;border:1px solid #bbf7d0;'>
            Live Data
        </span>
        <span style='background:#eff6ff;color:#1d4ed8;font-size:11px;font-weight:700;
                     padding:6px 14px;border-radius:20px;border:1px solid #bfdbfe;'>
            AI Powered
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Search Box ────────────────────────────────────────────────
st.markdown("""
<div style='background:#ffffff;border:1.5px solid #e2e8f0;border-radius:20px;
            padding:24px 32px 16px;margin-bottom:16px;
            box-shadow:0 4px 20px rgba(0,0,0,0.04);'>
    <div style='font-size:15px;font-weight:700;color:#0f172a;margin-bottom:4px;'>
        Search any stock worldwide
    </div>
    <div style='font-size:12px;color:#94a3b8;'>
        NYSE · NASDAQ · NSE · BSE · LSE · TSX and more
    </div>
</div>
""", unsafe_allow_html=True)

search_col, btn_col = st.columns([5, 1], gap="small")
with search_col:
    top_search = st.text_input(
        "",
        value=st.session_state.get("current_symbol", "AAPL"),
        placeholder="Type ticker — AAPL, TCS.NS, RELIANCE.NS, TSLA, NVDA, BP.L...",
        label_visibility="collapsed",
        key="top_search_input"
    ).upper().strip()

with btn_col:
    st.markdown('<div class="search-btn">', unsafe_allow_html=True)
    search_btn = st.button("Search", use_container_width=True, key="main_search_btn")
    st.markdown('</div>', unsafe_allow_html=True)

# ── Quick Picks ───────────────────────────────────────────────
st.markdown("""
<div style='font-size:11px;color:#94a3b8;font-weight:600;
            text-transform:uppercase;letter-spacing:0.08em;
            margin:10px 0 8px;'>
    Quick pick
</div>
""", unsafe_allow_html=True)

popular_list = [
    "AAPL", "MSFT", "GOOGL", "TSLA",
    "NVDA", "AMZN", "META", "NFLX",
    "TCS.NS", "INFY.NS", "JPM", "V",
]

st.markdown('<div class="pop-btn">', unsafe_allow_html=True)
pop_cols = st.columns(len(popular_list), gap="small")
quick_pick = None
for i, tick in enumerate(popular_list):
    if pop_cols[i].button(tick, key=f"pop_{tick}"):
        quick_pick = tick
st.markdown('</div>', unsafe_allow_html=True)

# ── Resolve Symbol ────────────────────────────────────────────
if quick_pick:
    symbol = quick_pick
    st.session_state["current_symbol"] = symbol
    trigger = True
elif search_btn and top_search:
    symbol = top_search
    st.session_state["current_symbol"] = symbol
    trigger = True
elif sidebar_analyze:
    symbol = st.session_state.get("current_symbol", "AAPL")
    trigger = True
else:
    symbol = st.session_state.get("current_symbol", "AAPL")
    trigger = "data" not in st.session_state

st.markdown("<hr>", unsafe_allow_html=True)

# ── Fetch Data ────────────────────────────────────────────────
if trigger:
    with st.spinner(f"Analyzing {symbol}..."):
        data = APIClient.analyze_stock(symbol, period)
    st.session_state["data"] = data

data = st.session_state.get("data")

if not data:
    st.markdown("""
    <div style='text-align:center;padding:80px 40px;'>
        <div style='font-size:20px;font-weight:700;color:#0f172a;margin-bottom:8px;'>
            Search for any stock above
        </div>
        <div style='font-size:14px;color:#94a3b8;'>
            Enter a ticker symbol or click a quick pick
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

if "error" in data:
    st.markdown(f"""
    <div style='background:#fef2f2;border:1.5px solid #fecaca;border-radius:16px;
                padding:24px 28px;margin:20px 0;'>
        <div style='font-size:15px;font-weight:700;color:#dc2626;margin-bottom:8px;'>
            Could not find "{symbol}"
        </div>
        <div style='font-size:13px;color:#991b1b;line-height:1.7;'>
            Please check the symbol is correct.<br>
            For Indian stocks add .NS — e.g. TCS.NS, INFY.NS, RELIANCE.NS<br>
            For London stocks add .L — e.g. BP.L, HSBA.L
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Stock Header ──────────────────────────────────────────────
pct   = data['percentage_change']
delta = data['price_change']
is_up = delta >= 0
trend_color  = "#10b981" if is_up else "#ef4444"
trend_bg     = "#ecfdf5" if is_up else "#fef2f2"
trend_border = "#a7f3d0" if is_up else "#fecaca"
sign         = "+" if is_up else ""
sector       = data.get("sector", "")

st.markdown(f"""
<div style='background:#ffffff;border:1.5px solid #e2e8f0;border-radius:20px;
            padding:32px 40px;margin-bottom:28px;
            box-shadow:0 4px 20px rgba(0,0,0,0.05);'>
    <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
        <div>
            <div style='font-size:30px;font-weight:800;color:#0f172a;
                        letter-spacing:-0.5px;margin-bottom:10px;'>
                {data.get('company_name', symbol)}
            </div>
            <div style='display:flex;align-items:center;gap:10px;flex-wrap:wrap;'>
                <span style='font-size:13px;font-weight:700;color:#2563eb;
                             background:#eff6ff;padding:5px 12px;
                             border-radius:8px;border:1px solid #bfdbfe;'>
                    {symbol}
                </span>
                {'<span style="background:#f1f5f9;color:#475569;font-size:12px;padding:5px 12px;border-radius:8px;border:1px solid #e2e8f0;font-weight:600;">' + sector + '</span>' if sector and sector != 'N/A' else ''}
            </div>
        </div>
        <div style='text-align:right;'>
            <div style='font-size:44px;font-weight:800;color:#0f172a;
                        letter-spacing:-1.5px;line-height:1;margin-bottom:12px;'>
                ${data['current_price']:,.2f}
            </div>
            <div style='font-size:15px;font-weight:700;color:{trend_color};
                        background:{trend_bg};padding:8px 16px;
                        border-radius:10px;border:1.5px solid {trend_border};
                        display:inline-block;'>
                {sign}{delta:.2f} ({sign}{pct:.2f}%)
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Metrics ───────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5, gap="medium")
c1.metric("Market cap",  f"${data['market_cap']/1e9:.1f}B"      if data.get('market_cap', 0) > 0 else "N/A")
c2.metric("P/E ratio",   f"{data['pe_ratio']:.1f}"              if data.get('pe_ratio', 0) > 0 else "N/A")
c3.metric("52W high",    f"${data.get('52w_high', 0):.2f}"      if data.get('52w_high', 0) > 0 else "N/A")
c4.metric("52W low",     f"${data.get('52w_low', 0):.2f}"       if data.get('52w_low', 0) > 0 else "N/A")
c5.metric("Avg volume",  f"{data.get('avg_volume',0)/1e6:.1f}M" if data.get('avg_volume', 0) > 0 else "N/A")

st.markdown("<hr>", unsafe_allow_html=True)

# ── Chart ─────────────────────────────────────────────────────
st.markdown("""
<div style='font-size:16px;font-weight:700;color:#0f172a;
            margin-bottom:16px;letter-spacing:-0.3px;'>
    Price & Volume Analysis
</div>
""", unsafe_allow_html=True)

cd = data["chart_data"]
df = pd.DataFrame(cd)
df["dates"] = pd.to_datetime(df["dates"])
ma = data.get("moving_averages", {})
bb = data.get("bollinger", {})

fig = make_subplots(
    rows=3, cols=1, shared_xaxes=True,
    row_heights=[0.58, 0.22, 0.20],
    vertical_spacing=0.025,
)

fig.add_trace(go.Candlestick(
    x=df["dates"], open=df["opens"], high=df["highs"],
    low=df["lows"], close=df["closes"], name="Price",
    increasing_line_color="#10b981",
    decreasing_line_color="#ef4444",
    increasing_fillcolor="rgba(16,185,129,0.8)",
    decreasing_fillcolor="rgba(239,68,68,0.8)",
), row=1, col=1)

ma_colors = {"MA20":"#3b82f6","MA50":"#f59e0b","MA200":"#8b5cf6"}
for label in indicators:
    if label in ma and label in ma_colors:
        fig.add_trace(go.Scatter(
            x=df["dates"], y=ma[label], name=label,
            line=dict(color=ma_colors[label], width=2),
        ), row=1, col=1)

if "Bollinger Bands" in indicators and "bb_upper" in bb:
    fig.add_trace(go.Scatter(
        x=df["dates"], y=bb["bb_upper"], name="BB Upper",
        line=dict(color="rgba(59,130,246,0.4)", width=1.5, dash="dot"),
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=df["dates"], y=bb["bb_lower"], name="BB Lower",
        fill="tonexty", fillcolor="rgba(59,130,246,0.05)",
        line=dict(color="rgba(59,130,246,0.4)", width=1.5, dash="dot"),
    ), row=1, col=1)

vol_colors = ["#10b981" if c >= o else "#ef4444"
              for c, o in zip(df["closes"], df["opens"])]
fig.add_trace(go.Bar(
    x=df["dates"], y=df["volumes"],
    marker_color=vol_colors, name="Volume",
    showlegend=False, opacity=0.65,
), row=2, col=1)

rsi_vals = data.get("rsi", [])
fig.add_trace(go.Scatter(
    x=df["dates"], y=rsi_vals, name="RSI",
    line=dict(color="#3b82f6", width=2), showlegend=False,
), row=3, col=1)
fig.add_hrect(y0=70, y1=100, fillcolor="rgba(239,68,68,0.07)",
              line_width=0, row=3, col=1)
fig.add_hrect(y0=0, y1=30, fillcolor="rgba(16,185,129,0.07)",
              line_width=0, row=3, col=1)
fig.add_hline(y=70, line=dict(color="#ef4444", width=1, dash="dash"), row=3, col=1)
fig.add_hline(y=30, line=dict(color="#10b981", width=1, dash="dash"), row=3, col=1)

fig.update_layout(
    height=660,
    paper_bgcolor="#ffffff",
    plot_bgcolor="#ffffff",
    font=dict(color="#6b7280", size=11, family="Inter"),
    legend=dict(
        orientation="h", y=1.02, x=0,
        bgcolor="rgba(0,0,0,0)",
        font=dict(size=11),
    ),
    xaxis_rangeslider_visible=False,
    margin=dict(l=10, r=10, t=10, b=10),
    hovermode="x unified",
    hoverlabel=dict(
        bgcolor="#0f172a", bordercolor="#3b82f6",
        font_color="#f8fafc", font_size=12,
    ),
)
for i in range(1, 4):
    fig.update_xaxes(gridcolor="#f1f5f9", linecolor="#e2e8f0",
                     showgrid=True, zeroline=False, row=i, col=1)
    fig.update_yaxes(gridcolor="#f1f5f9", linecolor="#e2e8f0",
                     showgrid=True, zeroline=False, row=i, col=1)

fig.update_yaxes(title_text="Price",   title_font=dict(size=11), row=1, col=1)
fig.update_yaxes(title_text="Volume",  title_font=dict(size=11), row=2, col=1)
fig.update_yaxes(title_text="RSI 14",  title_font=dict(size=11), row=3, col=1)

st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

st.markdown("<hr>", unsafe_allow_html=True)

# ── AI Analysis ───────────────────────────────────────────────
analysis = data.get("analysis", {})
rec       = analysis.get("recommendation", "HOLD").upper()
risk      = analysis.get("risk", "Moderate")
rec_cfg   = {
    "BUY":  ("#10b981", "#f0fdf4", "#a7f3d0"),
    "SELL": ("#ef4444", "#fef2f2", "#fecaca"),
}.get(rec, ("#f59e0b", "#fffbeb", "#fde68a"))

st.markdown("""
<div style='font-size:20px;font-weight:800;color:#0f172a;
            letter-spacing:-0.5px;margin-bottom:24px;'>
    AI-Powered Analysis
</div>
""", unsafe_allow_html=True)

left_col, right_col = st.columns([1.8, 1.2], gap="large")

with left_col:
    news = data.get("news_summary", "")
    if news:
        st.markdown(f"""
        <div style='background:#f8fafc;border:1.5px solid #e2e8f0;
                    border-left:4px solid #3b82f6;border-radius:16px;
                    padding:24px 28px;margin-bottom:16px;'>
            <div style='font-size:11px;text-transform:uppercase;letter-spacing:0.12em;
                        color:#2563eb;font-weight:800;margin-bottom:10px;'>
                Market Overview
            </div>
            <div style='font-size:14px;color:#1f2937;line-height:1.8;'>{news}</div>
        </div>
        """, unsafe_allow_html=True)

with right_col:
    st.markdown(f"""
    <div style='display:flex;flex-direction:column;gap:12px;'>
        <div style='background:{rec_cfg[1]};border:2px solid {rec_cfg[2]};
                    border-radius:16px;padding:28px 24px;text-align:center;'>
            <div style='font-size:10px;text-transform:uppercase;letter-spacing:0.15em;
                        color:{rec_cfg[0]};font-weight:800;margin-bottom:10px;'>
                Recommendation
            </div>
            <div style='font-size:40px;font-weight:900;color:{rec_cfg[0]};
                        letter-spacing:-1px;'>{rec}</div>
        </div>
        <div style='background:#ffffff;border:1.5px solid #e2e8f0;
                    border-radius:16px;padding:20px;text-align:center;'>
            <div style='font-size:10px;text-transform:uppercase;letter-spacing:0.12em;
                        color:#94a3b8;font-weight:800;margin-bottom:6px;'>Risk Level</div>
            <div style='font-size:20px;font-weight:800;color:#0f172a;'>{risk}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)

# Analysis cards
analysis_items = [
    ("Technical Analysis", "technical_analysis"),
    ("Price Trend",        "trend"),
    ("Key Levels",         "support_resistance"),
]

cols = st.columns(3, gap="large")
for col, (label, key) in zip(cols, analysis_items):
    val = analysis.get(key, "")
    if not val or val == "N/A":
        val = "Insufficient data for this period."

    sentences = [s.strip() for s in val.replace(". ", ".|").split("|") if s.strip()]
    bullets_html = "".join(
        f"<div style='display:flex;gap:12px;margin-bottom:12px;align-items:flex-start;'>"
        f"<div style='min-width:7px;height:7px;border-radius:50%;background:#3b82f6;"
        f"flex-shrink:0;margin-top:6px;'></div>"
        f"<span style='color:#374151;font-size:13px;line-height:1.7;'>{s}</span>"
        f"</div>"
        for s in sentences[:4]
    )

    with col:
        st.markdown(f"""
        <div style='background:#ffffff;border:1.5px solid #e2e8f0;
                    border-radius:16px;padding:24px;height:100%;
                    box-shadow:0 2px 8px rgba(0,0,0,0.04);'>
            <div style='font-size:11px;font-weight:800;color:#0f172a;
                        text-transform:uppercase;letter-spacing:0.12em;
                        margin-bottom:16px;padding-bottom:12px;
                        border-bottom:2px solid #eff6ff;'>
                {label}
            </div>
            {bullets_html}
        </div>
        """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────
st.markdown(f"""
<div style='margin-top:48px;padding:20px 0;border-top:1.5px solid #e2e8f0;
            display:flex;justify-content:space-between;align-items:center;'>
    <span style='font-size:12px;font-weight:600;color:#94a3b8;'>
        StockMind AI · Global Market Intelligence
    </span>
    <span style='font-size:11px;color:#cbd5e1;'>
        {data.get('timestamp','')[:19].replace('T', ' ')} UTC
    </span>
</div>
""", unsafe_allow_html=True)