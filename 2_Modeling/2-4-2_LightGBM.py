'''
CLI 실행 명령어
$ python 2_Modeling/2-4-2_LightGBM.py
'''

# 라이브러리 및 함수 Import
from custom_modules.modeling import *
import pickle


# 데이터 불러오기 기능
print("\n(Data Loading)")
print("\t(Depression)")
df_X_depr, df_y_depr = data_load(target_name='depression', filepath='./2_Modeling/downloads/Encoded_depr.csv')
print("\n\t(MDD)")
df_X_mdd, df_y_mdd = data_load(target_name='MDD', filepath='./2_Modeling/downloads/Encoded_mdd.csv')


# 데이터 분리 기능
print("\n(Data Splitting)")
print("\t(Depression)")
X_train_depr, X_test_depr, y_train_depr, y_test_depr = data_split(df_X_depr, df_y_depr)
print("\n\t(MDD)")
X_train_mdd, X_test_mdd, y_train_mdd, y_test_mdd = data_split(df_X_mdd, df_y_mdd)


# Baseline (최빈 Class) 생성 기능
print("\n(Baseline)")
print("\t(Depression)")
baseline_depr = make_baseline(y_train_depr)
print("\n\t(MDD)")
baseline_mdd = make_baseline(y_train_mdd)


# LightGBM Classifier Tuning (GridSearchCV)
print("\n(GridSearchCV) - Depression")
tuned_model_depr = Tuning_LGBM(X_train_depr, y_train_depr, cv=4)
print("\n(GridSearchCV) - MDD")
tuned_model_mdd = Tuning_LGBM(X_train_mdd, y_train_mdd, cv=4)


# Encoding Tuning Models to .pkl file (Pickle)
# 튜닝을 거친 모델을 pkl file로 부호화하여 저장함 (모델 비교 시 다시 사용될 예정)
with open('./tuning-models/LightGBM_depr.pkl', 'wb') as pf:
    pickle.dump(tuned_model_depr, pf)
with open('./tuning-models/LightGBM_mdd.pkl', 'wb') as pf:
    pickle.dump(tuned_model_mdd, pf)
print("\nModel Export to pkl file : Success\n")