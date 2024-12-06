from sklearn.metrics import classification_report
import torch
from transformers import BertForSequenceClassification
from train import val_loader

# Load saved model
model = BertForSequenceClassification.from_pretrained('logbert_model').to('cuda')

# Evaluation Loop
model.eval()
all_predictions, all_labels = [], []

with torch.no_grad():
    for batch in val_loader:
        input_ids = batch["input_ids"].to('cuda')
        attention_mask = batch["attention_mask"].to('cuda')
        labels = batch["label"].to('cuda')

        outputs = model(input_ids, attention_mask=attention_mask)
        predictions = torch.argmax(outputs.logits, dim=1)
        all_predictions.extend(predictions.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())

# Print classification report
print(classification_report(all_labels, all_predictions))
