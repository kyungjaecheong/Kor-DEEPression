'''
CLI 실행 명령어
$ python 2_Modeling/2-1_PostgreSQL-Query.py
'''

# 라이브러리 및 함수 Import
import os
import sys
import psycopg2
from dotenv import load_dotenv
from custom_modules.postgresql_down import *

# .env파일에 저장된 정보들을 불러옴
load_dotenv(verbose=True)

# HOST, PORT, DATABASE, USERNAME, PASSWORD를 전역변수로 저장
HOST = os.getenv('postgre_host')
PORT = 5432
DATABASE = os.getenv('postgre_database')
USERNAME = os.getenv('postgre_user')
PASSWORD = os.getenv('postgre_password')

# 파일이 실행되면 자동으로 동작하는 main 함수
def main():
    
    # postgreSQL 연결
    try:
        conn = psycopg2.connect(
            host=HOST,
            port=PORT,
            database=DATABASE,
            user=USERNAME,
            password=PASSWORD)
        # 커서 지정
        cur = conn.cursor()
        print('\nconnection success to DB\n')
    
    # 예외처리 : 연결 실패할 경우 시스템을 중단
    except:
        print('\nconnection error to DB\n')
        sys.exit()
    '''
    connection success to DB
    '''    
    
    # Query & Get csv(temp) : SQL Qurey문을 통해 csv 데이터를 생성하는 기능
    # EDA모드에서는 범주형 변수의 테이블을 모두 JOIN하여 모두 문자열로 불러옴
    get_csv_file(cur, mode='EDA', target='depression', savepath="./2_Modeling/downloads/temp_data/EDA_depr_temp.csv")
    get_csv_file(cur, mode='EDA', target='MDD', savepath="./2_Modeling/downloads/temp_data/EDA_mdd_temp.csv")
    # Model모드에서는 모두 수치형으로 데이터를 불러옴
    get_csv_file(cur, mode='Model', target='depression', savepath="./2_Modeling/downloads/temp_data/Model_depr_temp.csv")
    get_csv_file(cur, mode='Model', target='MDD', savepath="./2_Modeling/downloads/temp_data/Model_mdd_temp.csv")
    # #error checking
    # get_csv_file(cur, mode='error', target='depression', savepath="./2_Modeling/downloads/error.csv")
    # get_csv_file(cur, mode='error', target='MDD', savepath="./2_Modeling/downloads/error.csv")
    # get_csv_file(cur, mode='EDA', target='error', savepath="./2_Modeling/downloads/error.csv")
    # get_csv_file(cur, mode='Model', target='error', savepath="./2_Modeling/downloads/error.csv")
    '''
    EDA_depression_temp.csv file created Successfully
    EDA_MDD_temp.csv file created Successfully
    Model_depression_temp.csv file created Successfully
    Model_MDD_temp.csv file created Successfully
    '''
    
    # postgreSQL 연결 종료
    conn.close()    
    print('\nSuccessfully Disconnected to DB\n')
    '''
    Successfully Disconnected to DB
    '''
    
    # Data loading : column 이름을 추가하기 위해 저장한 임시 데이터를 다시 불러옴
    df_eda_depr = load_df_with_columns(mode='EDA', target='depression', filepath="./2_Modeling/downloads/temp_data/EDA_depr_temp.csv")
    df_eda_mdd = load_df_with_columns(mode='EDA', target='MDD', filepath="./2_Modeling/downloads/temp_data/EDA_mdd_temp.csv")
    df_depr = load_df_with_columns(mode='Model', target='depression', filepath="./2_Modeling/downloads/temp_data/Model_depr_temp.csv")
    df_mdd = load_df_with_columns(mode='Model', target='MDD', filepath="./2_Modeling/downloads/temp_data/Model_mdd_temp.csv")
    # #error checking
    # df_error = load_df_with_columns(mode='error', target='depression', filepath="./2_Modeling/downloads/temp_data/Model_mdd_temp.csv")
    # df_error = load_df_with_columns(mode='error', target='MDD', filepath="./2_Modeling/downloads/temp_data/Model_mdd_temp.csv")
    # df_error = load_df_with_columns(mode='EDA', target='error', filepath="./2_Modeling/downloads/temp_data/Model_mdd_temp.csv")
    # df_error = load_df_with_columns(mode='Model', target='error', filepath="./2_Modeling/downloads/temp_data/Model_mdd_temp.csv")
    print('Data loading : Success\n')
    '''
    EDA_depression : (16570, 21)
    EDA_MDD : (3359, 21)
    Model_depression : (16570, 20)
    Model_MDD : (3359, 20)
    Data loading : Success
    '''
    
    # Data to csv(final) : column 이름을 추가한 최종 데이터들을 Export함
    # EDA 모드에서는 이진변수를 문자열(Yes,No)로 수정
    df_to_csv(df_eda_depr, mode='EDA', target='depression', savepath='./2_Modeling/downloads/EDA_depr.csv')
    df_to_csv(df_eda_mdd, mode='EDA', target='MDD', savepath='./2_Modeling/downloads/EDA_mdd.csv')
    # Model 모드에서는 'id' column을 제외
    df_to_csv(df_depr, mode='Model', target='depression', savepath='./2_Modeling/downloads/Model_depr.csv')
    df_to_csv(df_mdd, mode='Model', target='MDD', savepath='./2_Modeling/downloads/Model_mdd.csv')
    # #error checking
    # df_to_csv(df_mdd, mode='error', savepath='./2_Modeling/downloads/error.csv')
    print('Data to csv file : Success\n')
    '''
    csv file for EDA_depression exported Successfully
    csv file for EDA_MDD exported Successfully
    csv file for Model_depression exported Successfully
    csv file for Model_MDD exported Successfully
    Data to csv file : Success
    '''

# 파일이 실행되면 자동으로 main 함수를 동작하도록 함  
if __name__ == '__main__':
    main()