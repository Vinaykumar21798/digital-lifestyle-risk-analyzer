from llm_report import generate_health_report
import streamlit as st
from datetime import date
from database import create_table, insert_data, fetch_data, generate_dummy_data
import pandas as pd
import numpy as np


st.set_page_config(
    page_title="Digital Lifestyle Risk Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.main {
    background-color: #0E1117;
}
.block-container {
    padding-top: 2rem;
}
.metric-card {
    background-color: #1C1F26;
    padding: 20px;
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)


create_table()

st.sidebar.title("Digital Behavior Input")

sleep = st.sidebar.number_input("Sleep Hours", 0.0, 24.0, step=0.5)
water = st.sidebar.number_input("Water Intake (L)", 0.0, 10.0, step=0.1)
exercise = st.sidebar.number_input("Exercise Minutes", 0, 300)
mood = st.sidebar.slider("Mood (1-5)", 1, 5)
steps = st.sidebar.number_input("Steps", 0, 50000)
screen = st.sidebar.number_input("Screen Time (hrs)", 0.0, 24.0, step=0.5)

if st.sidebar.button("Save Data"):
    insert_data(str(date.today()), sleep, water, exercise, mood, steps, screen)
    st.sidebar.success("Data Saved")

if st.sidebar.button("Generate Dummy Data"):
    generate_dummy_data()
    st.sidebar.success("Dummy Data Added")
df = fetch_data()

menu = st.sidebar.radio(
    "Navigation",
    ["📊 Dashboard", "⚠ Digital Risk Engine", "📈 Analytics", "🤖 AI Behavioral Coach"]
)

if not df.empty:

    df["date"] = pd.to_datetime(df["date"])
    latest = df.iloc[-1]

    sleep_variance = df["sleep_hours"].rolling(7).std().iloc[-1] or 0
    mood_variance = df["mood_score"].rolling(7).std().iloc[-1] or 0

    digital_load = (
        min(latest["screen_time"] / 10, 1) * 40 +
        min(sleep_variance / 2, 1) * 20 +
        min(mood_variance / 1.5, 1) * 20 +
        (1 - min(latest["sleep_hours"] / 8, 1)) * 20
    )

    digital_load = round(digital_load, 2)

    x = np.arange(len(df))
    sleep_slope = np.polyfit(x, df["sleep_hours"], 1)[0]
    screen_slope = np.polyfit(x, df["screen_time"], 1)[0]

    behavioral_drift = sleep_slope < 0 and screen_slope > 0



    correlation = df["screen_time"].corr(df["mood_score"])
    mood_impact_risk = correlation is not None and correlation < -0.5

   

    if digital_load < 30:
        risk_level = "Low"
    elif digital_load < 60:
        risk_level = "Moderate"
    elif digital_load < 80:
        risk_level = "High"
    else:
        risk_level = "Critical"

    
    if menu == "📊 Dashboard":

        st.title("Digital Lifestyle Intelligence Dashboard")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Sleep (hrs)", latest["sleep_hours"])
        col2.metric("Screen Time (hrs)", latest["screen_time"])
        col3.metric("Mood", latest["mood_score"])
        col4.metric("Steps", latest["steps"])

        st.markdown("### Digital Load Index")
        st.progress(int(digital_load))
        st.metric("DLI (0-100)", digital_load)

    

    elif menu == "⚠ Digital Risk Engine":

        st.title("Digital Risk Engine")

        st.metric("Digital Load Index", digital_load)
        st.progress(int(digital_load))

        if risk_level == "Low":
            st.success("Risk Level: LOW")
        elif risk_level == "Moderate":
            st.warning("Risk Level: MODERATE")
        elif risk_level == "High":
            st.error("Risk Level: HIGH")
        else:
            st.error("Risk Level: CRITICAL")

        st.markdown("---")

        st.subheader("Behavioral Drift Analysis")
        st.write("Drift Detected" if behavioral_drift else "Stable Pattern")

        st.subheader("Mood Impact Correlation")
        st.write(f"Correlation: {round(correlation,2) if correlation else 'Insufficient Data'}")

        if mood_impact_risk:
            st.warning("High Screen Exposure Correlates with Mood Decline")

    # ==========================================================
    # 📈 ANALYTICS
    # ==========================================================

    elif menu == "📈 Analytics":

        st.title("Behavioral Trend Analytics")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Sleep Trend")
            st.line_chart(df.set_index("date")["sleep_hours"])

        with col2:
            st.subheader("Screen Time Trend")
            st.line_chart(df.set_index("date")["screen_time"])

        col3, col4 = st.columns(2)

        with col3:
            st.subheader("Mood Trend")
            st.line_chart(df.set_index("date")["mood_score"])

        with col4:
            st.subheader("Water Intake")
            st.line_chart(df.set_index("date")["water_liters"])

    # ==========================================================
    # 🤖 AI BEHAVIORAL COACH
    # ==========================================================

    elif menu == "🤖 AI Behavioral Coach":

        st.title("AI Digital Lifestyle Coach")

        health_data_summary = {
            "Digital_Load_Index": digital_load,
            "Risk_Level": risk_level,
            "Behavioral_Drift": behavioral_drift,
            "Mood_Screen_Correlation": correlation,
            "Latest_Screen_Time": latest["screen_time"],
            "Latest_Sleep": latest["sleep_hours"],
            "Latest_Mood": latest["mood_score"]
        }

        if st.button("Generate AI Behavioral Analysis"):
            with st.spinner("Analyzing digital behavior patterns..."):
                report = generate_health_report(health_data_summary)
            st.markdown(report)

else:
    st.warning("No data available. Please add entries from sidebar.")