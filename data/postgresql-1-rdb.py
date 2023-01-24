import os
import sys
import csv
import json
import psycopg2
from dotenv import load_dotenv

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

    # 테이블 초기화
    cur.execute("""DROP TABLE IF EXISTS id_year;""")
    print('table initialization complete')
    
    # 테이블 생성
    sql_create_table_idy = """CREATE TABLE IF NOT EXISTS id_year (
    id VARCHAR NOT NULL,
    year INTEGER,
    CONSTRAINT id_year_pk PRIMARY KEY (id)
    );"""
    
    cur.execute(sql_create_table_idy)
    print('table created complete')
    
    with open('./data/downloads/HN_year.csv', 'r') as cf:
        csv_reader = csv.reader(cf)
        next(csv_reader)
        cur.copy_from(cf, 'id_year', sep=',')
        
    conn.commit()
    conn.close()
    
    print('data insert complete')
    
if __name__ == '__main__':
    main()