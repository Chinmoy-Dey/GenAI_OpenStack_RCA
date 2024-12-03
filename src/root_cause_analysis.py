from typing import List, Dict
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from typing import List, Dict

# Load the fine-tuned GPT model for root cause generation
# TODO: Safawat/trouble-shooting-using-T5
# TODO : google/flan-t5-xl

MODEL_NAME = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(MODEL_NAME)
model = GPT2LMHeadModel.from_pretrained(MODEL_NAME)
def generate_root_cause(logs: List[str], anomalies: List[int]) -> Dict[int, str]:
    """
    Generate root cause explanations for detected anomalies.
    """
    root_cause_map = {}
    for idx, (log, anomaly) in enumerate(zip(logs, anomalies)):
        if anomaly == 1:
            input_text = f"Log: {log}\nExplain the issue:"
            inputs = tokenizer(input_text, return_tensors="pt", truncation=True, padding="max_length", max_length=512)
            outputs = model.generate(**inputs, max_length=100, num_return_sequences=1)
            explanation = tokenizer.decode(outputs[0], skip_special_tokens=True)
            root_cause_map[idx] = explanation
    return root_cause_map

def analyze_root_cause(logs: List[str], anomalies: List[int]) -> Dict[int, str]:
    """
    Analyze root causes of anomalies in the logs.

    Parameters:
        logs (List[str]): List of log entries.
        anomalies (List[int]): List of anomaly flags (1 for anomaly, 0 for normal).

    Returns:
        Dict[int, str]: Mapping of anomaly indices to their potential root causes.
    """
    root_cause_map = {}
    for idx, (log, anomaly) in enumerate(zip(logs, anomalies)):
        if anomaly == 1:
            # Placeholder for RCA logic: look for keywords or patterns in the log
            if "error" in log.lower():
                root_cause_map[idx] = "Error detected in log"
            elif "timeout" in log.lower():
                root_cause_map[idx] = "Potential timeout issue"
            else:
                root_cause_map[idx] = "Unknown anomaly"
    return root_cause_map
