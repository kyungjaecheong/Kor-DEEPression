import pandas as pd
import numpy as np

col_demo = ['year', 'age', 'HE_BMI', 'sex', 'educ', 'genertn', 'marri_2', 'EC1_1']
col_health = ['D_1_1', 'LQ4_00', 'D_2_1', 'BO1', 'BO1_1', 'BO2_1']
col_life = ['BD1', 'BD1_11', 'BD2_1', 'sm_presnt', 'BP1']
col_dpr = ['DF2_pr', 'mh_PHQ_S', 'BP5']

def data_load(filedir):
    df0 = pd.read_csv(filedir, low_memory=False)
    # print(df0.shape)
    if 'ID' in df0.columns:
        col_list = ['ID']+col_demo+col_health+col_life+col_dpr
        df1 = df0[col_list].rename(columns={'ID':'id'})
    else:
        col_list = ['id']+col_demo+col_health+col_life+col_dpr
        df1 = df0[col_list]
    # print(df1.shape)
    return df1

# df14 = data_load('./data/downloads/HN14_ALL.csv')
# print(df14.shape)
# df16 = data_load('./data/downloads/HN16_ALL.csv')
# print(df16.shape)
# df18 = data_load('./data/downloads/HN18_ALL.csv')
# print(df18.shape)
# df20 = data_load('./data/downloads/HN20_ALL.csv')
# print(df20.shape)

def fill_nan(value):
    if value == ' ':
        value = np.nan
    return value

def fill_nan_df(df):
    df1 = df.copy()
    df1 = df1.applymap(fill_nan)
    return df1

def drop_nan_df(df):
    df1 = df.copy()
    df1 = fill_nan_df(df1)
    df1 = df1.dropna(axis=0, how='any')
    return df1

# df14 = data_load('./data/downloads/HN14_ALL.csv')
# df14_drop = drop_nan_df(df14)
# print(df14_drop.shape)
# df16 = data_load('./data/downloads/HN16_ALL.csv')
# df16_drop = drop_nan_df(df16)
# print(df16_drop.shape)
# df18 = data_load('./data/downloads/HN18_ALL.csv')
# df18_drop = drop_nan_df(df18)
# print(df18_drop.shape)
# df20 = data_load('./data/downloads/HN20_ALL.csv')
# df20_drop = drop_nan_df(df20)
# print(df20_drop.shape)

def concat_df(df_list):
    df = pd.concat(df_list, ignore_index=True)
    return df

df14 = data_load('./data/downloads/HN14_ALL.csv')
df16 = data_load('./data/downloads/HN16_ALL.csv')
df18 = data_load('./data/downloads/HN18_ALL.csv')
df20 = data_load('./data/downloads/HN20_ALL.csv')
df_list = [df14, df16, df18, df20]
df = concat_df(df_list)
df_drop = drop_nan_df(df)
print(df_drop.shape)