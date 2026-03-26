from pymongo import MongoClient
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

client = MongoClient("mongodb://localhost:27017/")
col = client["gpu_telemetry"]["gpu_metrics"]


def detect_anomalies():

    data = list(col.find().sort("timestamp",-1).limit(300))

    if len(data) < 50:
        return []

    df = pd.DataFrame(data)

    anomalies = []

    # ---------- Z-SCORE METHOD ----------
    for metric in ["utilization", "temperature", "memory"]:

        mean = df[metric].mean()
        std = df[metric].std()

        if std == 0:
            continue

        df["z_score"] = (df[metric] - mean) / std

        outliers = df[np.abs(df["z_score"]) > 2]

        for _, row in outliers.iterrows():

            severity = "medium"
            if abs(row["z_score"]) > 3:
                severity = "high"

            anomalies.append({
                "gpu_index": int(row["gpu_index"]),
                "metric": metric,
                "value": float(row[metric]),
                "z_score": round(float(row["z_score"]),2),
                "method": "z-score",
                "severity": severity
            })

    # ---------- ISOLATION FOREST ----------
    model = IsolationForest(contamination=0.05)

    df["iso"] = model.fit_predict(
        df[["utilization","temperature","memory"]]
    )

    iso_outliers = df[df["iso"] == -1]

    for _, row in iso_outliers.iterrows():

        anomalies.append({
            "gpu_index": int(row["gpu_index"]),
            "metric": "multi",
            "value": float(row["utilization"]),
            "z_score": None,
            "method": "isolation_forest",
            "severity": "high"
        })

    return anomalies