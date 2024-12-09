from transformers import BertModel
import torch.nn as nn

# Define the architecture
class LogAnomalyDetector(nn.Module):
    def __init__(self, base_model: str = 'bert-base-uncased'):
        super().__init__()
        self.bert = BertModel.from_pretrained(base_model)
        self.anomaly_head = nn.Sequential(
            nn.Linear(self.bert.config.hidden_size, 128),
            nn.ReLU(),
            nn.Linear(128, 1),
            nn.Sigmoid()
        )

    def forward(self, input_ids, attention_mask):
        bert_output = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask
        )
        cls_embedding = bert_output.last_hidden_state[:, 0, :]
        anomaly_score = self.anomaly_head(cls_embedding)
        return anomaly_score
