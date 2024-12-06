import pandas as pd

# Load the structured and template files
structured_file = 'data/OpenStack_2k.log_structured.csv'
templates_file = 'data/OpenStack_2k.log_templates.csv'

structured_df = pd.read_csv(structured_file)
templates_df = pd.read_csv(templates_file)

print(structured_df.columns)
print(structured_df.head())

# Check data consistency
print(f"Structured log columns: {structured_df.columns}")
print(f"Template log columns: {templates_df.columns}")

# Group by 'Pid' and collect 'EventId' to create input sequences
event_sequences = structured_df.groupby('Pid')['EventId'].apply(list)

# Convert lists of EventIds into space-separated strings
input_texts = [' '.join(map(str, sequence)) for sequence in event_sequences]

# Assign default labels (0 for normal, no anomaly data available)
labels = [0] * len(input_texts)

# Save processed data for training
processed_data = pd.DataFrame({'input_text': input_texts, 'label': labels})
processed_data.to_csv('processed_data.csv', index=False)
print(f"Preprocessed data saved to 'processed_data.csv'.")