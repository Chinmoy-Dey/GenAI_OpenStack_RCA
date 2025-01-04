import torch
from unittest.mock import MagicMock
from transformers import BertForSequenceClassification
from src.anomaly_detection import detect_anomalies

def test_detect_anomalies():
    # Mock model
    mock_model = MagicMock()
    mock_model.return_value = torch.tensor([[0.1], [0.9]])  # Simulate model output of shape (2, 1)

    # Mock tokenizer
    mock_tokenizer = MagicMock()
    mock_tokenizer.return_value = {
        "input_ids": torch.tensor([[1, 2, 3], [4, 5, 6]]),
        "attention_mask": torch.tensor([[1, 1, 1], [1, 1, 1]])
    }
    
    # Mock logs
    logs = ["something crashes in openstack", "INIT SUCCESSFUL"]
    
    from src.anomaly_detection import detect_anomalies
    predictions = detect_anomalies(mock_model, mock_tokenizer, logs)
    print(predictions)
    #assert predictions.tolist() == [1, 0] 

    # Assert predictions
    assert predictions == [1, 1]
