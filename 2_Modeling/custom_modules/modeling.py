'''
Custom Modules for Step 2-4 ML/DL Modeling

Project (Step) : Kor-Deepression (Step 2 : Modeling)

Project_repo_url : https://github.com/kyungjaecheong/Kor-DEEPression

Contributor : Kyung Jae, Cheong (정경재)
'''

# 함수 리스트 및 __all__ 정의(import * 할 때 불러올 함수들을 정의)
# from custom_modules.postgresql_down import *
# __all__ = []


# 라이브러리 import
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.linear_model import LogisticRegression
import lightgbm as lgbm
import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers import *
from keras.callbacks import EarlyStopping, ModelCheckpoint

# Data Import 기능 (Feature, Target 분리기능 포함)
def data_load(filepath, target_name):
    '''
    data_load
        데이터 불러오기 기능 (X, y 분리 기능도 추가)
    ---
    입력 변수 정보
        filepath : (str)불러올 파일의 디렉토리
        target_name : (str) target 변수명
    ---
    출력 : DataFrame, DataFrame
    '''
    # csv데이터를 DataFrame으로 불러옴
    df0 = pd.read_csv(filepath)
    print(f"\tDataFrame Shape : {df0.shape}")
    
    # 독립변수 및 종속변수 분리
    df_X = df0.drop(columns=[target_name])
    df_y = df0[target_name]
    print(f"\tFeatures(X) Shape : {df_X.shape}")
    print(f"\tTarget(y) Shape : {df_y.shape}")
    
    # DataFrame들을 Tuple형태로 반환
    return df_X, df_y


# Train Test Split 기능
    # 옵션으로 Validation 데이터 생성가능, DL 모델 학습과정에서 이용할 예정
def data_split(X_data, y_data, seed=2023, val_set=False):
    '''
    data_split
        데이터 분리 기능
    ---
    입력 변수 정보
        X_data : (DataFrame) 독립변수(X, features)
        y_data : (DataFrame, Series) 종속변수(y, target)
        seed : (int) Random Seed 값 (기본값 2023)
        val_set : (Boolean) 기본값 False, 검증용 데이터셋도 생성할지 결정
    ---
    출력 : DataFrame, DataFrame
    '''
    # Train & Test 분리 (비율은 8:2) 
    X_tr, X_test, y_tr, y_test = train_test_split(X_data, y_data, test_size=0.2, random_state=seed)
    
    # val_set=False(기본값)
    if val_set is False:
        print(f"\tX_train, y_train : {X_tr.shape}, {y_tr.shape}")
        print(f"\tX_test, y_test : {X_test.shape}, {y_test.shape}")
        return X_tr, X_test, y_tr, y_test
    
    # val_set=True (0.75 : 0.25 비율로 split) : 최종 비율 (6:2:2) 
    elif val_set is True:
        X_train, X_val, y_train, y_val = train_test_split(X_tr, y_tr, test_size=0.25, random_state=seed)
        print(f"\tX_train, y_train : {X_train.shape}, {y_train.shape}")
        print(f"\tX_val, y_val : {X_val.shape}, {y_val.shape}")
        print(f"\tX_test, y_test : {X_test.shape}, {y_test.shape}")
        return X_train, X_val, X_test, y_train, y_val, y_test
    

# Baseline (최빈class) 생성 기능
def make_baseline(y_data):
    '''
    make_baseline
        Baseline (최빈class) 생성 기능
    ---
    입력 변수 정보        
        y_data : (DataFrame, Series) 종속변수(y, target)        
    ---
    출력 : List
    '''
    # 최빈 Class 산출
    base_mode = y_data.mode()[0]
    
    # Baseline 리스트 생성
    baseline = [base_mode]*len(y_data)
    
    # 평가지표(정확도, AUCscore) 출력
    print("\tBaseline Accuracy : {:.4f}".format(accuracy_score(y_data, baseline)))
    print("\tBaseline AUC_score : {:.1f}".format(roc_auc_score(y_data, baseline)))
    
    # Baseline data 반환
    return baseline


# Logistic Regression Tuning (GridSearchCV)
# 튜닝을 거친 후의 모델을 반환하도록 프로그래밍
def Tuning_Logistic(train_X, train_y, cv=4):
    '''
    Tuning_Logistic
        Logistic Regression Tuning(GridSearchCV) & Make Tuning model
    ---
    입력 변수 정보        
        train_X : (DataFrame, ndarray) 독립변수(X, features)
        train_y : (Series, ndarray) 종속변수(y, target)        
    ---
    출력 : Model
    '''
    # LogisticRegression 모델 생성
    model = LogisticRegression(max_iter=100)
    
    # 탐색 파라미터 범위 지정
    params = {'C':np.logspace(-4,4,50),
              'max_iter':[100,200,400,800]}
    
    # GridSearchCV 모델 정의 (평가지표 기준은 AUC score)
    grid_model = GridSearchCV(estimator=model,
                              param_grid=params,
                              n_jobs=-1,
                              cv=cv,
                              scoring='roc_auc',
                              verbose=1)
    
    # Fit (GridSearchCV 실시)
    grid_model.fit(train_X, train_y)
    
    # 최적 하이퍼파라미터 및 최적 AUC score 출력
    print("Best Parameters: ", grid_model.best_params_)
    print("Best AUC Score: ", grid_model.best_score_)
    
    # 최적 하이퍼파라미터로 모델을 재정의
    tuned_model = LogisticRegression(C=grid_model.best_params_['C'],
                                     max_iter=grid_model.best_params_['max_iter'])
    
    # 튜닝을 거친 모델을 반환함
    return tuned_model


# LightGBM Classifier Tuning (GridSearchCV)
# 튜닝을 거친 후의 모델을 반환하도록 프로그래밍
def Tuning_LGBM(train_X, train_y, cv=4):
    '''
    Tuning_LGBM
        LightGBM Classifier Tuning(GridSearchCV) & Make Tuning model
    ---
    입력 변수 정보 
        train_X : (DataFrame, ndarray) 독립변수(X, features)
        train_y : (Series, ndarray) 종속변수(y, target)        
    ---
    출력 : Model
    '''
    # LightGBM Classifier 모델 생성
    model = lgbm.LGBMClassifier(objective='binary', boosting_type='gbdt')
    
    # 탐색 파라미터 범위 지정
    params = {'learning_rate' : [0.01, 0.05, 0.1],
              'n_estimators' : [100, 200, 300],
              'max_depth' : [3, 5, 7, 9],
              'subsample' : [0.7, 0.8]}
    
    # GridSearchCV 모델 정의 (평가지표 기준은 AUC score)
    grid_model = GridSearchCV(estimator=model,
                              param_grid=params,
                              n_jobs=-1,
                              cv=cv,
                              scoring='roc_auc',
                              verbose=1)
    
    # Fit (GridSearchCV 실시)
    grid_model.fit(train_X, train_y)
    
    # 최적 하이퍼파라미터 및 최적 AUC score 출력
    print("Best Parameters: ", grid_model.best_params_)
    print("Best AUC Score: ", grid_model.best_score_)
    
    # 최적 하이퍼파라미터로 모델을 재정의
    tuned_model = lgbm.LGBMClassifier(objective='binary',
                                      boosting_type='gbdt',
                                      learning_rate=grid_model.best_params_['learning_rate'],
                                      n_estimators=grid_model.best_params_['n_estimators'],
                                      max_depth=grid_model.best_params_['max_depth'],
                                      subsample=grid_model.best_params_['subsample'])
    
    # 튜닝을 거친 모델을 반환함
    return tuned_model


# Keras Tuner용 Model 함수 정의 (MLP : Multi-Layer Perceptron)
def model_builder_mlp(hp):
    # Sequential model 정의
    model = Sequential(name='Sequential_MLP')
    
    # Tuning Parameter 1 : 은닉층 Dense 노드 수 (units)
    hp_units_1 = hp.Int('units_1', min_value=8, max_value=64, step=8)
    model.add(Dense(units=hp_units_1, name='Dense_1', activation='relu', input_dim=47))
    
    # Tuning Parameter 2 : 은닉층 Dense 노드 수 (units)
    hp_units_2 = hp.Int('units_2', min_value=8, max_value=64, step=8)
    model.add(Dense(units=hp_units_2, name='Dense_2', activation='relu'))
    
    # 출력층(Sigmoid)
    model.add(Dense(units=1, name='Output_Layer', activation='sigmoid'))
    
    # Model Compile (평가지표 : AUCscore)
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=[tf.keras.metrics.AUC(name='auc')])
    
    # Model 반환
    return model


# Keras Tuner용 Model 함수 정의 (1D-CNN : 1D-Convolutional Neural Networks)
def model_builder_cnn(hp):
    # Sequential model 정의
    model = Sequential(name='Sequential')
    
    # Tuning Parameter 1 : 합성곱층 Conv1D 필터 수 (filters)
    hp_filters = hp.Choice('Conv1D_Filters', values = [4, 8, 16, 32])
    # Tuning Parameter 2 : 합성곱층 Conv1D 커널 크기 (kernel_size)
    hp_kernel_size = hp.Int('kernel_size', min_value = 3, max_value = 7, step=1)
    # 합성곱층 Conv1D 추가
    model.add(Conv1D(filters=hp_filters, kernel_size=hp_kernel_size, strides=1,
                     activation='relu', kernel_initializer='he_normal',
                     input_shape=(47,1), name='Conv1D_Layer'))
    # 입력값이 쏠리는 것을 막기위해 BatchNormalization 실시    
    model.add(BatchNormalization(name='Batch_Normalization'))
    
    # Flatten으로 FC(Fully Connected)층을 추가
    model.add(Flatten(name='Flatten_Layer'))
    
    # Tuning Parameter 3 : FC(Fully Connected)층 Dense unit 수
    hp_fc_units = hp.Int('FC_units', min_value=64, max_value=256, step=64)
    model.add(Dense(units=hp_fc_units, name='FC_Dense_Layer',
                    activation='relu', kernel_initializer='he_normal'))
    
    # 과적합 방지를 위한 Dropout층 추가
    # Tuning Parameter 3 : Dropout층 dropout_rate
    hp_dropout_rate = hp.Choice('Dropout_rate', values = [0.7, 0.8, 0.9])
    model.add(Dropout(rate=hp_dropout_rate, name='Dropout'))
    
    # 출력층(Sigmoid)
    model.add(Dense(units=1, name='Output_Layer',
                    activation='sigmoid', kernel_initializer='glorot_normal'))
    
    # Tuning Parameter 4 : Adam optimizer의 learning_rate
    hp_learning_rate = hp.Choice('learning_rate', values = [1e-2, 1e-3, 1e-4])
    model.compile(optimizer = keras.optimizers.Adam(learning_rate=hp_learning_rate),
                  loss = 'binary_crossentropy',
                  metrics = [tf.keras.metrics.AUC(name='auc')])
    
    # Model 반환
    return model


# Callback 함수 정의(EarlyStopping, ModelCheckpoint)
def callback_sets(monitor, mode, patience, savepath):
    '''
    callback_sets
        Keras 모델들의 callback함수를 하나로 묶어주는 기능
    ---
    입력 변수 정보 
        monitor : (str) 기준 평가지표 혹은 손실값
        mode : (str) 'max'(metric) 혹은 'min'(loss)
        patience : (int) early stop의 적용 기준
        savepath : (str) best 모델을 저장할 경로  
    ---
    출력 : List
    '''
    # EarlyStopping
    early_stop = EarlyStopping(monitor=monitor, mode=mode, patience=patience,
                               restore_best_weights=True)
    # ModelCheckpoint
    check_point = ModelCheckpoint(filepath=savepath, monitor=monitor, mode=mode,
                                  verbose=0, save_best_only=True)
    # 출력 : list
    return [early_stop, check_point]

