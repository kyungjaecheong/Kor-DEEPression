'''
Custom Modules for Step 2-3 Data Preprocessing

Project (Step) : Kor-Deepression (Step 2 : Modeling)

Project_repo_url : https://github.com/kyungjaecheong/Kor-DEEPression

Contributor : Kyung Jae, Cheong (정경재)
'''

# 함수 리스트 및 __all__ 정의(import * 할 때 불러올 함수들을 정의)
# from custom_modules.postgresql_down import *
__all__ = ['data_load',
           'limitation',
           'min_max_scaler',
           'one_hot_endcoding',
           'export_to_csv']


# 라이브러리 import
import pandas as pd


# 데이터 불러오기 기능
def data_load(filedir, target_name):
    '''
    data_load
        데이터 불러오기 기능 (X, y 분리 기능도 추가)
    ---
    입력 변수 정보
        filedir : (str)불러올 파일의 디렉토리
        target_name : (str) target 변수명
    ---
    출력 : DataFrame, DataFrame
    '''
    # csv데이터를 DataFrame으로 불러옴
    df0 = pd.read_csv(filedir)
    # Feature column 정의
    features = df0.drop(columns=[target_name]).columns
    
    # 독립변수 및 종속변수 분리
    df_X = df0[features]
    df_y = df0[target_name]
    
    # DataFrame들을 Tuple형태로 반환
    return df_X, df_y


# EDA를 통해 설정한 이상치를 제한하기 위한 기능
def limitation(data, column, min_value, max_value):
    '''
    limitation
        데이터값 제한 함수
    ---
    입력 변수 정보
        data : (DataFrame) 변경 대상 데이터프레임
        column : (str) 변경 대상 column
        min_value : (int, float) 제한하고자하는 최소값
        max_value : (int, float) 제한하고자하는 최대값
    ---
    출력 : DataFrame
    '''
    # 빈 리스트 생성
    new_data = []
    # 이상치를 설정한 최소값 및 최대값으로 append
    for index, value in enumerate(data[column]):
        if value < min_value:
            new_data.append(min_value)
        elif value > max_value:
            new_data.append(max_value)
        else: new_data.append(value)
    
    # 기존 column에 덮어쓰기
    df_fix = data.copy()
    df_fix[column] = new_data
    
    # 덮어쓴 DataFrame을 반환
    return df_fix


# min_max scaler 기능
def min_max_scaler(data, column, min_value=None, max_value=None):
    '''
    min_max_scaler
        연속형 데이터를 0~1사이의 값으로 변환시키는 기능
    ---
    입력 변수 정보
        data : (DataFrame) 변경 대상 데이터프레임
        column : (str) 변경 대상 column
        min_value : 최소값 (기본값 : None)
        max_value : 최대값 (기본값 : None)
    ---
    출력 : DataFrame
    '''
    # 원본 수정 방지를 위한 copy실시
    df_fix = data.copy()
    
    # (optional)min_value 혹은 max_value를 설정하지 않은 경우 최소값 및 최대값을 산출
    if min_value is None:
        min_value = df_fix[column].min()
    if max_value is None:
        max_value = df_fix[column].max()
    
    # min_max_scaling을 통해 기존 column에 덮어쓰기
    df_fix[column] = (df_fix[column] - min_value) / (max_value - min_value)
    
    # 덮어쓴 DataFrame을 반환
    return df_fix


# One-Hot Endcoding 기능
def one_hot_endcoding(data, cat_columns):
    '''
    one_hot_endcoding
        이진형 변수가 아닌 범주형 변수들을 이진형 변수로 변환하는 기능 
    ---
    입력 변수 정보
        data : (DataFrame) 인코딩 대상 데이터프레임
        cat_columns : (list) 인코딩 대상 column 리스트
    ---
    출력 : DataFrame
    '''
    # Pandas의 get_dummies함수를 이용하여 One_hot_Encoding 실시
    df_ohe = pd.get_dummies(data, columns=cat_columns)
    
    # One_hot_Encoding을 적용한 DataFrame을 반환
    return df_ohe


# Modeling data Export 기능
def export_to_csv(X_data, y_data, savepath):
    '''
    export_to_csv
        독립변수(X)와 종속변수(y)를 병합하고 csv로 export하는 기능 
    ---
    입력 변수 정보
        X_data : (DataFrame) 독립변수(X)
        y_data : (DataFrame, Series) 종속변수(y)
        savepath : (str) csv file 저장 경로
    ---
    출력 : None
    '''
    # Concat (데이터 병합, 열방향(axis=1))
    df = pd.concat([X_data, y_data], axis=1)
    
    # csv로 지정한 경로(savepath)에 파일을 생성 혹은 덮어쓰기
    df.to_csv(savepath, index=False)
    
    # # 테스트용 코드
    # print(df.shape)
    # print(df.iloc[:,-1].value_counts(normalize=True))
