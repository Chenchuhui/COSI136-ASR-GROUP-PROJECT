import pandas as pd
from sklearn.model_selection import train_test_split

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('metadata.csv')

# Add a temporary column to store the split status
df['temp_status'] = ''

# First, split into training and test sets with a 70-30 split
train_df, test_df = train_test_split(df, test_size=0.3, stratify=df[['gender', 'age_group']])
train_df['temp_status'] = 'train'
test_df['temp_status'] = 'test'

# Further split the training data into training and development sets
train_df, dev_df = train_test_split(train_df, test_size=0.1, stratify=train_df[['gender', 'age_group']])
dev_df['temp_status'] = 'dev'

# Combine the split DataFrames back into one DataFrame
combined_df = pd.concat([train_df, dev_df, test_df])

# Update the 'status' column in the original DataFrame
df['status'] = combined_df['temp_status']

# Drop the temporary status column from the original DataFrame
df.drop(columns=['temp_status'], inplace=True)

# Drop temp_status in train, dev and test data frame
train_df['status'] = train_df['temp_status']
dev_df['status'] = dev_df['temp_status']
test_df['status'] = test_df['temp_status']
train_df.drop(columns=['temp_status'], inplace=True)
dev_df.drop(columns=['temp_status'], inplace=True)
test_df.drop(columns=['temp_status'], inplace=True)

# Write the updated DataFrame back to CSV
df.to_csv('metadata.csv', index=False)

# Write the data frame to seperate CSV
train_df.to_csv('train.csv', index=False)
dev_df.to_csv('dev.csv', index=False)
test_df.to_csv('test.csv', index=False)

print("The status column in metadata.csv has been updated.")
