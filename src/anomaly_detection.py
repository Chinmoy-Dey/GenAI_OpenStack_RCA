import torch
from typing import List
# from src.model import load_model
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.model import load_model

def predict_log(logs: str) -> int:
    model, tokenizer = load_model()
    return detect_anomalies(model, tokenizer, logs)

def predict_logs(logs: List[str]) -> List[int]:
    return [predict_log(log) for log in logs]

# def detect_anomalies(model, tokenizer, logs):
#     inputs = tokenizer(logs, return_tensors="pt", truncation=True, padding="max_length", max_length=512)
#     # Remove 'token_type_ids' if it's not needed by your model
#     if 'token_type_ids' in inputs: 
#         del inputs['token_type_ids']  
#     outputs = model(**inputs)
#     # print("detect_anomalies output {}".format(outputs))
#     # Assume threshold-based classification
#     hidden_states = outputs.hidden_states
#     # print("detect_anomalies hidden_states {}".format(hidden_states))
#     last_hidden_state = hidden_states[-1]
#     anomaly_score = torch.mean(last_hidden_state).item()
#     print("detect_anomalies anomaly_score {} "
#           "last_hidden_state {}".format( anomaly_score, last_hidden_state))
#     return 1 if anomaly_score > 0.5 else 0

def detect_anomalies(model, tokenizer, logs):
    # Tokenize the input logs
    inputs = tokenizer(logs, return_tensors="pt", truncation=True, padding="max_length", max_length=512)
    
    # Remove 'token_type_ids' if present, as BERT models often don't use it
    if 'token_type_ids' in inputs: 
        del inputs['token_type_ids']
    
    # Get the model's output (anomaly score)
    anomaly_score = model(**inputs)  # This directly returns the score as a tensor
    
    # Convert the score to a probability and threshold it
    anomaly_probability = anomaly_score.item()  # Extract the scalar value
    print(f"detect_anomalies anomaly_probability: {anomaly_probability}") 
    
    # Return 1 if the anomaly probability exceeds 0.5, else return 0
    return 1 if anomaly_probability > 0.1 else 0


def detect_anomalies1(model, tokenizer, logs):
    inputs = tokenizer(
        logs, padding=True, truncation=True, return_tensors="pt", max_length=128
    )
    outputs = model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=-1)
    print(predictions)
    return predictions