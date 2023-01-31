'''
CLI 실행 명령어
$ python 1_DataBase/1-2_PostgreSQL-RDB.py
'''

import os
import sys
import psycopg2
from dotenv import load_dotenv
from custom_modules.postgresql_upload import *

load_dotenv(verbose=True)

HOST = os.getenv('postgre_host')
PORT = 5432
DATABASE = os.getenv('postgre_database')
USERNAME = os.getenv('postgre_user')
PASSWORD = os.getenv('postgre_password')

def main():
    # postgreSQL 연결
    try:
        conn = psycopg2.connect(
            host=HOST,
            port=PORT,
            database=DATABASE,
            user=USERNAME,
            password=PASSWORD)
        cur = conn.cursor()
        print('connection success to DB')
    except:
        print('connection error to DB')
        sys.exit()

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
    
    # 테이블 초기화
    table_initialization(cursor=cur, table_list=table_list)
    print('table initialization complete')
    
    # 테이블 생성
    table_creation(cursor=cur, table_list=table_list)
    print('table created complete')
    
    # 데이터 삽입
    insertion_csv(cur, table_list[0], path='./1_DataBase/downloads/HN_year.csv')
    insertion_csv(cur, table_list[1], path='./1_DataBase/downloads/HN_target.csv')
    insertion_json(cur, table_list[2:-1], path='./1_DataBase/json_variable.json')
    insertion_csv(cur, table_list[-1], path='./1_DataBase/downloads/HN_feature.csv')
    print('data insert complete')

    conn.commit()
    conn.close()
    
    print('Successfully Disconnected to DB')
    
if __name__ == '__main__':
    main()