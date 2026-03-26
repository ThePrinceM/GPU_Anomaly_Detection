# Usage prediction

from pymongo import MongoClient
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

client = MongoClient("mongodb://localhost:27017/")
col = client["gpu_telemetry"]["gpu_metrics"]

def predict():

    data = list(col.find().sort("timestamp",-1).limit(200))

    if len(data) < 30:
        return None

    df = pd.DataFrame(data).sort_values("timestamp")

    df["t"] = range(len(df))

    X = df[["t"]]
    y = df["utilization"]

    model = LinearRegression()
    model.fit(X,y)

    future = np.array([[len(df)+15]])

    return round(float(model.predict(future)[0]),2)