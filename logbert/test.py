
from sklearn.metrics import classification_report
import torch
from transformers import BertForSequenceClassification
from train import val_loader
from transformers import BertTokenizer, AdamW


def predict(log_texts):
    model = BertForSequenceClassification.from_pretrained('logbert_model').to('cuda')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    #tokenizer = BertTokenizer.from_pretrained('logbert_model').to('cuda')

    model.eval()

    results = []
    with torch.no_grad():
        for text in log_texts:
            inputs = tokenizer(text, return_tensors="pt", padding="max_length", truncation=True, max_length=128).to('cuda')
            outputs = model(**inputs)
            prediction = torch.argmax(outputs.logits, dim=1).item()
            results.append("Anomalous" if prediction == 1 else "Normal")
    return results

# Example usage
log_samples = ["ID1 ID2 ID3", "ID4 ID5 ID6"]
predictions = predict(log_samples)
print(predictions)
