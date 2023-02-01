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

    # Query & Get csv(temp) : SQL Qurey문을 통해 csv 데이터를 생성하는 기능
    get_csv_file(cur, mode='EDA', savepath='./2_Modeling/downloads/temp_data/EDA_temp.csv')
    get_csv_file(cur, mode='Depression', savepath='./2_Modeling/downloads/temp_data/Depression_temp.csv')
    get_csv_file(cur, mode='MDD', savepath='./2_Modeling/downloads/temp_data/MDD_temp.csv')
    # get_csv_file(cur, mode='error', savepath='./2_Modeling/downloads/temp_data/error_temp.csv')
    
    # postgreSQL 연결 종료
    conn.close()    
    print('\nSuccessfully Disconnected to DB\n')
    
    
    # Data loading : column 이름을 추가하기 위해 저장한 임시 데이터를 다시 불러옴
    df_eda = load_df_with_columns('./2_Modeling/downloads/temp_data/EDA_temp.csv', mode='EDA')
    df_depr = load_df_with_columns('./2_Modeling/downloads/temp_data/Depression_temp.csv', mode='Depression')
    df_mdd = load_df_with_columns('./2_Modeling/downloads/temp_data/MDD_temp.csv', mode='MDD')
    # df_error = load_df_with_columns('./2_Modeling/downloads/temp_data/error_temp.csv', mode='error')
    print('Data loading : Success\n')
    
    # Data to csv(final) : column 이름을 추가한 최종 데이터들을 Export함
    df_to_csv(df_eda, mode='EDA', savepath='./2_Modeling/downloads/EDA.csv')
    df_to_csv(df_depr, mode='Depression', savepath='./2_Modeling/downloads/Depression.csv')
    df_to_csv(df_mdd, mode='MDD', savepath='./2_Modeling/downloads/MDD.csv')
    # df_to_csv(df_mdd, mode='error', savepath='./2_Modeling/downloads/error.csv')

# 파일이 실행되면 자동으로 main 함수를 동작하도록 함  
if __name__ == '__main__':
    main()