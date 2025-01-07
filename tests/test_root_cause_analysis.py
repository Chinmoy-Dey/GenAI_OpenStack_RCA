import torch
from unittest.mock import MagicMock, patch
from src.root_cause_analysis import generate_root_cause,analyze_root_cause
from typing import List, Dict  # Add this import to fix the issue
from transformers import GPT2LMHeadModel, GPT2Tokenizer

MODEL_NAME = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(MODEL_NAME)
tokenizer.pad_token = tokenizer.eos_token  # Set the padding token
model = GPT2LMHeadModel.from_pretrained(MODEL_NAME)

def test_analyze_root_cause():
    logs = [
        "Error: Connection failed at 10:23",
        "Timeout while waiting for response",
        "System running smoothly",
        "Error: Disk space exceeded",
        "Unexpected behavior detected"
    ]
    anomalies = [1, 1, 0, 1, 0]
    
    expected_output = {
        0: "Error detected in log",
        1: "Potential timeout issue",
        3: "Error detected in log"
    }
    
    result = analyze_root_cause(logs, anomalies)
    assert result == expected_output, f"Expected {expected_output}, but got {result}"

def test_analyze_root_cause_no_anomalies():
    logs = [
        "All systems operational",
        "Service response time within limits",
        "System running smoothly"
    ]
    anomalies = [0, 0, 0]
    
    expected_output = {}
    
    result = analyze_root_cause(logs, anomalies)
    assert result == expected_output, f"Expected {expected_output}, but got {result}"

def test_analyze_root_cause_mixed_case():
    logs = [
        "ERROR: Unexpected crash occurred",
        "Timeout while processing request",
        "Warning: High memory usage",
        "Error: System overheated"
    ]
    anomalies = [1, 1, 0, 1]
    
    expected_output = {
        0: "Error detected in log",
        1: "Potential timeout issue",
        3: "Error detected in log"
    }
    
    result = analyze_root_cause(logs, anomalies)
    assert result == expected_output, f"Expected {expected_output}, but got {result}"

def test_analyze_root_cause_unknown_patterns():
    logs = [
        "Unusual activity detected",
        "Performance degraded slightly",
        "Unknown issue identified"
    ]
    anomalies = [1, 1, 1]
    
    expected_output = {
        0: "Unknown anomaly",
        1: "Unknown anomaly",
        2: "Unknown anomaly"
    }
    
    result = analyze_root_cause(logs, anomalies)
    assert result == expected_output, f"Expected {expected_output}, but got {result}"

def test_analyze_root_cause_empty_input():
    logs = []
    anomalies = []
    
    expected_output = {}
    
    result = analyze_root_cause(logs, anomalies)
    assert result == expected_output, f"Expected {expected_output}, but got {result}"

def generate_root_cause(logs: List[str], anomalies: List[int]) -> Dict[int, str]:
    root_cause_map = {}
    for idx, (log, anomaly) in enumerate(zip(logs, anomalies)):
        if anomaly == 1:
            input_text = f"Log: {log}\nExplain the issue:"
            inputs = tokenizer(
                input_text,
                return_tensors="pt",
                truncation=True,
                padding="max_length",
                max_length=100  # Truncate input to match the output length
            )
            outputs = model.generate(
                **inputs,
                max_length=150,  # Increased max_length to avoid mismatch
                num_return_sequences=1
            )
            explanation = tokenizer.decode(outputs[0], skip_special_tokens=True)
            root_cause_map[idx] = explanation
    return root_cause_map

# Test case for generate_root_cause
def test_generate_root_cause_simple():
    logs = ["Error: Database connection failed"]
    anomalies = [1]

    result = generate_root_cause(logs, anomalies)

    assert isinstance(result, dict), "Result should be a dictionary."
    assert 0 in result, "Anomaly index 0 should be in the result."
    assert isinstance(result[0], str), "The explanation should be a string."
    assert len(result[0]) > 0, "The explanation should not be empty."

def test_generate_root_cause_empty_input():
    logs = []
    anomalies = []

    result = generate_root_cause(logs, anomalies)

    assert isinstance(result, dict), "Result should be a dictionary."
    assert len(result) == 0, "Result should be empty for no logs and anomalies."

def test_generate_root_cause_no_anomalies():
    logs = ["System is operating normally", "Database connection established"]
    anomalies = [0, 0]

    result = generate_root_cause(logs, anomalies)

    assert isinstance(result, dict), "Result should be a dictionary."
    assert len(result) == 0, "Result should be empty for no anomalies."

def test_generate_root_cause_multiple_anomalies():
    logs = [
        "Error: Disk space exceeded",
        "Timeout while connecting to server",
        "Warning: High memory usage",
        "Error: Database connection lost"
    ]
    anomalies = [1, 1, 0, 1]

    result = generate_root_cause(logs, anomalies)

    assert isinstance(result, dict), "Result should be a dictionary."
    assert len(result) == 3, "Result should contain three explanations."
    assert all(isinstance(explanation, str) and len(explanation) > 0 for explanation in result.values()), (
        "All explanations should be non-empty strings."
    )

def test_generate_root_cause_long_logs():
    logs = [
        "This is a very long log message " * 20,
        "Another long log message that repeats itself " * 15
    ]
    anomalies = [1, 1]

    result = generate_root_cause(logs, anomalies)

    assert isinstance(result, dict), "Result should be a dictionary."
    assert len(result) == 2, "Result should contain two explanations for the two anomalies."
    assert all(isinstance(explanation, str) and len(explanation) > 0 for explanation in result.values()), (
        "All explanations should be non-empty strings."
    )

def test_generate_root_cause_mixed_logs():
    logs = [
        "Error: Database timeout occurred",
        "System running normally",
        "Critical: Server crash detected",
        "No issues detected",
        "Error: File read permission denied"
    ]
    anomalies = [1, 0, 1, 0, 1]

    result = generate_root_cause(logs, anomalies)

    assert isinstance(result, dict), "Result should be a dictionary."
    assert len(result) == 3, "Result should contain three explanations for the anomalies."
    assert all(isinstance(explanation, str) and len(explanation) > 0 for explanation in result.values()), (
        "All explanations should be non-empty strings."
    )

def test_generate_root_cause_duplicate_logs():
    logs = [
        "Error: Server not responding",
        "Error: Server not responding",
        "Error: Server not responding"
    ]
    anomalies = [1, 1, 1]

    result = generate_root_cause(logs, anomalies)

    assert isinstance(result, dict), "Result should be a dictionary."
    assert len(result) == 3, "Result should contain three explanations for the anomalies."
    assert all(isinstance(explanation, str) and len(explanation) > 0 for explanation in result.values()), (
        "All explanations should be non-empty strings."
    )


