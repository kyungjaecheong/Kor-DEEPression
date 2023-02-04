'''
CLI 실행 명령어
$ python 2_Modeling/2-3_Preprocess.py
'''

# 라이브러리 및 함수 Import
from custom_modules.data_preprocess import *


# 데이터 불러오기 기능
df_X_depr, df_y_depr = data_load(target_name='depression', filedir='./2_Modeling/downloads/Model_depr.csv')
df_X_mdd, df_y_mdd = data_load(target_name='MDD', filedir='./2_Modeling/downloads/Model_mdd.csv')
# print(df_X_depr.shape, df_y_depr.shape)
# print(df_X_mdd.shape, df_y_mdd.shape)

print("\nData Loading : Success\n")


# EDA를 통해 설정한 이상치를 제한하기 위한 기능
# BMI 최소값 : 14미만, 최대값 : 50초과
limit_bmi_depr = limitation(df_X_depr, 'BMI', min_value=14, max_value=50)
limit_bmi_mdd = limitation(df_X_mdd, 'BMI', min_value=14, max_value=50)

# min_max scaler 기능 (옵션으로 min값과 max값을 추가적으로 설정 가능)
mms_age_depr = min_max_scaler(limit_bmi_depr, 'age')
mms_age_mdd = min_max_scaler(limit_bmi_mdd, 'age')
df_mms_depr = min_max_scaler(mms_age_depr, 'BMI', min_value=14, max_value=50)
df_mms_mdd = min_max_scaler(mms_age_mdd, 'BMI', min_value=14, max_value=50)
# print(df_mms_depr.age.min(), df_mms_depr.age.max())
# print(df_mms_mdd.age.min(), df_mms_mdd.age.max())
# print(df_mms_depr.BMI.min(), df_mms_depr.BMI.max())
# print(df_mms_mdd.BMI.min(), df_mms_mdd.BMI.max())

print("Standardization of 'age' & 'BMI' : Success\n")


# One-Hot Endcoding 기능 (이진형 변수가 아닌 범주형 변수들을 이진형 변수로 변환)
# 변환 대상 column 지정
cat_cols = ['sex', 'education', 'household', 'marital', 'economy',
            'subj_health', 'drk_freq', 'drk_amount', 'smoke', 'stress']
# One-Hot Endcoding
df_ohe_depr = one_hot_endcoding(df_mms_depr, cat_columns=cat_cols)
df_ohe_mdd = one_hot_endcoding(df_mms_mdd, cat_columns=cat_cols)
# print(df_ohe_depr.shape, df_ohe_mdd.shape)
# print(df_ohe_depr.min().min(), df_ohe_depr.max().max())
# print(df_ohe_mdd.min().min(), df_ohe_mdd.max().max())

print("OneHotEncoding : Success\n")


# Modeling data Export 기능(concat기능도 포함)
export_to_csv(df_ohe_depr, df_y_depr, savepath='./2_Modeling/downloads/Encoded_depr.csv')
export_to_csv(df_ohe_mdd, df_y_mdd, savepath='./2_Modeling/downloads/Encoded_mdd.csv')

print("Export to CSV : Success\n")
