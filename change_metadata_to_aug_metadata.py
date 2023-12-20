import pandas as pd

def generate_augmented_metadata_with_sentence_two_columns(df, subset_type):
    """
    Generate augmented metadata with sentences for the given dataframe, formatted into two columns.
    The first column is the modified file path, and the second column is the sentence.
    """
    augmented_metadata = []
    for _, row in df.iterrows():
        augmented_path = f"audio_data_aug/{subset_type}/wavs/noise-{row['filepath'].split('/')[-1]}"
        augmented_metadata.append({
            'filepath': augmented_path,
            'sentence': row['sentence']
        })

    return augmented_metadata

dev_subset = pd.read_csv('dev_subset.csv')
train_subset = pd.read_csv('train_subset.csv')
# Generating augmented metadata with sentences for dev_subset and train_subset
dev_aug_metadata_with_sentence_2col = generate_augmented_metadata_with_sentence_two_columns(dev_subset, 'dev')
train_aug_metadata_with_sentence_2col = generate_augmented_metadata_with_sentence_two_columns(train_subset, 'train')

# Saving the new augmented metadata as text files
dev_aug_metadata_with_sentence_2col_path = './metadata_aug/dev_aug.csv'
train_aug_metadata_with_sentence_2col_path = './metadata_aug/train_aug.csv'

dev_aug_metadata_with_sentence_2col_df = pd.DataFrame(dev_aug_metadata_with_sentence_2col)
train_aug_metadata_with_sentence_2col_df = pd.DataFrame(train_aug_metadata_with_sentence_2col)

# Saving the new augmented metadata as CSV files
dev_aug_metadata_with_sentence_2col_df.to_csv(dev_aug_metadata_with_sentence_2col_path, index=False)
train_aug_metadata_with_sentence_2col_df.to_csv(train_aug_metadata_with_sentence_2col_path, index=False)

