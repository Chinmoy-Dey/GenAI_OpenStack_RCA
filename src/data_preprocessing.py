import pandas as pd

def load_and_preprocess(file_path):
    df = pd.read_csv(file_path)
    
    # Example preprocessing: remove duplicates
    df.drop_duplicates(inplace=True)
    return df
