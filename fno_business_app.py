import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ultimate F&O Business Dashboard", layout="wide")
st.title("📊 Ultimate F&O Trading Decision Engine")
st.write("**Founder:** Tallapalli Venkata Prasad | **Goal:** ₹10,000 Daily Income Business")

st.markdown("---")

st.sidebar.header("🛠️ Risk Management Settings")
capital = st.sidebar.number_input("Trading Capital (₹)", value=250000, step=10000)
daily_target = st.sidebar.number_input("Daily Profit Target (₹)", value=10000)
daily_stoploss = st.sidebar.number_input("Max Daily Loss Limit (₹)", value=5000)

st.sidebar.header("🌍 Global Event Catalyst")
us_news = st.sidebar.selectbox("US Inflation / Global News Sentiment", ["Bullish (Lower Inflation Expected)", "Neutral / Sideways", "Bearish (Higher Inflation Expected)"])

st.sidebar.header("📂 1-Year Historical Chart Pattern Match")
historical_pattern = st.sidebar.selectbox("Past 1-Year Similar Chart Model", ["Strong Support Breakout (Bullish)", "No Match / Sideways Pattern", "Resistance Rejection (Bearish)"])

st.sidebar.header("⏱️ Live 5-Min Price Action Data")
last_candle = st.sidebar.selectbox("Previous 5-Min Candle Type", ["Green (Bullish Candle)", "Red (Bearish Candle)"])
vwap_status = st.sidebar.selectbox("Previous Candle Close vs VWAP", ["Closed Above VWAP", "Closed Below VWAP"])

st.sidebar.header("📈 Active Trade Settings")
nifty_spot = st.sidebar.number_input("Nifty Current Price", value=24950)
trade_type = st.sidebar.selectbox("Trade Type", ["Call Option (CE)", "Put Option (PE)"])
premium_paid = st.sidebar.number_input("Option Premium Price (₹)", value=150)
lots = st.sidebar.number_input("Number of Lots (1 Lot = 65 Qty)", value=5, step=1)

LOT_SIZE = 65
total_qty = lots * LOT_SIZE
total_risk_capital = premium_paid * total_qty

bullish_points = 0
bearish_points = 0

if us_news == "Bullish (Lower Inflation Expected)": bullish_points += 30
elif us_news == "Bearish (Higher Inflation Expected)": bearish_points += 30

if historical_pattern == "Strong Support Breakout (Bullish)": bullish_points += 30
elif historical_pattern == "Resistance Rejection (Bearish)": bearish_points += 30

if last_candle == "Green (Bullish Candle)": bullish_points += 20
else: bearish_points += 20

if vwap_status == "Closed Above VWAP": bullish_points += 20
else: bearish_points += 20

total_score = bullish_points + bearish_points
green_probability = int((bullish_points / total_score) * 100) if total_score > 0 else 50
red_probability = 100 - green_probability

if green_probability >= 65:
    next_candle_estimate = "🟢 GREEN (High Probability Bullish)"
    trade_advice = "⚡ AUTOMATIC ENTRY: Recommended: Buy ATM Call Option."
    advice_color = "success"
elif red_probability >= 65:
    next_candle_estimate = "🔴 RED (High Probability Bearish)"
    trade_advice = "⚡ AUTOMATIC ENTRY: Recommended: Buy ATM Put Option."
    advice_color = "error"
else:
    next_candle_estimate = "🟡 NEUTRAL / UNCERTAIN"
    trade_advice = "🛡️ NO-TRADE ZONE: Signals are clashing. Protect your capital."
    advice_color = "warning"

p_col1, p_col2, p_col3 = st.columns(3)
with p_col1: st.metric(label="Estimated Next 5-Min Candle", value=next_candle_estimate)
with p_col2: st.metric(label="Green Candle Probability (%)", value=f"{green_probability}%")
with p_col3: st.metric(label="Red Candle Probability (%)", value=f"{red_probability}%")

if advice_color == "success": st.success(trade_advice)
elif advice_color == "error": st.error(trade_advice)
else: st.warning(trade_advice)

st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1: st.metric(label="Total Premium Invested", value=f"₹{total_risk_capital:,.2f}")
with col2:
    if total_risk_capital > (capital * 0.20): st.error(f"⚠️ Risk Alert: Investing too much capital!")
    else: st.success("✅ Position Sizing Within Safe Limits")
with col3: st.info(f"Target: +₹{daily_target} | StopLoss: -₹{daily_stoploss}")

st.subheader("🎯 Expected Business Profit / Loss Simulation Chart")
price_range = list(range(int(nifty_spot * 0.98), int(nifty_spot * 1.02), 20))

if trade_type == "Call Option (CE)":
    pnl = [(max(0, price - nifty_spot) - premium_paid) * total_qty for price in price_range]
else:
    pnl = [(max(0, nifty_spot - price) - premium_paid) * total_qty for price in price_range]

chart_data = pd.DataFrame({"Nifty Price": price_range, "Profit / Loss (₹)": pnl})
chart_data.set_index("Nifty Price", inplace=True)
st.line_chart(chart_data)
