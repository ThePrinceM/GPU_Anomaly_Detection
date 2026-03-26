# 🚀 GPU Monitoring & Analytics System

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![MongoDB](https://img.shields.io/badge/MongoDB-Database-green)
![ML](https://img.shields.io/badge/MachineLearning-Enabled-orange)
![Status](https://img.shields.io/badge/Status-Active-success)

A real-time **GPU monitoring dashboard** built using **Streamlit, MongoDB, and Machine Learning**.  
This system collects GPU telemetry, performs analytics, detects anomalies, and sends intelligent alerts.

---

## 📌 Features

### 🔥 Core Monitoring
- Real-time GPU telemetry collection (utilization, temperature, memory)
- Multi-GPU performance tracking
- Live Streamlit dashboard

### 📊 Analytics
- Rolling window analytics (5-minute stats)
- GPU performance trends
- GPU load ranking
- Heatmap visualization

### 🤖 Machine Learning
- GPU usage prediction (Linear Regression)
- Hybrid anomaly detection:
  - Z-score (statistical)
  - Isolation Forest (ML-based)

### 🚨 Alerts System
- Telegram alerts for critical anomalies
- Alert throttling (prevents spam)
- Severity-based alert classification

### 🧠 Intelligence Layer
- GPU Health Score (custom KPI)
- Trend detection (increasing/decreasing load)
- Collector failure detection

### 📁 Reporting
- CSV report export
- Historical data analysis

### 🎨 UI/UX
- Enterprise-level dashboard layout
- Sidebar navigation (Overview, Analytics, Alerts, System Health)
- Professional dark theme

---

## 🏗️ Project Architecture

```
collector.py        → collects GPU data
        ↓
MongoDB             → stores telemetry
        ↓
ml_model.py         → prediction
anomaly.py          → anomaly detection
alerts.py           → alert system
        ↓
dashboard.py        → visualization (Streamlit)
```

---

## ⚙️ Tech Stack

- Python  
- Streamlit  
- MongoDB  
- Scikit-learn  
- Pandas / NumPy  
- Telegram Bot API  

---

## ▶️ How to Run

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 2️⃣ Start MongoDB

```bash
net start MongoDB
```

---

### 3️⃣ Run collector

```bash
python collector.py
```

---

### 4️⃣ Run dashboard

```bash
python -m streamlit run dashboard.py
```

Open in browser:

```
http://localhost:8501
```

---

## 🔐 Login Credentials

```
Username: admin  
Password: gpu123
```

---

## 🔑 secrets.toml (Required)

Create file:

```
.streamlit/secrets.toml
```

Add:

```toml
USER="admin"
PASS="gpu123"

BOT_TOKEN="your_telegram_bot_token"
CHAT_ID="your_chat_id"
```

---

## 📊 Example Use Cases

### ⭐ Real-time Monitoring
The system continuously collects GPU data and displays it live.

---

### ⭐ Anomaly Detection

```
GPU 0 | temperature anomaly  
Value: 92°C  
Severity: HIGH
```

---

### ⭐ Telegram Alert Example

```
🔥 GPU CRITICAL ALERT

GPU 1 | utilization → 98  
GPU 0 | temperature → 91  
```

---

### ⭐ Predictive Analytics

```
Predicted GPU Load: 87%
```

---

### ⭐ GPU Health Score

```
Health Score = 78 (Good condition)
```

---

### ⭐ System Reliability Check

```
⚠️ Collector not sending data
```

---

## 🚨 Alert Conditions

Alerts are triggered when:

- Temperature > 85°C  
- High severity anomaly detected  

✔ Includes cooldown (5 minutes)  
✔ Prevents alert spam  

---

## 📁 Folder Structure

```
gpu-monitor/

│── collector.py
│── dashboard.py
│── login.py
│── ml_model.py
│── anomaly.py
│── alerts.py
│── requirements.txt
│── README.md
│── .streamlit/
      └── secrets.toml
```

---

## 🎯 Key Highlights

- Real-time GPU monitoring system  
- Hybrid anomaly detection (Z-score + Isolation Forest)  
- ML-based prediction model  
- Telegram alert integration  
- MongoDB time-series storage  
- Enterprise dashboard UI  
- Modular system design  

---

## 📌 Future Improvements

- Email alerts  
- Docker deployment  
- Cloud deployment (MongoDB Atlas + Streamlit Cloud)  
- Deep learning forecasting  
- WebSocket streaming  

---

## ⭐ Conclusion

This project demonstrates a **complete end-to-end monitoring system** combining:

- Data Engineering  
- Machine Learning  
- System Design  
- Real-time Visualization  

👉 It simulates a real-world GPU monitoring platform used in AI and cloud infrastructure.

---

## 🙌 Author

Developed by *Prince Maurya*
