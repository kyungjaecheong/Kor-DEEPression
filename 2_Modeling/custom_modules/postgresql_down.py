'''
Custom Modules for Step 2-1 Data Query & Download

Project (Step) : Kor-Deepression (Step 2 : Modeling)

Project_repo_url : https://github.com/kyungjaecheong/Kor-DEEPression

Contributor : Kyung Jae, Cheong (정경재)
'''

# 함수 리스트 및 __all__ 정의(import * 할 때 불러올 함수들을 정의)
# from custom_modules.postgresql_down import *
__all__ = ['get_csv_file',
           'load_df_with_columns',
           'df_to_csv']

# 라이브러리 import
import pandas as pd


# SQL Qurey문을 통해 csv 데이터를 생성하는 기능
# mode를 지정하여 목적에 맞게 쿼리를 실시함
def get_csv_file(cursor, mode, savepath):
    '''
    get_csv_file
        SQL Qurey문을 통해 csv 데이터를 생성하는 기능
    ---
    입력 변수 정보
        cursor : (object) psycopg2.connect.cursor()
        mode : (str) 'EDA', 'Depression', 'MDD'
        savepath : (str) 저장 파일 경로
    ---
    출력 : None 
    '''
    
    # mode가 'EDA' 인 경우
    if mode == 'EDA':
        sql_query = """
        SELECT f.id , y."year" , f.age , f.bmi , f1.sex , f2.education , f3.household , f4.marital , f5.economy , 
            f6.subj_health , f.limitation , f.modality , f.w_change , f.high_bp , f.diabetes , f.dyslipidemia , 
            f7.drk_freq , f8.drk_amount , f9.smoke , f10.stress , t.depression , t.mdd 
        FROM features AS f
        JOIN targets AS t ON f.id = t.id
        JOIN id_year AS y ON f.id = y.id
        JOIN sex AS f1 ON f.sex = f1.id_sex 
        JOIN education AS f2 ON f.education = f2.id_education 
        JOIN household AS f3 ON f.household = f3.id_household 
        JOIN marital AS f4 ON f.marital = f4.id_marital 
        JOIN economy AS f5 ON f.economy = f5.id_economy 
        JOIN subj_health AS f6 ON f.subj_health = f6.id_subj_health 
        JOIN drk_freq AS f7 ON f.drk_freq = f7.id_drk_freq 
        JOIN drk_amount AS f8 ON f.drk_amount = f8.id_drk_amount 
        JOIN smoke AS f9 ON f.smoke = f9.id_smoke 
        JOIN stress AS f10 ON f.stress = f10.id_stress 
        """
    
    # mode가 'Depression'인 경우
    elif mode == 'Depression':
        sql_query = """
        SELECT f.* , t.depression
        FROM features AS f
        JOIN targets AS t ON f.id = t.id
        """
    
    # mode가 'MDD'인 경우
    elif mode == 'MDD':
        sql_query = """
        SELECT f.* , t.mdd
        FROM features AS f
        JOIN targets AS t ON f.id = t.id
        WHERE t.depression = 1
        """
    
    # 예외처리 : Exception 문을 출력하도록 설정하고 함수를 종료 시킴
    else:
        raise Exception("\nERROR : 'mode' must be in ['EDA', 'Depression', 'MDD']")
    
    # csv 생성 SQL 쿼리문
    sql_csv = f"""COPY ({sql_query}) TO STDOUT WITH CSV DELIMITER ',';"""
    with open(savepath, 'w', encoding='utf-8') as cf:
        cursor.copy_expert(sql_csv, cf)
    
    # 동작 여부를 확인하기 위한 print문
    print(f"{mode}_temp.csv file created Successfully")


# DataFrame을 통해 column 이름을 추가하는 함수
# mode를 지정하여 목적에 맞게 기능을 수행함
def load_df_with_columns(filepath, mode):
    '''
    load_df_with_columns
        column 이름을 추가하는 함수
    ---
    입력 변수 정보
        filepath : (str) 파일 경로
        mode : (str) 'EDA', 'Depression', 'MDD'        
    ---
    출력 : DataFrame 
    '''
    
    # 공통적으로 담고 있는 Feature의 리스트를 정의함
    col_feat = ['age', 'BMI', 'sex', 'education', 'household', 'marital', 'economy',
                'subj_health', 'limitation', 'modality', 'w_change', 'high_bp',
                'diabetes', 'dyslipidemia', 'drk_freq', 'drk_amount', 'smoke', 'stress']
    
    # 지정한 mode에 따라 column 이름 리스트를 결정함
    if mode == 'EDA':
        col_list = ['id', 'year'] + col_feat + ['depression', 'MDD']
    elif mode == 'Depression':
        col_list = ['id'] + col_feat + ['depression']
    elif mode == 'MDD':
        col_list = ['id'] + col_feat + ['MDD']
    else: # 예외처리 : Exception 문을 출력하도록 설정하고 함수를 종료 시킴
        raise Exception("\nERROR : 'mode' must be in ['EDA', 'Depression', 'MDD']")
    
    # 위에서 결정한 col_list에 따라서 column의 이름을 붙여주면서 DataFrame을 불러옴
    df = pd.read_csv(filepath, names=col_list)
    
    # 동작여부 테스트용 코드
    # print(f"{mode} : {df.shape}")
    
    # 출력 : DataFrame
    return df


# column 이름을 추가한 DataFrame을 csv로 저장하는 기능
# mode를 지정하여 목적에 맞게 기능을 수행함(EDA 모드에서는 새로운 column을 생성)
def df_to_csv(df, mode, savepath):
    '''
    df_to_csv
        DataFrame을 csv로 저장하는 기능
    ---
    입력 변수 정보
        df : (DataFrame) 저장할 DataFrame
        mode : (str) 'EDA', 'Depression', 'MDD'
        savepath : (str) 저장 파일 경로
    ---
    출력 : None 
    '''
    
    # mode가 'EDA'인 경우
    if mode == 'EDA':
        # 추가할 column(정상vs경도우울증vs주요우울장애)의 리스트를 생성
        new_y = []
        for i in range(len(df)):
            if df.loc[i, 'depression'] == 0:
                new_y.append("정상")
            else:
                if df.loc[i, 'MDD'] == 0:
                    new_y.append("경도우울증")
                else:
                    new_y.append("주요우울장애(MDD)")
        # 리스트 값으로 새로운 column(Depr_MDD)을 추가함
        df['Depr_MDD'] = new_y
        # 지정한 경로에 DataFrame을 csv로 Export
        df.to_csv(savepath, index=False)
    
    # mode가 'Depression' 혹은 'MDD' 인 경우 : 지정한 경로에 DataFrame을 csv로 Export
    elif mode == 'Depression':
        df.to_csv(savepath, index=False)
    elif mode == 'MDD':
        df.to_csv(savepath, index=False)
    
    # 예외처리 : Exception 문을 출력하도록 설정하고 함수를 종료 시킴
    else:
        raise Exception("\nERROR : 'mode' must be in ['EDA', 'Depression', 'MDD']")
    
    # 동작 여부를 확인하기 위한 print문
    print(f"csv file for {mode} created Successfully")
