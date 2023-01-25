import pandas as pd
from custom_modules import preprocess


# df14 = preprocess.data_load('./data/downloads/HN14_ALL.csv')
# df16 = preprocess.data_load('./data/downloads/HN16_ALL.csv')
# df18 = preprocess.data_load('./data/downloads/HN18_ALL.csv')
# df20 = preprocess.data_load_20('./data/downloads/HN20_ALL.csv')

# df_list = [df14, df16, df18, df20]
# df = preprocess.concat_df(df_list)
# df_drop = preprocess.drop_nan_df(df)
# df_drop.to_csv('./data/downloads/ver2/HN_drop_14_20.csv', index=False)

# df_test = pd.read_csv('./data/downloads/ver2/HN_drop_14_20.csv')

# df_query = preprocess.query_df(df_test)


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


df14 = preprocess.data_load('./data/downloads/HN14_ALL.csv')
df16 = preprocess.data_load('./data/downloads/HN16_ALL.csv')
df18 = preprocess.data_load('./data/downloads/HN18_ALL.csv')
df20 = preprocess.data_load_20('./data/downloads/HN20_ALL.csv')

df_list = [df14, df16, df18, df20]
df = preprocess.concat_df(df_list)
df_drop = preprocess.drop_nan_df(df)
df_drop.to_csv('./data/downloads/ver2/HN_drop_14_20.csv', index=False)

df_test = pd.read_csv('./data/downloads/ver2/HN_drop_14_20.csv')

df_query = preprocess.query_df(df_test).reset_index(drop=True)
# df_query.to_csv('./data/downloads/ver2/HN_query_14_20.csv', index=False)
# print(df_query.tail())
# print(f'\n{df_query.shape}')

df_add_targets = preprocess.get_targets(df_query)
# print(df_add_targets.Depression.value_counts(normalize=True))
# print(df_add_targets.MDD.value_counts(normalize=True))

