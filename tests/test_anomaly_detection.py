import torch
from unittest.mock import MagicMock
from transformers import BertForSequenceClassification
from src.anomaly_detection import detect_anomalies

def test_detect_anomalies():
    # Mock the model and tokenizer
    model = MagicMock()
    tokenizer = MagicMock()

    # Configure the tokenizer mock to return a dummy tensor dictionary
    tokenizer.return_value = {
        'input_ids': torch.tensor([[1, 2, 3]]),
        'attention_mask': torch.tensor([[1, 1, 1]])
    }

    # Configure the model mock to return a dummy tensor with a scalar value
    mock_output = MagicMock()
    mock_output.item.return_value = 0.2  # Set a float value for the anomaly score
    model.return_value = mock_output

    # Logs to test
    logs = ['something crashes in openstack', 'INIT SUCCESSFUL']

    # Call the function
    result = detect_anomalies(model, tokenizer, logs)

    # Assert the result
    assert result == 1  # Based on the threshold logic
