import torch
from src.model import load_model

def predict_log(logs: str) -> int:
    model, tokenizer = load_model()
    return detect_anomalies(model, tokenizer, logs)

def detect_anomalies(model, tokenizer, logs):
    inputs = tokenizer(
        logs, padding=True, truncation=True, return_tensors="pt", max_length=128
    )
    outputs = model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=-1)
    print(predictions)
    return predictions
