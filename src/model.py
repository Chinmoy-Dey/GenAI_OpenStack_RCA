from transformers import AutoModelForSequenceClassification, AutoTokenizer
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import AutoTokenizer, AutoModel

#from src.export import g_logBert, g_tokenizer 

def load_model():
    # if g_logBert is not None and g_tokenizer is not None:
    #     return g_logBert, g_tokenizer
    # Load model and tokenizer globally to avoid reloading
    g_tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    g_logBert = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)
    g_logBert.eval()
    return g_logBert, g_tokenizer