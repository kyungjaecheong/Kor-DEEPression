'''
CLI 실행 명령어
$ python 2_Modeling/2-4-1_Logistic.py
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
'''
(Data Loading)
        (Depression)
        DataFrame Shape : (16570, 48)
        Features(X) Shape : (16570, 47)
        Target(y) Shape : (16570,)

        (MDD)
        DataFrame Shape : (3359, 48)
        Features(X) Shape : (3359, 47)
        Target(y) Shape : (3359,)
'''


# 데이터 분리 기능
print("\n(Data Splitting)")
print("\t(Depression)")
X_train_depr, X_test_depr, y_train_depr, y_test_depr = data_split(df_X_depr, df_y_depr)
print("\n\t(MDD)")
X_train_mdd, X_test_mdd, y_train_mdd, y_test_mdd = data_split(df_X_mdd, df_y_mdd)
'''
(Data Splitting)
        (Depression)
        X_train, y_train : (13256, 47), (13256,)
        X_test, y_test : (3314, 47), (3314,)

        (MDD)
        X_train, y_train : (2687, 47), (2687,)
        X_test, y_test : (672, 47), (672,)
'''


# Baseline (최빈 Class) 생성 기능
print("\n(Baseline)")
print("\t(Depression)")
baseline_depr = make_baseline(y_train_depr)
print("\n\t(MDD)")
baseline_mdd = make_baseline(y_train_mdd)
'''
(Baseline)
        (Depression)
        Baseline Accuracy : 0.7956
        Baseline AUC_score : 0.5

        (MDD)
        Baseline Accuracy : 0.7276
        Baseline AUC_score : 0.5
'''


# Logistic Regression Tuning (GridSearchCV)
print("\n(GridSearchCV) - Depression")
tuned_model_depr = Tuning_Logistic(X_train_depr, y_train_depr, cv=4)
print("\n(GridSearchCV) - MDD")
tuned_model_mdd = Tuning_Logistic(X_train_mdd, y_train_mdd, cv=4)
'''
(GridSearchCV) - Depression
Fitting 4 folds for each of 200 candidates, totalling 800 fits
Best Parameters:  {'C': 0.12648552168552957, 'max_iter': 100}
Best AUC Score:  0.8160942375138954

(GridSearchCV) - MDD
Fitting 4 folds for each of 200 candidates, totalling 800 fits
Best Parameters:  {'C': 0.040949150623804234, 'max_iter': 100}
Best AUC Score:  0.7500140314821807
'''


# Encoding Tuning Models to .pkl file (Pickle)
# 튜닝을 거친 모델을 pkl file로 부호화하여 저장함 (모델 비교 시 다시 사용될 예정)
with open('./tuning-models/Logistic_depr.pkl', 'wb') as pf:
    pickle.dump(tuned_model_depr, pf)
with open('./tuning-models/Logistic_mdd.pkl', 'wb') as pf:
    pickle.dump(tuned_model_mdd, pf)
print("\nModel Export to pkl file : Success\n")
'''
Model Export to pkl file : Success
'''