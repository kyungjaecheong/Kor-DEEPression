import pandas as pd
import preprocess

df14 = preprocess.data_load('./data/downloads/HN14_ALL.csv')
# print(df14.shape)

# df14_fillnan = preprocess.fill_nan_df(df14)
# print(df14_fillnan.info())

df14_dropnan = preprocess.drop_nan_df(df14)
# print(df14_dropnan.info())

df14_dropnan.to_csv('./data/downloads/HN14_drop.csv', index=False)
df14_test = pd.read_csv('./data/downloads/HN14_drop.csv')
print(df14_test.info())