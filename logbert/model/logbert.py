from transformers import BertForSequenceClassification

class LogBERT:
    def __init__(self, pretrained_model='bert-base-uncased', num_labels=2):
        self.model = BertForSequenceClassification.from_pretrained(pretrained_model, num_labels=num_labels)

    def save(self, save_path):
        self.model.save_pretrained(save_path)
        print(f"Model saved at {save_path}")
