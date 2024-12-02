def validate_data(data):
    if data.isnull().values.any():
        raise ValueError("Null values detected in data")
