import pandas as pd
from custom_modules import preprocess


df14 = preprocess.data_load('./data/downloads/HN14_ALL.csv')
df16 = preprocess.data_load('./data/downloads/HN16_ALL.csv')
df18 = preprocess.data_load('./data/downloads/HN18_ALL.csv')
df20 = preprocess.data_load_20('./data/downloads/HN20_ALL.csv')

df_list = [df14, df16, df18, df20]
df = preprocess.concat_df(df_list)
df_drop = preprocess.drop_nan_df(df)
df_drop.to_csv('./data/downloads/ver3/HN_drop_14_20.csv', index=False)

df_test = pd.read_csv('./data/downloads/ver3/HN_drop_14_20.csv')

df_query = preprocess.query_df(df_test).reset_index(drop=True)
df_add_targets = preprocess.get_targets(df_query)
df_add_features = preprocess.get_features(df_add_targets)

col_year = ['id', 'year']
col_feature = ['id', 'age', 'HE_ht', 'HE_wt', 'HE_BMI',
               'sex', 'edu', 'household', 'marital', 'EC1_1',
               'D_1_1', 'limit', 'modality', 'w_change',
               'HE_HBP', 'HE_DB', 'HE_HCHOL', 'HE_HTG',
               'dr_freq', 'dr_amount', 'sm_presnt', 'BP1']
col_target = ['id', 'Depression', 'MDD']

df_year = df_add_features[col_year]
df_feature = df_add_features[col_feature]
df_target = df_add_features[col_target]

df_year.to_csv('./data/downloads/ver3/HN_year.csv', index=False)
df_feature.to_csv('./data/downloads/ver3/HN_feature.csv', index=False)
df_target.to_csv('./data/downloads/ver3/HN_target.csv', index=False)

# ---------TEST CODES---------
# df14 = preprocess.data_load('./data/downloads/HN14_ALL.csv')
# print(df14.shape)

# df14_fillnan = preprocess.fill_nan_df(df14)
# print(df14_fillnan.info())

# df14_dropnan = preprocess.drop_nan_df(df14)
# print(df14_dropnan.info())

# df14_dropnan.to_csv('./data/downloads/ver2/HN14_drop.csv', index=False)
# df14_test = pd.read_csv('./data/downloads/ver2/HN14_drop.csv')
# print(df14_test.info())


# df14 = preprocess.data_load('./data/downloads/HN14_ALL.csv')
# df16 = preprocess.data_load('./data/downloads/HN16_ALL.csv')
# df18 = preprocess.data_load('./data/downloads/HN18_ALL.csv')
# df20 = preprocess.data_load_20('./data/downloads/HN20_ALL.csv')

# df_list = [df14, df16, df18, df20]
# df = preprocess.concat_df(df_list)
# df_drop = preprocess.drop_nan_df(df)
# df_drop.to_csv('./data/downloads/ver2/HN_drop_14_20.csv', index=False)

# df_test = pd.read_csv('./data/downloads/ver2/HN_drop_14_20.csv')

# df_query = preprocess.query_df(df_test).reset_index(drop=True)
# df_query.to_csv('./data/downloads/ver2/HN_query_14_20.csv', index=False)
# print(df_query.tail())
# print(f'\n{df_query.shape}')

# df_add_targets = preprocess.get_targets(df_query)
# print(df_add_targets.Depression.value_counts(normalize=True))
# print(df_add_targets.MDD.value_counts(normalize=True))

# df_add_features = preprocess.get_features(df_add_targets)
# print(df_add_features.shape)
# print(df_add_features.columns)

# col_year = ['id', 'year']
# col_feature = ['id', 'age', 'HE_ht', 'HE_wt', 'HE_BMI',
#                'sex', 'edu', 'household', 'marital', 'EC1_1',
#                'health', 'limit', 'modality', 'w_change', 'w_control',
#                'HE_HBP', 'HE_DB', 'HE_HCHOL', 'HE_HTG',
#                'dr_freq', 'dr_amount', 'sm_presnt', 'BP1']
# col_target = ['id', 'Depression', 'MDD']

# df_year = df_add_features[col_year]
# df_feature = df_add_features[col_feature]
# df_target = df_add_features[col_target]

# print(df_year.shape, df_feature.shape, df_target.shape)