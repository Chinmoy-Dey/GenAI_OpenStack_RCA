import torch
from typing import List
from src.model import load_model

def predict_log(logs: str) -> int:
    model, tokenizer = load_model()
    return detect_anomalies(model, tokenizer, logs)

def predict_logs(logs: List[str]) -> List[int]:
    return [predict_log(log) for log in logs]

def detect_anomalies(model, tokenizer, logs):
    inputs = tokenizer(logs, return_tensors="pt", truncation=True, padding="max_length", max_length=512)
    outputs = model(**inputs, output_hidden_states=True)
    # print("detect_anomalies output {}".format(outputs))
    # Assume threshold-based classification
    hidden_states = outputs.hidden_states
    # print("detect_anomalies hidden_states {}".format(hidden_states))
    last_hidden_state = hidden_states[-1]
    anomaly_score = torch.mean(last_hidden_state).item()
    print("detect_anomalies anomaly_score {} "
          "last_hidden_state {}".format( anomaly_score, last_hidden_state))
    return 1 if anomaly_score > 0.5 else 0

def detect_anomalies1(model, tokenizer, logs):
    inputs = tokenizer(
        logs, padding=True, truncation=True, return_tensors="pt", max_length=128
    )
    outputs = model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=-1)
    print(predictions)
    return predictions
