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

print(df_add_target.info())