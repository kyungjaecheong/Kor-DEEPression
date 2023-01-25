import pandas as pd
import numpy as np

col_demo = ['year', 'age', 'HE_ht', 'HE_wt', 'HE_BMI', 'sex', 'edu', 'genertn', 'marri_2', 'EC1_1']
col_health = ['D_1_1', 'LQ4_00', 'D_2_1', 'BO1_1', 'BO2_1']
col_life = ['BD1_11', 'BD2_1', 'sm_presnt', 'BP1']
col_disease = ['HE_HP', 'HE_DM', 'HE_HCHOL', 'HE_HTG']
col_disease_20 = ['HE_HP', 'HE_DM_HbA1c', 'HE_HCHOL', 'HE_HTG']
col_dpr = ['DF2_pr', 'mh_PHQ_S']

def data_load(filedir):
    df0 = pd.read_csv(filedir, low_memory=False)
    col_list = ['id']+col_demo+col_health+col_disease+col_life+col_dpr
    df1 = df0[col_list]
    return df1

def data_load_20(filedir):
    df0 = pd.read_csv(filedir, low_memory=False)
    col_list = ['ID']+col_demo+col_health+col_disease_20+col_life+col_dpr
    df1 = df0[col_list].rename(columns={'ID':'id','HE_DM_HbA1c':'HE_DM'})
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
        value = None
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

# df14 = data_load('./data/downloads/HN14_ALL.csv')
# df16 = data_load('./data/downloads/HN16_ALL.csv')
# df18 = data_load('./data/downloads/HN18_ALL.csv')
# df20 = data_load('./data/downloads/HN20_ALL.csv')
# df_list = [df14, df16, df18, df20]
# df = concat_df(df_list)
# df_drop = drop_nan_df(df)
# print(df_drop.shape)

def query_df(df):
    df1 = df.query('marri_2!=99 and marri_2!=8 and marri_2!=9')
    df2 = df1.query('D_1_1!=9 and BO1_1!=9 and BD1_11!=9 and BD2_1!=9 and BP1!=9')
    return df2

def get_targets(df):
    depression = []
    MDD = []
    df_targets = df[col_dpr]    # ['DF2_pr', 'mh_PHQ_S', 'BP5']
    for i in range(len(df_targets)):
        if df_targets.loc[i, 'DF2_pr'] == 1\
        or df_targets.loc[i, 'mh_PHQ_S'] > 4:
            depression.append(1)
            if df_targets.loc[i, 'mh_PHQ_S'] > 9:
                MDD.append(1)
            else:
                MDD.append(0)
        else:
            depression.append(0)
            MDD.append(0)
    df['Depression'] = depression
    df['MDD'] = MDD
    return df

def get_features(df):
    marital = []
    weight_change = []
    weight_control = []
    drink_freq = []
    drink_amount = []
    
    for i in range(len(df)):
        if df.loc[i, 'marri_2'] in [1,2]:
            marital.append(1)
        elif df.loc[i, 'marri_2'] in [3,4]:
            marital.append(2)
        elif df.loc[i, 'marri_2'] == 88:
            marital.append(3)

        if df.loc[i, 'BO1_1'] == 1:
            weight_change.append(1)
        elif df.loc[i, 'BO1_1'] in [2,3]:
            weight_change.append(2)
        
        if df.loc[i, 'BO2_1'] in [1,2,3]:
            weight_control.append(1)
        elif df.loc[i, 'BO2_1'] == 4:
            weight_control.append(2)
        
        if df.loc[i, 'BD1_11'] in [1,2,8]:
            drink_freq.append(1)
        elif df.loc[i, 'BD1_11'] not in [1,2,8]:
            drink_freq.append(df.loc[i, 'BD1_11'])
        
        if df.loc[i, 'BD2_1'] == 8:
            drink_amount.append(0)
        elif df.loc[i, 'BD2_1'] !=8:
            drink_amount.append(df.loc[i, 'BD2_1'])
        
    df['marital'] = marital
    df['w_change'] = weight_change
    df['w_control'] = weight_control
    df['dr_freq'] = drink_freq
    df['df_amount'] = drink_amount
    
    return df