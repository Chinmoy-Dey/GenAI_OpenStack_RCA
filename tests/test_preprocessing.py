import os
import pandas as pd
from tempfile import NamedTemporaryFile
from src.data_preprocessing import load_and_preprocess

def test_load_and_preprocess():
    # Create a temporary CSV file with sample data
    with NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
        temp_file.write(b"Content\nLog message 1\nLog message 2\n")
        temp_file_name = temp_file.name

    try:
        # Load and preprocess the temporary CSV file
        df = load_and_preprocess(temp_file_name)
        assert not df.empty  # Ensure the dataframe is not empty
    finally:
        os.remove(temp_file_name)  # Clean up the temporary file
