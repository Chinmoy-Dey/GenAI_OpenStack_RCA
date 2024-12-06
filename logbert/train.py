import pandas as pd
import torch
from transformers import BertTokenizer, AdamW
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from tqdm import tqdm

from model.logbert import LogBERT

# Load processed data
data = pd.read_csv('processed_data.csv')
train_texts, val_texts, train_labels, val_labels = train_test_split(
    data['input_text'], data['label'], test_size=0.2, random_state=42
)

# Tokenizer and Dataset
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

class LogDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length=128):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        inputs = self.tokenizer(
            text, max_length=self.max_length, padding="max_length", truncation=True, return_tensors="pt"
        )
        return {
            "input_ids": inputs["input_ids"].squeeze(0),
            "attention_mask": inputs["attention_mask"].squeeze(0),
            "label": torch.tensor(label, dtype=torch.long),
        }

train_dataset = LogDataset(train_texts.tolist(), train_labels.tolist(), tokenizer)
val_dataset = LogDataset(val_texts.tolist(), val_labels.tolist(), tokenizer)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

# Initialize model
logbert = LogBERT()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = logbert.model.to(device)
optimizer = AdamW(model.parameters(), lr=5e-5)

# Training Loop
epochs = 3
for epoch in range(epochs):
    model.train()
    loop = tqdm(train_loader, leave=True)
    for batch in loop:
        optimizer.zero_grad()
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["label"].to(device)
        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        loop.set_description(f"Epoch {epoch}")
        loop.set_postfix(loss=loss.item())

# Save the model
logbert.save('logbert_model')
