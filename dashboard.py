import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from pymongo import MongoClient
from streamlit_autorefresh import st_autorefresh

from login import login
from ml_model import predict
from anomaly import detect_anomalies
from alerts import telegram_alert


# ---------------- LOGIN ----------------
login()

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="GPU Monitoring Console",
    layout="wide"
)

st_autorefresh(interval=3000, key="refresh")

# ---------------- ENTERPRISE THEME ----------------
st.markdown("""
<style>
html, body { background-color:#0f172a; color:#e5e7eb; }

.metric-card{
background:#111827;
padding:18px;
border-radius:10px;
border:1px solid #1f2937;
text-align:center;
}

.gpu-card{
background:#111827;
padding:15px;
border-radius:10px;
border:1px solid #1f2937;
margin-bottom:12px;
}

.section{
background:#111827;
padding:20px;
border-radius:10px;
border:1px solid #1f2937;
margin-top:15px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🖥 GPU Console")

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "GPU Analytics",
        "Alerts",
        "System Health"
    ]
)

# ---------------- DB ----------------
client = MongoClient("mongodb://localhost:27017/")
col = client["gpu_telemetry"]["gpu_metrics"]

data = list(col.find().sort("timestamp",-1).limit(400))

if not data:
    st.warning("No telemetry data. Start collector.")
    st.stop()

df = pd.DataFrame(data).sort_values("timestamp")

# ---------------- COMMON METRICS ----------------
avg_util = df["utilization"].mean()
max_temp = df["temperature"].max()
avg_mem = df["memory"].mean()

health = 100 - (
    0.5*avg_util +
    0.3*(max_temp-40) +
    0.2*(avg_mem/100)
)

pred = predict()
anomalies = detect_anomalies()

last_time = df["timestamp"].max()
delay = (datetime.utcnow() - last_time).seconds

# ---------------- OVERVIEW PAGE ----------------
if page == "Overview":

    st.title("GPU System Overview")

    c1,c2,c3,c4 = st.columns(4)

    c1.markdown(f'<div class="metric-card"><h3>Avg Util</h3><h1>{round(avg_util,2)}%</h1></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card"><h3>Max Temp</h3><h1>{round(max_temp,2)}°C</h1></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card"><h3>Health Score</h3><h1>{round(health,2)}</h1></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="metric-card"><h3>Predicted Load</h3><h1>{pred}</h1></div>', unsafe_allow_html=True)

    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.subheader("GPU Cards")

    for gpu, gdf in df.groupby("gpu_index"):

        util = gdf["utilization"].mean()
        temp = gdf["temperature"].max()
        mem = gdf["memory"].mean()

        st.markdown(f"""
        <div class="gpu-card">
        <b>GPU {gpu}</b><br>
        Utilization: {round(util,2)} % <br>
        Temperature: {round(temp,2)} °C <br>
        Memory: {round(mem,2)} MB
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- ANALYTICS PAGE ----------------
elif page == "GPU Analytics":

    st.title("Performance Analytics")

    cutoff = datetime.utcnow() - timedelta(minutes=5)
    recent = df[df["timestamp"] >= cutoff]

    r1,r2 = st.columns(2)

    r1.metric("Rolling Util", round(recent["utilization"].mean(),2))
    r2.metric("Rolling Max Temp", round(recent["temperature"].max(),2))

    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.subheader("Utilization Trend")
    st.line_chart(df.set_index("timestamp")["utilization"])
    st.subheader("Temperature Trend")
    st.line_chart(df.set_index("timestamp")["temperature"])
    st.subheader("Memory Trend")
    st.line_chart(df.set_index("timestamp")["memory"])
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- ALERT PAGE ----------------
elif page == "Alerts":

    st.title("🚨 Alert Center")

# ---------- NO ANOMALY ----------
    if len(anomalies) == 0:
        st.success("No anomalies detected")

# ---------- ANOMALY PRESENT ----------
    else:

        critical_anomalies = []

        for a in anomalies:

            msg = f"""
🔴 GPU {a['gpu_index']} | {a['metric']} anomaly
Value: {a['value']}
Method: {a['method']}
Severity: {a['severity']}
"""

        # ---------- UI DISPLAY ----------
        if a["severity"] == "high":
            st.error(msg)
            critical_anomalies.append(a)
        else:
            st.warning(msg)

    # ---------- TELEGRAM ALERT ----------
    import time

    if "last_alert" not in st.session_state:
        st.session_state.last_alert = 0

    # send only if HIGH severity exists
    if len(critical_anomalies) > 0:

        if time.time() - st.session_state.last_alert > 300:

            # ---------- BUILD DETAILED MESSAGE ----------
            alert_msg = "🔥 GPU CRITICAL ALERT\n\n"

            for a in critical_anomalies:
                alert_msg += (
                    f"GPU {a['gpu_index']} | {a['metric']} → {a['value']}\n"
                )

            # ---------- SEND TELEGRAM ----------
            telegram_alert(alert_msg)

            st.session_state.last_alert = time.time()

# ---------------- SYSTEM HEALTH PAGE ----------------
elif page == "System Health":

    st.title("System Diagnostics")

    ranking = df.groupby("gpu_index")["utilization"].mean().sort_values()

    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.subheader("GPU Load Ranking")
    st.bar_chart(ranking)
    st.markdown('</div>', unsafe_allow_html=True)

    df["minute"] = pd.to_datetime(df["timestamp"]).dt.minute
    heat = df.pivot_table(
        values="utilization",
        index="gpu_index",
        columns="minute"
    )

    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.subheader("Utilization Heatmap")
    st.dataframe(heat)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Export CSV Report", key="report_btn"):
        df.to_csv("gpu_report.csv")
        st.success("Report Exported")