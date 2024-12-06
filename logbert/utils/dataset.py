from transformers import BertTokenizer
from torch.utils.data import Dataset

class LogDataset(Dataset):
    def __init__(self, logs, tokenizer, max_length):
        self.logs = logs
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.logs)

    def __getitem__(self, idx):
        log = self.logs[idx].strip()
        inputs = self.tokenizer(
            log,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )
        return {
            "input_ids": inputs["input_ids"].squeeze(0),
            "attention_mask": inputs["attention_mask"].squeeze(0),
        }
