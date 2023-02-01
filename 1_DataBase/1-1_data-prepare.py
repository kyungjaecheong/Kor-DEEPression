'''
CLI 실행 명령어
$ python 1_DataBase/1-1_data-prepare.py
'''

# 라이브러리 및 함수 Import
import pandas as pd
from custom_modules.preprocess import *


# 데이터 불러오기 기능
df14 = data_load('./1_DataBase/downloads/raw_data/HN14_ALL.csv')
df16 = data_load('./1_DataBase/downloads/raw_data/HN16_ALL.csv')
df18 = data_load('./1_DataBase/downloads/raw_data/HN18_ALL.csv')
df20 = data_load_20('./1_DataBase/downloads/raw_data/HN20_ALL.csv')
print('\nData Loading : Success')
print(df14.shape, df16.shape, df18.shape, df20.shape)


# 데이터 병합 기능
df_list = [df14, df16, df18, df20]
df = concat_df(df_list)
print('\nData Merge : Success')
print(df.shape)


# 결측치 제거 기능 1
df_drop = drop_nan_df(df)
print('\nDroped NaN values : Success')
# print(df_drop.info())


# dtype변환을 간단하게 처리하기 위해 임시 저장 후 다시 불러오기
df_drop.to_csv('./1_DataBase/downloads/temp_data/HN_drop_14_20.csv', index=False)
df_temp = pd.read_csv('./1_DataBase/downloads/temp_data/HN_drop_14_20.csv')
# print(df_temp.info())


# 결측치 제거 기능 2
df_drop2 = drop_9s_df(df_temp)
print('Dropped 9 or 99 values : Success')
# print(f"{df_drop2.tail()}\n{df_drop2.shape}")
print(df_drop2.shape)


# Target Column 및 가공한 Feature Column들을 추가하는 기능
df_add_targets = get_targets(df_drop2)
df_add_features = get_features(df_add_targets)
print('\nAdd Features & Add Targets : Success')


# 가공한 DataFrame을 RDB형태에 맞도록 분리하는 기능
df_year, df_feature, df_target = devide_for_RDB(df_add_features)
print('\nData division completed')
print('Shapes : df_year, df_feature, df_target')
print(df_year.shape, df_feature.shape, df_target.shape)


# 최종 DataFrame들을 csv로 Export
df_year.to_csv('./1_DataBase/downloads/HN_year.csv', index=False)
df_feature.to_csv('./1_DataBase/downloads/HN_feature.csv', index=False)
df_target.to_csv('./1_DataBase/downloads/HN_target.csv', index=False)
print('\nData Saved at "Kor-DEEPression/1_DataBase/downloads/"\n')