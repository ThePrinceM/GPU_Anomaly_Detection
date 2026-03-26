#telemetry background


import subprocess
import random
import time
from datetime import datetime, timezone
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
col = client["gpu_telemetry"]["gpu_metrics"]

def collect():
    try:
        r = subprocess.run(
            ["nvidia-smi",
             "--query-gpu=index,utilization.gpu,temperature.gpu,memory.used",
             "--format=csv,noheader,nounits"],
            capture_output=True,
            text=True
        )

        lines = r.stdout.strip().split("\n")
        records = []

        for l in lines:
            p = l.split(",")
            records.append({
                "gpu_index": int(p[0]),
                "utilization": float(p[1]),
                "temperature": float(p[2]),
                "memory": float(p[3]),
                "timestamp": datetime.now(timezone.utc)
            })

        return records

    except:
        return [{
            "gpu_index": random.randint(0,1),
            "utilization": random.randint(10,95),
            "temperature": random.randint(40,90),
            "memory": random.randint(500,8000),
            "timestamp": datetime.now(timezone.utc)
        }]

while True:
    data = collect()
    col.insert_many(data)
    print("Inserted", len(data))
    time.sleep(2)