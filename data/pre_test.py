import pandas as pd
import preprocess

# df14 = preprocess.data_load('./data/downloads/HN14_ALL.csv')
# # print(df14.shape)

# # df14_fillnan = preprocess.fill_nan_df(df14)
# # print(df14_fillnan.info())

# df14_dropnan = preprocess.drop_nan_df(df14)
# # print(df14_dropnan.info())

# df14_dropnan.to_csv('./data/downloads/HN14_drop.csv', index=False)
# df14_test = pd.read_csv('./data/downloads/HN14_drop.csv')
# print(df14_test.info())

df14 = preprocess.data_load('./data/downloads/HN14_ALL.csv')
df16 = preprocess.data_load('./data/downloads/HN16_ALL.csv')
df18 = preprocess.data_load('./data/downloads/HN18_ALL.csv')
df20 = preprocess.data_load('./data/downloads/HN20_ALL.csv')

df_list = [df14, df16, df18, df20]
df = preprocess.concat_df(df_list)
df_drop = preprocess.drop_nan_df(df)
df_drop.to_csv('./data/downloads/HN_drop_14_20.csv', index=False)

df_test = pd.read_csv('./data/downloads/HN_drop_14_20.csv')
# print(df_test.info())

df_add_target = preprocess.get_targets(df_test)
# print(df_add_target.Depression.value_counts(normalize=True).sort_index())
# print('\n')
# print(df_add_target.MDD.value_counts(normalize=True).sort_index())

# print(df_add_target.info())
# df_add_target2 = df_add_target.copy()
# df_add_target2['age'] = df_add_target2['age'].astype(int)
# df_add_target2['genertn'] = df_add_target2['genertn'].astype(int)
# df_add_target2['marri_2'] = df_add_target2['marri_2'].astype(int)

# print(df_add_target2.info())

# print(df_add_target.shape)
df_q1 = preprocess.query_df(df_add_target)
# print(df_q1.shape)

df_q1.to_csv('./data/downloads/HN_drop_14_20_2.csv', index=False)
df_test2 = pd.read_csv('./data/downloads/HN_drop_14_20_2.csv')
# print(df_test2.info())

df_add_features = preprocess.get_features(df_test2)
# print(df_add_features.info())

col_year = ['id', 'year']
col_feature = ['id', 'age', 'HE_BMI', 'sex', 'educ', 'genertn', 'marital', 'EC1_1',
               'D_1_1', 'LQ4_00', 'D_2_1', 'w_change', 'w_control',
               'dr_freq', 'df_amount', 'sm_presnt', 'BP1']
col_target = ['id', 'Depression', 'MDD']

df_year = df_add_features[col_year]
df_feature = df_add_features[col_feature]
df_target = df_add_features[col_target]

# print(df_year.shape, df_feature.shape, df_target.shape)

df_year.to_csv('./data/downloads/HN_year.csv', index=False)
df_feature.to_csv('./data/downloads/HN_feature.csv', index=False)
df_target.to_csv('./data/downloads/HN_target.csv', index=False)