def analyze_root_cause(logs, anomalies):
    return {log: "Potential Issue" for log, anomaly in zip(logs, anomalies) if anomaly == 1}
