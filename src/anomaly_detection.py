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
    
# Get the model's output
    anomaly_score = model(**inputs)  # This should now return a proper tensor
    print(f"Model output (anomaly_score): {anomaly_score}")

    # Ensure the model output is a tensor of the correct shape
    if anomaly_score.dim() != 2 or anomaly_score.shape[1] != 1:
        raise ValueError("Model output must be a tensor with shape (batch_size, 1).")

    # Convert to probabilities
    anomaly_probability = anomaly_score.squeeze(1).tolist()  # Convert to a list of probabilities
    print(f"Anomaly probabilities: {anomaly_probability}")

    # Return binary classification based on threshold
    return [1 if prob > 0.1 else 0 for prob in anomaly_probability]

def detect_anomalies1(model, tokenizer, logs):
    inputs = tokenizer(
        logs, padding=True, truncation=True, return_tensors="pt", max_length=128
    )
    outputs = model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=-1)
    print(predictions)
    return predictions
