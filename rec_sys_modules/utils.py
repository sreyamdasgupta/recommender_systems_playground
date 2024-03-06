import pandas as pd
import numpy as np

def train_test_split(df, user_col, item_col, time_col = None, train_end_date = None, val_end_date = None, train_percentage = None, val_percentage = None):
    val_df = None
    if time_col is not None:
        df[time_col] = pd.to_datetime(df[time_col])
        df_sorted = df.sort_values(by=time_col)
        train_df = df_sorted[df_sorted[time_col]<=train_end_date]
        if val_end_date is None:
            test_df = df_sorted[df_sorted[time_col]>train_end_date]
        else:
            val_df = val_df[(val_df[time_col]>train_end_date)&(val_df[time_col]<=val_end_date)]
            test_df = df_sorted[df_sorted[time_col]>val_end_date]
    else:
        print ("It is recommended to do the split based on a time columns")
        df_randomized = df.sample(frac=1).reset_index().drop("index",axis="columns")
        train_len = int(train_percentage*len(df_randomized))
        train_df = df_randomized[:train_len]
        if val_percentage is None:
            test_df = df_randomized[train_len:]
        else:
            val_len = int(val_percentage*len(df_randomized))
            val_df = df_randomized[train_len:train_len + val_len]
            test_df = df_randomized[train_len + val_len:]

    print ("We are not recommending for new users or new items")
    print ("Train size:", len(train_df))
    unique_train_users = list(train_df[user_col].unique())
    unique_train_items = list(train_df[item_col].unique())
    test_df = test_df[(test_df[user_col].isin(unique_train_users))&(test_df[item_col].isin(unique_train_items))]
    if  val_df is None: 
        print ("Test size:", len(test_df))
        return train_df, test_df
    else:
        val_df = val_df[(val_df[user_col].isin(unique_train_users))&(val_df[item_col].isin(unique_train_items))]
        print ("Validation size:", len(val_df))
        print ("Test size:", len(test_df))
        return train_df, val_df, test_df

def rename_primary_cols(df, user_col, item_col, rating_col):
    rename_dict = {user_col:'userID',item_col:'itemID',rating_col:'rating'}
    df = df.rename(columns=rename_dict)
    return df, rename_dict



        

