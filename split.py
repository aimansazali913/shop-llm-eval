import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("data/messages.csv")  # Load your dataset
dev, test = train_test_split(df, test_size=0.3, random_state=42, stratify=df['label'])  # Split into dev and test sets
dev.to_csv("data/dev.csv", index=False)  # Save dev set
test.to_csv("data/test.csv", index=False)  # Save test set
print(len(dev), 'dev rows,', len(test), 'test rows')  # Print the lengths of the dev and test sets