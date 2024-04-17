import pandas as pd
import numpy as np

train_size = 0.7

df = pd.read_csv('data_processed.csv', header=0)
idxs = np.array(df.index)

l = int(len(df) * train_size)
train_idxs = idxs[:l]
test_idxs = idxs[l:]
train_idxs.sort()

df.iloc[train_idxs, :].to_csv('data_train.csv', header=None, index=None)
df.iloc[test_idxs, :].to_csv('data_test.csv', header=None, index=None)
