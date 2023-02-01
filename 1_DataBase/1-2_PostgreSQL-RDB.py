'''
CLI 실행 명령어
$ python 1_DataBase/1-2_PostgreSQL-RDB.py
'''

# 라이브러리 및 함수 Impoert
import os
import sys
import psycopg2
from dotenv import load_dotenv
from custom_modules.postgresql_upload import *

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
        print('\nconnection success to DB')
    
    # 예외처리 : 연결 실패할 경우 시스템을 중단
    except:
        print('\nconnection error to DB')
        sys.exit()


    # 테이블 리스트 정의 (id_year-->targets-->범주형변수들-->features)
    table_list = ['id_year',
                  'targets',
                  'sex',
                  'education',
                  'household',
                  'marital',
                  'economy',
                  'subj_health',
                  'drk_freq',
                  'drk_amount',
                  'smoke',
                  'stress',
                  'features']
    
    
    # 테이블 초기화 (features-->범주형변수들-->targets-->id_year)
    table_initialization(cursor=cur, table_list=table_list)
    print('\ntable initialization complete')
    
    
    # 테이블 생성 (id_year-->targets-->범주형변수들-->features)
    table_creation(cursor=cur, table_list=table_list)
    print('\ntable created complete')
    
    
    # 데이터 삽입 (id_year-->targets-->범주형변수들-->features)
    insertion_csv(cur, table_list[0], path='./1_DataBase/downloads/HN_year.csv')
    insertion_csv(cur, table_list[1], path='./1_DataBase/downloads/HN_target.csv')
    insertion_json(cur, table_list[2:-1], path='./1_DataBase/json_variable.json')
    insertion_csv(cur, table_list[-1], path='./1_DataBase/downloads/HN_feature.csv')
    print('\ndata insert complete')


    # 변경사항을 저장(commit)
    conn.commit()
    
    # postgreSQL 연결 종료
    conn.close()    
    print('\nSuccessfully Disconnected to DB\n')


# 파일이 실행되면 자동으로 main 함수를 동작하도록 함  
if __name__ == '__main__':
    main()