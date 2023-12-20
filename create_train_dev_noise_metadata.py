import os
import pandas as pd

def generate_single_entry_metadata(df):
    """
    Generate metadata with each row as a single string in the format 'filepath|filesize|'.
    """
    metadata_entries = []
    for filepath in df['filepath']:
        full_path = './' + filepath
        try:
            file_size = os.path.getsize(full_path)
        except FileNotFoundError:
            file_size = 'File Not Found'
        metadata_entry = f"{filepath}|{file_size}|"
        metadata_entries.append(metadata_entry)

    return "\n".join(metadata_entries)

dev_subset = pd.read_csv('dev_subset.csv')
train_subset = pd.read_csv('train_subset.csv')
test_subset = pd.read_csv('metadata/test.csv').head(400)
# Generating metadata with single string entries for dev_subset and train_subset
dev_metadata_single_entry = generate_single_entry_metadata(dev_subset)
train_metadata_single_entry = generate_single_entry_metadata(train_subset)
test_metadata_single_entry = generate_single_entry_metadata(test_subset)

# Saving the new metadata as text files
dev_metadata_single_entry_path = './dev_metadata_single_entry.csv'
train_metadata_single_entry_path = './train_metadata_single_entry.csv'
test_metadata_single_entry_path = './test_metadata_single_entry.csv'

with open(dev_metadata_single_entry_path, 'w') as file:
    file.write(dev_metadata_single_entry)

with open(train_metadata_single_entry_path, 'w') as file:
    file.write(train_metadata_single_entry)

with open(test_metadata_single_entry_path, 'w') as file:
    file.write(test_metadata_single_entry)