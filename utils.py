import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pyarrow.feather as feather
from tqdm import tqdm

def create_idx_df(df, lookup_df):
    idx_df = pd.DataFrame()
    for col in df.columns:
        new_column = []
        for val in df[col]:
            new_column.append(int(lookup_df.loc[lookup_df[col] == val][f'{col}_index']))
        idx_df[col] = new_column
    feather.write_feather(idx_df, 'idx_df.feather')
    return idx_df

def create_lookup(columns: list):
    '''
    creates a lookup pandas DataFrame of unique values and indices
    columns: list of columns to be encoded from a pandas DataFrame
    '''
    lookup_df = pd.DataFrame()
    for col in columns:
        w = create_w2i_i2w_v(col)
        lookup_df[f'{col.name}'] = pd.Series(list(w.keys()))
        lookup_df[f'{col.name}_index'] = pd.Series(list(w.values()))
    feather.write_feather(lookup_df, 'lookup_df.feather')
    return lookup_df
    
def create_w2i_i2w_v(column):
    tokenized_items = tokenize_corpus(column)
    vocabulary = []
    for sentence in tokenized_items:
        for token in sentence:
            if token not in vocabulary:
                vocabulary.append(token)
    word2idx = {w: idx for (idx, w) in enumerate(vocabulary)}
    return word2idx

def tokenize_corpus(corpus):
    tokens = [x.split() for x in corpus]
    return tokens