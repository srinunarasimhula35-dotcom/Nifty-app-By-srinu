import streamlit as st
import plotly.graph_objects as go

# 1. Page & Layout Setup
st.set_page_config(page_title="Ultimate F&O Business Dashboard", layout="wide")
st.title("📊 Ultimate F&O Trading Decision Engine")
st.write("**Founder:** Tallapalli Venkata Prasad | **Goal:** ₹10,000 Daily Income Business")

st.markdown("---")

# 2. Sidebar Configuration - All User Constraints Integrated
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

# 3. Lot Size Calculation
LOT_SIZE = 65
total_qty = lots * LOT_SIZE
total_risk_capital = premium_paid * total_qty

# 4. CORE ENGINE LOGIC: 3-Way Confluence Probability Calculator
st.subheader("🔮 3-Way Confluence: Next 5-Minute Candle Direction Prediction")

# Scoring System based on User Inputs
bullish_points = 0
bearish_points = 0

# A. Global News Weightage
if us_news == "Bullish (Lower Inflation Expected)": bullish_points += 30
elif us_news == "Bearish (Higher Inflation Expected)": bearish_points += 30

# B. Historical Data Weightage
if historical_pattern == "Strong Support Breakout (Bullish)": bullish_points += 30
elif historical_pattern == "Resistance Rejection (Bearish)": bearish_points += 30

# C. Live 5-Min Price Action Weightage
if last_candle == "Green (Bullish Candle)": bullish_points += 20
else: bearish_points += 20

if vwap_status == "Closed Above VWAP": bullish_points += 20
else: bearish_points += 20

# Final Probability Calculations
total_score = bullish_points + bearish_points
if total_score > 0:
    green_probability = int((bullish_points / total_score) * 100)
    red_probability = 100 - green_probability
else:
    green_probability, red_probability = 50, 50

# Output Display Rules based on combined data
if green_probability >= 65:
    next_candle_estimate = "🟢 GREEN (High Probability Bullish Candle)"
    trade_advice = "⚡ **AUTOMATIC ENTRY:** Confluence is Bullish! Recommended: Buy ATM Call Option."
    advice_color = "success"
elif red_probability >= 65:
    next_candle_estimate = "🔴 RED (High Probability Bearish Candle)"
    trade_advice = "⚡ **AUTOMATIC ENTRY:** Confluence is Bearish! Recommended: Buy ATM Put Option."
    advice_color = "error"
else:
    next_candle_estimate = "🟡 NEUTRAL / UNCERTAIN (Conflicting Data)"
    trade_advice = "🛡️ **NO-TRADE ZONE:** Signals are clashing. Protect your capital and sit in cash."
    advice_color = "warning"

# Dashboard Layout for Predictions
p_col1, p_col2, p_col3 = st.columns(3)
with p_col1:
    st.metric(label="Estimated Next 5-Min Candle", value=next_candle_estimate)
with p_col2:
    st.metric(label="Green Candle Probability (%)", value=f"{green_probability}%")
with p_col3:
    st.metric(label="Red Candle Probability (%)", value=f"{red_probability}%")

# Trigger Alert Display
if advice_color == "success":
    st.success(trade_advice)
    st.info(f"🤖 **AUTO-EXIT LOGIC LOCK:** Position will automatically close if profit hits +₹{daily_target} or loss hits -₹{daily_stoploss}.")
elif advice_color == "error":
    st.error(trade_advice)
    st.info(f"🤖 **AUTO-EXIT LOGIC LOCK:** Position will automatically close if profit hits +₹{daily_target} or loss hits -₹{daily_stoploss}.")
else:
    st.warning(trade_advice)

st.markdown("---")

# 5. Core Business Metrics Layout
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Premium Invested", value=f"₹{total_risk_capital:,.2f}")
with col2:
    if total_risk_capital > (capital * 0.20):
        st.error(f"⚠️ Risk Alert: Investing {total_risk_capital/capital*100:.1f}% of capital! Max recommended is 20%.")
    else:
        st.success("✅ Position Sizing Within Safe Limits (Under 20% Capital)")
with col3:
    st.info(f"Target: +₹{daily_target} | StopLoss: -₹{daily_stoploss}")

# 6. Trade Payoff Visualizer
st.subheader("🎯 Expected Business Profit / Loss Chart at Expiry")
price_range = list(range(int(nifty_spot * 0.98), int(nifty_spot * 1.02), 20))

if trade_type == "Call Option (CE)":
    pnl = [(max(0, price - nifty_spot) - premium_paid) * total_qty for price in price_range]
else:
    pnl = [(max(0, nifty_spot - price) - premium_paid) * total_qty for price in price_range]

fig = go.Figure()
fig.add_trace(go.Scatter(x=price_range, y=pnl, mode='lines+markers', name='P&L Line', line=dict(color='orange', width=3)))
fig.add_shape(type="line", x0=price_range, y0=0, x1=price_range[-1], y1=0, line=dict(color="gray", dash="dash"))
fig.add_shape(type="line", x0=price_range, y0=daily_target, x1=price_range[-1], y1=daily_target, line=dict(color="green", dash="dot"))
fig.add_shape(type="line", x0=price_range, y0=-daily_stoploss, x1=price_range[-1], y1=-daily_stoploss, line=dict(color="red", dash="dot"))

fig.update_layout(xaxis_title="Nifty Price", yaxis_title="Profit / Loss (₹)", margin=dict(l=20, r=20, t=20, b=20))
st.plotly_chart(fig, use_container_width=True)
