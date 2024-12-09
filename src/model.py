from transformers import AutoModelForSequenceClassification, AutoTokenizer
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import AutoTokenizer, AutoModel

#from src.export import g_logBert, g_tokenizer 
import sys
from pathlib import Path

# Add the src directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent))

# Import LogAnomalyDetector
from model_architecture import LogAnomalyDetector


def load_model_base():
    # if g_logBert is not None and g_tokenizer is not None:
    #     return g_logBert, g_tokenizer
    # Load model and tokenizer globally to avoid reloading
    g_tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    g_logBert = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)
    g_logBert.eval()
    return g_logBert, g_tokenizer


def load_model():
    """
    Load the LogAnomalyDetector model and its tokenizer.

    Returns:
        model: The loaded LogAnomalyDetector model in evaluation mode.
        tokenizer: The tokenizer associated with the model.
    """
    # Define the model architecture
    model = LogAnomalyDetector(base_model="bert-base-uncased")  # Ensure this matches your training code

    # Load the state dictionary into the model
    model.load_state_dict(torch.load("./model_files/LogAnomalyDetector/model.pth", map_location=torch.device('cpu')))

    # Set the model to evaluation mode
    model.eval()

    # Load the tokenizer
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

    return model, tokenizer
